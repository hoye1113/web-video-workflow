"""验证：把 girl.jpg 挂进提示词（从项目素材库选），并**截图确认**它真的挂上了。

判据（三选一，越多越好）：
  ① 提示框附近出现一个小缩略图（chip）
  ② 页面文字里出现文件名
  ③ 截图肉眼确认
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
SHOT = ROOT / "experiments" / "uitest" / "flow" / "attach-check.png"


def dump(f, tag):
    v = f._run(
        "(()=>{const vis=(e)=>e.offsetParent!==null;"
        "const imgs=[...document.querySelectorAll('img')].filter(vis)"
        ".filter(i=>i.naturalWidth>30&&i.naturalWidth<500)"
        ".map(i=>i.naturalWidth+'x'+i.naturalHeight);"
        "const t=(document.body.innerText||'').replace(/\\n+/g,' | ');"
        "const eds=[...document.querySelectorAll('[contenteditable=true]')].filter(vis);"
        "return {小图:imgs.slice(0,10), 提示框数:eds.length,"
        " 有文件名:/girl\\.jpg/.test(t), 文字尾:t.slice(-260)};})()")
    print(f"--- {tag} ---")
    print(json.dumps(v, ensure_ascii=False, indent=1)[:900])
    return v


f = flowgen.Flow()
try:
    out, _, _ = flowgen._bsk("session", "start", json_out=True, timeout=180)
    f.sid = json.loads(out).get("session_id")
    flowgen._bsk("window", "resize", "--session", f.sid, "--width", "1600", "--height", "900", timeout=60)
    flowgen._bsk("navigate", PROJECT, "--session", f.sid, timeout=180)
    time.sleep(8)
    print("会话:", f.sid)
    dump(f, "进项目")

    out, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "16000", timeout=300)
    m = re.search(r'@(e\d+)\s+button\s+"Add ingredients', out or "")
    print("ingredients:", "@" + m.group(1) if m else "没找到")
    flowgen._bsk("click", "@" + m.group(1), "--session", f.sid, timeout=120)
    time.sleep(4)
    dump(f, "打开素材面板")

    # 选中 girl.jpg（点素材块）
    marked = f._run(
        "(()=>{const all=[...document.querySelectorAll('*')];"
        "const hit=all.filter(e=>/girl\\.jpg/.test(e.textContent||'')&&e.children.length<=3);"
        "if(!hit.length)return 'not found';let el=hit[0];"
        "for(let i=0;i<5&&el;i++){if(el.classList.contains('FLOW-IMAGE-TILE')||el.tagName==='LI'||el.getAttribute('role')==='option')break;el=el.parentElement;}"
        "(el||hit[0]).setAttribute('data-pick','1');return el?el.className:'fallback';})()")
    print("素材块：", marked)
    o, e, c = flowgen._bsk("click", "--session", f.sid, "--selector", "[data-pick='1']", timeout=180)
    print("点击素材：", ((o or "") + (e or "")).strip()[:120] or "(ok)")
    time.sleep(3)
    dump(f, "选中之后")

    # 找 "Add to prompt"（可能刚出现）
    found = f._run(
        "(()=>{const bs=[...document.querySelectorAll('button')];"
        "const b=bs.find(x=>/add to prompt/i.test(x.textContent||''));"
        "if(!b)return {found:false, 附近按钮:bs.map(x=>(x.textContent||'').trim().slice(0,20)).filter(x=>x).slice(0,18)};"
        "b.setAttribute('data-add','1');return {found:true, disabled:!!b.disabled};})()")
    print("Add to prompt：", json.dumps(found, ensure_ascii=False)[:400])
    if found.get("found"):
        flowgen._bsk("click", "--session", f.sid, "--selector", "[data-add='1']", timeout=180)
        time.sleep(4)
        dump(f, "Add to prompt 之后")

    SHOT.parent.mkdir(parents=True, exist_ok=True)
    flowgen._bsk("screenshot", "--session", f.sid, "--out", str(SHOT), timeout=180)
    print("截图：", SHOT.relative_to(ROOT))
finally:
    print("会话:", f.sid)
