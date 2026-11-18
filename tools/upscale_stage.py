"""把队列里的成片图放大到交付画布尺寸（默认 1920×1080），原地覆盖。

Flow 出图是 1376×768；直接进浏览器会被二次缩放、边缘发糊。
先按 Lanczos 放大到 STAGE 尺寸再渲染。

用法：
    python tools/upscale_stage.py <片名>
    VF_STAGE=1440x1080 python tools/upscale_stage.py film-1105-audio
"""
import os
import pathlib
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import pipeline  # noqa: E402

LIB = ROOT / "projects" / "scene-library"
STAGE = tuple(int(x) for x in os.environ.get("VF_STAGE", "1920x1080").lower().split("x", 1))


def main():
    proj = sys.argv[1] if len(sys.argv) > 1 else ""
    if not proj:
        sys.exit("用法：python tools/upscale_stage.py <片名>")
    q = pipeline.queue(proj)
    n = 0
    for t in q["tasks"]:
        name = t.get("img") or ""
        if not name:
            continue
        src = LIB / name
        if not src.exists():
            continue
        with Image.open(src) as im:
            if im.size == STAGE:
                continue
            out = im.convert("RGB").resize(STAGE, Image.LANCZOS)
        out.save(src)
        n += 1
    print(f"  {n} 张放大到 {STAGE[0]}×{STAGE[1]}（{LIB}）")


if __name__ == "__main__":
    main()
