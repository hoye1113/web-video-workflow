"""video-factory 面板：人在网页上把片子点出来。

设计原则（照用户要求）：
  ① **网页是入口**：建片、跑阶段、审产物、给反馈（通过/打回）都在网页上
  ② **面板只调现成的工具**：不把逻辑写进面板（工具在 tools/ 和引擎里，命令行怎么跑面板就怎么调）
  ③ **反馈落盘**：通过/打回写进 `projects/<片子>/docs/审批.json`，下次迭代读它
  ④ 零依赖：Python 标准库 + 前端一个文件（不装包、不打包）

用法：
    python tools/panel/server.py            # → http://127.0.0.1:8899
    python tools/panel/server.py --port 8899

阶段（按钮）：
    建片 → 台词(cue 硬切) → 剧本(script.js) → 配音(voice.js) → 字幕(srt) →
    出图(Flow，走浏览器) → 排页(pages/*.js) → 渲染(mp4) → 验收(机器判据) → 抽帧(对照表)
"""
import argparse
import html
import json
import os
import pathlib
import re
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
ENGINE = ROOT / "experiments" / "frametell-src" / "frametell-main" / "packages" / "engine"
PY = sys.executable or "python"
LOCALBIN = pathlib.Path.home() / ".local" / "bin"

# 阶段表：名字 / 命令 / 在哪个目录跑 / 说明
STEPS = [
    ("剧本", [PY, "tools/make_script_js.py", "--from-source"], ROOT, "script-source.json → script.js"),
    ("台词", [PY, "tools/check_cues.py"], ROOT, "审 12 字硬切（目标 0 条）"),
    ("配音", [PY, "tools/make_voice.py"], ROOT, "TTS → audio/*.wav + voice.js（约 10 分钟）"),
    ("排页", [PY, "tools/make_pages.py", "--project", "{proj}"], ROOT, "page-spec.json → pages/pNN.js"),
    ("出图", [PY, "tools/gen_scenes.py"], ROOT, "Flow 生图（要走浏览器：Chrome 登录 + bsk）"),
    ("字幕", ["node", str(ENGINE / "tools" / "script.mjs")], "PROJ", "out/口播脚本.md + out/字幕.srt"),
    ("渲染", ["node", str(ENGINE / "tools" / "render.mjs")], "PROJ", "out/*.mp4（约 20 分钟）"),
    ("验收", [PY, "tools/accept_emotion.py"], ROOT, "黑页 / 空页 / 字幕带"),
    ("抽帧", [PY, "tools/qc_snap.py"], ROOT, "26 页对照表 → out/snap/qc*.jpg"),
]
STEP_DESC = {s[0]: s[3] for s in STEPS}

KIND = {".png": "image", ".jpg": "image", ".jpeg": "image", ".webp": "image",
        ".mp4": "video", ".srt": "text", ".md": "text", ".json": "text", ".js": "text",
        ".txt": "text", ".log": "text", ".wav": "audio"}


def env():
    e = os.environ.copy()
    e["PATH"] = str(LOCALBIN) + os.pathsep + e.get("PATH", "")
    e["PYTHONUTF8"] = "1"
    e["PYTHONIOENCODING"] = "utf-8"
    return e


def projects():
    d = ROOT / "projects"
    return sorted([p.name for p in d.iterdir() if p.is_dir() and (p / "script-source.json").exists()])


def artifacts(proj):
    d = ROOT / "projects" / proj
    out = []
    for pat in ("out/**/*", "docs/*", "audio/*.wav", "pages/*.js", "voice.js", "script-source.json",
                "page-spec.json", "README.md"):
        for f in d.glob(pat):
            rel = f.relative_to(d).as_posix()
            # 审阅不该看到中间产物：分段/字幕分段/缓存 —— 否则 151 个 seg 把该看的淹了
            if rel.startswith(("out/chunks/", "out/subs/", "out/segments/")):
                continue
            if f.is_file() and f.stat().st_size > 0:
                out.append({"rel": rel, "kind": KIND.get(f.suffix.lower(), "file"),
                            "kb": max(1, int(f.stat().st_size / 1024)),
                            "mtime": int(f.stat().st_mtime)})

    # 该看的排前面：成片 → 抽帧表/对比图 → 字幕 → 图/页 → 其余
    def rank(a):
        r = a["rel"]
        if r.startswith("out/") and r.endswith(".mp4"):
            return 0
        if a["kind"] == "image" and (r.startswith("out/snap/") or r.startswith("docs/")):
            return 1
        if r.endswith((".srt", "口播脚本.md")):
            return 2
        if a["kind"] == "image":
            return 3
        if r.startswith(("pages/", "script-source.json", "page-spec.json")):
            return 5
        return 4
    return sorted(out, key=lambda a: (rank(a), -a["mtime"]))[:60]


