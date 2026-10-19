"""列出 Flow 里已有的项目，找到用户传了 girl.jpg/boy.jpg 的那个。"""
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
    # 只开会话 + 打开首页，别进新项目
    out, err, _ = flowgen._bsk("session", "start", json_out=True, timeout=180)
    f.sid = json.loads(out).get("session_id")
    print("会话:", f.sid)
    flowgen._bsk("window", "resize", "--session", f.sid, "--width", "1600", "--height", "900", timeout=60)
    flowgen._bsk("navigate", "https://flow.google.com", "--session", f.sid, timeout=180)
    time.sleep(6)

    print("\n=== 首页文字（找项目列表 / Recent） ===")
    print(f._run("(document.body.innerText||'').replace(/\\n+/g,' | ').slice(0,900)"))

    print("\n=== 项目选择器：点开看选项 ===")
    out2, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "16000", timeout=300)
    m = re.search(r'@(e\d+)\s+combobox\s+"Select project', out2 or "")
    print("Select project ref:", "@" + m.group(1) if m else "没找到")
    if m:
        flowgen._bsk("click", "@" + m.group(1), "--session", f.sid, timeout=120)
        time.sleep(3)
        items = f._run(
            "(()=>{const vis=(e)=>e.offsetParent!==null;"
            "const t=[...document.querySelectorAll('[role=option],[role=menuitem],li,div')].filter(vis)"
            ".map(e=>(e.textContent||'').trim()).filter(x=>x && x.length<40 && /Oct|月|项目|project/i.test(x));"
            "return [...new Set(t)].slice(0,20);})()")
        print("项目选项：", json.dumps(items, ensure_ascii=False)[:600])

    print("\n=== 首页上的项目卡片（链接/按钮） ===")
    cards = f._run(
        "(()=>{const vis=(e)=>e.offsetParent!==null;"
        "return [...document.querySelectorAll('a,button,[role=button],[role=link]')].filter(vis)"
        ".map(e=>((e.getAttribute('aria-label')||'')+'|'+(e.textContent||'').trim().slice(0,40)).trim())"
        ".filter(x=>/Oct|项目|untitled|more_vert/i.test(x)).slice(0,20);})()")
    print(json.dumps(cards, ensure_ascii=False)[:700])
finally:
    print("\n会话留着:", f.sid)
