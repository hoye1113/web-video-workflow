"""找项目的链接/URL —— 能直接导航进去最稳（不依赖点击）。"""
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
    out, err, _ = flowgen._bsk("session", "start", json_out=True, timeout=180)
    f.sid = json.loads(out).get("session_id")
    flowgen._bsk("window", "resize", "--session", f.sid, "--width", "1600", "--height", "900", timeout=60)
    flowgen._bsk("navigate", "https://flow.google.com", "--session", f.sid, timeout=180)
    time.sleep(6)
    print("会话:", f.sid)

    print("=== 页面上所有链接 ===")
    print(json.dumps(f._run(
        "(()=>[...document.querySelectorAll('a')].map(a=>({h:a.getAttribute('href'),t:(a.textContent||'').trim().slice(0,24)}))"
        ".filter(x=>x.h).slice(0,25))()"), ensure_ascii=False)[:900])

    print("\n=== 含日期的元素：标签 / role / 类名 ===")
    info = f._run(
        "(()=>{const all=[...document.querySelectorAll('*')];"
        "const hit=all.filter(e=>/Oct 16 - 16:43/.test(e.textContent||'') && e.querySelectorAll('*').length<4);"
        "return hit.slice(0,3).map(e=>({tag:e.tagName, cls:(e.className||'').toString().slice(0,70),"
        " role:e.getAttribute('role')||'', d:e.getAttribute('data-id')||''}));})()")
    print(json.dumps(info, ensure_ascii=False, indent=1)[:900])

    print("\n=== 试着点：把含日期的元素标一下，用 bsk 点它的祖先 ===")
    f._run("(()=>{const all=[...document.querySelectorAll('*')];"
           "const hit=all.filter(e=>/Oct 16 - 16:43/.test(e.textContent||''));"
           "if(!hit.length)return 'none';let p=hit[0];"
           "for(let i=0;i<8&&p;i++){p.setAttribute('data-vf'+(i===0?'':'x'),'1');p=p.parentElement;}"
           "return 'marked';})()")
    o, e, c = flowgen._bsk("click", "--session", f.sid, "--selector", "[data-vfx='1']", timeout=180)
    print("  点外层容器：", ((o or "") + (e or "")).strip()[:160] or "(ok)")
    time.sleep(6)
    print("  地址：", f._run("location.href"))
    print("  文字：", f._run("(document.body.innerText||'').replace(/\\n+/g,' | ').slice(0,200)"))
finally:
    print("\n会话留着:", f.sid)
