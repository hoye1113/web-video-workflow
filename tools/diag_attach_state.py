"""诊断：挂完角色之后，页面上到底有几个输入框、面板关没关。

（批次 C 的第一次试跑卡在这：提示框附近读到的是面板的 cancel/close，不是 chip。）
"""
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

PROJECT = "https://flow.google.com/project/2423a8a2-2219-4dd5-83ea-563fd00a79fb"
SHOT = ROOT / "experiments" / "uitest" / "flow" / "after-attach.png"

JS_EDITABLES = r"""
(()=>{const out=[];
[...document.querySelectorAll('[contenteditable=true]')].forEach((e,i)=>{
  const r=e.getBoundingClientRect();
  out.push({i:i, x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height),
            vis:r.width>0&&r.height>0, text:(e.innerText||'').slice(0,60)});
});
return out;})()
"""

f = flowgen.Flow(log=lambda *a: print("   ", *a, flush=True))
try:
    f.enter(PROJECT)
    print("=== 挂角色前 ===")
    print("  输入框：", json.dumps(f._run(JS_EDITABLES), ensure_ascii=False))
    f.attach_character("小树")
    time.sleep(2)
    print("\n=== 挂角色后 ===")
    print("  输入框：", json.dumps(f._run(JS_EDITABLES), ensure_ascii=False))
    print("  提示框附近：", repr(f.prompt_area()))
    print("  页面尾：", repr(f._run("(document.body.innerText||'').replace(/\\n+/g,' | ').slice(-300)")))
    flowgen._bsk("screenshot", "--session", f.sid, "--out", str(SHOT), timeout=180)
    print("\n  截图：", SHOT.relative_to(ROOT))
    print("\n（会话留着：", f.sid, "）")
    f.sid_keep = f.sid
    f.sid = None          # 别关，留着下一轮继续看
finally:
    if f.sid:
        f.close()
