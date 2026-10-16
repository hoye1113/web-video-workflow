"""项目与镜头的落盘读写。

一个项目 = projects/<name>/ 一个目录：

    projects/<name>/
    ├── project.json      项目元数据：画风锁、文案、镜头表
    ├── scenes/<镜号>.js   镜头的场景代码（引擎的 SCENES 格式）
    ├── assets/           生成的贴图、素材
    └── out/<镜号>.mp4     渲染产物（还有 成片.mp4）

引擎只认自己根目录下的 demos/，所以这里用 Windows 目录联接（junction）把项目挂进去，
零拷贝、上游代码一行不改。渲染完或删除项目时把联接摘掉。
"""
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ROOT / "projects"
ENGINE = ROOT / "base-arch" / "scripts" / "engine"
DEMOS = ENGINE / "demos"

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9_]{0,38}$")   # 引擎的 ?film= 只认 [a-z0-9_]
SHOT_RE = re.compile(r"^[a-z0-9][a-z0-9_]{0,23}$")


def valid_name(n):
    return bool(NAME_RE.match(n or ""))


def valid_shot(n):
    return bool(SHOT_RE.match(n or ""))


def pdir(name):
    return PROJECTS / name


def meta_path(name):
    return pdir(name) / "project.json"


def scene_path(name, shot):
    return pdir(name) / "scenes" / f"{shot}.js"


def out_path(name, shot):
    return pdir(name) / "out" / f"{shot}.mp4"


def default_project(name, title=""):
    return {
        "name": name,
        "title": title or name,
        "fps": 30,
        "width": 1920,
        "height": 1080,
        "style": {"look": "", "palette": [], "character": ""},
        "script": "",
        "shots": [],
    }


def load(name):
    p = meta_path(name)
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def save(name, data):
    d = pdir(name)
    (d / "scenes").mkdir(parents=True, exist_ok=True)
    (d / "assets").mkdir(parents=True, exist_ok=True)
    (d / "out").mkdir(parents=True, exist_ok=True)
    meta_path(name).write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    sync_eras(name)
    link_demo(name)                      # 让引擎和 render.py 都能按 demos/<name>/ 取到
    return data


def patch_shot(name, sid, **fields):
    """只改某一页的几个字段：**现读现写**，绝不攥着一份旧副本。

    踩过（丢更新）：写场景代码要调模型，一分钟；这期间生图任务往 project.json 里
    写了 07/08/10 三页的 images 字段。写场景的活儿拿的是"模型调用之前"加载的副本，
    最后一把 save 把那些字段覆盖回"没有图"——图明明在硬盘上，项目里却没记。
    规矩：**长活儿一律不许持有项目副本**，落盘统一走这里。
    """
    cur = load(name) or {}
    hit = None
    for s in cur.get("shots", []):
        if s.get("id") == sid:
            s.update(fields)
            hit = s
    if hit is None:
        raise ValueError(f"没有第 {sid} 页")
    save(name, cur)
    return hit


def list_projects():
    if not PROJECTS.exists():
        return []
    out = []
    for d in sorted(PROJECTS.iterdir()):
        if not d.is_dir() or not valid_name(d.name):
            continue
        m = load(d.name)
        if not m:
            continue
        n = len(m.get("shots", []))
        done = sum(1 for s in m.get("shots", []) if s.get("status") == "rendered")
        out.append({"name": d.name, "title": m.get("title", d.name), "shots": n, "rendered": done})
    return out


def create(name, title=""):
    if not valid_name(name):
        raise ValueError("项目名只能用 a-z 0-9 _ ，1 到 39 位")
    if pdir(name).exists():
        raise ValueError(f"项目 {name} 已存在")
    data = default_project(name, title)
    save(name, data)
    return data


def delete(name):
    if not valid_name(name) or not pdir(name).exists():
        raise ValueError("项目不存在")
    unlink_demo(name)
    shutil.rmtree(pdir(name), ignore_errors=True)


# ---------- 引擎侧的目录联接 ----------

def demo_link(name):
    return DEMOS / name


def link_demo(name):
    """把 projects/<name>/ 挂到 engine/demos/<name>/，让引擎和 render.py 能按相对路径取到。"""
    if not valid_name(name):
        raise ValueError("项目名不合法")
    link = demo_link(name)
    if link.exists():
        return link
    DEMOS.mkdir(parents=True, exist_ok=True)
    target = pdir(name)
    target.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(link), str(target)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if r.returncode != 0:
        raise RuntimeError(f"创建目录联接失败：{r.stdout}{r.stderr}")
    return link


