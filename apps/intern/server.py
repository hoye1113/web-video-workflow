"""实习生工作台（intern studio）：**只填表、只点头、只下载**。

用户能看到的东西（全部）：
    ① 一张表：讲什么 / 多久 / 谁的声音 / 用哪个角色  →  [开始]
    ② 进度：写台词 → 画图 → 出片（只有这三种词，没有 stage/queue/render 这些词）
    ③ 三次点头：分镜行不行 / 图行不行 / 成片行不行
    ④ 下载：有字幕版 / 无字幕版 / 字幕文件

后面干活的是已经跑通的那套（**实习生看不到**）：
    OpenCode 的 material agent（读手册、写台词、写页表）
      → bsk 操作浏览器在 Flow 里挂角色 chip 生图（tools/gen_worker.py）
      → frametell 引擎写代码出片（script.mjs / render.mjs）
      → tools/conductor.py 自动推进（闸门没过就停）

跑法：
    python apps/intern/server.py --port 8900 [--host 0.0.0.0]
"""
import argparse
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
sys.path.insert(0, str(ROOT / "tools"))
import agent_bridge                                          # noqa: E402
import conductor                                             # noqa: E402
import pipeline                                              # noqa: E402

UI = pathlib.Path(__file__).resolve().parent / "ui.html"

# 实习生能选的配音（全都免费、免密钥）
VOICES = {
    "female-calm": ("zh-CN-XiaoxiaoNeural", "女声 · 温和（默认）"),
    "male-calm": ("zh-CN-YunjianNeural", "男声 · 沉稳"),
    "male-news": ("zh-CN-YunyangNeural", "男声 · 播报"),
    "female-lively": ("zh-CN-XiaoyiNeural", "女声 · 活泼"),
}
CASTS = {"小树": "小男孩（灰发·头顶嫩芽）", "小芽": "小女孩（栗发·头顶嫩芽）"}

# 三个"点头"的闸门（给实习生看的话）
GATES = {
    "map": {"title": "分镜看过了吗？", "ok": "就这样，开始画图", "no": "要改一下"},
    "img": {"title": "图都看过了吗？", "ok": "都可以，去出片", "no": "有几张要重画"},
    "film": {"title": "这版成片可以吗？", "ok": "可以，就这样", "no": "还要改"},
}

# 后台推进（一次只跑一件事）
LOCK = threading.Lock()
RUNNING = {"what": None, "film": None}


SNAP = ROOT / "projects" / "_snapshots"
_snap_at = {}


def guard_files(f):
    """防止 agent 把关键文件删空：有内容就快照；不见了就从快照恢复（每 10 秒最多写一次）。"""
    d = film_dir(f)
    snap = SNAP / f
    now = time.time()
    do_write = now - _snap_at.get(f, 0) > 10
    for name in ("brief.json", "script-source.json", "page-spec.json"):
        src, dst = d / name, snap / name
        try:
            if src.exists() and src.stat().st_size > 4:
                if do_write:
                    txt = src.read_text(encoding="utf-8")
                    if name != "script-source.json" or '"pages"' in txt:
                        snap.mkdir(parents=True, exist_ok=True)
                        dst.write_text(txt, encoding="utf-8")
            elif not src.exists() and dst.exists() and dst.stat().st_size > 4:
                src.write_text(dst.read_text(encoding="utf-8"), encoding="utf-8")
                pipeline.emit(f, "log", text=f"⚠ {name} 不见了，已从快照恢复")
        except Exception:                                     # noqa: BLE001
            pass
    if do_write:
        _snap_at[f] = now


def film_dir(f):
    return pipeline.proj_dir(f)


def brief(f):
    return pipeline.read_json(film_dir(f) / "brief.json", {}) or {}


