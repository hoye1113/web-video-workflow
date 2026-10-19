"""用已建好的角色（小树）生成一张：Add ingredients → Characters 标签 → 选角色 → Add to prompt → 生成。

这是"量产角色视图"的关键一步：能自动化，后面 30 张就能批量出。
"""
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

PROJECT = "https://flow.google.com/project/2423a8a2-2219-4dd5-83ea-563fd00a79fb"
CHAR = sys.argv[1] if len(sys.argv) > 1 else "小树"
PROMPT = "同一角色的近景头像：**忍住不哭**的表情（眼睛含着、嘴唇抿住、眉微皱）；纯白底，无道具无文字。"
OUT = ROOT / "experiments" / "cast-views"

f = flowgen.Flow()
try:
    out, _, _ = flowgen._bsk("session", "start", json_out=True, timeout=180)
    f.sid = json.loads(out).get("session_id")
    flowgen._bsk("window", "resize", "--session", f.sid, "--width", "1600", "--height", "900", timeout=60)
    flowgen._bsk("navigate", PROJECT, "--session", f.sid, timeout=180)
    time.sleep(8)
    print("会话:", f.sid)

    out, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "16000", timeout=300)
    m = re.search(r'@(e\d+)\s+button\s+"Add ingredients', out or "")
    flowgen._bsk("click", "@" + m.group(1), "--session", f.sid, timeout=120)
    time.sleep(4)

    # 素材面板里切到 Characters 标签
    print("=== 面板里的标签 ===")
    print(f._run("(()=>{const vis=(e)=>e.offsetParent!==null;"
                 "return [...document.querySelectorAll('[role=tab],button')].filter(vis)"
                 ".map(e=>(e.textContent||'').trim().slice(0,20)).filter(x=>x).slice(0,18);})()"))
    tab = f._run("(()=>{const vis=(e)=>e.offsetParent!==null;"
                 "const t=[...document.querySelectorAll('[role=tab],button')].filter(vis)"
                 ".find(e=>/^Characters$/.test((e.textContent||'').trim()));"
                 "if(!t)return 'no tab';t.setAttribute('data-chartab','1');return 'ok';})()")
    print("Characters 标签：", tab)
    if tab == "ok":
        flowgen._bsk("click", "--session", f.sid, "--selector", "[data-chartab='1']", timeout=180)
        time.sleep(3)

    print("\n=== Characters 面板里的角色 ===")
    print(f._run("(document.body.innerText||'').replace(/\\n+/g,' | ').slice(0,400)"))

    # 点角色块
    pick = f._run("(()=>{const all=[...document.querySelectorAll('*')];"
                  "const hit=all.filter(e=>(e.textContent||'').trim()==='" + CHAR + "'&&e.children.length<=3);"
                  "if(!hit.length)return 'not found';"
                  "let el=hit[0];for(let i=0;i<5&&el;i++){"
                  "if(el.classList.contains('FLOW-IMAGE-TILE')||el.getAttribute('role')==='option'||el.tagName==='LI'||el.tagName==='BUTTON')break;"
                  "el=el.parentElement;}(el||hit[0]).setAttribute('data-char','1');"
                  "return (el||hit[0]).className.toString().slice(0,50);})()")
    print("角色块：", pick)
    if pick != "not found":
        flowgen._bsk("click", "--session", f.sid, "--selector", "[data-char='1']", timeout=180)
        time.sleep(3)

    add = f._run("(()=>{const b=[...document.querySelectorAll('button')].find(x=>/add to prompt/i.test(x.textContent||''));"
                 "if(!b)return false;b.setAttribute('data-add','1');return true;})()")
    print("Add to prompt 在：", add)
    if add:
        flowgen._bsk("click", "--session", f.sid, "--selector", "[data-add='1']", timeout=180)
        time.sleep(4)
        print("挂后提示框附近：", f._run(
            "(()=>{const vis=(e)=>e.offsetParent!==null;"
            "return [...document.querySelectorAll('img')].filter(vis).filter(i=>i.naturalWidth>20&&i.naturalWidth<300)"
            ".map(i=>i.naturalWidth+'x'+i.naturalHeight).slice(0,6);})()"))

    print("\n=== 生成 ===")
    OUT.mkdir(parents=True, exist_ok=True)
    blobs = f.generate(PROMPT, timeout=300)
    for i, b in enumerate(blobs, 1):
        p = OUT / f"{CHAR}-表情-忍-{i}.png"
        p.write_bytes(b)
        print("  存:", p.relative_to(ROOT), f"({len(b)//1024} KB)")
finally:
    print("会话:", f.sid)
