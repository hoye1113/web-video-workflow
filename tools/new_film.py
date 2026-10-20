"""开一部新片：脚手架（省掉"建工程/挂引擎/写骨架"那几步）。

用法：
    python tools/new_film.py 我的新片 --title "新片标题" --minutes 6

做的事：
  ① 建 projects/<名字>/{pages,docs} + index.html + .gitignore
  ② 写一份 script-source.json 骨架（带字数预算与 cue 规矩说明）
  ③ 让引擎挂进来（engine / engine_modules 两个 junction）
  ④ 打印接下来的命令

之后照着 `docs/新题材开工手册.md` 走：写词 → 出图 → 排页 → 配音 → 渲染 → 验收。
"""
import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ENGINE = ROOT / "experiments" / "frametell-src" / "frametell-main" / "packages" / "engine"

INDEX = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="engine-modules" content="engine_modules/">
<title>__TITLE__</title>
<script src="script.js"></script>
<script src="engine/boot.js"></script>
</head>
<body></body>
</html>
"""

SOURCE = {
    "title": "",
    "gap": 0.8,
    "voice": {"speaker": "zh-CN-XiaoxiaoNeural", "provider": "edge"},
    "note": ("口播稿：一条 cue ≤12 字且第 12 字前要有标点（不然字幕切开词）；"
             "一页 4-8 条 = 10-15 秒。改完跑 tools/check_cues.py（目标 0 条硬切）"
             "→ tools/make_script_js.py --from-source → tools/make_voice.py"),
    "pages": [
        {"id": "p01", "section": "钩子", "title": "（一句话论点）", "cues": [
            "第一句（12 字以内，",
            "第二句。",
        ]},
    ],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name", help="工程目录名（projects/<名字>）")
    ap.add_argument("--title", default="未命名新片")
    ap.add_argument("--minutes", type=float, default=6.0, help="目标片长（分钟）")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    ep = ROOT / "projects" / a.name
    if ep.exists() and not a.force:
        sys.exit(f"{ep} 已经存在（要覆盖加 --force）")
    (ep / "pages").mkdir(parents=True, exist_ok=True)
    (ep / "docs").mkdir(exist_ok=True)
    (ep / "index.html").write_text(INDEX.replace("__TITLE__", a.title), encoding="utf-8")
    (ep / ".gitignore").write_text("engine\nengine_modules\nout/\n.studio/\naudio/\nvoice.js\nagent-session.json\n",
                                   encoding="utf-8")
    src = dict(SOURCE)
    src["title"] = a.title
    (ep / "script-source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1),
                                           encoding="utf-8")
    # 页表：从 emotion-full 复制一份当模板（改它，不改工具）
    demo = ROOT / "projects" / "emotion-full" / "page-spec.json"
    if demo.exists():
        pages = json.loads(demo.read_text(encoding="utf-8"))
        for p in pages[::-1][:len(pages) - 1]:        # 只留第一页当例子，其余删掉
            pages.remove(p)
        pages[0]["id"] = "p01"
        pages[0]["title"] = "（一句话论点）"
        (ep / "page-spec.json").write_text(json.dumps(pages, ensure_ascii=False, indent=1),
                                           encoding="utf-8")
    (ep / "README.md").write_text(
        f"# {a.title}\n\n"
        f"> 目标片长 **{a.minutes:g} 分钟** ≈ **{int(a.minutes * 194)} 字**（实测 194 字/分钟）。\n\n"
        "照 `docs/新题材开工手册.md` 走：\n"
        "1. 写词 `script-source.json`（cue ≤12 字、第 12 字前有标点）→ `tools/check_cues.py`\n"
        "2. 出图 `tools/gen_scenes.py`（先翻 `projects/scene-library/` 有没有能复用的）\n"
        "3. 排页 改 `tools/make_pages.py` 的 PAGES → `python tools/make_pages.py`\n"
        "4. 配音 `python tools/make_voice.py` → 字幕/渲染（见手册第 4 节）\n"
        "5. 验收 `tools/qc_snap.py` + `tools/accept_emotion.py`\n",
        encoding="utf-8")

    # 挂引擎（junction）
    r = subprocess.run(
        ["node", "-e",
         "import('./packages/engine/tools/project.mjs')"
         f".then(m=>{{m.linkProject('{ep.as_posix()}');console.log('linked')}})"],
        cwd=str(ROOT / "experiments" / "frametell-src" / "frametell-main"),
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    linked = "linked" in (r.stdout or "")

    print(f"建好：projects/{a.name}")
    print(f"  目标 {a.minutes:g} 分钟 ≈ {int(a.minutes * 194)} 字；骨架在 script-source.json")
    print(f"  引擎挂载：{'ok' if linked else '失败（手动跑一次 linkProject）'}")
    print("\n接下来：")
    print(f"  1. 写 projects/{a.name}/script-source.json（cue ≤12 字、第 12 字前有标点）")
    print("  2. python tools/check_cues.py --src …（或先照 emotion-full 的例子改）")
    print("  3. python tools/make_script_js.py --from-source")
    print(f"  4. 排页：改 projects/{a.name}/page-spec.json（照 emotion-full 那份的表）")
    print(f"     python tools/make_pages.py --project {a.name}")
    print("  5. 出图 / 配音 / 渲染 / 验收：见 docs/新题材开工手册.md")


if __name__ == "__main__":
    main()
