"""12布布 / 李安老师 · 3:4 封面模板（2026-11-23 定稿）。

版式固定：
  1080×1440
  顶部品牌小标  →  两行主标题  →  两行副标题  →  黄色短线
  下半部满宽场景图 1080×840（从 y=600 一直到底部）
  底部不留任何文字

图可以按内容换；标题、副标题、栏目名按当期文案换。
中文字用本地字体排版，不让 AI 写标题。

用法：
  python tools/cover_3x4.py 场景.png 输出.png
  python tools/cover_3x4.py 场景.png 输出.png --brand "李安老师 · 婚姻与孩子" ^
      --title1 "想离婚的人" --title2 "先看看孩子" ^
      --sub1 "孩子要承受的，" --sub2 "远比你想的多。"
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1440
BG = (11, 18, 32)
YELLOW = (241, 207, 94)
CREAM = (245, 234, 210)
SOFT = (201, 185, 154)

FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_REG = r"C:\Windows\Fonts\msyh.ttc"
MAX_TEXT_W = 912


def fit(draw, text, path, max_size, min_size, max_width=MAX_TEXT_W):
    for size in range(max_size, min_size - 1, -1):
        f = ImageFont.truetype(path, size)
        bbox = draw.textbbox((0, 0), text, font=f)
        if bbox[2] - bbox[0] <= max_width:
            return f
    return ImageFont.truetype(path, min_size)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scene")
    ap.add_argument("out")
    ap.add_argument("--brand", default="李安老师 · 婚姻与孩子")
    ap.add_argument("--title1", default="想离婚的人")
    ap.add_argument("--title2", default="先看看孩子")
    ap.add_argument("--sub1", default="孩子要承受的，")
    ap.add_argument("--sub2", default="远比你想的多。")
    a = ap.parse_args()

    im = Image.new("RGB", (W, H), BG)
    dr = ImageDraw.Draw(im)

    if a.brand:
        dr.text((84, 92), a.brand, fill=YELLOW, font=fit(dr, a.brand, FONT_BOLD, 26, 20))
    dr.text((84, 164), a.title1, fill=CREAM, font=fit(dr, a.title1, FONT_BOLD, 126, 84))
    dr.text((84, 300), a.title2, fill=YELLOW, font=fit(dr, a.title2, FONT_BOLD, 126, 84))
    if a.sub1:
        dr.text((84, 468), a.sub1, fill=SOFT, font=fit(dr, a.sub1, FONT_REG, 38, 28))
    if a.sub2:
        dr.text((84, 518), a.sub2, fill=SOFT, font=fit(dr, a.sub2, FONT_REG, 38, 28))
    dr.rectangle([84, 568, 224, 572], fill=YELLOW)

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
    dr.rectangle([0, 598, W - 1, 600], fill=YELLOW)

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=95)
    print(out, im.size)


if __name__ == "__main__":
    main()
