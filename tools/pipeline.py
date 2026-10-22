"""流水线共享层：队列 / 事件 / 审批 / 阶段表 / 环境自检。

面板（`tools/panel/server.py`）和生图执行器（`tools/gen_worker.py`）都只认这一份约定 ——
**面板 = 遥控器，执行器 = 干活的人，约定 = 文件**。

落盘位置（都在片子里，跟片子走）：
    projects/<片>/events.jsonl    事件流（append-only；面板读它渲染"过程"，带游标可续读）
    projects/<片>/gen-queue.json  生图队列（人/面板/agent 写，执行器读）
    projects/<片>/docs/审批.json  审批（人写；key 可以是 docs/xxx、out/xxx、library/xxx）
"""
import json
import os
import pathlib
import re
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENGINE = ROOT / "experiments" / "frametell-src" / "frametell-main" / "packages" / "engine"
LOCALBIN = pathlib.Path.home() / ".local" / "bin"
PY = sys.executable or "python"
EDGE_PY = pathlib.Path.home() / ".frametell" / "edge-venv" / "Scripts" / "python.exe"

# 阶段表：名字 / 命令 / 在哪跑（ROOT 或 PROJ）/ 说明
# 三态文案（照 frametell 的 run.ts）：doing=正在做 · done=做好了 · start=开始
STEPS = [
    ("剧本", [PY, "tools/make_script_js.py", "{proj}", "--from-source"], ROOT,
     {"start": "开始整理剧本", "doing": "在把台词编成剧本", "done": "剧本好了"}),
    ("台词", [PY, "tools/check_cues.py"], ROOT,
     {"start": "开始审台词", "doing": "在审 12 字硬切", "done": "台词审过了"}),
    ("配音", [PY, "tools/make_voice.py", "{proj}"], ROOT,
     {"start": "开始配音", "doing": "正在配音", "done": "配音好了"}),
    ("排页", [PY, "tools/make_pages.py", "--project", "{proj}"], ROOT,
     {"start": "开始排页", "doing": "正在排页", "done": "页面排好了"}),
    ("出图", [PY, "tools/gen_worker.py", "{proj}"], ROOT,
     {"start": "开始出图", "doing": "正在逐张出图", "done": "图都出好了"}),
    ("素材", [PY, "tools/lib_index.py"], ROOT,
     {"start": "开始整理素材库", "doing": "在整理素材库索引", "done": "素材库索引好了"}),
    ("字幕", ["node", str(ENGINE / "tools" / "script.mjs")], "PROJ",
     {"start": "开始写字幕", "doing": "在写口播脚本与字幕", "done": "字幕好了"}),
    ("渲染", ["node", str(ENGINE / "tools" / "render.mjs"), "--workers", "6"], "PROJ",
     {"start": "开始渲染", "doing": "正在渲染成片", "done": "成片好了"}),
    ("验收", [PY, "tools/accept_emotion.py", "{proj}"], ROOT,
     {"start": "开始验收", "doing": "在逐页体检", "done": "体检完了"}),
    ("抽帧", [PY, "tools/qc_snap.py", "{proj}"], ROOT,
     {"start": "开始抽帧", "doing": "在抽帧拼表", "done": "对照表好了"}),
]
STEP = {s[0]: s for s in STEPS}

# 三个审批点（照 frametell 的"分镜审批"；我们天然有三个）
GATES = {
    "map": {"label": "页 → 处境映射表", "ask": "确认这张表，就开始出图",
            "hint": "要改哪里，直接在下面说", "file": "docs/页-处境映射.md"},
    "img": {"label": "逐张的图", "ask": "图都看过了，就继续排页",
            "hint": "不满意的写一句话改法，就打回重画", "file": "scene-library/index.json"},
    "film": {"label": "成片", "ask": "这版可以发，就导出",
             "hint": "想改哪一页，直接说", "file": "out"},
}


def env(*extra):
    e = os.environ.copy()
    e["PATH"] = str(LOCALBIN) + os.pathsep + e.get("PATH", "")
    e["PYTHONUTF8"] = "1"
    e["PYTHONIOENCODING"] = "utf-8"
    return e


def run(cmd, cwd=ROOT, timeout=600):
    return subprocess.run([str(c) for c in cmd], cwd=str(cwd), capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=env(), timeout=timeout)


def proj_dir(proj):
    return ROOT / "projects" / proj


def projects():
    """有台词的工程（第一部 emotion-full 也在列）。"""
    d = ROOT / "projects"
    return sorted([p.name for p in d.iterdir()
                   if p.is_dir() and (p / "script-source.json").exists()])


# ---------- 事件流 ----------

