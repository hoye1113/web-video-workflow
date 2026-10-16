"""最大化窗口 + 试拖放（绕开文件输入的权限问题）。

bsk 的报错是：set_file_input_files 被 Chrome 拒（"Not allowed"），
提示要 Chrome 扩展开 'Allow access to file URLs'。拖放走的是另一条路（CDP 的拖放事件），
值得先试 —— 不行再请用户点那个权限。
"""
import json
import pathlib
import re
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

IMG = str(ROOT / "cast" / "girl.jpg")
STATE = (
    "(()=>{const vis=(e)=>e.offsetParent!==null;"
    "const imgs=[...document.querySelectorAll('img')].filter(vis).filter(i=>i.naturalWidth>20);"
    "return {imgs:imgs.length, sizes:imgs.map(i=>i.naturalWidth+'x'+i.naturalHeight).slice(0,8),"
    " text:(document.body.innerText||'').replace(/\\n+/g,' | ').slice(0,240)};})()"
)

f = flowgen.Flow()
try:
    f.open()
    print("=== 窗口放到 1600x900 ===")
    o, e, c = flowgen._bsk("window", "resize", "--session", f.sid, "--width", "1600", "--height", "900", timeout=120)
    print("  ", ((o or "") + (e or "")).strip()[:160] or "(ok)", "| 退出码", c)
    time.sleep(2)

    out, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "14000", timeout=300)
    print("\n=== 窗口变大后的元素（按钮/文本框） ===")
    for line in (out or "").splitlines():
        if re.search(r"button|textbox|menuitem", line):
            print("  " + line.strip()[:120])

    m = re.search(r'@(e\d+)\s+textbox\s+"What do you want to create"', out or "")
    print("\n提示框 ref：", "@" + m.group(1) if m else "没找到")
    if not m:
        raise SystemExit(0)

    print("\n=== 试：drop 到提示框 ===")
    o, e, c = flowgen._bsk("upload", "--file", IMG, "--session", f.sid, "--ref", "@" + m.group(1),
                           "--mode", "drop", "--json", "--timeout", "120s", timeout=300)
    print("  stdout:", (o or "").strip()[:500])
    print("  stderr:", (e or "").strip()[:300])
    print("  退出码:", c)
    time.sleep(4)
    print("  之后状态：", json.dumps(f._run(STATE), ensure_ascii=False)[:320])
finally:
    print("\n会话:", f.sid)
