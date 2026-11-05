"""把队列里的图居中裁成 4:3，写回队列（img 改成 *-43.png）。

Flow 的 4:3 是会话级设置，关闭设置面板会打断输入框，脚本化不稳定；
所以统一按 16:9 出图，再确定性裁切。构图在提示词里要求"主体居中、左右留安全边距"。

用法：
    python tools/crop_43.py <片名>
"""
import json
import pathlib
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import pipeline  # noqa: E402

LIB = ROOT / "projects" / "scene-library"


def main():
    proj = sys.argv[1] if len(sys.argv) > 1 else ""
    if not proj:
        sys.exit("用法：python tools/crop_43.py <片名>")
    q = pipeline.queue(proj)
    n = 0
    for t in q["tasks"]:
        name = t.get("img") or ""
        if not name:
            continue
        src = LIB / name
        if not src.exists():
            continue
        if name.endswith("-43.png"):
            continue
        im = Image.open(src).convert("RGB")
        w, h = im.size
        tw = round(h * 4 / 3)
        if tw > w:
            th = round(w * 3 / 4)
            top = (h - th) // 2
            out = im.crop((0, top, w, top + th))
        else:
            left = (w - tw) // 2
            out = im.crop((left, 0, left + tw, h))
        dst = src.with_name(src.stem + "-43.png")
        out.save(dst)
        t["img"] = dst.name
        n += 1
    pipeline.queue_save(proj, q)
    print(f"  {n} 张裁成 4:3（{LIB}）")


if __name__ == "__main__":
    main()
