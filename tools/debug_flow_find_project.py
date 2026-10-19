"""建"项目标题 → 项目 URL"对照表，并直接进入用户那个（Oct 16 - 16:43），确认素材在里面。"""
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

    table = f._run(
        "(()=>{const out=[];for(const a of document.querySelectorAll('a[href^=\"/project/\"]')){"
        "let p=a, txt='';for(let i=0;i<4&&p;i++){p=p.parentElement;if(p&&/Oct|Sep|Aug/.test(p.textContent||'')){txt=(p.textContent||'').trim().slice(0,40);break;}}"
        "out.push({href:a.getAttribute('href'), near:txt});}return out.slice(0,16);})()")
    print("=== 项目链接 → 标题 ===")
    for row in (table or []):
        print("  %-46s %s" % (row.get("href"), row.get("near")))

    target = next((r for r in (table or []) if "16:43" in (r.get("near") or "")), None)
    print("\n目标项目：", json.dumps(target, ensure_ascii=False))
    if target:
        flowgen._bsk("navigate", "https://flow.google.com" + target["href"], "--session", f.sid, timeout=180)
        time.sleep(7)
        print("地址：", f._run("location.href"))
        print("标题区文字：", f._run("(document.querySelector('header,[role=banner]')||document.body).innerText.replace(/\\n+/g,' | ').slice(0,160)"))
        # 打开素材面板看有没有 girl.jpg
        out3, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "16000", timeout=300)
        m = re.search(r'@(e\d+)\s+button\s+"Add ingredients', out3 or "")
        print("ingredients ref:", "@" + m.group(1) if m else "没找到")
        if m:
            flowgen._bsk("click", "@" + m.group(1), "--session", f.sid, timeout=120)
            time.sleep(5)
            assets = f._run(
                "(()=>{const vis=(e)=>e.offsetParent!==null;"
                "const t=[...document.querySelectorAll('*')].filter(vis).map(e=>(e.textContent||'').trim())"
                ".filter(x=>/girl|boy|\\.jpg/i.test(x)&&x.length<40);"
                "return [...new Set(t)].slice(0,10);})()")
            print("面板里的素材：", json.dumps(assets, ensure_ascii=False))
            print("面板按钮：", json.dumps(f._run(
                "(()=>{const vis=(e)=>e.offsetParent!==null;"
                "return [...document.querySelectorAll('button')].filter(vis).map(b=>(b.textContent||'').trim().slice(0,22)).filter(x=>x).slice(0,16);})()"),
                ensure_ascii=False))
finally:
    print("\n会话留着:", f.sid)
