"""把垂直切片做好的两镜塞进项目里，让界面一打开就有东西可看、可渲。

用法：python tools/seed_demo.py
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import store  # noqa: E402

ENGINE = ROOT / "base-arch" / "scripts" / "engine"
PROJ = "marriage"

SHOTS = [
    dict(id="22", title="一只沙漏，细沙一粒粒往下落", dur=5, camera="停", text="", note="细沙连续下落，沙堆长高",
         src=ENGINE / "scenes" / "zz_hourglass.js", old="zz_hourglass"),
    dict(id="23", title="床沿凹下去一块，男人的手撑在上面", dur=5, camera="缓推", text="", note="手压下去，床沿凹陷",
         src=ENGINE / "scenes" / "zz_bedside.js", old="zz_bedside", assets=["hand_v2.png"]),
]


def main():
    if not (ROOT / "projects" / PROJ / "project.json").exists():
        store.create(PROJ, "犯错的男人还会不会爱")

    # 贴图搬进项目
    (ROOT / "projects" / PROJ / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copy(ENGINE / "assets" / "hand_v2.png", ROOT / "projects" / PROJ / "assets" / "hand_v2.png")

    m = store.load(PROJ)
    m["style"] = {
        "look": "扁平矢量线稿：米白底、深灰墨线勾勒、砖红与暖黄点缀，整套画风从头到尾不换",
        "palette": ["#F3EEE6", "#2A2A2A", "#8A8A8A", "#C8553D", "#E9B872"],
        "character": "只出手和背影，不画脸",
    }
    if not m.get("script"):
        m["script"] = (ROOT / "experiments" / "demo" / "文稿.txt").read_text(encoding="utf-8")

    for s in SHOTS:
        code = s["src"].read_text(encoding="utf-8")
        code = code.replace(f"SCENES['{s['old']}']", f"SCENES['{s['id']}']")
        code = code.replace("'assets/hand_v2.png'", f"'demos/{PROJ}/assets/hand_v2.png'")
        (ROOT / "projects" / PROJ / "scenes" / f"{s['id']}.js").write_text(code, encoding="utf-8")

    m["shots"] = [
        {k: v for k, v in s.items() if k not in ("src", "old")} | {"status": "draft"}
        for s in SHOTS
    ]
    store.save(PROJ, m)
    print(f"项目 {PROJ} 已就绪：{len(m['shots'])} 镜")


if __name__ == "__main__":
    main()
