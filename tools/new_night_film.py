"""开一部新的 night-insight 片：从独立模板复制，挂引擎。

用法：
    python tools/new_night_film.py 夜读-和好 --title "为什么你越安慰，她越崩溃"

之后：
    1. 如果已有音频：python tools/audio_film.py 夜读-和好 transcript.json audio.mp4 --style night-insight
    2. 没有音频：改 night-spec.js / script.js，先出静音 demo
    3. 渲染：cd projects/夜读-和好 && node engine/tools/render.mjs --skip-subs
"""
import argparse
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "projects" / "night-insight-template"
IGNORE = shutil.ignore_patterns("engine", "engine_modules", "out", ".git", "__pycache__")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--title", default="未命名 · 夜读")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    dst = ROOT / "projects" / a.name
    if dst.exists() and not a.force:
        sys.exit(f"{dst} 已存在（要覆盖加 --force）")
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(TEMPLATE, dst, ignore=IGNORE)

    # 只换标题/项目名；内容等接音频后再改
    for f in ["script.js", "night-spec.js", "index.html"]:
        p = dst / f
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        text = text.replace("night-insight-template", a.name)
        text = text.replace("为什么你越安慰，她越崩溃", a.title)
        p.write_text(text, encoding="utf-8")

    r = subprocess.run(
        ["node", "-e",
         "import('./packages/engine/tools/project.mjs')"
         f".then(m=>{{m.linkProject('{dst.as_posix()}');console.log('linked')}})"],
        cwd=str(ROOT / "experiments" / "frametell-src" / "frametell-main"),
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    linked = "linked" in (r.stdout or "")

    print(f"建好：projects/{a.name}")
    print(f"  引擎挂载：{'ok' if linked else '失败（手动跑 linkProject）'}")
    print("\n接下来：")
    print(f"  1. 有音频：python tools/audio_film.py {a.name} <transcript.json> <audio.mp4> --style night-insight")
    print(f"  2. 改版式：projects/{a.name}/night-spec.js")
    print(f"  3. 渲染：cd projects/{a.name} && node engine/tools/render.mjs --skip-subs")


if __name__ == "__main__":
    main()
