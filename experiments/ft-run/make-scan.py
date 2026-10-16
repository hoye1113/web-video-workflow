"""造一份"扫描件"PDF 当测试夹具：把文字画成图片，再塞进 PDF —— 于是**没有文字层**。

用法：uv run --with pymupdf --with pillow python make-scan.py <输出目录>
"""
import sys
from pathlib import Path

import fitz
from PIL import Image, ImageDraw, ImageFont

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
OUT.mkdir(parents=True, exist_ok=True)

PAGES = [
    ["丈夫出轨后的三个阶段", "", "第一阶段：暴露前的暗流", "关系在出事之前就进入了无波无澜的状态。", "两个人之间的对话从每天几十句，降到只剩家务分工。"],
    ["第二阶段：暴露与恐惧", "", "被发现的当晚，他的第一反应不是解释，是恐惧。", "恐惧的对象是：失去现在的生活秩序。", "于是他开始补偿：更顺从、更早回家、更主动做家务。"],
    ["第三阶段：修复还是消耗", "", "补偿不等于修复。", "真正的修复是重新建立规则和边界，", "让关系重新变得可承受、可持续。"],
]

# 用系统里的中文字体把文字画成图
font_path = r"C:\Windows\Fonts\msyh.ttc"
title_font = ImageFont.truetype(font_path, 46)
body_font = ImageFont.truetype(font_path, 34)

doc = fitz.open()
for lines in PAGES:
    im = Image.new("RGB", (1240, 1754), "white")     # A4 @150dpi 左右
    d = ImageDraw.Draw(im)
    y = 150
    for i, line in enumerate(lines):
        if not line:
            y += 20
            continue
        d.text((130, y), line, fill=(24, 24, 28), font=title_font if i == 0 else body_font)
        y += 80
    png = OUT / f"_tmp_{len(doc)}.png"
    im.save(png)
    page = doc.new_page(width=595, height=842)       # A4 pt
    page.insert_image(fitz.Rect(0, 0, 595, 842), filename=str(png))
    png.unlink()

pdf = OUT / "materials" / "婚姻修复_扫描稿.pdf"
pdf.parent.mkdir(parents=True, exist_ok=True)
doc.save(pdf)
doc.close()
print("造好：", pdf, f"（{len(PAGES)} 页，无文字层）")

# 验一下："没有文字层"是不是真的
d2 = fitz.open(pdf)
text = "".join(d2.load_page(i).get_text() for i in range(d2.page_count))
print("提取到的文字长度：", len(text.strip()), "字  ← 应该是 0（这就是扫描件的样子）")
d2.close()
