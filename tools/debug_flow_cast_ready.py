"""看看用户在 Flow Characters 里建好的两个角色（清单 + 能不能点名用）。"""
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
    m = re.search(r'@(e\d+)\s+button\s+"Characters"', out or "")
    print("Characters ref:", "@" + m.group(1) if m else "没找到")
    flowgen._bsk("click", "@" + m.group(1), "--session", f.sid, timeout=120)
    time.sleep(4)

    st = f._run(
        "(()=>{const vis=(e)=>e.offsetParent!==null;"
        "const imgs=[...document.querySelectorAll('img')].filter(vis).filter(i=>i.naturalWidth>40);"
        "const btns=[...document.querySelectorAll('button')].filter(vis)"
        ".map(b=>((b.getAttribute('aria-label')||'')+'|'+(b.textContent||'').trim().slice(0,28)).trim());"
        "return {thumbs:imgs.map(i=>i.naturalWidth+'x'+i.naturalHeight+' '+i.src.slice(0,40)).slice(0,10),"
        " buttons:[...new Set(btns)].slice(0,30),"
        " text:(document.body.innerText||'').replace(/\\n+/g,' | ').slice(0,700)};})()")
    print("=== Characters 面板 ===")
    print(json.dumps(st, ensure_ascii=False, indent=1)[:2000])

    out2, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "16000", timeout=300)
    print("\n=== observe：角色相关的元素 ===")
    for line in (out2 or "").splitlines():
        if re.search(r"charact|角色|image|Delete|Edit|Use|\"", line) and len(line.strip()) < 150:
            if re.search(r"charact|Delete|Edit|Use|Select|New", line, re.I):
                print("  " + line.strip()[:130])
finally:
    print("\n会话:", f.sid)
