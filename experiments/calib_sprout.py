"""校准「嫩芽色」的判据：老窗口（g>190,r>160,b<200,g-b>30）对暗一点的嫩芽会漏判。

目标：把「有嫩芽」和「没嫩芽」分开 —— 判据要宽到认得橄榄绿的嫩芽，
又不能宽到把纸面/衣服的灰绿算进去。

用法：python experiments/calib_sprout.py
"""
import pathlib

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB = ROOT / "projects" / "scene-library"
SPARE = ROOT / "experiments" / "spare"

HAVE = ["p04-phone-pushaway.png", "p08-phone-ignored.png", "p13-phone-in-hand.png",
        "p15-phone-flip.png", "p23-turn-away.png", "female-02-phone-glow.png",
        "male-02-phone-glow.png", "p03-cases.png", "p24-clench.png", "p16-keys.png",
        "p15-night-door.png", "p13-two-lights.png"]
NONE = ["rescue-01.png", "rescue-02.png"]          # 背对镜头 → 实测没有嫩芽

WINDOWS = {
    "old": lambda r, g, b: g > 190 and r > 160 and b < 200 and (g - b) > 30,
    "mid": lambda r, g, b: g > 150 and r > 110 and b < 190 and (g - b) > 25,
    "w2": lambda r, g, b: g > 120 and r > 90 and b < 195 and (g - b) > 20,
    "w3": lambda r, g, b: g > 105 and r > 80 and b < 200 and (g - b) > 15,
}


def count(p, mode):
    im = Image.open(p).convert("RGB").resize((160, 90))
    px = list(im.getdata())
    fn = WINDOWS[mode]
    return sum(1 for r, g, b in px if fn(r, g, b))


for mode in WINDOWS:
    have = [count(LIB / n, mode) for n in HAVE if (LIB / n).exists()]
    none = [count(SPARE / n, mode) for n in NONE if (SPARE / n).exists()]
    print(f"{mode:>4}: 有嫩芽 min={min(have):>4} 全部={have}")
    print(f"      没嫩芽      {none}")
