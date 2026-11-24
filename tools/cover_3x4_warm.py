"""以安 · 3:4 抖音情感封面（暖纸版）。

和 12布布 的深色封面分开：
  1080×1440
  暖米白底 + 深棕标题 + 陶土红强调 + 鼠尾草绿小芽
  顶部品牌“以安 · <栏目>”
  两行主标题 / 两行副标题 / 暖色短线
  下半部 1080×840 满宽暖纸图，底部不留字

用法：
  python tools/cover_3x4_warm.py 场景.png 输出.png
  python tools/cover_3x4_warm.py 场景.png 输出.png --brand "以安 · 依恋关系" ^
      --title1 "回避型最后都是" --title2 "怎么变好变正常的" ^
      --sub1 "看懂回避型，" --sub2 "才知道怎么继续。"
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
BG = (246, 237, 225)
INK = (74, 58, 50)
TERRA = (176, 92, 69)
SUB = (122, 106, 92)
SAGE = (124, 139, 111)
AMBER = (217, 160, 91)

FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_REG = r"C:\Windows\Fonts\msyh.ttc"
MAX_TEXT_W = 912


def fit_size(draw, text, path, max_size, min_size, max_width=MAX_TEXT_W):
    for size in range(max_size, min_size - 1, -1):
        f = ImageFont.truetype(path, size)
        bbox = draw.textbbox((0, 0), text, font=f)
        if bbox[2] - bbox[0] <= max_width:
            return size
    return min_size


def sprout(dr, x, y):
    """小树/小芽的两片叶小图标。"""
    dr.line([(x + 8, y + 20), (x + 8, y + 6)], fill=SAGE, width=2)
    dr.polygon([(x + 8, y + 12), (x - 3, y + 3), (x + 1, y - 5), (x + 9, y + 4)], fill=SAGE)
    dr.polygon([(x + 9, y + 12), (x + 20, y + 3), (x + 16, y - 5), (x + 8, y + 4)], fill=SAGE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scene")
    ap.add_argument("out")
    ap.add_argument("--brand", default="以安 · 依恋关系")
    ap.add_argument("--title1", default="回避型最后都是")
    ap.add_argument("--title2", default="怎么变好变正常的")
    ap.add_argument("--sub1", default="看懂回避型，")
    ap.add_argument("--sub2", default="才知道怎么继续。")
    a = ap.parse_args()

    im = Image.new("RGB", (W, H), BG)
    dr = ImageDraw.Draw(im)

    if a.brand:
        sprout(dr, 84, 96)
        dr.text((116, 92), a.brand, fill=INK, font=ImageFont.truetype(FONT_BOLD, 26))

    t1 = fit_size(dr, a.title1, FONT_BOLD, 126, 84)
    t2 = fit_size(dr, a.title2, FONT_BOLD, 126, 84)
    ts = min(t1, t2)
    tf = ImageFont.truetype(FONT_BOLD, ts)
    dr.text((84, 164), a.title1, fill=INK, font=tf)
    dr.text((84, 164 + ts + 12), a.title2, fill=TERRA, font=tf)

    s1 = fit_size(dr, a.sub1, FONT_REG, 38, 28)
    s2 = fit_size(dr, a.sub2, FONT_REG, 38, 28)
    ss = min(s1, s2)
    sf = ImageFont.truetype(FONT_REG, ss)
    sub_y = 164 + ts * 2 + 52
    if a.sub1:
        dr.text((84, sub_y), a.sub1, fill=SUB, font=sf)
    if a.sub2:
        dr.text((84, sub_y + ss + 12), a.sub2, fill=SUB, font=sf)
    dr.rectangle([84, sub_y + ss * 2 + 34, 224, sub_y + ss * 2 + 38], fill=AMBER)

    with Image.open(a.scene) as src:
        src = src.convert("RGB")
        ar = 1080 / 840
        if src.width / src.height > ar:
            ch = src.height
            cw = round(ch * ar)
        else:
            cw = src.width
            ch = round(cw / ar)
        left = (src.width - cw) // 2
        top = (src.height - ch) // 2
        panel = src.crop((left, top, left + cw, top + ch)).resize((1080, 840), Image.LANCZOS)
    im.paste(panel, (0, 600))
    dr.rectangle([0, 598, W - 1, 600], fill=AMBER)

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=95)
    print(out, im.size)


if __name__ == "__main__":
    main()