def emit(proj, kind, **kw):
    """往 events.jsonl 追加一条（append-only，面板按游标读）。"""
    f = proj_dir(proj) / "events.jsonl"
    f.parent.mkdir(parents=True, exist_ok=True)
    rec = {"at": time.strftime("%Y-%m-%d %H:%M:%S"), "ts": time.time(), "kind": kind, **kw}
    with f.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def events(proj, since=0.0, limit=400):
    f = proj_dir(proj) / "events.jsonl"
    if not f.exists():
        return []
    out = []
    for line in f.read_text(encoding="utf-8").splitlines():
        try:
            r = json.loads(line)
        except Exception:                                      # noqa: BLE001
            continue
        if r.get("ts", 0) > since:
            out.append(r)
    return out[-limit:]


# ---------- 生图队列 ----------

QUEUE = "gen-queue.json"


def queue(proj):
    f = proj_dir(proj) / QUEUE
    if not f.exists():
        return {"tasks": []}
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except Exception:                                          # noqa: BLE001
        return {"tasks": []}


def queue_save(proj, q):
    f = proj_dir(proj) / QUEUE
    f.write_text(json.dumps(q, ensure_ascii=False, indent=1), encoding="utf-8")
    return q


def queue_add(proj, page, cast, scene, out=None):
    q = queue(proj)
    n = sum(1 for t in q["tasks"] if t.get("page") == page) + 1
    tid = f"{page}-{n}"
    out = out or f"{page}-{tid}.png"
    q["tasks"].append({"id": tid, "page": page, "cast": cast, "scene": scene, "out": out,
                       "status": "queued", "tries": 0, "error": "", "img": "", "metrics": {},
                       "at": time.strftime("%Y-%m-%d %H:%M:%S")})
    queue_save(proj, q)
    emit(proj, "page", id=page, status="queued", detail=f"入队：{scene[:18]}…（{cast}）")
    return tid


def queue_set(proj, tid, **patch):
    q = queue(proj)
    for t in q["tasks"]:
        if t["id"] == tid:
            t.update(patch)
            queue_save(proj, q)
            return t
    return None


# ---------- 审批 ----------

def approvals(proj):
    f = proj_dir(proj) / "docs" / "审批.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def mark(proj, key, verdict, note=""):
    f = proj_dir(proj) / "docs" / "审批.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    d = approvals(proj)
    d[key] = {"verdict": verdict, "note": note, "at": time.strftime("%Y-%m-%d %H:%M:%S")}
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    emit(proj, "approval", key=key, verdict=verdict, note=note)
    return d


def gate_state(proj):
    """三个闸门的状态：open=等确认 / passed=已通过 / None=还没到"""
    d = approvals(proj)
    st = {}
    for g in GATES:
        rec = d.get(f"gate:{g}")
        st[g] = rec["verdict"] if rec else "open"
    return st


# ---------- 环境自检（照 frametell 的 env()）----------

def env_check(deep=False):
    out = []
    r = run(["bsk", "status", "--json"], timeout=60)
    ok = '"daemon_version"' in (r.stdout or "")
    out.append({"name": "bsk daemon", "ok": ok,
                "hint": "" if ok else "跑 `bsk daemon start`（后台）"})
    r = run(["bsk", "doctor"], timeout=120)
    doc = (r.stdout or "") + (r.stderr or "")
    ok = re.search(r"\bok\b\s+extension connected", doc) is not None
    out.append({"name": "浏览器扩展", "ok": ok,
                "hint": "" if ok else "扩展要装在**登录 Flow 的那个 Chrome Profile** 里（另：daemon 要在跑）"})
    ok = EDGE_PY.exists()
    out.append({"name": "edge-tts 配音环境", "ok": ok,
                "hint": "" if ok else f"缺 {EDGE_PY}"})
    r = run(["ffmpeg", "-version"], timeout=60)
    out.append({"name": "ffmpeg", "ok": r.returncode == 0, "hint": ""})
    ok = (ENGINE / "tools" / "render.mjs").exists()
    out.append({"name": "引擎（frametell）", "ok": ok,
                "hint": "" if ok else "fork 不在这台机器上？"})
    # 角色：Flow 项目里的 Characters（要开浏览器，只在深检时做）
    if deep:
        try:
            sys.path.insert(0, str(ROOT / "app"))
            import flowgen                                         # noqa: PLC0415
            f = flowgen.Flow(log=lambda *a: None)
            f.enter("https://flow.google.com/project/2423a8a2-2219-4dd5-83ea-563fd00a79fb")
            n = f._run("(()=>{const t=document.body.innerText||'';"
                       "return ['小树','小芽'].filter(x=>t.includes(x));})()")
            f.close()
            ok = isinstance(n, list) and len(n) >= 1
            out.append({"name": "Flow 项目与角色", "ok": ok,
                        "hint": f"看到：{n}" if ok else "Flow 里找不到 小树/小芽（或没登录）"})
        except Exception as e:                                  # noqa: BLE001
            out.append({"name": "Flow 项目与角色", "ok": False, "hint": f"打不开：{e}"[:120]})
    return out


def read_json(p, default=None):
    try:
        return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))
    except Exception:                                          # noqa: BLE001
        return default


def slug(s):
    return re.sub(r"[^\w-]", "-", (s or "").strip())[:32] or "new-film"
