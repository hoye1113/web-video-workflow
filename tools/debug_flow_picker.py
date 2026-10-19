"""找到素材项和 "Add to prompt" 的 DOM，然后完整走一遍：
选 girl.jpg → Add to prompt → 验证提示框上出现了配料（缩略图）。
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
    flowgen._bsk("click", "@" + m.group(1), "--session", f.sid, timeout=120)
    time.sleep(3)

    print("=== 素材项的 DOM（含 girl 的元素） ===")
    html = f._run(
        "(()=>{const all=[...document.querySelectorAll('*')];"
        "const hit=all.filter(e=>/girl\\.jpg/.test(e.textContent||'') && e.querySelectorAll('*').length<6);"
        "const e=hit[hit.length-1];return e?e.outerHTML.slice(0,700):'not found';})()")
    print(html)
    print()
    print("=== Add to prompt 按钮的 DOM ===")
    print(f._run("(()=>{const b=[...document.querySelectorAll('button')].find(x=>/add to prompt/i.test(x.textContent||''));"
                 "return b?b.outerHTML.slice(0,300):'not found';})()"))
    print()
    print("=== 面板里的按钮（含 disabled 状态） ===")
    print(json.dumps(f._run(
        "(()=>{const vis=(e)=>e.offsetParent!==null;"
        "return [...document.querySelectorAll('button')].filter(vis)"
        ".map(b=>({t:(b.textContent||'').trim().slice(0,24), d:b.disabled,"
        " aria:(b.getAttribute('aria-label')||'').slice(0,30)})).slice(0,20);})()"),
        ensure_ascii=False, indent=1)[:1200])
finally:
    print("\n会话:", f.sid)
