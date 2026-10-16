"""video-factory 本地服务：静态预览 + 项目/镜头 API + 渲染队列 + LLM 接口。

只依赖标准库。跑：python app/server.py [--port 8777]
"""
import argparse
import json
import mimetypes
import os
import re
import subprocess
import sys
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import store                       # noqa: E402
import jobs as jobs_mod            # noqa: E402
import prompts                     # noqa: E402
import llm as llm_mod              # noqa: E402
import director                    # noqa: E402
import presets                     # noqa: E402
import text as T                   # noqa: E402
import scene_check                 # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WEB = ROOT / "app" / "web"
ENGINE = ROOT / "base-arch" / "scripts" / "engine"
PROJECTS = ROOT / "projects"

QUEUE = jobs_mod.Manager()
AI = llm_mod.LLM()

# 一个够用的示例场景，给模型当结构参考（学结构，不抄题材）
EXAMPLE = """// 一只沙漏，细沙一粒粒往下落
SCENES['zz_hourglass'] = (() => {
  const W = 1920, H = 1080, TAU = Math.PI * 2;
  const { clamp, lerp, ease, rng } = U;
  const C = { bg:'#F3EEE6', ink:'#2A2A2A', sand:'#E9B872', sandDk:'#D9A860', red:'#C8553D' };
  const ink = (c, path, fill, lw = 5) => {
    if (fill) { c.fillStyle = fill; c.fill(path); }
    if (lw) { c.strokeStyle = C.ink; c.lineWidth = lw; c.lineJoin='round'; c.lineCap='round'; c.stroke(path); }
  };
  const CX = 960, TOP = 258, BOT = 826, HW = 188, NY = 548, NW = 16;
  const glass = (() => { const p = new Path2D();
    p.moveTo(CX-HW, TOP); p.quadraticCurveTo(CX-HW+58, NY-132, CX-NW, NY);
    p.quadraticCurveTo(CX-HW+58, NY+132, CX-HW, BOT); p.lineTo(CX+HW, BOT);
    p.quadraticCurveTo(CX+HW-58, NY+132, CX+NW, NY);
    p.quadraticCurveTo(CX+HW-58, NY-132, CX+HW, TOP); p.closePath(); return p; })();
  const SAND = []; { const r = rng(22); for (let i=0;i<36;i++) SAND.push({o:r()*2-1, ph:r(), sp:0.85+r()*0.6}); }
  return {
    draw(c, lt, t) {
      const p = clamp(lt / 5);
      c.fillStyle = C.bg; c.fillRect(0, 0, W, H);                    // 背景自己画
      ink(c, glass, '#FDFBF7');
      const surfY = lerp(TOP+58, NY-92, ease.inOut(p));
      const peakY = BOT - Math.pow(p, 1.2) * 250;
      c.save(); c.clip(glass);
      c.fillStyle = C.sand; c.fillRect(CX-HW, surfY, HW*2, NY-surfY+6);          // 上沙面下降
      const hill = new Path2D();                                                  // 下沙堆长高
      const dxB = (BOT + 12 - peakY) * 0.95;
      hill.moveTo(CX-dxB, BOT+14); hill.lineTo(CX-22, peakY+10);
      hill.quadraticCurveTo(CX, peakY-4, CX+22, peakY+10); hill.lineTo(CX+dxB, BOT+14);
      hill.closePath(); c.fillStyle = C.sand; c.fill(hill);
      c.strokeStyle = '#C9944C'; c.lineWidth = 3.4; c.lineCap='round';            // 落沙粒子
      for (const s of SAND) {
        const q = (t*s.sp*1.05 + s.ph) % 1;
        const y = NY + q*(peakY-NY+20), x = CX + s.o*(5+q*7);
        c.beginPath(); c.moveTo(x, y); c.lineTo(x, y + 4*(2.2+q*2.6)); c.stroke();
      }
      c.restore();
      ink(c, glass, null);                                                        // 轮廓压回最上层
      ink(c, U.poly([[CX-HW-40, TOP-58],[CX+HW+40, TOP-58],[CX+HW+40, TOP],[CX-HW-40, TOP]]), C.red);
    },
  };
})();"""


RATE = 400          # 字/分钟。实测口播语速（186 秒 1248 字），不是估的 220

# 场景文件的注册行：SCENES['02'] = ...
_SCENE_REG = re.compile(r"SCENES\['([^']+)'\]\s*=")


def clip_minutes(script):
    return max(0.5, len(re.sub(r"\s", "", script or "")) / RATE)