def mini_steps(f):
    """把内部阶段翻译成实习生的三个词 + 一行答复。"""
    d = film_dir(f)
    q = pipeline.queue(f)
    gates = pipeline.gate_state(f)
    films = sorted((d / "out").glob("*.mp4")) if (d / "out").exists() else []
    src = pipeline.read_json(d / "script-source.json", {}) or {}
    pages = src.get("pages", [])
    imgs = [t for t in q["tasks"] if t.get("img")]
    review = [t for t in q["tasks"] if t.get("status") == "review"]
    running = RUNNING["film"] == f and RUNNING["what"]

    # ① 写台词：有**像样的**台词才算好（脚手架只有 1 页 2 句，不能算）
    total_cues = sum(len(p.get("cues", [])) for p in pages)
    has_script = len(pages) >= 3 and total_cues >= 6
    s1 = "done" if has_script else ("doing" if running and "台词" in str(RUNNING["what"]) else "todo")
    # ② 画图：页表里已经指定了图 = 画完了（老片子没有队列记录，也不能显示成没画）
    spec = pipeline.read_json(d / "page-spec.json", []) or []
    need = len(spec) or len(pages)
    has_assets = any((p or {}).get("asset") for p in spec)
    got = len([t for t in q["tasks"] if t.get("img")])
    if has_assets:
        s2 = "done"
    elif pages and gates.get("map") != "ok":
        s2 = "locked"
    elif pages:
        # 分镜已经点头了：从这一刻起就是"正在画"，哪怕第一张还没出来
        s2 = "doing" if (got or not films) else "done"
    else:
        s2 = "doing" if got or (running and "图" in str(RUNNING["what"])) else "todo"
    # ③ 出片：有 mp4 就是出过了（不因为闸门状态而假装没出）
    s3 = "done" if films else (
        "doing" if (running and any(k in str(RUNNING["what"]) for k in ("配音", "字幕", "渲染"))) else "todo")
    if gates.get("img") != "ok" and not films:
        s3 = "locked"

    doing = [t for t in q["tasks"] if t.get("status") in ("browser", "prompt", "generating", "fetching")]
    img_hint = f"已经画好 {got}/{need} 张" if need else "等分镜确认"
    if doing:
        img_hint = f"已经画好 {got}/{need} 张 · 正在画第 {doing[0].get('page', '')} 页"
    elif got and got < need and gates.get("map") == "ok":
        img_hint = f"已经画好 {got}/{need} 张 · 还有 {need - got} 张在排队"

    return {
        "steps": [
            {"key": "script", "label": "写台词", "state": s1,
             "hint": ("台词写好了，等你看看分镜" if pages else "正在按你的题目写台词…")},
            {"key": "images", "label": "画图", "state": s2, "hint": img_hint},
            {"key": "film", "label": "出片", "state": s3,
             "hint": ("成片好了，播一下看看" if films else "等图确认")},
        ],
        "pages": len(pages), "need": need, "got": got,
        "review_images": len(review),
        "gates": gates,
        "film": (films[-1].name if films else ""),
        "running": RUNNING["what"] if running else "",
    }


def ask_agent(f, text):
    """交给 material agent（它自己会读手册、跑 bsk/Flow/脚本）。"""
    try:
        agent_bridge.ask(f, text)
        return True, ""
    except Exception as e:                                    # noqa: BLE001
        pipeline.emit(f, "log", text=f"✗ 交给导演失败：{e}")
        return False, str(e)


def prompt_script(f, topic, minutes):
    chars = int(minutes * 330)
    return (
        f"这是一位只填表的同事交来的片子：主题「{topic}」，目标 {minutes:g} 分钟（≈{chars} 字台词）。\n"
        f"按 docs/新题材开工手册.md 干活，**只做第一阶段，不要生成任何图、不要跑渲染**：\n"
        f"1) 写 projects/{f}/script-source.json（页面骨架：钩子→案例/论点→结论→行动；每条 cue ≤12 字，"
        f"第 12 字前必须有标点；总字数 ≈{chars}）\n"
        f"2) 写 projects/{f}/docs/页-处境映射.md：一页一行（页号 | 一句话论点 | 处境一句话 | 用哪个角色）\n"
        f"3) 更新 projects/{f}/page-spec.json：每页 id/title/asset 先留空（asset 等图出来再填）、"
        f"theme/cam 按 warm-emotion 的规矩给；**lights 一律写 []**（光已经画在 Flow 的图里，"
        f"再叠 P.light 会在同一个位置加一团假光斑）\n"
        f"做完停下来，等我在页面上点「就这样，开始画图」。"
    )


