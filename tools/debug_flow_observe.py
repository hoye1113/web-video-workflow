"""探路四：把 observe 的输出打出来，找"接文件的区域"和 ingredients 的二级菜单。
"""
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
    out, err, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "12000", timeout=300)
    text = out or ""
    print("observe 输出 %d 字符" % len(text))
    keep = []
    for line in text.splitlines():
        if re.search(r"ingredient|drop|media|upload|image|file|prompt|editor|box|attach", line, re.I):
            keep.append(line.rstrip()[:150])
    print("=== 相关行 ===")
    for l in keep[:40]:
        print("  " + l)
    print()
    print("=== 输出开头 25 行（看格式） ===")
    for l in text.splitlines()[:25]:
        print("  " + l.rstrip()[:150])
finally:
    print("\n会话：", f.sid)
