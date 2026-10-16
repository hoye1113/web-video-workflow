"""探 Flow 的 Characters（角色）功能 —— 它自带的"跨图形象一致"。

期望：能上传一张参考图建一个角色，之后生成时点名这个角色。
这一步顺便确认：上传文件到底是"文件输入"（受 Chrome 权限限制）还是别的机制。
"""
import json
import pathlib
import re
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

PANEL = (
    "(()=>{const vis=(e)=>e.offsetParent!==null;"
    "const btns=[...document.querySelectorAll('button')].filter(vis)"
    ".map(b=>((b.getAttribute('aria-label')||'')+' | '+(b.textContent||'').trim().slice(0,30)).trim());"
    "const files=[...document.querySelectorAll('input[type=file]')].map(i=>({accept:i.accept,hidden:!i.offsetParent}));"
    "return {buttons:[...new Set(btns)].slice(0,26), files,"
    " text:(document.body.innerText||'').replace(/\\n+/g,' | ').slice(-500)};})()"
)

f = flowgen.Flow()
try:
    f.open()
    out, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "14000", timeout=300)
    m = re.search(r'@(e\d+)\s+button\s+"Characters"', out or "")
    print("Characters 按钮 ref：", "@" + m.group(1) if m else "没找到")
    if not m:
        print(out[:800]); raise SystemExit(1)
    flowgen._bsk("click", "@" + m.group(1), "--session", f.sid, timeout=120)
    time.sleep(3)
    print("\n=== 点开 Characters 之后 ===")
    print(json.dumps(f._run(PANEL), ensure_ascii=False, indent=1)[:1500])
    out2, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "14000", timeout=300)
    print("\n=== observe：跟角色有关的元素 ===")
    for line in (out2 or "").splitlines():
        if re.search(r"charact|角色|new|create|add|upload|photo|image", line, re.I):
            print("  " + line.strip()[:130])
finally:
    print("\n会话:", f.sid)
