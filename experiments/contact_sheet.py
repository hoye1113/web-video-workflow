"""contact sheet: 把一批图拼成一张带文件名的对照表，方便一眼挑能复用的。

用法：
    python experiments/contact_sheet.py <out.png> <cols> <img1> <img2> ...
"""
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\arial.ttf",
]


def font(size):
    for p in FONT_CANDIDATES:
        if pathlib.Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:                                    # noqa: BLE001
                pass
    return ImageFont.load_default()


def main():
    out = pathlib.Path(sys.argv[1])
    cols = int(sys.argv[2])
    files = [pathlib.Path(x) for x in sys.argv[3:]]
    cw, ch = 420, 235
    lab = 26
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw, rows * (ch + lab)), (245, 245, 242))
    d = ImageDraw.Draw(sheet)
    f = font(16)
    for i, p in enumerate(files):
        x, y = (i % cols) * cw, (i // cols) * (ch + lab)
        try:
            im = Image.open(p).convert("RGB")
        except Exception:                                        # noqa: BLE001
            continue
        im.thumbnail((cw - 8, ch - 8))
        sheet.paste(im, (x + 4, y + 4))
        name = p.name
        d.text((x + 6, y + ch + 2), name[:34], fill=(20, 20, 20), font=f)
        d.text((x + 6, y + ch + 2), f"{i}", fill=(200, 60, 60), font=f)
    sheet.save(out)
    print(f"{out} ({len(files)} images, {cols} cols)")


if __name__ == "__main__":
    main()
