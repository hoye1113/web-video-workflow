"""把一部片子的 26 页图按页序拼成对照表（p01…p26），一眼看整片连续性。

用法：python experiments/sheet_film.py <片名> [每行张数]
"""
import json
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB = ROOT / "projects" / "scene-library"
FONT_CANDIDATES = [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"]


def font(size):
    for p in FONT_CANDIDATES:
        if pathlib.Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except Exception:                                    # noqa: BLE001
                pass
    return ImageFont.load_default()


def main():
    proj = sys.argv[1] if len(sys.argv) > 1 else "film-1020-1522"
    cols = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    spec = json.loads((ROOT / "projects" / proj / "page-spec.json").read_text(encoding="utf-8"))
    cw, ch, lab = 400, 225, 30
    rows = (len(spec) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw, rows * (ch + lab)), (245, 245, 242))
    d = ImageDraw.Draw(sheet)
    f = font(15)
    for i, p in enumerate(spec):
        x, y = (i % cols) * cw, (i // cols) * (ch + lab)
        a = LIB / (p.get("asset") or "")
        if a.exists():
            im = Image.open(a).convert("RGB")
            im.thumbnail((cw - 8, ch - 8))
            sheet.paste(im, (x + 4, y + 4))
        d.text((x + 6, y + ch + 4), f'{p["id"]} · {p.get("theme")} · {p.get("cam")}', fill=(20, 20, 20), font=f)
        d.text((x + 6, y + ch + 4), f'{p["id"]}', fill=(200, 60, 60), font=f)
    out = ROOT / "experiments" / f"sheet-{proj}.png"
    sheet.save(out)
    print(out)


if __name__ == "__main__":
    main()
