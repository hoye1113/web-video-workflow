"""补平 Flow 图底部的纯白边。

裁成 4:3 再放大到 1440×1080 后，底部常留一条 2–6px 的纯白边。
从底部 20% 往上找连续 5 行 R>249.5 且 std<8 的行，取顶部背景色，
用 10px 渐变把底边融回去。原地覆盖队列里的图。

用法：
    python tools/clean_bottom.py <片名>
"""
import pathlib
import sys

import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import pipeline  # noqa: E402

LIB = ROOT / "projects" / "scene-library"


def clean(p, min_frac=0.80):
    im = Image.open(p).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    h, _w, _ = a.shape
    bg = a[:10].reshape(-1, 3).mean(axis=0)
    start = None
    for y in range(int(h * min_frac), h - 4):
        rows = a[y:y + 5]
        if rows[:, :, 0].mean() > 249.5 and rows.std() < 8:
            start = y
            break
    if start is None:
        return None
    start = max(0, start - 5)
    for y in range(start, h):
        k = min(1.0, (y - start) / 10.0)
        a[y] = a[y] * (1 - k) + bg * k
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(p)
    return start


def main():
    proj = sys.argv[1] if len(sys.argv) > 1 else ""
    if not proj:
        sys.exit("用法：python tools/clean_bottom.py <片名>")
    q = pipeline.queue(proj)
    fixed = 0
    for t in q["tasks"]:
        name = t.get("img") or ""
        if not name:
            continue
        src = LIB / name
        if not src.exists():
            continue
        start = clean(src)
        if start is not None:
            fixed += 1
            print(f"  {src.stem} band @ {start}")
    print(f"  {fixed} 张补平底部白边（{LIB}）")


if __name__ == "__main__":
    main()