class H(BaseHTTPRequestHandler):
    server_version = "video-factory"
    protocol_version = "HTTP/1.1"

    # ---------- 小工具 ----------

    def log_message(self, fmt, *a):
        pass

    def _send(self, code, body=b"", ctype="application/json; charset=utf-8"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode("utf-8")
        elif isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _err(self, code, msg):
        self._send(code, {"error": str(msg)})

    def _json_body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if not n:
            return {}
        raw = self.rfile.read(n).decode("utf-8", "replace")
        try:
            return json.loads(raw)
        except Exception as e:                                  # noqa: BLE001
            print(f"[err] 请求体不是合法 JSON（{e}）：{raw[:300]}", flush=True)
            raise

    def _file(self, path: Path):
        if not path.is_file():
            return self._err(404, f"没有这个文件：{path.name}")
        ctype = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        if ctype.startswith("text/") or ctype in ("application/javascript", "application/json"):
            ctype += "; charset=utf-8"
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Accept-Ranges", "none")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        try:
            self.wfile.write(data)
        except (BrokenPipeError, ConnectionResetError):
            pass

    # ---------- GET ----------

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        p, q = u.path, urllib.parse.parse_qs(u.query)
        try:
            return self._get(p, q)
        except Exception as e:                                      # noqa: BLE001
            return self._err(500, e)

    def _get(self, p, q):
        # 页面与静态
        if p in ("/", "/index.html"):
            return self._file(WEB / "index.html")
        if p.startswith("/web/"):
            return self._safe_file(WEB, p[5:])
        if p.startswith("/engine/"):
            return self._safe_file(ENGINE, p[8:])
        if p.startswith("/work/"):
            return self._safe_file(PROJECTS, p[6:])

        # API
        if p == "/api/projects":
            return self._send(200, store.list_projects())
        m = re.match(r"^/api/projects/([a-z0-9_]+)$", p)
        if m:
            d = store.load(m.group(1))
            if not d:
                return self._err(404, "项目不存在")
            # 给每一页带上状态：有没有代码、代码是不是按当前设定写的
            for s in d.get("shots", []):
                s["hasScene"] = store.scene_path(m.group(1), s["id"]).exists()
                s["stale"] = bool(s.get("sceneHash")) and s["sceneHash"] != store.shot_fingerprint(s)
            return self._send(200, d)
        m = re.match(r"^/api/projects/([a-z0-9_]+)/scene/([a-z0-9_]+)$", p)
        if m:
            src = store.read_scene(m.group(1), m.group(2))
            return self._send(200, {"source": src})
        if p == "/api/jobs":
            return self._send(200, QUEUE.list())
        if p == "/api/presets":
            return self._send(200, presets.listing())
        # 刻意不提供"列模型/换模型"的接口：绑定 OpenCode Go 套餐，模型写死在 llm.MODEL
        return self._err(404, "没有这个路由")

    def _safe_file(self, base: Path, rel: str):
        # 注意：这里不能用 Path.resolve()——它会把 Windows 目录联接解析到真实目标，
        # 于是 engine/demos/<项目> 会被判成"越界"。用字面路径归一化，只挡 ../
        rel = urllib.parse.unquote(rel).replace("\\", "/").lstrip("/")
        base_abs = os.path.abspath(base)
        f = os.path.abspath(os.path.join(base_abs, rel))
        if os.path.commonpath([base_abs, f]) != base_abs:
            return self._err(403, "越界")
        return self._file(Path(f))

    # ---------- POST / PUT / DELETE ----------

    def do_POST(self):
        u = urllib.parse.urlparse(self.path)
        try:
            return self._post(u.path)
        except Exception as e:                                      # noqa: BLE001
            import traceback
            tb = traceback.format_exc()
            print(f"[err] POST {u.path}\n{tb}", flush=True)
            return self._err(500, f"{e}\n{tb.splitlines()[-3] if len(tb.splitlines())>3 else ''}")

    do_PUT = do_POST

    def _post(self, p):
        b = self._json_body()

        if p == "/api/projects":
            return self._send(200, store.create(b.get("name", ""), b.get("title", "")))

        m = re.match(r"^/api/projects/([a-z0-9_]+)$", p)
        if m:
            name = m.group(1)
            cur = store.load(name) or store.default_project(name)
            for k in ("title", "style", "script", "shots", "fps", "width", "height",
                      "skeleton", "approved"):
                if k not in b:
                    continue
                cur[k] = _text(b[k], k) if k in ("title", "script") else b[k]
            if isinstance(cur.get("style"), dict) and cur["style"].get("preset"):
                cur["style"] = presets.expand(cur["style"])       # 选预设就自动带上画风锁和色板
            store.save(name, cur)
            return self._send(200, cur)

        m = re.match(r"^/api/projects/([a-z0-9_]+)/scene/([a-z0-9_]+)$", p)
        if m:
            store.write_scene(m.group(1), m.group(2), b.get("source", ""))
            return self._send(200, {"ok": True})

        m = re.match(r"^/api/projects/([a-z0-9_]+)/shots/([a-z0-9_]+)$", p)
        if m:
            name, sid = m.group(1), m.group(2)
            cur = store.load(name) or {}
            shots = cur.get("shots", [])
            found = False
            for s in shots:
                if s.get("id") == sid:
                    s.update({k: v for k, v in b.items() if k != "id"})
                    found = True
            if not found:
                shots.append({"id": sid, **b})
            cur["shots"] = shots
            store.save(name, cur)
            return self._send(200, cur)

        if p == "/api/render":
            name, sid = b["project"], b["shot"]
            shots = (store.load(name) or {}).get("shots", [])
            shot = next((s for s in shots if s["id"] == sid), None)
            if not shot:
                return self._err(400, "没有这个镜头")
            store.link_demo(name)
            fps = (store.load(name) or {}).get("fps", 30)
            j = QUEUE.render_shot(name, sid, shot.get("dur", 4), fps)
            return self._send(200, j.dict())

        if p == "/api/stills":
            name, sid = b["project"], b["shot"]
            shots = (store.load(name) or {}).get("shots", [])
            shot = next((s for s in shots if s["id"] == sid), None)
            if not shot:
                return self._err(400, "没有这个镜头")
            store.link_demo(name)
            at = b.get("at") or [0.3, float(shot.get("dur", 4)) * 0.4, float(shot.get("dur", 4)) * 0.85]
            j = QUEUE.render_still(name, sid, shot.get("dur", 4), at)
            return self._send(200, j.dict())

        if p == "/api/images":
            # 按 imagePrompt 去 Flow 生图（mode=image/mixed 的页）。不传 shots 就挑全部缺图的页。
            name = self._proj(b)
            import flowgen
            only = b.get("shots") or None
            j = QUEUE.submit_fn("images", f"{name} · 生图" + (f" {len(only)} 页" if only else ""),
                                lambda job: setattr(job, "result", flowgen.do_images(name, only, job)))
            return self._send(200, j.dict())

        if p == "/api/image_audit":
            # 生图体检：量构图，不合格的带着修正要求重画（重画过的页要重写场景代码）
            name = self._proj(b)
            only = b.get("shots") or None
            j = QUEUE.submit_fn("image_audit", f"{name} · 生图体检" + (f" {len(only)} 页" if only else ""),
                                lambda job: setattr(job, "result",
                                                    flowgen.do_image_audit(name, only, job,
                                                                           regen=bool(b.get("regen", True)))))
            return self._send(200, j.dict())

        if p == "/api/lint_fix":
            # 只按静态检查改（小修）：不重跑整页生成
            name = self._proj(b)
            shots = b.get("shots") or None
            j = QUEUE.submit_fn("lint_fix", f"{name} · 按静态检查改 {len(shots) if shots else '全部'} 页",
                                lambda job: setattr(job, "result", do_lint_fix(name, shots, job)))
            return self._send(200, j.dict())

        if p == "/api/scenes":
            # 批量写场景代码。不传 shots 就把还没写（或设定变了）的页都写了。
            name = self._proj(b)
            only = b.get("shots") or None
            j = QUEUE.submit_fn("scenes", f"{name} · 写场景代码" + (f" {len(only)} 页" if only else "（全部缺的）"),
                                lambda job: setattr(job, "result", do_scenes(name, only, job)))
            return self._send(200, j.dict())

        if p == "/api/film":
            # 一键整片：逐页渲 + 拼接。之前只有"拼接"（只能拼已经渲好的），整片从没跑过。
            name = self._proj(b)
            j = QUEUE.submit_fn("film", f"{name} · 整片出片",
                                lambda job: setattr(job, "result", do_film(name, job)))
            return self._send(200, j.dict())

        if p == "/api/concat":
            name = b["project"]
            shots = [s["id"] for s in (store.load(name) or {}).get("shots", [])]
            store.link_demo(name)
            j = QUEUE.concat(name, shots, b.get("name") or "成片.mp4")
            return self._send(200, j.dict())

        if p == "/api/jobs/clear":
            QUEUE.clear_finished()
            return self._send(200, {"ok": True})

        if p == "/api/shotlist":
            return self._shotlist(b)

        if p == "/api/scene":
            return self._scene(b)

        if p == "/api/review":
            return self._review(b)

        if p == "/api/revise":
            return self._revise(b)

        if p == "/api/chat":
            return self._chat(b)

        if p == "/api/director":
            name, sid = b["project"], b["shot"]
            shots = (store.load(name) or {}).get("shots", [])
            if not any(s["id"] == sid for s in shots):
                return self._err(400, "没有这个镜头")
            if not store.read_scene(name, sid).strip():
                return self._err(400, "这一镜还没有代码，先「写场景代码」")
            store.link_demo(name)
            rounds = max(1, min(int(b.get("rounds") or 3), 6))
            j = QUEUE.submit_fn("director", f"{name} · 镜 {sid} 导演回路 {rounds} 轮",
                                director.make_loop(AI, name, sid, rounds=rounds))
            return self._send(200, j.dict())

        if p == "/api/versions":
            name, sid = b["project"], b["shot"]
            return self._send(200, store.list_versions(name, sid))

        return self._err(404, "没有这个路由")

    # ---------- LLM：全部做成后台任务 ----------

    def _job(self, kind, title, fn):
        j = QUEUE.submit_fn(kind, title, fn)
        return self._send(200, j.dict())

    def _chat(self, b):
        """聊天：按 Vercel AI SDK 的 UI message stream 协议流式返回。

        前端用 `useDataStreamRuntime({ api: "/api/chat" })` 直接吃，不用写运行时。
        模型写死在 llm.MODEL（绑定 OpenCode Go 套餐，不给切）。

        注意请求体形状：assistant-ui 发来的**不是** {message: "..."}，
        而是 AI SDK 的整个线程 {messages: [{role, parts:[{type:"text",text}]}]}
        （旧版是 content 而不是 parts）。两种都认。
        """
        import chat as chat_mod
        name = self._proj(b)
        msg = _last_user_text(b)
        if not msg:
            print("[chat] 收到不认识的请求体：" + json.dumps(b, ensure_ascii=False)[:400], flush=True)
            return self._err(400, "没有消息")
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("x-vercel-ai-ui-message-stream", "v1")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "close")
        self.end_headers()

        def write(chunk):
            try:
                self.wfile.write(chunk)
                self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass

        try:
            chat_mod.stream(name, msg, write)
        except Exception as e:                                  # noqa: BLE001
            import traceback
            print("[chat] " + traceback.format_exc(), flush=True)
            write(chat_mod.sse({"type": "text-delta", "id": "t0", "delta": f"\n\n出错了：{e}"}))
            write(chat_mod.sse({"type": "finish"}))
            write(chat_mod.sse("[DONE]"))
        self.close_connection = True

    def _proj(self, b):
        name = b.get("project", "")
        if not store.valid_name(name) or not store.load(name):
            raise ValueError("项目不存在")
        return name

    def _shotlist(self, b):
        name = self._proj(b)
        script = _text(b.get("script") or (store.load(name) or {}).get("script"), "script").strip()
        if not script:
            raise ValueError("没有文案")
        return self._job("shotlist", f"{name} · 切成页面",
                         lambda j: setattr(j, "result", do_shotlist(name, script, j)))

    def _scene(self, b):
        name, sid = self._proj(b), b["shot"]
        return self._job("scene", f"{name} · 页 {sid} 写场景",
                         lambda j: setattr(j, "result", do_scene(name, sid, j)))

    def _review(self, b):
        name, sid = self._proj(b), b["shot"]
        return self._job("review", f"{name} · 页 {sid} 评审",
                         lambda j: setattr(j, "result", do_review(name, sid, j)))

    def _revise(self, b):
        name, sid = self._proj(b), b["shot"]
        rev = b.get("review") or {}
        return self._job("revise", f"{name} · 页 {sid} 按意见改",
                         lambda j: setattr(j, "result", do_revise(name, sid, rev, j)))
