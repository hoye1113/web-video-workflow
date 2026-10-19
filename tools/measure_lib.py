"""在已知的图库上找判据：能不能一眼分出「小树（男）」和「小芽（女）」。

思路：头发和衣服是主要区别 —— 男：灰蓝发 + 灰蓝外套（偏冷）；女：浅栗发 + 米白卫衣（偏暖）。
数两类像素：
  warm_px：R-B>25 且 R>120（栗色/暖棕）
  cool_px：B-R>10 且 B>90（灰蓝）
把整图缩到 320x180 数。
"""
import pathlib
import sys

from PIL import Image

LIB = pathlib.Path(__file__).resolve().parent.parent / "projects" / "scene-library"
CAST = pathlib.Path(__file__).resolve().parent.parent / "cast"


def stat(p):
    im = Image.open(p).convert("RGB").resize((320, 180))
    warm = cool = 0
    for r, g, b in im.getdata():
        if r - b > 25 and r > 120:
            warm += 1
        if b - r > 10 and b > 90:
            cool += 1
    return warm, cool


print(f"{'文件':<28}{'warm(栗/暖棕)':>14}{'cool(灰蓝)':>12}   判定")
for p in sorted(LIB.glob("*.png")) + sorted(CAST.glob("*.jpg")):
    w, c = stat(p)
    verdict = "男·小树" if c > w else "女·小芽"
    print(f"{p.name:<28}{w:>14}{c:>12}   {verdict}")