def approvals(proj):
    f = ROOT / "projects" / proj / "docs" / "审批.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


class Handler(BaseHTTPRequestHandler):
    server_version = "video-factory-panel"

    def log_message(self, *a):        # 安静点
        pass

    def _send(self, code, body: bytes, ctype="text/html; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    # ---------- 路由 ----------
    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path == "/":
            return self._send(200, PAGE.encode("utf-8"))
        if u.path == "/api/state":
            proj = (q.get("project") or [""])[0]
            return self._json({"projects": projects(), "project": proj,
                               "steps": [{"name": s[0], "desc": s[3]} for s in STEPS],
                               "artifacts": artifacts(proj) if proj else [],
                               "approvals": approvals(proj) if proj else {}})
        if u.path == "/api/run":
            return self._run(q)
        if u.path == "/api/file":
            return self._file(q)
        return self._json({"error": "no such route"}, 404)

    def do_POST(self):
        u = urlparse(self.path)
        n = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(n) or b"{}")
        if u.path == "/api/new":
            return self._new(body)
        if u.path == "/api/mark":
            return self._mark(body)
        return self._json({"error": "no such route"}, 404)

    # ---------- 动作 ----------
    def _new(self, body):
        name = re.sub(r"[^\w-]", "-", (body.get("name") or "").strip()) or "new-film"
        cmd = [PY, "tools/new_film.py", name,
               "--title", body.get("title") or "未命名", "--minutes", str(body.get("minutes") or 6)]
        r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", env=env())
        return self._json({"ok": r.returncode == 0, "log": (r.stdout or "") + (r.stderr or ""), "project": name})

    def _mark(self, body):
        proj, rel, verdict = body.get("project"), body.get("rel"), body.get("verdict")
        f = ROOT / "projects" / proj / "docs" / "审批.json"
        f.parent.mkdir(parents=True, exist_ok=True)
        d = approvals(proj)
        d[rel] = {"verdict": verdict, "at": time.strftime("%Y-%m-%d %H:%M:%S")}
        f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        return self._json({"ok": True, "approvals": d})

    def _file(self, q):
        proj = (q.get("project") or [""])[0]
        rel = (q.get("rel") or [""])[0]
        base = (ROOT / "projects" / proj).resolve()
        f = (base / rel).resolve()
        if not str(f).startswith(str(base)) or not f.is_file():
            return self._json({"error": "bad path"}, 400)
        ctype = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp",
                 "mp4": "video/mp4", "srt": "text/plain; charset=utf-8", "md": "text/plain; charset=utf-8",
                 "json": "application/json; charset=utf-8", "js": "text/plain; charset=utf-8",
                 "wav": "audio/wav"}.get(f.suffix.lower().lstrip("."), "application/octet-stream")
        return self._send(200, f.read_bytes(), ctype)

    def _run(self, q):
        """跑一个阶段，把输出按 SSE 流出去（面板上实时看）。"""
        proj = (q.get("project") or [""])[0]
        step = (q.get("step") or [""])[0]
        hit = [s for s in STEPS if s[0] == step]
        if not proj or not hit:
            return self._json({"error": "缺 project 或 step"}, 400)
        _, cmd, cwd, _ = hit[0]
        cmd = [x.replace("{proj}", proj) for x in cmd]
        cwd = str(ROOT / "projects" / proj) if cwd == "PROJ" else str(ROOT)
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

        def sse(obj):
            try:
                self.wfile.write(("data: " + json.dumps(obj, ensure_ascii=False) + "\n\n").encode("utf-8"))
                self.wfile.flush()
            except Exception:                                      # noqa: BLE001
                pass

        sse({"line": f"$ {' '.join(str(c) for c in cmd)}", "cwd": cwd})
        t0 = time.time()
        try:
            p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 text=True, encoding="utf-8", errors="replace", env=env(), bufsize=1)
            for line in p.stdout:
                sse({"line": line.rstrip("\n")})
            p.wait()
            sse({"done": True, "code": p.returncode, "seconds": round(time.time() - t0, 1)})
        except Exception as e:                                     # noqa: BLE001
            sse({"line": f"✗ 面板出错：{e}", "done": True, "code": -1})