def _last_user_text(b):
    """从 AI SDK 的请求体里取出最后一条用户消息的文本。

    assistant-ui 的 data-stream 运行时发来的**不是** {message: "..."}，
    而是整个线程 {messages: [{role, parts:[{type:"text",text}]}]}
    （旧版是 content 而不是 parts）。两种都认。
    """
    if isinstance(b.get("message"), str) and b["message"].strip():
        return b["message"].strip()
    for m in reversed(b.get("messages") or []):
        if not isinstance(m, dict) or m.get("role") != "user":
            continue
        parts = m.get("parts")
        if isinstance(parts, list):
            t = "".join(p.get("text") or "" for p in parts
                        if isinstance(p, dict) and p.get("type") == "text")
            if t.strip():
                return t.strip()
        c = m.get("content")
        if isinstance(c, str) and c.strip():
            return c.strip()
        if isinstance(c, list):
            t = "".join(p.get("text") or "" for p in c
                        if isinstance(p, dict) and p.get("type") == "text")
            if t.strip():
                return t.strip()
    return ""


_text = T.text_field          # 请求字段类型校验（PowerShell 会把长字符串包成 {value:...}）
_strip_fence = T.strip_fence
_extract_json = T.extract_json
_fix_scene_id = T.fix_scene_id


# ---------------------------------------------------------------- 长调用（进队列跑）
#
# 这几个都要调模型，一次 30 秒到 3 分钟。**不能同步等**：实测客户端等满 25 分钟、
# 会话被拖死。统一丢进队列，立刻返回 job id，前端轮询拿 result。

