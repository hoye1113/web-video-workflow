"""探路二：ingredients 的二级菜单里有什么（有没有"上传"）。
"""
import json
import pathlib
import re
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

MENU = (
    "(()=>{const vis=(e)=>e.offsetParent!==null;"
    "const items=[...document.querySelectorAll('[role=menuitem],[role=menuitemradio],[role=option],li')]"
    ".filter(vis).map(e=>((e.getAttribute('aria-label')||'')+' | '+(e.textContent||'').trim().slice(0,40)).trim())"
    ".filter(x=>x.replace(/[|\\s]/g,'').length>0);"
    "const files=[...document.querySelectorAll('input[type=file]')].map(i=>({accept:i.accept,multiple:i.multiple,hidden:!i.offsetParent}));"
    "const dlg=[...document.querySelectorAll('[role=dialog],[role=menu]')].filter(vis).map(e=>(e.innerText||'').slice(0,300));"
    "return {items:[...new Set(items)].slice(0,30), files, dlg};})()"
)

f = flowgen.Flow()
try:
    f.open()
    out, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "8000", timeout=180)
    m = re.search(r'@(e\d+)\s+button\s+"([^"]*ingredient[^"]*)"', out or "", re.I)
    if not m:
        print("没找到 ingredients 按钮"); sys.exit(1)
    ref = "@" + m.group(1)
    print("点：", m.group(2)[:50])
    flowgen._bsk("click", ref, "--session", f.sid, timeout=120)
    time.sleep(3)
    print(json.dumps(f._run(MENU), ensure_ascii=False, indent=1)[:1600])

    # 菜单里如果有"上传"，点它，再看有没有文件输入
    r = f._run("(()=>{const e=[...document.querySelectorAll('[role=menuitem],li,button')]"
               ".find(x=>/upload|上传|device|媒体|media|photo|图片/i.test((x.textContent||'')));"
               "if(!e)return 'no upload item';e.scrollIntoView();return {text:(e.textContent||'').trim().slice(0,40),"
               "aria:e.getAttribute('aria-label')||'',tag:e.tagName};})()")
    print("菜单里像上传的项：", json.dumps(r, ensure_ascii=False)[:300])
finally:
    print("（会话留着）")