def prompt_images(f):
    return (
        f"分镜已确认。现在给 projects/{f} 出图（第二阶段），只做图、并把图接进页表；不要出片：\n"
        f"1) 按 docs/页-处境映射.md，把每页要生成的处境写进 gen-queue.json（用 tools/pipeline.py 的 queue_add，"
        f"或直接写文件）：page / cast（小树/小芽）/ scene（谁+在哪+在做什么+光从哪来）/ out 文件名（以页号开头）\n"
        f"2) 跑 python tools/gen_worker.py {f}（bsk 开浏览器在 Flow 里挂角色 chip 生图，串行，一张约 60–100 秒）\n"
        f"3) 每张出来之后按 character-cards 的一致性判据看图；不合格的标 retry 重排\n"
        f"4) 全部出完：把 page-spec.json 每页的 asset 填成**该页对应的那张图**（图在 projects/scene-library/），"
        f"然后跑 python tools/make_pages.py --project {f}\n"
        f"出完停下来，等我在页面上点「都可以，去出片」。"
    )


def prompt_fix_images(f, note):
    return (
        f"图被打回了，按这个意见改：{note}\n"
        f"只改动相关的那几页（projects/{f}/gen-queue.json 里把要重画的标成 retry，必要时改 scene），"
        f"然后跑 python tools/gen_worker.py {f}；其余不动。"
    )


def prompt_fix_script(f, note):
    return (
        f"分镜被打回了，按这个意见改：{note}\n"
        f"只改 projects/{f}/script-source.json 与 docs/页-处境映射.md（必要时 page-spec.json），"
        f"改完停下等我再确认。"
    )


class Server(ThreadingHTTPServer):
    """**不允许两个实例抢同一个端口**（Windows 下 SO_REUSEADDR 会静默允许重复绑定，
    结果请求一半打到僵住的旧实例上 —— 页面"没反应"就是这么来的）。"""
    allow_reuse_address = False
    daemon_threads = True


