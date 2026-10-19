"""摸清：怎么把项目素材库里的 girl.jpg 挂进提示词（Add to prompt）。

用户已经把 girl.jpg / boy.jpg 传进 Flow 项目素材库了 —— 走这条路不用本地文件权限。
要探清：Add ingredients 的菜单里有没有"从项目选"这一项，以及素材面板怎么操作。
"""
import json
import pathlib
import re
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

f = flowgen.Flow()
try:
    f.open()
    out, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "16000", timeout=300)
    m = re.search(r'@(e\d+)\s+button\s+"Add ingredients', out or "")
    print("ingredients ref:", "@" + m.group(1) if m else "没找到")
    flowgen._bsk("click", "@" + m.group(1), "--session", f.sid, timeout=120)
    time.sleep(3)

    out2, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "16000", timeout=300)
    print("=== 菜单图层里的**全部**元素 ===")
    for line in (out2 or "").splitlines():
        s = line.strip()
        if re.search(r"@e\d+|@layers", s) and len(s) < 160:
            print("  " + s)
finally:
    print("\n会话:", f.sid)
