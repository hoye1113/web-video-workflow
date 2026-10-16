"""探路三：把 cast/girl.jpg 挂成 Flow 的参考图（ingredients）。

三条路依次试，看哪条能成：
  A. 直接对 ingredients 按钮做 upload --mode input（bsk 会点触发器 + 接管文件选择器）
  B. hover 出二级菜单，再点菜单里的"上传/设备"
  C. 把图 drop 到提示框区域
每次试完都看：提示框附近有没有多出一个缩略图。
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
    "const eds=[...document.querySelectorAll('[contenteditable=true]')].filter(vis);"
    "return {imgs:imgs.length, thumbs:imgs.map(i=>i.naturalWidth+'x'+i.naturalHeight).slice(0,8),"
    " eds:eds.length, hint:(document.body.innerText||'').replace(/\\n+/g,' | ').slice(0,260)};})()"
)

f = flowgen.Flow()
try:
    f.open()
    print("初始状态：", json.dumps(f._run(STATE), ensure_ascii=False)[:300])

    print()
    print("=== A. upload --mode input 直指 ingredients 按钮 ===")
    o, e, c = flowgen._bsk("upload", "--file", IMG, "--session", f.sid,
                           "--selector", 'button[aria-label*="ingredient" i]',
                           "--mode", "input", "--timeout", "90s", timeout=180)
    print("  输出：", ((o or "") + (e or "")).strip()[:300], " 退出码", c)
    time.sleep(5)
    print("  之后：", json.dumps(f._run(STATE), ensure_ascii=False)[:300])

    if "girl" not in json.dumps(f._run(STATE)):
        print()
        print("=== B. hover 出二级菜单 ===")
        out, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "8000", timeout=180)
        m = re.search(r'@(e\d+)\s+button\s+"([^"]*ingredient[^"]*)"', out or "", re.I)
        if m:
            flowgen._bsk("hover", "@" + m.group(1), "--session", f.sid, timeout=120)
            time.sleep(3)
            items = f._run("(()=>{const vis=(e)=>e.offsetParent!==null;"
                           "const t=[...document.querySelectorAll('[role=menuitem],[role=option],li,button,div')]"
                           ".filter(vis).map(e=>(e.textContent||'').trim()).filter(x=>x&&x.length<26);"
                           "return [...new Set(t)].slice(0,26);})()")
            print("  hover 后可见项：", json.dumps(items, ensure_ascii=False)[:500])

    print()
    print("=== C. drop 到提示框 ===")
    o, e, c = flowgen._bsk("upload", "--file", IMG, "--session", f.sid,
                           "--selector", '[contenteditable=true]',
                           "--mode", "drop", "--timeout", "90s", timeout=180)
    print("  输出：", ((o or "") + (e or "")).strip()[:300], " 退出码", c)
    time.sleep(5)
    print("  之后：", json.dumps(f._run(STATE), ensure_ascii=False)[:300])
finally:
    print("\n（会话留着：", f.sid, "）")
