from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

LIB = Path(r"C:\Users\QWQ\web-video-workflow\projects\scene-library")
OUT = Path(r"E:\video-factory\1124\work")

ids = [f"p{i:02d}" for i in range(1, 22)]
missing = [pid for pid in ids if not (LIB / f"f1124-{pid}.png").exists()]
print("missing", missing)

cw, ch, pad, head = 420, 236, 6, 30
cols, rows = 4, 6
font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 18)
im = Image.new("RGB", (cols * cw + (cols + 1) * pad, head + rows * ch + (rows + 1) * pad), (16, 22, 34))
dr = ImageDraw.Draw(im)
dr.text((pad, 5), "1124  xiaoshu / xiaoya  p01-p21", font=font, fill=(245, 230, 190))
for i, pid in enumerate(ids):
    p = LIB / f"f1124-{pid}.png"
    if not p.exists():
        continue
    with Image.open(p) as src:
        tile = src.convert("RGB").resize((cw, ch), Image.LANCZOS)
    x = pad + (i % cols) * (cw + pad)
    y = head + pad + (i // cols) * (ch + pad)
    im.paste(tile, (x, y))
    dr.rectangle([x, y, x + 56, y + 24], fill=(16, 22, 34))
    dr.text((x + 4, y + 2), pid, font=font, fill=(255, 210, 120))
out = OUT / "sheet.jpg"
im.save(out, quality=92)
print(out, im.size)
