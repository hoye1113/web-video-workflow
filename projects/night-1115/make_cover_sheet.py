# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

here = Path(__file__).resolve().parent
out_dir = here / "out"
a = Image.open(out_dir / "封面A-3x4.png").convert("RGB").resize((540, 720), Image.LANCZOS)
b = Image.open(out_dir / "封面B-3x4.png").convert("RGB").resize((540, 720), Image.LANCZOS)
out = Image.new("RGB", (1080, 760), (5, 7, 10))
out.paste(a, (0, 40))
out.paste(b, (540, 40))
d = ImageDraw.Draw(out)
f = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 24)
d.text((16, 8), "封面 A · 情绪版", font=f, fill=(220, 235, 238))
d.text((556, 8), "封面 B · 五步版", font=f, fill=(220, 235, 238))
dst = Path("E:/video-factory/night-1115")
dst.mkdir(parents=True, exist_ok=True)
out.save(dst / "封面AB对比.png")
print(dst / "封面AB对比.png")
