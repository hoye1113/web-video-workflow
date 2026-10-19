"""video-factory 面板后端：照 frametell 的信息架构给我们的流程做前台。

    首页（一句话开工）→ 工作台（左对话 / 右画面）→ 素材库（角色 / 处境图 / 本片素材）

设计纪律（照 `docs/harness-架构建议.md`）：
  · 面板只做两件事：**调 agent / 调脚本**、**读写文件状态**；编排逻辑不写在面板里
  · 过程用事件流（`events.jsonl`）驱动；原始终端输出只作为"展开看"
  · 审批落 `docs/审批.json`（人是唯一能点通过的人）

跑：
    python tools/panel/server.py            # http://127.0.0.1:8899
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs, unquote

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import pipeline                                    # noqa: E402

UI = pathlib.Path(__file__).resolve().parent / "ui.html"
LOCK = threading.Lock()          # 一次只让一个阶段在跑（生图/渲染都是重活）
RUNNING = {"step": None, "project": None}
AUTO = {"on": True}              # 自动推进开关（人点"暂停"就关）


def conductor_loop():
    """后台自动推进：每 5 秒看一眼，把"没做完的下一件事"做掉。

    照 frametell 的分工 —— 阶段自动走，人只说/点头/看。**闸门没过就不动**：
    所以在"等你确认分镜"时它什么都不会做。
    """
    sys.path.insert(0, str(ROOT / "tools"))
    import conductor                                          # noqa: PLC0415
    while True:
        time.sleep(5)
        if not AUTO["on"] or RUNNING["step"]:
            continue
        for proj in pipeline.projects():
            if conductor.paused(proj):
                continue
            with LOCK:
                if RUNNING["step"]:
                    continue
                RUNNING.update(step="（自动）", project=proj)
            try:
                conductor.advance(proj, say=lambda m: pipeline.emit(proj, "log", text=m))
            except Exception as e:                            # noqa: BLE001
                pipeline.emit(proj, "log", text=f"推进器出错：{e}")
            finally:
                RUNNING.update(step=None, project=None)

EDGE_VOICES = [("zh-CN-XiaoxiaoNeural", "小晓 · 女声（默认）"), ("zh-CN-XiaoyiNeural", "小艺 · 女声"),
               ("zh-CN-YunxiNeural", "云希 · 男声"), ("zh-CN-YunyangNeural", "云扬 · 男声（播报）"),
               ("zh-CN-YunjianNeural", "云健 · 男声（沉稳）")]


def status_of(proj):
    """项目状态（照 frametell 首页那几个状态）。"""
    d = pipeline.proj_dir(proj)
    q = pipeline.queue(proj)
    g = pipeline.gate_state(proj)
    ev = pipeline.events(proj, limit=60)
    running = RUNNING["step"] if RUNNING["project"] == proj else None
    film = sorted((d / "out").glob("*.mp4")) if (d / "out").exists() else []
    if running:
        st = "running"
    elif film:
        st = "done" if g.get("film") == "ok" else "awaiting"
    elif any(e.get("kind") == "stage" and e.get("status") == "failed" for e in ev[-6:]):
        st = "failed"
    elif any(t["status"] in ("queued", "retry") for t in q["tasks"]):
        st = "running"
    else:
        st = "idle"
    src = pipeline.read_json(d / "script-source.json", {}) or {}
    pages = src.get("pages", [])
    return {"id": proj, "title": src.get("title") or proj, "pages": len(pages),
            "cues": sum(len(p.get("cues", [])) for p in pages),
            "status": st, "running": running,
            "images": sum(1 for t in q["tasks"] if t["status"] == "review"),
            "gates": g, "film": film[-1].name if film else "",
            "at": int((d / "events.jsonl").stat().st_mtime) if (d / "events.jsonl").exists() else 0}


class H(BaseHTTPRequestHandler):
    server_version = "vf-panel"

    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False)
        b = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(b)

    # ---------- GET ----------
    def do_GET(self):
        try:
            return self._do_GET()
        except Exception as e:                                  # noqa: BLE001
            import traceback
            traceback.print_exc()
            try:
                return self._send(500, {"error": f"{type(e).__name__}: {e}"})
            except Exception:                                   # noqa: BLE001
                pass

    def _do_GET(self):
        u, q = urlparse(self.path), None
        q = parse_qs(u.query)
        one = lambda k, d="": (q.get(k) or [d])[0]      # noqa: E731
        if u.path == "/":
            return self._send(200, UI.read_text(encoding="utf-8"), "text/html; charset=utf-8")
        if u.path == "/api/projects":
            return self._send(200, [status_of(p) for p in pipeline.projects()])
        if u.path == "/api/state":
            proj = one("project")
            if not proj:
                return self._send(400, {"error": "缺 project"})
            d = pipeline.proj_dir(proj)
            sys.path.insert(0, str(ROOT / "tools"))
            import conductor                                      # noqa: PLC0415
            try:
                nxt = conductor.step_for(proj)
            except Exception as e:                                # noqa: BLE001
                nxt = (None, f"推进器判断出错：{e}")
            return self._send(200, {
                "project": status_of(proj),
                "next": {"step": nxt[0], "why": nxt[1]},
                "paused": conductor.paused(proj),
                "steps": [{"name": s[0], "say": s[3], "desc": " ".join(s[1][1:3])} for s in pipeline.STEPS],
                "gates": pipeline.GATES, "gate_state": pipeline.gate_state(proj),
                "queue": pipeline.queue(proj)["tasks"],
                "approvals": pipeline.approvals(proj),
                "artifacts": artifacts(proj),
                "page_spec": pipeline.read_json(d / "page-spec.json", []) or [],
                "running": RUNNING if RUNNING["project"] == proj else None,
                "voices": EDGE_VOICES,
            })
        if u.path == "/api/events":
            return self._events(one("project"), float(one("since", "0") or 0))
        if u.path == "/api/library":
            idx = pipeline.read_json(ROOT / "projects" / "scene-library" / "index.json", {})
            return self._send(200, idx or {"images": []})
        if u.path == "/api/timeline":
            return self._send(200, timeline(one("project")))
        if u.path == "/api/env":
            return self._send(200, pipeline.env_check(deep=(one("deep") == "1")))
        if u.path == "/api/file":
            return self._file(one("project"), one("rel"))
        if u.path == "/api/libfile":
            return self._libfile(one("rel"))
        return self._send(404, {"error": "no route"})

    # ---------- POST ----------
    def do_POST(self):
        try:
            return self._do_POST()
        except Exception as e:                                  # noqa: BLE001
            import traceback
            traceback.print_exc()
            try:
                return self._send(500, {"error": f"{type(e).__name__}: {e}"})
            except Exception:                                   # noqa: BLE001
                pass

    def _do_POST(self):
        u = urlparse(self.path)
        n = int(self.headers.get("Content-Length") or 0)
        b = json.loads(self.rfile.read(n) or b"{}")
        if u.path == "/api/new":
            return self._new(b)
        if u.path == "/api/run":
            return self._run(b)
        if u.path == "/api/queue":
            tid = pipeline.queue_add(b["project"], b["page"], b.get("cast", "小树"),
                                     b.get("scene", ""), b.get("out"))
            return self._send(200, {"ok": True, "id": tid})
        if u.path == "/api/queue/retry":
            pipeline.queue_set(b["project"], b["id"], status="retry", error="")
            pipeline.emit(b["project"], "page", id=b.get("page", ""), status="retry", detail="打回重做")
            return self._send(200, {"ok": True})
        if u.path == "/api/approve":
            pipeline.mark(b["project"], f'gate:{b["gate"]}',
                          b.get("verdict", "ok"), b.get("note", ""))
            if b.get("gate") == "img" and b.get("note"):
                pipeline.emit(b["project"], "say", text=b["note"])
            return self._send(200, {"ok": True, "gate_state": pipeline.gate_state(b["project"])})
        if u.path == "/api/mark":
            d = pipeline.mark(b["project"], b["rel"], b.get("verdict", "ok"), b.get("note", ""))
            return self._send(200, {"ok": True, "approvals": d})
        if u.path == "/api/assign":
            # 把库里的一张图指定给某一页：改 page-spec.json 的 asset，再重生成该页代码
            proj, page, asset = b["project"], b["page"], b["asset"]
            spec_f = pipeline.proj_dir(proj) / "page-spec.json"
            spec = pipeline.read_json(spec_f, []) or []
            hit = next((p for p in spec if p.get("id") == page), None)
            if not hit:
                return self._send(404, {"error": f"{proj} 的页表里没有 {page}"})
            hit["asset"] = asset
            spec_f.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
            r = pipeline.run([pipeline.PY, "tools/make_pages.py", "--project", proj], timeout=300)
            pipeline.emit(proj, "page", id=page, status="saved",
                          detail=f"换成 {asset}（页代码已重生成）")
            pipeline.mark(proj, f"library/{asset}", "ok", f"指定给 {page}")
            return self._send(200, {"ok": r.returncode == 0, "log": (r.stdout or "") + (r.stderr or "")})
        if u.path == "/api/pause":
            sys.path.insert(0, str(ROOT / "tools"))
            import conductor                                      # noqa: PLC0415
            conductor.set_paused(b["project"], b.get("on", True))
            AUTO["on"] = not b.get("on", True) is True or AUTO["on"]
            return self._send(200, {"ok": True, "paused": conductor.paused(b["project"])})
        if u.path == "/api/say":
            pipeline.emit(b["project"], "say", text=b.get("text", ""),
                          refs=b.get("refs") or [])
            return self._send(200, {"ok": True})
        return self._send(404, {"error": "no route"})

    # ---------- 具体动作 ----------
    def _new(self, b):
        name = pipeline.slug(b.get("name") or b.get("topic", ""))
        minutes = float(b.get("minutes") or 6)
        cmd = [pipeline.PY, "tools/new_film.py", name, "--title", b.get("title") or b.get("topic") or name,
               "--minutes", str(minutes), "--force"]
        r = pipeline.run(cmd, timeout=300)
        proj = pipeline.proj_dir(name)
        # 主题与参数记进工程（人物/配音/时长），并把角色记进 README
        meta = {"topic": b.get("topic", ""), "minutes": minutes, "voice": b.get("voice", ""),
                "cast": b.get("cast") or ["小树", "小芽"], "style": "warm-emotion",
                "materials": b.get("materials") or []}
        (proj / "brief.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
        pipeline.emit(name, "say", text=f'新片：{b.get("topic") or name}（目标 {minutes:g} 分钟）')
        pipeline.emit(name, "stage", stage="建片", status="done", detail=f"projects/{name}")
        return self._send(200, {"ok": r.returncode == 0, "project": name,
                                "log": (r.stdout or "") + (r.stderr or "")})

    def _run(self, b):
        proj, step = b.get("project"), b.get("step")
        hit = pipeline.STEP.get(step)
        if not proj or not hit:
            return self._send(400, {"error": "缺 project 或 step"})
        if RUNNING["step"]:
            return self._send(409, {"error": f'正在跑「{RUNNING["step"]}」，等它完'})
        _, cmd, cwd, say = hit
        cmd = [x.replace("{proj}", proj) for x in cmd]
        cwd = pipeline.proj_dir(proj) if cwd == "PROJ" else pipeline.ROOT
        pipeline.emit(proj, "stage", stage=step, status="start", detail=say["start"])

        def worker():
            RUNNING.update(step=step, project=proj)
            t0 = time.time()
            try:
                p = subprocess.Popen([str(c) for c in cmd], cwd=str(cwd), stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, text=True, encoding="utf-8",
                                     errors="replace", env=pipeline.env(), bufsize=1)
                for line in p.stdout:
                    pipeline.emit(proj, "log", text=line.rstrip("\n")[:400], step=step)
                p.wait()
                code = p.returncode
            except Exception as e:                              # noqa: BLE001
                code = -1
                pipeline.emit(proj, "log", text=f"✗ {e}", step=step)
            pipeline.emit(proj, "stage", stage=step,
                          status="done" if code == 0 else "failed",
                          detail=f'{say["done"] if code == 0 else "没成"}（{time.time() - t0:.0f}s）')
            RUNNING.update(step=None, project=None)

        threading.Thread(target=worker, daemon=True).start()
        return self._send(200, {"ok": True, "started": step})

    # ---------- 事件流（SSE） ----------
    def _events(self, proj, since):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        cur = since
        beat = 0
        while beat < 240:                     # 最多挂 4 分钟，前端会重连
            for r in pipeline.events(proj, since=cur):
                cur = max(cur, r.get("ts", cur))
                try:
                    self.wfile.write(("data: " + json.dumps(r, ensure_ascii=False) + "\n\n").encode("utf-8"))
                    self.wfile.flush()
                except Exception:                               # noqa: BLE001
                    return
            time.sleep(1.0)
            beat += 1

    # ---------- 文件 ----------
    def _file(self, proj, rel):
        base = pipeline.proj_dir(proj).resolve()
        f = (base / rel).resolve()
        if not str(f).startswith(str(base)) or not f.is_file():
            return self._send(400, {"error": "bad path"})
        return self._send(200, f.read_bytes(), ctype(f))

    def _libfile(self, rel):
        base = (ROOT / "projects" / "scene-library").resolve()
        f = (base / rel).resolve()
        if not str(f).startswith(str(base)) or not f.is_file():
            return self._send(400, {"error": "bad path"})
        return self._send(200, f.read_bytes(), ctype(f))


def ctype(f: pathlib.Path):
    return {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp",
            "mp4": "video/mp4", "wav": "audio/wav", "srt": "text/plain; charset=utf-8",
            "md": "text/plain; charset=utf-8", "json": "application/json; charset=utf-8",
            "js": "text/plain; charset=utf-8", "txt": "text/plain; charset=utf-8"}.get(
        f.suffix.lower().lstrip("."), "application/octet-stream")


def artifacts(proj):
    """产物（给"画面/产物"两处用）：**成片永远排第一**，其次对照图，再其次字幕/文档。"""
    d = pipeline.proj_dir(proj)
    out = []
    for pat in ("out/*.mp4", "out/snap/*.jpg", "docs/*.jpg", "out/字幕.srt", "out/口播脚本.md",
                "docs/*.md", "pages/*.js", "script-source.json", "page-spec.json", "voice.js"):
        for f in d.glob(pat):
            if f.is_file() and f.stat().st_size > 0:
                rel = f.relative_to(d).as_posix()
                kind = ("video" if f.suffix == ".mp4" else
                        "image" if f.suffix in (".png", ".jpg") else "text")
                out.append({"rel": rel, "kind": kind, "kb": max(1, int(f.stat().st_size / 1024)),
                            "mtime": int(f.stat().st_mtime)})

    def rank(a):
        r = a["rel"]
        if r.startswith("out/") and r.endswith(".mp4"):
            return 0
        if a["kind"] == "image":
            return 1
        if r.endswith(".srt"):
            return 2
        return 3
    return sorted(out, key=lambda a: (rank(a), -a["mtime"]))[:40]


_TIMELINE_CACHE = {}
_TIMELINE_LOCK = threading.Lock()


def timeline(proj):
    """页的起止时间（走引擎 layout；带配音时是真实语速）。缓存 60 秒。"""
    hit = _TIMELINE_CACHE.get(proj)
    if hit and time.time() - hit[0] < 60:
        return hit[1]
    with _TIMELINE_LOCK:                      # 同时来两个请求时别互相踩临时文件
        hit = _TIMELINE_CACHE.get(proj)
        if hit and time.time() - hit[0] < 60:
            return hit[1]
        js = (f"import {{ loadEpisode }} from '{pipeline.ENGINE.as_uri()}/tools/lib.mjs';\n"
              "const { L } = loadEpisode();\n"
              "console.log(JSON.stringify({duration: L.duration,\n"
              " pages: L.pages.map(p => ({id: p.id, start: p.start, end: p.end, title: p.title,\n"
              "   cues: p.cues.map(c => ({t: c.text, s: c.start}))}))}));\n")
        import tempfile
        fd, path = tempfile.mkstemp(suffix=".mjs", prefix="vf-timeline-")
        try:
            os.write(fd, js.encode("utf-8"))
            os.close(fd)
            r = pipeline.run(["node", path], cwd=pipeline.proj_dir(proj), timeout=120)
        finally:
            pathlib.Path(path).unlink(missing_ok=True)
        line = [x for x in (r.stdout or "").splitlines() if x.strip().startswith("{")]
        data = json.loads(line[-1]) if line else {"pages": [], "duration": 0,
                                                  "error": (r.stderr or "")[:200]}
        _TIMELINE_CACHE[proj] = (time.time(), data)
        return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8899)
    ap.add_argument("--host", default="127.0.0.1")
    a = ap.parse_args()
    srv = ThreadingHTTPServer((a.host, a.port), H)
    print(f"面板：http://{a.host}:{a.port}   工程目录：{pipeline.ROOT / 'projects'}")
    threading.Thread(target=conductor_loop, daemon=True).start()
    print("自动推进：开（面板上可暂停；闸门没过时它不会动）")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()


if __name__ == "__main__":
    main()