def do_shotlist(name, script, job):
    cur = store.load(name) or {}
    style = cur.get("style") or {}
    mins = clip_minutes(script)
    n = max(3, min(round(mins * 60 / 15), 30))            # 平均 15 秒一页
    job.say(f"文案 {len(script)} 字 ≈ {mins:.1f} 分钟，目标 {n} 页左右")
    job.say("模型在读文案、定骨架…")
    prompt = prompts.SHOTLIST.format(
        minutes=mins, nmin=max(3, round(n * 0.8)), nmax=max(5, round(n * 1.25)),
        look=style.get("look") or "（未指定，你定一套克制的）",
        palette="、".join(style.get("palette") or []) or "（未指定，你定 3-6 个色值，不要蓝紫渐变）",
        character=style.get("character") or "只出手和背影，不画脸",
        script=script,
    )
    text = AI.generate(prompt)
    obj = _extract_json(text, dict)
    pages = obj.get("pages", [])
    skeleton = obj.get("skeleton", [])
    if not pages:
        raise ValueError("模型没有给出页面：" + text[:300])
    # 页列表换了，旧场景对应的是旧页：挪走，不要留着被当成新页的代码用
    moved = store.archive_scenes(name, time.strftime("%Y%m%d_%H%M%S"))
    if moved:
        job.say(f"旧的 {moved} 个场景已挪到 scenes_old/（页换了，它们对不上了）")
    for p in pages:
        p.setdefault("status", "draft")
        p.setdefault("role", "")
        p.setdefault("narration", "")
        p.setdefault("mode", "code")
        p.setdefault("imagePrompt", "")
    cur["script"] = script
    cur["skeleton"] = skeleton
    cur["filmType"] = obj.get("filmType") or ""
    cur["shots"] = pages
    cur["approved"] = False                               # 等用户签字
    store.save(name, cur)
    n_img = sum(1 for p in pages if p.get("mode") in ("image", "mixed"))
    job.say(f"骨架 {len(skeleton)} 段 · {len(pages)} 页 · 片型 {cur['filmType'] or '未定'}")
    job.say(f"其中 {n_img} 页要走生图，{len(pages) - n_img} 页代码画")
    return {"skeleton": skeleton, "shots": pages, "minutes": round(mins, 2),
            "filmType": cur["filmType"]}