def unlink_demo(name):
    link = demo_link(name)
    if link.exists():
        # rmdir 只删联接本身，不会删到目标目录里的东西
        subprocess.run(["cmd", "/c", "rmdir", str(link)], capture_output=True,
                       text=True, encoding="utf-8", errors="replace")


# ---------- 段落表（eras.js）----------

def sync_eras(name):
    """按 project.json 生成引擎要的 demos/<name>/eras.js。镜头里没有场景文件的会被跳过。"""
    m = load(name)
    if not m:
        return
    lines = [
        "// 由 video-factory 生成，勿手改；改镜头请用项目面板。",
        "window.PUNCH = 0;",
        f"window.SCENE_DIR = 'demos/{name}/scenes';",
        "window.ERAS = [",
    ]
    for s in m.get("shots", []):
        sid = s.get("id")
        if not valid_shot(sid):
            continue
        if not scene_path(name, sid).exists():
            continue
        dur = float(s.get("dur") or 4)
        assets = s.get("assets") or []
        bits = [f"id: '{sid}'", f"dur: {dur:g}"]
        if assets:
            arr = ", ".join(f"'demos/{name}/assets/{a}'" for a in assets)
            bits.append(f"assets: [{arr}]")
        lines.append("  { " + ", ".join(bits) + " },")
    lines.append("];")
    (pdir(name) / "eras.js").write_text("\n".join(lines) + "\n", encoding="utf-8")


def read_scene(name, shot):
    p = scene_path(name, shot)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8")


def write_scene(name, shot, src):
    if not valid_shot(shot):
        raise ValueError("镜号只能用 a-z 0-9 _")
    p = scene_path(name, shot)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(src, encoding="utf-8")
    sync_eras(name)
    return p


def delete_scene(name, shot):
    p = scene_path(name, shot)
    if p.exists():
        p.unlink()
    sync_eras(name)


# ---------- 版本存档（导演回路每轮留一版，最后只保留最好的那版）----------

def versions_dir(name, shot):
    return pdir(name) / "versions" / shot


# ---------- 页的指纹：页的设定变了，旧场景就不该再被用 ----------

def shot_fingerprint(shot):
    """页的设定（标题/画面/旁白/时长/镜头/屏上字/做法/素材）的短摘要。

    场景代码是按这些写出来的；哪天这些改了而场景没重写，渲出来的就是另一页的画面。
    写场景时把当时的指纹记进 shot['sceneHash']，对不上就说明要重写。

    mode 和 images 也算进来：贴图页换了一张图，代码就该重写（图里的东西变了）。
    """
    import hashlib
    parts = [str(shot.get(k) or "") for k in
             ("title", "note", "narration", "dur", "camera", "text", "mode")]
    parts.append(",".join(shot.get("images") or []))
    return hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:10]


def archive_scenes(name, tag):
    """把当前所有场景文件挪到 scenes_old/<tag>/，工作目录清空。

    重跑切页时用：页列表换了，旧场景对应的是旧页，留着会被静默当成新页的代码。
    挪而不是删，要找回还有。
    """
    src = pdir(name) / "scenes"
    if not src.exists():
        return 0
    files = list(src.glob("*.js"))
    if not files:
        return 0
    dst = pdir(name) / "scenes_old" / tag
    dst.mkdir(parents=True, exist_ok=True)
    for f in files:
        shutil.move(str(f), str(dst / f.name))
    sync_eras(name)
    return len(files)


def save_version(name, shot, src, review=None):
    d = versions_dir(name, shot)
    d.mkdir(parents=True, exist_ok=True)
    n = 1
    while (d / f"v{n}.js").exists():
        n += 1
    (d / f"v{n}.js").write_text(src, encoding="utf-8")
    (d / f"v{n}.json").write_text(
        json.dumps(review or {}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return n


def list_versions(name, shot):
    d = versions_dir(name, shot)
    if not d.exists():
        return []
    out = []
    for f in sorted(d.glob("v*.js"), key=lambda p: int(re.findall(r"\d+", p.stem)[0])):
        n = int(re.findall(r"\d+", f.stem)[0])
        rev = {}
        rp = d / f"v{n}.json"
        if rp.exists():
            rev = json.loads(rp.read_text(encoding="utf-8"))
        out.append({"n": n, "score": rev.get("score", -1), "ok": rev.get("ok", False),
                    "problems": rev.get("problems", [])})
    return out


def load_version(name, shot, n):
    p = versions_dir(name, shot) / f"v{n}.js"
    return p.read_text(encoding="utf-8") if p.exists() else None


def update_version_review(name, shot, n, review):
    p = versions_dir(name, shot) / f"v{n}.json"
    p.write_text(json.dumps(review or {}, ensure_ascii=False, indent=2), encoding="utf-8")
