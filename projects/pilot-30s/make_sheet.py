# -*- coding: utf-8 -*-
"""把 7 张关键帧拼成一张 3×3 对照表。"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
KEYS = ROOT / "out" / "keyframes"
OUT = ROOT / "out" / "contact-sheet.jpg"

ITEMS = [
    ("p01", "钩子"),
    ("p02", "反常识"),
    ("p03", "错误示范"),
    ("p04", "机制"),
    ("p05", "正确动作"),
    ("p06", "选择权"),
    ("p07", "收尾"),
]

cell_w, cell_h, gap = 620, 349, 15
cols, rows = 3, 3
width = cols * cell_w + (cols + 1) * gap
height = rows * cell_h + (rows + 1) * gap

sheet = Image.new("RGB", (width, height), (6, 8, 11))
draw = ImageDraw.Draw(sheet)
title_font = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 20)
note_font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 15)

for i, (pid, label) in enumerate(ITEMS):
    img = Image.open(KEYS / f"{pid}.png").convert("RGB")
    img = img.resize((cell_w, cell_h), Image.LANCZOS)
    x = gap + (i % cols) * (cell_w + gap)
    y = gap + (i // cols) * (cell_h + gap)
    sheet.paste(img, (x, y))
    draw.rectangle([x, y + cell_h - 34, x + cell_w, y + cell_h], fill=(0, 0, 0))
    draw.text((x + 14, y + cell_h - 30), f"{pid}  {label}", font=title_font, fill=(210, 230, 232))

x = gap + 2 * (cell_w + gap) + 14
y = gap + 2 * (cell_h + gap) + cell_h - 30
draw.text((x, y), "1920×1080 / 30s / 静音样片", font=note_font, fill=(90, 105, 115))

sheet.save(OUT, quality=92)
print(OUT, sheet.size)
