"""试 Flow Characters 的 Upload 入口：把 girl.jpg 传成一个可复用的角色。"""
import json
import pathlib
import re
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

IMG = str(ROOT / "cast" / "girl.jpg")
f = flowgen.Flow()
try:
    f.open()
    out, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "14000", timeout=300)
    m = re.search(r'@(e\d+)\s+button\s+"Characters"', out or "")
    flowgen._bsk("click", "@" + m.group(1), "--session", f.sid, timeout=120)
    time.sleep(3)
    out2, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "14000", timeout=300)
    m2 = re.search(r'@(e\d+)\s+button\s+"Upload"', out2 or "")
    print("Upload ref:", "@" + m2.group(1) if m2 else "没找到")
    if not m2:
        print(out2[:900]); raise SystemExit(1)

    # ① 先看这个按钮会不会激活一个 file input（bsk 自己会判断）
    o, e, c = flowgen._bsk("upload", "--file", IMG, "--session", f.sid, "--ref", "@" + m2.group(1),
                           "--mode", "input", "--json", "--timeout", "120s", timeout=300)
    print("=== upload 结果 ===")
    print("stdout:", (o or "").strip()[:600])
    print("stderr:", (e or "").strip()[:300])
    print("退出码:", c)
    time.sleep(5)

    # ② 看页面上发生了什么（有没有出现缩略图/角色名输入框）
    st = f._run("(()=>{const vis=(e)=>e.offsetParent!==null;"
                "const imgs=[...document.querySelectorAll('img')].filter(vis).filter(i=>i.naturalWidth>40);"
                "return {imgs:imgs.map(i=>i.naturalWidth+'x'+i.naturalHeight).slice(0,6),"
                " text:(document.body.innerText||'').replace(/\\n+/g,' | ').slice(-420)};})()")
    print("=== 之后页面 ===")
    print(json.dumps(st, ensure_ascii=False)[:600])
finally:
    print("\n会话:", f.sid)
