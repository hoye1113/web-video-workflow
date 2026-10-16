"""探路五：用 observe 给的 ref 试两条路
  A. 把图 drop 到提示框 @e12 本身
  B. 点 @e13 之后立刻 observe（二级菜单可能开在新图层里）
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
    " text:(document.body.innerText||'').replace(/\\n+/g,' | ').slice(0,220)};})()"
)


def refs(f, pat):
    out, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "12000", timeout=300)
    return (out or ""), re.findall(pat, out or "")


f = flowgen.Flow()
try:
    f.open()
    obs, _ = refs(f, r"")
    m = re.search(r"@(e\d+)\s+textbox\s+\"What do you want to create\"", obs)
    box = "@" + m.group(1) if m else None
    print("提示框 ref：", box)

    print("\n=== A. drop 到提示框 ===")
    o, e, c = flowgen._bsk("upload", "--file", IMG, "--session", f.sid, "--ref", box,
                           "--mode", "drop", "--timeout", "90s", timeout=240)
    print("  ", ((o or "") + (e or "")).strip()[:260], "| 退出码", c)
    time.sleep(4)
    print("  状态：", json.dumps(f._run(STATE), ensure_ascii=False)[:300])

    print("\n=== B. 点 ingredients 后立刻观察（找新图层/菜单） ===")
    obs2, _ = refs(f, r"")
    m2 = re.search(r"@(e\d+)\s+button\s+\"Add ingredients", obs2)
    if m2:
        flowgen._bsk("click", "@" + m2.group(1), "--session", f.sid, timeout=120)
        time.sleep(2)
        obs3, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "12000", timeout=300)
        print("  点后 observe 有多层吗：", ("@layers 2" in (obs3 or "")) or ("@layers 3" in (obs3 or "")))
        for line in (obs3 or "").splitlines():
            if re.search(r"ingredient|menu|upload|device|character|参考|素材|照片|media", line, re.I):
                print("    " + line.strip()[:140])
finally:
    print("\n会话：", f.sid)