def fix_syntax(src, sid, job, tries=1):
    """存盘前用 node 解析一遍。有错就让它**只修那一处**，别的一概不许动。

    实测模型会写出 `}})();` 这种多一个括号的代码。等渲染抽帧才发现的话，
    要起 Playwright、等十几秒，报回来还是句 "Unexpected token '}'"，
    得人肉回去数括号。这里 50 毫秒拦下来。
    """
    return scene_check.fix_syntax(AI, src, sid, say=job.say, tries=tries)


def fix_lint(name, sid, src, job, tries=1):
    """存盘前把静态检查的问题当意见，让模型改**一轮**。

    为什么放在这里：静态检查是**秒级、免费**的（不像渲帧 + 评审要十几秒和一次模型调用），
    所以**根本不该把没过静态检查的代码存进去**。过了才存，后面每条链路都省一遍。
    （踩过的具体一条：屏上字画到 y=880，正好压在字幕带里 —— 20 页都这样，
    因为提示词里的参考例子就是这么写的。检查拦住比事后人肉发现便宜得多。）
    """
    import checks
    for _ in range(tries):
        st = checks.scene_lint(name, sid, src=src)
        if not st["problems"]:
            return src, st
        for p in st["problems"]:
            job.say("  静态检查 ✗ " + p)
        job.say("让模型按检查意见改一轮…")
        out = _strip_fence(AI.generate(
            prompts.FIX_LINT.format(problems="\n".join(f"- {p}" for p in st["problems"]),
                                    src=src, shot=sid), timeout=420))
        out, _ = _fix_scene_id(out, sid)
        out = fix_syntax(out, sid, job)                     # 改完还得是合法 JS
        src = out
    st = checks.scene_lint(name, sid, src=src)
    if st["problems"]:
        job.say("  改完还是没过：" + "；".join(st["problems"]))
    return src, st


def do_scene(name, sid, job):
    cur = store.load(name) or {}
    shots = cur.get("shots", [])
    idx = next((i for i, s in enumerate(shots) if s["id"] == sid), None)
    if idx is None:
        raise ValueError("没有这个镜头")
    shot = shots[idx]
    style = cur.get("style") or {}
    palette = style.get("palette") or ["#F3EEE6", "#2A2A2A", "#8A8A8A", "#C8553D", "#E9B872"]
    fmt = lambda s: f'页{s["id"]}「{s.get("role","")}·{s.get("title","")}」' if s else "（无）"
    job.say("在读上下文（前后各两页）…")

    mode = shot.get("mode") or "code"
    images = shot.get("images") or []

    if mode in ("image", "mixed") and images:
        # 贴图 + 运动：图已经生成好了，代码只负责怎么动
        assets = [f"demos/{name}/assets/{f}" for f in images]
        # 先量一下这张图（主体是什么、在哪、多大）—— 量过的页直接复用，不重复花钱
        import measure
        got = measure.of(name, sid, ai=AI, say=job.say)
        framing = None
        if got:
            z0, fx, fy, note = measure.framing(got["box"])
            framing = (z0, fx, fy)
            if note:
                job.say("  " + note)
        job.say(f"贴图 + 运动（{len(assets)} 张图）：{shot.get('title','')}")
        prompt = prompts.SCENE_IMAGE.format(
            shot=sid, dur=shot.get("dur", 15), role=shot.get("role", ""),
            title=shot.get("title", ""), note=shot.get("note", ""),
            camera=shot.get("camera", "缓慢推近"), text=shot.get("text", ""),
            narration=shot.get("narration") or "（这一页没有分到旁白）",
            pos=idx + 1, total=len(shots),
            assets="\n".join(f"  {i+1}. `{a}`" for i, a in enumerate(assets)),
            framing=prompts.framing_text(got, framing),
            extra="\n" + prompts._IMG_MIXED if mode == "mixed" else "",
            api=prompts.ENGINE_API_IMAGE.replace("__SHOT__", sid),
            example=prompts.example_image(shot, assets, palette, pos=idx + 1,
                                          total=len(shots), framing=framing),
        )
        # 让引擎把这些图加载进 IMG（eras.js 的 assets 字段）。**现读现写**：
        # 上面那些字段拼了几百毫秒，期间别的任务可能往项目里写过东西。
        store.patch_shot(name, sid, assets=images, status="draft")
    else:
        if mode in ("image", "mixed") and not images:
            raise ValueError(f"页 {sid} 走的是生图（mode={mode}），但还没有图："
                             f"先生图（说「把缺的图生出来」），或者把这一页改成代码画")
        job.say(f"代码画：{shot.get('title','')}")
        prompt = prompts.SCENE.format(
            shot=sid, dur=shot.get("dur", 15), role=shot.get("role", ""),
            title=shot.get("title", ""), note=shot.get("note", ""),
            camera=shot.get("camera", "停"), text=shot.get("text", ""),
            narration=shot.get("narration") or "（这一页没有分到旁白）",
            look=style.get("look") or "扁平矢量线稿，米白底，墨线勾勒，少量强调色",
            palette="、".join(palette),
            character=style.get("character") or "只出手和背影，不画脸",
            prev="；".join(fmt(shots[i]) for i in range(max(0, idx - 2), idx)) or "（本页是第一页）",
            next="；".join(fmt(shots[i]) for i in range(idx + 1, min(len(shots), idx + 3))) or "（本页是最后一页）",
            api=prompts.ENGINE_API.replace("__SHOT__", sid),
            example=EXAMPLE,
        )
    job.say("模型在写这一页的场景代码…")
    # 代码画的页一页 4000-6000 字，420 秒不够（实测超时后模型还在写，文件反而写进去了）。
    src = _strip_fence(AI.generate(prompt, timeout=int(os.environ.get("VF_SCENE_TIMEOUT") or 900)))
    src, renamed = _fix_scene_id(src, sid)
    if renamed:
        job.say(f"模型把注册名写错了，已改回 SCENES['{sid}']")
    src = fix_syntax(src, sid, job)                       # 有语法错就不许存盘
    src, _st = fix_lint(name, sid, src, job)              # 静态检查没过也不许存盘
    store.write_scene(name, sid, src)
    # 写盘一律现读现改：这一秒之间生图任务可能刚写进某页的图（踩过：覆盖成空）
    fresh = next((x for x in (store.load(name) or {}).get("shots", []) if x["id"] == sid), shot)
    patch = {"status": "draft", "sceneHash": store.shot_fingerprint(fresh)}
    if mode in ("image", "mixed"):
        patch["assets"] = images
    store.patch_shot(name, sid, **patch)
    job.say(f"写好了 {len(src)} 字（{len(src.splitlines())} 行）")
    return {"source": src}


