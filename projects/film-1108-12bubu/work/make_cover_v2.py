from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

LIB = Path(r"C:\Users\QWQ\web-video-workflow\projects\scene-library")
OUT = Path(r"E:\video-factory\1108-12bubu")
W, H = 1080, 1440
BG = (11, 18, 32)
YELLOW = (241, 207, 94)
CREAM = (245, 234, 210)
SOFT = (201, 185, 154)

FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_REG = r"C:\Windows\Fonts\msyh.ttc"


def font(path, size):
    return ImageFont.truetype(path, size)


def make(scene, out_path):
    im = Image.new("RGB", (W, H), BG)
    dr = ImageDraw.Draw(im)

    # 只保留顶部品牌小标，底部整行删除
    dr.text((84, 92), "李安老师 · 婚姻与孩子", fill=YELLOW, font=font(FONT_BOLD, 26))
    dr.text((84, 164), "想离婚的人", fill=CREAM, font=font(FONT_BOLD, 126))
    dr.text((84, 300), "先看看孩子", fill=YELLOW, font=font(FONT_BOLD, 126))
    dr.text((84, 468), "孩子要承受的，", fill=SOFT, font=font(FONT_REG, 38))
    dr.text((84, 518), "远比你想的多。", fill=SOFT, font=font(FONT_REG, 38))
    dr.rectangle([84, 596, 224, 600], fill=YELLOW)

    # 4:3 裁切后再放大，人物更大；左右留 60px，不铺满
    with Image.open(LIB / scene) as src:
        src = src.convert("RGB")
        cw, ch = 1440, 1080
        left = (src.width - cw) // 2
        top = (src.height - ch) // 2
        panel = src.crop((left, top, left + cw, top + ch)).resize((960, 720), Image.LANCZOS)
    im.paste(panel, (60, 620))
    dr.rectangle([60, 620, 1020, 622], fill=YELLOW)

    im.save(out_path, quality=95)
    print(out_path, im.size)


make("f1108b-p03.png", OUT / "封面A-3x4-李安老师.png")
make("f1108b-p10.png", OUT / "封面B-3x4-李安老师.png")

# 对比图
a = Image.open(OUT / "封面A-3x4-李安老师.png").convert("RGB").resize((540, 720), Image.LANCZOS)
b = Image.open(OUT / "封面B-3x4-李安老师.png").convert("RGB").resize((540, 720), Image.LANCZOS)
cmp = Image.new("RGB", (1096, 756), BG)
cmp.paste(a, (4, 32))
cmp.paste(b, (552, 32))
d = ImageDraw.Draw(cmp)
d.text((8, 4), "A  ·  儿童房", fill=CREAM, font=font(FONT_BOLD, 20))
d.text((556, 4), "B  ·  客厅书包", fill=CREAM, font=font(FONT_BOLD, 20))
cmp.save(OUT / "封面AB对比-李安老师.png", quality=95)
print("compare", cmp.size)
