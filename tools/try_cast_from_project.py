"""从项目素材库里选 girl.jpg → Add to prompt → 生成女主背面。

三条已探明的路合并成一条：
  ① 直接进项目 URL（用户把参考图传在这儿的素材库里，不用本地文件权限）
  ② Add ingredients 的菜单开在新图层 → 重新 observe 拿 ref
  ③ 选素材 → Add to prompt
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
OUT = ROOT / "experiments" / "cast-views"
PROMPT = (
    "同一张设定图里的那个 Q 版女孩，画她的**背面全身**："
    "浅栗灰粉齐肩微卷短发、**头顶一片两叶嫩芽**、米白色超大号连帽卫衣（袖子长到手背）、下摆盖过胯、"
    "光腿、深棕色小短靴。人物居中、占画面高度约七成，纯白底、无背景、无道具、无文字。"
    "画风与设定图完全一致：Q 版三头身、大头、平涂 + 细线（深棕不纯黑）、低饱和浅色。"
)


def pick_asset(f, name):
    """在素材面板里选中某个素材 → Add to prompt。"""
    # 找出素材项（含文件名的可点祖先），打个标记
    marked = f._run(
        "(()=>{const all=[...document.querySelectorAll('*')];"
        "const hit=all.filter(e=>(e.textContent||'').trim().startsWith('" + name + "') && e.children.length<=3);"
        "if(!hit.length)return 'not found';"
        "let el=hit[0];for(let i=0;i<5&&el;i++){if(el.getAttribute('role')==='option'||el.tagName==='LI'||el.tagName==='BUTTON'||el.onclick)break;el=el.parentElement;}"
        "(el||hit[0]).setAttribute('data-vfasset','1');"
        "return (el||hit[0]).tagName+'.'+((el||hit[0]).className||'').toString().slice(0,50);})()")
    print("  素材项：", marked)
    if marked == "not found":
        return False
    o, e, c = flowgen._bsk("click", "--session", f.sid, "--selector", "[data-vfasset='1']", timeout=180)
    print("  点击：", ((o or "") + (e or "")).strip()[:120] or "(ok)")
    time.sleep(2)
    # Add to prompt
    o, e, c = flowgen._bsk("click", "--session", f.sid, "--selector",
                           "button:not([disabled])", timeout=30) if False else (None, None, None)
    added = f._run(
        "(()=>{const b=[...document.querySelectorAll('button')].find(x=>/add to prompt/i.test(x.textContent||'')&&!x.disabled);"
        "if(!b)return 'no add button';b.setAttribute('data-vfadd','1');return 'ok';})()")
    print("  Add to prompt：", added)
    if added == "ok":
        o, e, c = flowgen._bsk("click", "--session", f.sid, "--selector", "[data-vfadd='1']", timeout=180)
        print("  点击 add：", ((o or "") + (e or "")).strip()[:120] or "(ok)")
    time.sleep(3)
    return True


f = flowgen.Flow()
try:
    out, _, _ = flowgen._bsk("session", "start", json_out=True, timeout=180)
    f.sid = json.loads(out).get("session_id")
    flowgen._bsk("window", "resize", "--session", f.sid, "--width", "1600", "--height", "900", timeout=60)
    flowgen._bsk("navigate", PROJECT, "--session", f.sid, timeout=180)
    time.sleep(7)
    print("会话:", f.sid)

    out, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "16000", timeout=300)
    m = re.search(r'@(e\d+)\s+button\s+"Add ingredients', out or "")
    print("ingredients:", "@" + m.group(1) if m else "没找到")
    flowgen._bsk("click", "@" + m.group(1), "--session", f.sid, timeout=120)
    time.sleep(4)
    pick_asset(f, "girl.jpg")

    print("\n=== 挂上之后：提示框附近有什么 ===")
    print(f._run("(()=>{const vis=(e)=>e.offsetParent!==null;"
                 "const imgs=[...document.querySelectorAll('img')].filter(vis).filter(i=>i.naturalWidth>40&&i.naturalWidth<400);"
                 "return {小图:imgs.map(i=>i.naturalWidth+'x'+i.naturalHeight).slice(0,8),"
                 " text:(document.body.innerText||'').replace(/\\n+/g,' | ').slice(0,200)};})()"))

    print("\n=== 生成 ===")
    OUT.mkdir(parents=True, exist_ok=True)
    blobs = f.generate(PROMPT, timeout=300)
    for i, b in enumerate(blobs, 1):
        p = OUT / f"girl-back-{i}.png"
        p.write_bytes(b)
        print("  存:", p.relative_to(ROOT), f"({len(b)//1024} KB)")
finally:
    print("会话:", f.sid)