def do_revise(name, sid, rev, job):
    src = store.read_scene(name, sid)
    if not src:
        raise ValueError("这一镜还没有代码")
    issues = "\n".join(f"- {x}" for x in (rev.get("problems") or [])) or "- （导演没提问题）"
    fixes = "\n".join(f"- {x}" for x in (rev.get("fixes") or [])) or "- （导演没给改法）"
    job.say(f"按 {len(rev.get('problems') or [])} 条意见改代码…")
    out = _strip_fence(AI.generate(prompts.REVISE.format(issues=issues, fixes=fixes, source=src),
                                   timeout=420))
    out, renamed = _fix_scene_id(out, sid)
    if renamed:
        job.say(f"改完注册名写错了，已改回 SCENES['{sid}']")
    out = fix_syntax(out, sid, job)
    store.write_scene(name, sid, out)
    job.say(f"改完 {len(out)} 字")
    return {"source": out}


def do_scenes(name, only, job):
    """批量写场景代码：把还没写过（或设定变了）的页依次写完。

    一页挂了接着下一页（失败不连坐），每页写完立刻落盘，中途掐了前面的也不白跑。
    """
    m = store.load(name) or {}
    shots = m.get("shots", [])
    todo = []
    for s in shots:
        if only and s["id"] not in only:
            continue
        if not only:
            has = store.read_scene(name, s["id"]).strip()
            if has and s.get("sceneHash") == store.shot_fingerprint(s):
                continue                                  # 写过、设定也没变
        todo.append(s)
    if not todo:
        raise ValueError("没有要写的页（都写过了，设定也没变）")
    job.say(f"要写 {len(todo)} 页：{' '.join(x['id'] for x in todo)}")
    done, failed = [], []
    for i, s in enumerate(todo, 1):
        job.step(i - 1, len(todo), f"页 {s['id']}")
        try:
            do_scene(name, s["id"], job)
            done.append(s["id"])
        except Exception as e:                              # noqa: BLE001
            job.say(f"  ✗ 页 {s['id']} 没写出来：{e}")
            failed.append({"shot": s["id"], "error": str(e)[:200]})
        job.step(i, len(todo), f"页 {s['id']}")
    job.say(f"═══ 写完：成功 {len(done)} 页，失败 {len(failed)} 页")
    for f in failed:
        job.say(f"  ✗ {f['shot']}：{f['error']}")
    return {"done": done, "failed": failed}


def _run_sync(cmd, job, cwd=None, tag=""):
    """在**当前任务线程里**同步跑一个命令，把输出接到任务日志。

    注意：不能用 QUEUE.submit（队列只有一个工人，在工人里再提交会死等自己）。
    """
    p = subprocess.Popen(cmd, cwd=str(cwd or ENGINE), env=jobs_mod._env(),
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         text=True, encoding="utf-8", errors="replace", bufsize=1)
    tail = []
    for line in p.stdout:
        line = line.rstrip()
        if not line:
            continue
        tail.append(line)
        del tail[:-12]
        if len(job.log) < 400:
            job.say(f"{tag}{line}")
    p.wait()
    if p.returncode != 0:
        raise RuntimeError(f"退出码 {p.returncode}：" + " / ".join(tail[-3:]))
    return tail


