"""把 upload 的完整报错打出来（上两次被截断了），好知道到底要什么权限。"""
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
    out, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "12000", timeout=300)
    m = re.search(r'@(e\d+)\s+button\s+"Add ingredients', out or "")
    print("ingredients ref:", "@" + m.group(1) if m else None)
    flowgen._bsk("click", "@" + m.group(1), "--session", f.sid, timeout=120)
    time.sleep(2)
    out2, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "12000", timeout=300)
    print("\n=== 菜单图层里有什么（全部） ===")
    for line in (out2 or "").splitlines():
        if "@layers" in line or re.search(r"button|menuitem|combobox", line):
            print("  " + line.strip()[:130])
    m2 = re.search(r'@(e\d+)\s+button\s+"Upload media"', out2 or "")
    print("\nUpload media ref:", "@" + m2.group(1) if m2 else None)
    o, e, c = flowgen._bsk("upload", "--file", str(ROOT / "cast" / "girl.jpg"), "--session", f.sid,
                           "--ref", "@" + m2.group(1), "--mode", "input", "--json", "--timeout", "120s", timeout=300)
    print("\n=== upload 完整输出 ===")
    print("stdout:", (o or "").strip()[:1200])
    print("stderr:", (e or "").strip()[:1200])
    print("退出码:", c)
finally:
    print("\n会话:", f.sid)
