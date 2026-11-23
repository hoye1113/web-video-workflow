from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

LIB = Path(r"C:\Users\QWQ\web-video-workflow\projects\scene-library")
OUT = Path(r"E:\video-factory\1108-12bubu")
W, H = 1080, 1440
BG = (11, 18, 32)
YELLOW = (241, 207, 94)
CREAM = (245, 234, 210)
SOFT = (201, 185, 154)
MUTED = (143, 163, 200)

FONT_BOLD = r"C:\Windows\Fonts\msyhbd.ttc"
FONT_REG = r"C:\Windows\Fonts\msyh.ttc"


def font(path, size):
    return ImageFont.truetype(path, size)


def draw_text(dr, xy, text, f, fill):
    dr.text(xy, text, font=f, fill=fill)


def make(scene, out_path):
    im = Image.new("RGB", (W, H), BG)
    dr = ImageDraw.Draw(im)

    draw_text(dr, (84, 92), "12布布 · 婚姻与孩子", font(FONT_BOLD, 26), YELLOW)
    draw_text(dr, (84, 164), "想离婚的人", font(FONT_BOLD, 126), CREAM)
    draw_text(dr, (84, 300), "先看看孩子", font(FONT_BOLD, 126), YELLOW)

    draw_text(dr, (84, 468), "孩子要承受的，", font(FONT_REG, 38), SOFT)
    draw_text(dr, (84, 518), "远比你想的多。", font(FONT_REG, 38), SOFT)
    dr.rectangle([84, 596, 224, 600], fill=YELLOW)

    # 16:9 场景面板，整幅缩小，保留两人和儿童道具
    with Image.open(LIB / scene) as src:
        panel = src.convert("RGB").resize((1080, 608), Image.LANCZOS)
    im.paste(panel, (0, 650))
    dr.rectangle([0, 650, W - 1, 652], fill=YELLOW)

    draw_text(dr, (84, 1348), "12布布 · 无字幕情感短片", font(FONT_REG, 24), MUTED)
    right = "先看见孩子"
    bbox = dr.textbbox((0, 0), right, font=font(FONT_REG, 24))
    draw_text(dr, (W - 84 - (bbox[2] - bbox[0]), 1348), right, font(FONT_REG, 24), MUTED)

    im.save(out_path, quality=95)
    print(out_path, im.size)


make("f1108b-p03.png", OUT / "封面A-3x4.png")
make("f1108b-p10.png", OUT / "封面B-3x4.png")

# A/B 对比图
a = Image.open(OUT / "封面A-3x4.png").convert("RGB").resize((540, 720), Image.LANCZOS)
b = Image.open(OUT / "封面B-3x4.png").convert("RGB").resize((540, 720), Image.LANCZOS)
cmp = Image.new("RGB", (1096, 756), BG)
cmp.paste(a, (4, 32))
cmp.paste(b, (552, 32))
d = ImageDraw.Draw(cmp)
d.text((8, 4), "A  ·  儿童房", fill=CREAM, font=font(FONT_BOLD, 20))
d.text((556, 4), "B  ·  客厅书包", fill=CREAM, font=font(FONT_BOLD, 20))
cmp.save(OUT / "封面AB对比.png", quality=95)
print("compare", cmp.size)