def _render_one(name, s, job, fps, d):
    """渲一页 → mp4。给 do_film 的并行工人用（render.py 的端口是系统分配的，互不冲突）。"""
    shot = s["id"]
    out = d / f"{shot}.mp4"
    cmd = [jobs_mod.UV, "run", "--offline", "--with", "playwright", "python",
           str(ENGINE / "render.py"), "--film", f"demos/{name}", "--solo", shot,
           "--from", "0", "--to", f"{shot_dur(s):g}", "--fps", str(fps),
           "--no-counter", "--out", str(out)]
    t0 = time.time()
    _run_sync(cmd, job, tag=f"[{shot}] ")
    return out.stat().st_size // 1024, time.time() - t0


def shot_dur(s):
    return float(s.get("dur") or 12)


def do_film(name, job):
    """整片：逐页渲成 mp4，再拼成一条。

    并行渲（默认 3 路）：一页 13 秒的 30fps 要 130 秒左右，26 页串行 ≈ 55 分钟，
    三路并行 ≈ 20 分钟。render.py 自己起 HTTP 服务、端口用 0 让系统分配，
    所以几个实例同时跑不会撞。
    某一页渲不出来不连坐，记下来接着下一页；**最后必须把失败的说清楚**，
    不许假装成片是完整的。
    """
    import concurrent.futures as cf
    m = store.load(name) or {}
    shots = m.get("shots", [])
    if not shots:
        raise ValueError("这个项目还没有页面")
    fps = int(m.get("fps") or 30)
    store.link_demo(name)
    d = PROJECTS / name / "out"
    d.mkdir(parents=True, exist_ok=True)

    todo = [s for s in shots if store.read_scene(name, s["id"]).strip()]
    skip = [s["id"] for s in shots if s not in todo]
    if skip:
        job.say(f"没有场景代码的页（跳过）：{' '.join(skip)}")
    if not todo:
        raise ValueError("一页场景代码都没有，先写场景")

    def _fresh(s):
        """这一页上次渲的 mp4 还算数吗？代码和素材都比它旧就能复用。

        （跟评审那条一个道理：帧比代码旧说明渲染失败了，这里的判断反过来用。）
        """
        out = d / f"{s['id']}.mp4"
        if not out.exists():
            return False
        marks = [store.scene_path(name, s["id"]).stat().st_mtime]
        for f in (s.get("images") or []):
            p = store.pdir(name) / "assets" / f
            if p.exists():
                marks.append(p.stat().st_mtime)
        return out.stat().st_mtime > max(marks)

    reuse = [s for s in todo if _fresh(s)]
    render = [s for s in todo if s not in reuse]
    if reuse:
        job.say(f"有 {len(reuse)} 页上次渲过、代码素材都没改，直接复用：{' '.join(x['id'] for x in reuse)}")

    workers = max(1, min(int(os.environ.get("VF_FILM_JOBS") or 3), len(render) or 1))
    job.say(f"要渲 {len(render)} 页，{workers} 路并行…")
    ok, bad = [s["id"] for s in reuse], []
    if render:
        with cf.ThreadPoolExecutor(workers) as ex:
            futs = {ex.submit(_render_one, name, s, job, fps, d): s for s in render}
            for i, fu in enumerate(cf.as_completed(futs), 1):
                s = futs[fu]
                try:
                    kb, secs = fu.result()
                    job.say(f"  ✓ 页 {s['id']}　{secs:.0f}s　{kb} KB")
                    ok.append(s["id"])
                except Exception as e:                        # noqa: BLE001
                    job.say(f"  ✗ 页 {s['id']} 渲不出来：{e}")
                    bad.append(s["id"])
                job.step(i, len(render), f"渲完 {i}/{len(render)}")

    if not ok:
        raise ValueError("一页都没渲出来，没法拼")
    order = [s["id"] for s in todo if s["id"] in ok]          # 拼接必须按页序
    job.say(f"渲染：成功 {len(ok)} 页，失败 {len(bad)} 页{'（' + ' '.join(bad) + '）' if bad else ''}")

    # ---- 字幕 ----
    # 页的 dur 本来就是按真实口播切出来的，所以**累加 dur 就是时间轴**。
    # 只算真的渲出来的页，否则没渲的那页会让后面所有字幕往前错位。
    import subtitle
    keep = [s for s in shots if s["id"] in ok]
    w, h = int(m.get("width") or 1920), int(m.get("height") or 1080)
    cs = subtitle.cues(keep)
    ass = d / "subs.ass"                                      # 给 libass 用（**ASCII 名**，
    subtitle.write_ass(cs, ass, w, h)                          # 中文路径在滤镜里容易出岔子）
    subtitle.write_srt(cs, d / "字幕.srt")                     # 给人看/上传平台用
    job.say(f"字幕 {len(cs)} 条（{len(keep)} 页的时间轴）→ subs.ass + 字幕.srt")

    job.say("开始拼接（同时把字幕烧进画面）…")
    lst = d / "_成片.txt"
    lst.write_text("".join(f"file '{(d / f'{s}.mp4').as_posix()}'\n" for s in order),
                   encoding="utf-8")
    out = d / "成片.mp4"
    # 有旁白音轨就混进去（放在 out/ 里叫 旁白.mp3/.m4a/.wav 都认）
    audio = next((d / f"旁白{ext}" for ext in (".m4a", ".mp3", ".wav", ".aac")
                  if (d / f"旁白{ext}").exists()), None)
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
           "-vf", "ass=subs.ass", "-r", str(fps), "-c:v", "libx264", "-crf", "16",
           "-pix_fmt", "yuv420p"]
    if audio:
        cmd += ["-i", str(audio), "-c:a", "aac", "-b:a", "192k", "-shortest"]
        job.say(f"混入旁白音轨：{audio.name}")
    else:
        cmd += ["-an"]
    cmd += [str(out)]
    _run_sync(cmd, job, cwd=d, tag="[ffmpeg] ")
    secs = sum(shot_dur(s) for s in keep)
    job.say(f"成片好了：projects/{name}/out/成片.mp4"
            f"（{len(keep)} 页，约 {secs:.0f} 秒 = {secs / 60:.1f} 分钟，"
            f"{out.stat().st_size // 1048576} MB，字幕已烧进画面）")
    if bad:
        job.say(f"⚠ 缺 {len(bad)} 页（{' '.join(bad)}），这一版成片是不完整的")
    return {"out": f"projects/{name}/out/成片.mp4", "done": order, "failed": bad,
            "seconds": round(secs, 1), "cues": len(cs),
            "seeds": f"projects/{name}/out/成片.mp4", "audio": audio.name if audio else ""}


