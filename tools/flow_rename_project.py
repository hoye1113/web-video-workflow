"""把这个项目改名（后面就用它当固定项目）。"""
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

PROJECT = "https://flow.google.com/project/2423a8a2-2219-4dd5-83ea-563fd00a79fb"
NEW = "video-factory"

f = flowgen.Flow()
try:
    out, _, _ = flowgen._bsk("session", "start", json_out=True, timeout=180)
    f.sid = json.loads(out).get("session_id")
    flowgen._bsk("window", "resize", "--session", f.sid, "--width", "1600", "--height", "900", timeout=60)
    flowgen._bsk("navigate", PROJECT, "--session", f.sid, timeout=180)
    time.sleep(7)
    print("会话:", f.sid, " 地址:", f._run("location.href"))

    # 标题元素长什么样
    info = f._run("(()=>{const es=[...document.querySelectorAll('[contenteditable=true],input,textarea')];"
                  "for(const e of es){const v=(e.value!==undefined?e.value:e.textContent||'').trim();"
                  "if(/Oct 16/.test(v))return {tag:e.tagName,ce:e.getAttribute('contenteditable'),val:v.slice(0,30),"
                  "cls:(e.className||'').toString().slice(0,60)};}return 'not found';})()")
    print("标题元素：", json.dumps(info, ensure_ascii=False))

    out2, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "16000", timeout=300)
    mt = re.search(r'@(e\d+)\s+textbox\s+"[^"]*" *="Oct 16', out2 or "") or \
         re.search(r'@(e\d+)\s+textbox\s+"Editable text"', out2 or "")
    print("标题 ref:", "@" + mt.group(1) if mt else "没找到")

    if mt:
        o, e, c = flowgen._bsk("fill", "@" + mt.group(1), NEW, "--session", f.sid, timeout=120)
        print("fill:", ((o or "") + (e or "")).strip()[:200] or "(ok)")
        flowgen._bsk("press", "Enter", "--session", f.sid, timeout=60)
        time.sleep(4)
        # 如果 fill 不生效（React contenteditable），退回 execCommand
        cur = f._run("(()=>{const es=[...document.querySelectorAll('[contenteditable=true],input')];"
                     "for(const e of es){const v=(e.value!==undefined?e.value:e.textContent||'').trim();"
                     "if(v&&!/Oct 16/.test(v))return v.slice(0,40);}return '';})()")
        print("改后（fill 的结果）：", repr(cur))
        if not cur:
            print("→ fill 没生效，用 execCommand 再试")
            js = ("(()=>{const es=[...document.querySelectorAll('[contenteditable=true],input')];"
                  "for(const e of es){const v=(e.value!==undefined?e.value:e.textContent||'').trim();"
                  "if(/Oct 16/.test(v)){e.focus();"
                  "if(e.tagName==='INPUT'){e.value='" + NEW + "';}"
                  "else{document.execCommand('selectAll',false,null);document.execCommand('insertText',false,'" + NEW + "');}"
                  "return 'typed';}}return 'no target';})()")
            print("  ", f._run(js))
            flowgen._bsk("press", "Enter", "--session", f.sid, timeout=60)
            time.sleep(4)
            print("  再查：", f._run("(document.querySelector('header,[role=banner]')||document.body).innerText.replace(/\\n+/g,' | ').slice(0,80)"))
    print("\n最终标题区：", f._run("(document.querySelector('header,[role=banner]')||document.body).innerText.replace(/\\n+/g,' | ').slice(0,90)"))
finally:
    print("会话留着:", f.sid)