PAGE = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>video-factory 面板</title>
<style>
 :root { --bg:#14161a; --card:#1d2026; --line:#2b3038; --ink:#e8e6e1; --dim:#9aa0aa; --warm:#d9a441; --cold:#6aa6c4; }
 * { box-sizing:border-box } body { margin:0; background:var(--bg); color:var(--ink); font:14px/1.6 "Segoe UI",system-ui,sans-serif }
 header { padding:14px 18px; border-bottom:1px solid var(--line); display:flex; gap:14px; align-items:center; flex-wrap:wrap }
 h1 { font-size:15px; margin:0 12px 0 0; font-weight:600; letter-spacing:.5px }
 select, input, button, textarea { background:var(--card); color:var(--ink); border:1px solid var(--line); border-radius:8px; padding:6px 10px; font:inherit }
 button { cursor:pointer } button:hover { border-color:var(--warm) }
 button.primary { background:#2a2f38 } button.primary:hover { background:#333a45 }
 main { display:grid; grid-template-columns: 1fr 420px; gap:14px; padding:14px }
 .card { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:12px }
 .steps { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:10px }
 .steps button { padding:7px 12px }
 .steps button small { display:block; color:var(--dim); font-size:11px; font-weight:400 }
 pre { margin:0; max-height:46vh; overflow:auto; font:12px/1.5 ui-monospace,Consolas,monospace; white-space:pre-wrap; color:#cfe3d8 }
 .arts { display:grid; grid-template-columns:repeat(2,1fr); gap:10px }
 .art { border:1px solid var(--line); border-radius:10px; overflow:hidden; background:#191c21 }
 .art img, .art video { width:100%; display:block; background:#000; max-height:190px; object-fit:contain }
 .art .meta { padding:6px 8px; font-size:11px; color:var(--dim); display:flex; justify-content:space-between; gap:6px; align-items:center }
 .art .meta b { color:var(--ink); font-weight:500; overflow:hidden; text-overflow:ellipsis; white-space:nowrap }
 .verdict { display:flex; gap:4px }
 .verdict button { padding:2px 7px; font-size:11px }
 .ok { border-color:#4c8f5a !important; box-shadow:0 0 0 1px #4c8f5a inset } 
 .no { border-color:#a05252 !important; box-shadow:0 0 0 1px #a05252 inset }
 .new { display:flex; gap:8px; flex-wrap:wrap; align-items:center }
 .hint { color:var(--dim); font-size:12px; padding:2px 0 8px }
 .tag { font-size:11px; color:var(--dim) }
</style></head><body>
<header>
  <h1>video-factory 面板</h1>
  <select id="proj"></select>
  <span class="tag" id="projinfo"></span>
  <span style="flex:1"></span>
  <span class="new">
    <input id="nname" placeholder="新片目录名" size="14">
    <input id="ntitle" placeholder="标题" size="16">
    <input id="nmins" placeholder="分钟" size="4" value="6">
    <button class="primary" onclick="newProject()">＋ 建片</button>
  </span>
</header>
<main>
  <div>
    <div class="card">
      <div class="steps" id="steps"></div>
      <div class="hint" id="stepdesc">选一个工程，然后点阶段按钮。日志会实时流在这里。</div>
      <pre id="log">（还没有输出）</pre>
    </div>
  </div>
  <div class="card">
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
      <b>产物审阅</b><span class="tag" id="artcount"></span>
    </div>
    <div class="hint">图片/视频直接看；✓ 通过 / ✗ 打回 会写进 docs/审批.json（下次迭代读它）</div>
    <div class="arts" id="arts"></div>
  </div>
</main>
<script>
let state = { projects: [], project: "", artifacts: [], approvals: {} };
const $ = (id) => document.getElementById(id);
const esc = (s) => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));

async function load(keepLog) {
  const p = $("proj").value || state.project || "";
  const r = await fetch("/api/state?project=" + encodeURIComponent(p));
  state = await r.json();
  const sel = $("proj");
  if (sel.options.length !== state.projects.length) {
    sel.innerHTML = state.projects.map(n => `<option ${n===state.project?"selected":""}>${esc(n)}</option>`).join("");
  }
  $("steps").innerHTML = state.steps.map(s =>
    `<button class="primary" onclick="run('${s.name}')" onmouseover="$('stepdesc').textContent='${esc(s.desc)}'">${s.name}<small>${esc(s.desc.slice(0,14))}</small></button>`).join("");
  renderArts();
}
function renderArts() {
  const a = state.artifacts || [];
  $("artcount").textContent = a.length + " 个文件";
  $("arts").innerHTML = a.map(f => {
    const url = "/api/file?project=" + encodeURIComponent(state.project) + "&rel=" + encodeURIComponent(f.rel);
    const v = state.approvals[f.rel]?.verdict;
    const cls = v === "ok" ? "ok" : v === "no" ? "no" : "";
    let body = "";
    if (f.kind === "image") body = `<a href="${url}" target="_blank"><img src="${url}" loading="lazy"></a>`;
    else if (f.kind === "video") body = `<video src="${url}" controls preload="metadata"></video>`;
    else body = `<div style="padding:10px;font-size:11px;color:#9aa0aa">${esc(f.rel)}</div>`;
    return `<div class="art ${cls}">${body}
      <div class="meta"><b title="${esc(f.rel)}">${esc(f.rel)}</b>
        <span>${f.kb}KB</span>
        <span class="verdict">
          <button onclick="mark('${esc(f.rel)}','ok')">✓</button>
          <button onclick="mark('${esc(f.rel)}','no')">✗</button>
        </span></div></div>`;
  }).join("") || '<div class="hint">这个工程还没有产物。</div>';
}
async function mark(rel, verdict) {
  const r = await fetch("/api/mark", {method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({project: state.project, rel, verdict})});
  state.approvals = (await r.json()).approvals; renderArts();
}
async function newProject() {
  const name = $("nname").value, title = $("ntitle").value, minutes = $("nmins").value;
  if (!name) { alert("给新片起个目录名"); return; }
  $("log").textContent = "建片中…";
  const r = await fetch("/api/new", {method:"POST", headers:{"Content-Type":"application/json"},
    body: JSON.stringify({name, title, minutes})});
  const d = await r.json();
  $("log").textContent = d.log;
  await load(true);
  $("proj").value = d.project; state.project = d.project; await load(true);
}
async function run(step) {
  if (!state.project) { alert("先选工程"); return; }
  $("log").textContent = "";
  $("stepdesc").textContent = step + "：跑起来了，日志在下面流…";
  const es = new EventSource("/api/run?project=" + encodeURIComponent(state.project) + "&step=" + encodeURIComponent(step));
  es.onmessage = (m) => {
    const d = JSON.parse(m.data);
    if (d.line !== undefined) $("log").textContent += d.line + "\\n";
    if (d.done) {
      $("log").textContent += `\\n—— 结束（退出码 ${d.code}，${d.seconds}s）\\n`;
      $("log").scrollTop = $("log").scrollHeight;
      es.close(); load(true);
    }
    $("log").scrollTop = $("log").scrollHeight;
  };
  es.onerror = () => { es.close(); load(true); };
}
$("proj").addEventListener("change", () => load(true));
load();
setInterval(() => { if (!eventSourceOpen()) load(true); }, 8000);
function eventSourceOpen() { return document.querySelector("pre").dataset.streaming === "1"; }
</script></body></html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8899)
    ap.add_argument("--host", default="127.0.0.1")
    a = ap.parse_args()
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    print(f"面板起来了：http://{a.host}:{a.port}")
    print(f"  （工程目录：{ROOT / 'projects'}；引擎：{ENGINE.name}）")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()


if __name__ == "__main__":
    main()