def do_lint_fix(name, shots, job):
    """只按静态检查改（**不重写整页**）。

    挪一个字的 y 这种小修，不该重跑一遍整页生成（那要调模型 + 量图）。实测：
    整页重写 1.5-6 分钟，只改检查项 30-40 秒 —— 而且只动该动的地方，风险小。
    """
    import checks
    m = store.load(name) or {}
    want = set(shots or [])
    todo = [s for s in m.get("shots", []) if not want or s["id"] in want]
    if not todo:
        raise ValueError("没有要改的页")
    job.say(f"按静态检查改 {len(todo)} 页：{' '.join(s['id'] for s in todo)}")
    fixed, ok, no_code = [], [], []
    for i, s in enumerate(todo):
        sid = s["id"]
        job.step(i, len(todo), f"页 {sid}")
        src = store.read_scene(name, sid)
        if not src.strip():
            job.say(f"  页 {sid}：还没有代码，跳过（要整页写）")
            no_code.append(sid)
            continue
        st = checks.scene_lint(name, sid, src=src)
        if not st["problems"]:
            job.say(f"  页 {sid}：静态检查通过")
            ok.append(sid)
            continue
        out, st2 = fix_lint(name, sid, src, job)
        if st2["problems"]:
            job.say(f"  页 {sid}：改完还是没过：" + "；".join(st2["problems"]))
            continue
        store.write_scene(name, sid, out)
        fixed.append(sid)
        job.say(f"  ✓ 页 {sid} 改好了（{len(src)} → {len(out)} 字）")
        job.step(i + 1, len(todo), f"页 {sid}")
    job.say(f"═══ 改完：{len(fixed)} 页动手，{len(ok)} 页本来就过，{len(no_code)} 页没代码")
    return {"fixed": fixed, "pure": ok, "no_code": no_code}


def do_review(name, sid, job):
    shots = (store.load(name) or {}).get("shots", [])
    shot = next((s for s in shots if s["id"] == sid), None)
    if not shot:
        raise ValueError("没有这个镜头")
    d = PROJECTS / name / "out" / f"{sid}_still"
    frames = sorted(d.glob("t*.png")) if d.exists() else []
    if not frames:
        raise ValueError("还没抽帧，先点「抽帧」")
    # 帧比代码旧 = 渲失败了，旧帧还留着。拿旧帧评审会给出假分数（踩过：分数从 4 掉到 3，
    # 其实评的是上一版画面）。这里直接拒掉。
    scene = store.scene_path(name, sid)
    if scene.exists():
        newest = max(f.stat().st_mtime for f in frames)
        if newest < scene.stat().st_mtime:
            raise ValueError("帧比代码旧（上一次渲染失败了），先重新抽帧再评审")
    style = (store.load(name) or {}).get("style") or {}
    job.say(f"让模型看 {len(frames)} 帧…")
    prompt = prompts.REVIEW.format(
        title=shot.get("title", ""), note=shot.get("note", ""), camera=shot.get("camera", "停"),
        look=style.get("look") or "扁平矢量线稿",
        palette="、".join(style.get("palette") or []),
    )
    text = AI.generate(prompt, files=[str(f) for f in frames[-6:]])
    rev = T.parse_review(text)
    job.say(f"得分 {rev.get('score')}/10 · ok={rev.get('ok')} · {len(rev.get('problems') or [])} 条问题")
    return {"review": rev}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8777)
    ap.add_argument("--host", default="127.0.0.1")
    a = ap.parse_args()
    PROJECTS.mkdir(parents=True, exist_ok=True)

    class Srv(ThreadingHTTPServer):
        daemon_threads = True
        def handle_error(self, request, client_address):      # 浏览器关页面时的连接重置不用刷屏
            e = sys.exc_info()[1]
            if isinstance(e, (ConnectionResetError, BrokenPipeError, ConnectionAbortedError)):
                return
            super().handle_error(request, client_address)

    srv = Srv((a.host, a.port), H)
    print(f"video-factory  http://{a.host}:{a.port}", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        AI.stop()


if __name__ == "__main__":
    main()
