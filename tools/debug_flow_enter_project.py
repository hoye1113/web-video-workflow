"""进用户的项目（Oct 16 - 16:43），确认里面能看到 girl.jpg / boy.jpg。"""
import json
import pathlib
import re
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

TARGET = "Oct 16 - 16:43"

f = flowgen.Flow()
try:
    out, err, _ = flowgen._bsk("session", "start", json_out=True, timeout=180)
    f.sid = json.loads(out).get("session_id")
    flowgen._bsk("window", "resize", "--session", f.sid, "--width", "1600", "--height", "900", timeout=60)
    flowgen._bsk("navigate", "https://flow.google.com", "--session", f.sid, timeout=180)
    time.sleep(6)
    print("会话:", f.sid)

    # 找那张卡片的结构
    html = f._run(
        "(()=>{const all=[...document.querySelectorAll('*')];"
        f"const hit=all.filter(e=>/^{TARGET}$/.test((e.textContent||'').trim()));"
        "if(!hit.length) return 'not found';"
        "let e=hit[hit.length-1]; let p=e; for(let i=0;i<4&&p;i++){ if(p.onclick||p.getAttribute('role')==='button'||p.tagName==='A'||p.tagName==='BUTTON') break; p=p.parentElement; }"
        "return {self:e.tagName+'.'+(e.className||'').toString().slice(0,60), parent:p?p.tagName+'.'+(p.className||'').toString().slice(0,60)+' role='+p.getAttribute('role'):'none'};})()")
    print("卡片结构：", json.dumps(html, ensure_ascii=False)[:400])

    # 用 bsk 点它（按 CSS 选择器 / 或者用它的文字找）
    # 不用文字选择器：直接遍历，找到含这段文字的**可点祖先**并交给 bsk 点不到 —— 所以用 JS 触发真实点击不可靠；
    # 这里改用：把该元素滚动到视野里，然后用 bsk 的 selector 点它的父卡片
    sel = f._run(
        "(()=>{const all=[...document.querySelectorAll('*')];"
        f"const hit=all.filter(e=>/^{TARGET}$/.test((e.textContent||'').trim()));"
        "if(!hit.length)return null; let p=hit[hit.length-1];"
        "for(let i=0;i<5&&p;i++){ if(p.tagName==='A'||p.getAttribute('role')==='button'||p.tagName==='BUTTON'||p.classList.contains('card')) break; p=p.parentElement; }"
        "if(!p)return null; p.setAttribute('data-vf','1'); return 'ok';})()")
    print("标记卡片：", sel)
    o, e, c = flowgen._bsk("click", "--session", f.sid, "--selector", "[data-vf='1']", timeout=180)
    print("点击：", ((o or "") + (e or "")).strip()[:200] or "(ok)")

    time.sleep(6)
    print("\n=== 进去之后的标题/文字 ===")
    print(f._run("(document.body.innerText||'').replace(/\\n+/g,' | ').slice(0,300)"))
    print("\n地址：", f._run("location.href"))

    # 打开 ingredients 素材面板，看有没有 girl.jpg
    out3, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "16000", timeout=300)
    m = re.search(r'@(e\d+)\s+button\s+"Add ingredients', out3 or "")
    if m:
        flowgen._bsk("click", "@" + m.group(1), "--session", f.sid, timeout=120)
        time.sleep(4)
        print("\n=== 素材面板里有什么 ===")
        print(f._run("(()=>{const vis=(e)=>e.offsetParent!==null;"
                     "const t=[...document.querySelectorAll('*')].filter(vis)"
                     ".map(e=>(e.textContent||'').trim()).filter(x=>/girl|boy|\\.jpg/i.test(x) && x.length<40);"
                     "return [...new Set(t)].slice(0,10);})()"))
        print("面板按钮：", f._run("(()=>{const vis=(e)=>e.offsetParent!==null;"
                                  "return [...document.querySelectorAll('button')].filter(vis)"
                                  ".map(b=>(b.textContent||'').trim().slice(0,22)).filter(x=>x).slice(0,14);})()"))
finally:
    print("\n会话留着:", f.sid)
