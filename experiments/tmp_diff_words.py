import json
import pathlib
import re
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
b = json.loads((ROOT / "projects/infidelity-1021/brief.json").read_text(encoding="utf-8"))
mat = re.sub(r"\s", "", b["materials"])
FILL = "啊呀呢吧嗯哦嘛哈哎呐呃噢"
orig = "".join(ch for ch in mat if ch not in FILL and ch not in "，。？！；：、,.!?;:")
d = json.loads((ROOT / "projects/infidelity-1021/script-source.json").read_text(encoding="utf-8"))
mine = "".join(c for p in d["pages"] for c in p["cues"])
mine = "".join(ch for ch in mine if ch not in "，。？！；：、,.!?;:")

co, cm = Counter(orig), Counter(mine)
dropped = co - cm
extra = cm - co
print("原文去标点去口水:", len(orig), "字")
print("我的稿子去标点   :", len(mine), "字")
print("\n原稿有、我漏掉的字：", "".join(sorted(dropped.elements())))
print("\n我多出来的字    ：", "".join(sorted(extra.elements())))