class H(BaseHTTPRequestHandler):
    server_version = "intern-studio"

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
            return self._get()
        except Exception as e:                                # noqa: BLE001
            import traceback
            traceback.print_exc()
            return self._send(500, {"error": f"{type(e).__name__}: {e}"})

    def _get(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        one = lambda k, d="": (q.get(k) or [d])[0]           # noqa: E731
        if u.path in ("/", "/f"):
            return self._send(200, UI.read_text(encoding="utf-8"), "text/html; charset=utf-8")
        if u.path == "/api/state":
            f = one("film")
            if not f:
                return self._send(200, {"films": [status_row(x) for x in pipeline.projects()],
                                        "voices": VOICES, "casts": CASTS, "gates": GATES})
            d = film_dir(f)
            guard_files(f)
            src = pipeline.read_json(d / "script-source.json", {}) or {}
            tasks = pipeline.queue(f)["tasks"]
            flags = {
                "need_script": not (src.get("pages") or []),
                "need_resume_images": (not RUNNING["what"]) and any(
                    t.get("status") in ("queued", "retry", "failed") for t in tasks),
            }
            return self._send(200, {
                "film": f, "brief": brief(f), "progress": mini_steps(f),
                "flags": flags,
                "gates": GATES, "gate_state": pipeline.gate_state(f),
                "approvals": pipeline.approvals(f),
                "images": [{"page": t["page"], "file": t.get("img") or "",
                            "status": t.get("status"), "scene": t.get("scene", ""),
                            "metrics": t.get("metrics") or {}}
                           for t in pipeline.queue(f)["tasks"]],
                "map": map_rows(f),
                "files": [{"rel": x.name, "kb": max(1, int(x.stat().st_size / 1024))}
                          for x in (d / "out").glob("*")
                          if x.is_file() and x.suffix.lower() in (".mp4", ".srt")] if (d / "out").exists() else [],
                "running": RUNNING if RUNNING["film"] == f else None,
            })
        if u.path == "/api/events":
            return self._events(one("film"), float(one("since", "0") or 0))
        if u.path == "/api/file":
            f, rel = one("film"), one("rel")
            base = film_dir(f).resolve()
            p = (base / rel).resolve()
            if not str(p).startswith(str(base)) or not p.is_file():
                return self._send(400, {"error": "bad path"})
            ct = {"mp4": "video/mp4", "srt": "text/plain; charset=utf-8",
                  "png": "image/png", "jpg": "image/jpeg"}.get(p.suffix.lstrip("."), "application/octet-stream")
            return self._send(200, p.read_bytes(), ct)
        if u.path == "/api/img":
            rel = one("rel")
            base = (ROOT / "projects" / "scene-library").resolve()
            p = (base / rel).resolve()
            if not str(p).startswith(str(base)) or not p.is_file():
                return self._send(400, {"error": "bad path"})
            return self._send(200, p.read_bytes(), "image/png")
        return self._send(404, {"error": "no route"})

    # ---------- POST ----------
    def do_POST(self):
        try:
            return self._post()
        except Exception as e:                                # noqa: BLE001
            import traceback
            traceback.print_exc()
            return self._send(500, {"error": f"{type(e).__name__}: {e}"})

    def _post(self):
        u = urlparse(self.path)
        n = int(self.headers.get("Content-Length") or 0)
        b = json.loads(self.rfile.read(n) or b"{}")
        if u.path == "/api/start":
            return self._start(b)
        if u.path == "/api/gate":
            return self._gate(b)
        if u.path == "/api/start-images":
            # 已经点头过、但当时没跑起来（或要补画）的片子：排队列 + 开画
            n = build_queue(b.get("film", ""))
            kick_images(b.get("film", ""))
            return self._send(200, {"ok": True, "added": n})
        if u.path == "/api/retry-script":
            # 台词阶段卡住（agent 中途停了）→ 带着题目再叫一次
            f = b.get("film", "")
            br = brief(f)
            ok, err = ask_agent(f, prompt_script(f, br.get("topic", "") or f,
                                                 float(br.get("minutes") or 6)))
            pipeline.emit(f, "say", text="（已重新叫导演写台词）")
            return self._send(200, {"ok": ok, "error": err})
        return self._send(404, {"error": "no route"})

    def _start(self, b):
        topic = (b.get("topic") or "").strip()
        if not topic:
            return self._send(400, {"error": "请先写一句「这条视频讲什么」"})
        minutes = float(b.get("minutes") or 6)
        name = (b.get("name") or "").strip() or time.strftime("film-%m%d-%H%M")
        name = pipeline.slug(name)
        voice_key = b.get("voice") or "female-calm"
        speaker, voice_label = VOICES.get(voice_key, VOICES["female-calm"])
        cast = [c for c in (b.get("cast") or list(CASTS)) if c in CASTS] or list(CASTS)
        r = pipeline.run([pipeline.PY, "tools/new_film.py", name,
                          "--title", (b.get("title") or topic)[:24], "--minutes", str(minutes), "--force"],
                         timeout=300)
        if r.returncode != 0:
            return self._send(500, {"error": "建工程失败", "log": (r.stdout or "") + (r.stderr or "")})
        d = film_dir(name)
        (d / "brief.json").write_text(json.dumps({
            "topic": topic, "minutes": minutes, "speaker": speaker, "voice_label": voice_label,
            "cast": cast, "materials": b.get("materials") or "",
        }, ensure_ascii=False, indent=1), encoding="utf-8")
        # 配音写进 script-source 的 voice（agent 之后改 script-source 时会保留）
        src = pipeline.read_json(d / "script-source.json", {}) or {}
        src["voice"] = {"speaker": speaker, "provider": "edge"}
        src["note"] = (src.get("note") or "")
        (d / "script-source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1), encoding="utf-8")
        pipeline.emit(name, "say", text=f"新片：{topic}（{minutes:g} 分钟 · {voice_label}）")
        ok, err = ask_agent(name, prompt_script(name, topic, minutes))
        return self._send(200, {"ok": ok, "film": name, "error": err})

    def _gate(self, b):
        f, gate, verdict = b.get("film"), b.get("gate"), b.get("verdict", "ok")
        note = (b.get("note") or "").strip()
        if not f or gate not in GATES:
            return self._send(400, {"error": "缺 film 或 gate"})
        pipeline.mark(f, f"gate:{gate}", verdict, note)
        pipeline.emit(f, "approval", key=f"gate:{gate}", verdict=verdict, note=note)
        if verdict == "ok":
            if gate == "map":
                # 先验一下：台词/分镜是不是真的写好了（别拿脚手架去建队列）
                sync_page_spec(f)                      # 页表先跟台词页数对齐（确定性兜底）
                src = pipeline.read_json(film_dir(f) / "script-source.json", {}) or {}
                pages = src.get("pages", [])
                rows = map_rows(f)
                if len(pages) < 3 or len(rows) < 3:
                    pipeline.emit(f, "log",
                                  text="台词/分镜还没写好（页面会自动刷新），稍等一下再点")
                    return self._send(200, {"ok": False, "error": "script/mapping not ready"})
                if len(rows) < len(pages) * 0.6:
                    pipeline.emit(f, "log",
                                  text=f"分镜只有 {len(rows)} 行、台词 {len(pages)} 页 —— 等分镜写完再点")
                    return self._send(200, {"ok": False, "error": "mapping incomplete"})
                # 分镜点头 → **脚本**把映射表变成队列并开画（不让 agent 做机械活）
                n = build_queue(f)
                pipeline.emit(f, "stage", stage="出图", status="start",
                              detail=f"按分镜排了 {n} 张图，开始逐张画")
                kick_images(f)
            elif gate == "img":
                kick(f)                      # 机械活：素材/排页/配音/字幕/渲染 交给推进器
            elif gate == "film":
                pipeline.emit(f, "say", text="用户确认成片")
        else:
            if gate == "map":
                ask_agent(f, prompt_fix_script(f, note or "（没写具体意见，按你的判断）"))
            elif gate == "img":
                ask_agent(f, prompt_fix_images(f, note or "（没写具体意见，挑不一致的重画）"))
            else:
                pipeline.emit(f, "say", text=f"成片要改：{note}")
        return self._send(200, {"ok": True})

    # ---------- 事件流 ----------
    def _events(self, f, since):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        cur, beat = since, 0
        while beat < 240:
            for r in pipeline.events(f, since=cur):
                cur = max(cur, r.get("ts", cur))
                try:
                    self.wfile.write(("data: " + json.dumps(r, ensure_ascii=False) + "\n\n").encode("utf-8"))
                    self.wfile.flush()
                except Exception:                             # noqa: BLE001
                    return
            time.sleep(1.0)
            beat += 1


def build_queue(f):
    """把「页 → 处境映射表」变成生图队列（**机械活，脚本干；不让 agent 做**）。

    表里的四列就是队列要的四样：页号 / 讲什么 / 处境 / 主角。
    已经有任务（重跑/重画过的）不覆盖。
    """
    rows = map_rows(f)
    q = pipeline.queue(f)
    have = {t.get("page") for t in q["tasks"] if t.get("status") in ("queued", "retry", "browser",
                                                                     "prompt", "generating", "fetching",
                                                                     "review", "saved", "failed")}
    added = 0
    for row in rows:
        pid = (row[0] or "").strip()
        if not pid:
            continue
        page = pid if pid.startswith("p") else f"p{int(pid):02d}"
        if page in have:
            continue
        what, scene, cast = (row[1] if len(row) > 1 else ""), (row[2] if len(row) > 2 else ""), ""
        # 表格里常有「（**复用** xxx）」「（**新生成**）」这类备注 —— 不能进提示词
        scene = re.sub(r"（[^（）]*\*\*[^（）]*）", "", scene or "")
        scene = scene.replace("**", "").strip()
        cast_raw = (row[3] if len(row) > 3 else "") or ""
        if "小芽" in cast_raw:
            cast = "小芽"
        elif "小树" in cast_raw:
            cast = "小树"
        else:
            cast = "小树" if added % 2 == 0 else "小芽"
        scene = (scene or what or "").strip()
        if not scene:
            continue
        out = f"{page}-{pipeline.slug(what or 'scene')[:14]}.png"
        pipeline.queue_add(f, page, cast, scene, out)
        added += 1
    return added


def sync_page_spec(f):
    """页表和台词页数不一致时，按台词页补齐/裁剪（确定性兜底，不依赖 agent）。"""
    d = film_dir(f)
    src = pipeline.read_json(d / "script-source.json", {}) or {}
    pages = src.get("pages", [])
    if not pages:
        return []
    spec = pipeline.read_json(d / "page-spec.json", []) or []
    by_id = {p.get("id"): p for p in spec}
    out = []
    for p in pages:
        pid = p.get("id")
        out.append(by_id.get(pid) or {"id": pid, "title": p.get("title", ""), "asset": "",
                                      "theme": "day", "cam": "push40", "reveal": [0.35, 1, 0.25, 1.4],
                                      "lights": [], "texts": []})
    if len(out) != len(spec):
        (d / "page-spec.json").write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                          encoding="utf-8")
        pipeline.emit(f, "stage", stage="排页", status="done",
                      detail=f"页表跟台词对齐到 {len(out)} 页")
    return out


def ensure_page_spec(f):
    """页表缺失时按台词页补一份最小页表（防 agent 中途停住导致后面没页可用）。"""
    d = film_dir(f)
    spec_f = d / "page-spec.json"
    spec = pipeline.read_json(spec_f, []) or []
    if spec:
        return spec
    src = pipeline.read_json(d / "script-source.json", {}) or {}
    pages = src.get("pages", [])
    if not pages:
        return []
    spec = [{"id": p.get("id", f"p{i:02d}"), "title": p.get("title", ""), "asset": "",
             "theme": "day", "cam": "push40", "reveal": [0.35, 1, 0.25, 1.4],
             "lights": [], "texts": []} for i, p in enumerate(pages, 1)]
    spec_f.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    pipeline.emit(f, "stage", stage="排页", status="done", detail=f"补了 {len(spec)} 页页表")
    return spec


def assign_images(f):
    """生图完成后，把队列里的图填进页表（asset），再重生成页代码 —— 机械活。"""
    d = film_dir(f)
    spec_f = d / "page-spec.json"
    spec = ensure_page_spec(f)
    by_page = {t.get("page"): t.get("img") for t in pipeline.queue(f)["tasks"] if t.get("img")}
    filled = 0
    for p in spec:
        img = by_page.get(p.get("id"))
        if img:
            p["asset"] = img
            filled += 1
    if filled:
        spec_f.write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
        pipeline.run([pipeline.PY, "tools/make_pages.py", "--project", f], timeout=300)
        pipeline.emit(f, "stage", stage="排页", status="done", detail=f"把 {filled} 张图填进页表")
    return filled


def kick_images(f):
    """后台跑生图执行器（**完全脱离**面板进程：面板重启不会把它带走）。"""
    def run():
        with LOCK:
            RUNNING.update(what="画图（Flow 生图）", film=f)
        try:
            pipeline.emit(f, "stage", stage="出图", status="start", detail="开始逐张出图")
            logf = ROOT / "logs" / f"gen-{f}.log"
            logf.parent.mkdir(parents=True, exist_ok=True)
            flags = 0
            if os.name == "nt":
                flags = 0x00000008 | 0x00000200        # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
            with open(logf, "ab") as fh:
                p = subprocess.Popen([pipeline.PY, "tools/gen_worker.py", f], cwd=str(ROOT),
                                     stdout=fh, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                                     env=pipeline.env(), creationflags=flags, close_fds=True)
            p.wait()
            assign_images(f)
        finally:
            pipeline.emit(f, "stage", stage="出图", status="done", detail="这一轮生图结束")
            RUNNING.update(what=None, film=None)
    threading.Thread(target=run, daemon=True).start()


def kick(f):
    """把出片链（素材→排页→配音→字幕→渲染→验收）交给**脱离面板的进程**跑。

    以前是面板里的线程 —— 面板一重启（比如改代码/换端口）整条链就断了（实测踩过）。
    """
    def run():
        with LOCK:
            RUNNING.update(what="出片（配音/字幕/渲染）", film=f)
        try:
            logf = ROOT / "logs" / f"conductor-{f}.log"
            logf.parent.mkdir(parents=True, exist_ok=True)
            flags = 0
            if os.name == "nt":
                flags = 0x00000008 | 0x00000200
            with open(logf, "ab") as fh:
                p = subprocess.Popen([pipeline.PY, "tools/conductor.py", f, "--drain"],
                                     cwd=str(ROOT), stdout=fh, stderr=subprocess.STDOUT,
                                     stdin=subprocess.DEVNULL, env=pipeline.env(),
                                     creationflags=flags, close_fds=True)
            p.wait()
        finally:
            pipeline.emit(f, "stage", stage="出片", status="done", detail="出片链结束")
            RUNNING.update(what=None, film=None)
    threading.Thread(target=run, daemon=True).start()


def map_rows(f):
    """给实习生看的分镜表：优先读 agent 写的 docs/页-处境映射.md；没有就从台词页标题生成。

    返回 4 列：[页号, 讲什么, 画面（处境）, 主角]。
    """
    d = film_dir(f)
    md = d / "docs" / "页-处境映射.md"
    rows = []
    if md.exists():
        lines = [l.strip() for l in md.read_text(encoding="utf-8").splitlines() if l.strip().startswith("|")]
        table = [[c.strip() for c in l.strip("|").split("|")] for l in lines]
        table = [r for r in table if not set("".join(r)) <= set("-: ")]
        if table:
            head = table[0]

            def col(*keys):
                for i, h in enumerate(head):
                    if any(k in h for k in keys):
                        return i
                return None
            ip = col("页", "页号", "#") or 0
            iw = col("讲", "论点", "标题", "骨架")
            isc = col("处境", "画面")
            ic = col("角色", "主角")
            for r in table[1:]:
                get = lambda i: (r[i] if i is not None and i < len(r) else "")   # noqa: E731
                pid = get(ip)
                if not re.match(r"^p?\d{1,2}$", pid.strip()):        # 只认"页号"开头的行（文档里可能还有别的表）
                    continue
                if any(x[0] == pid for x in rows):                   # 同一页出现两次就取第一次
                    continue
                rows.append([pid, get(iw if iw is not None else 1),
                             get(isc if isc is not None else 2), get(ic)])
    if not rows:                       # 兜底：台词页的标题就够实习生点头了
        src = pipeline.read_json(d / "script-source.json", {}) or {}
        for p in src.get("pages", []):
            rows.append([p.get("id", ""), p.get("title", ""), "", ""])
    return rows


def status_row(f):
    st = mini_steps(f)
    return {"film": f, "title": brief(f).get("title") or f,
            "steps": st["steps"], "film_file": st["film"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8900)
    ap.add_argument("--host", default="127.0.0.1")
    a = ap.parse_args()
    # 单实例守卫：端口已被占用就直接说清楚（别让两个实例同时听）
    import socket
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        probe.bind((a.host, a.port))
    except OSError:
        print(f"✗ 端口 {a.port} 已经被占用 —— 已经有一个工作台在跑了（先停掉再起：apps\\intern\\stop.ps1）")
        return 2
    finally:
        probe.close()
    print(f"实习工作台：http://{a.host}:{a.port}")
    print("  （只填表 → 三次点头 → 下载；工程细节在下面：OpenCode material agent + bsk/Flow + frametell 引擎）")
    srv = Server((a.host, a.port), H)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        srv.shutdown()


if __name__ == "__main__":
    sys.exit(main())
