"""实跑一次生成，把每一步的状态都打出来（哪里卡住一目了然）。

用法：python experiments/diag_gen_run.py
"""
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
sys.path.insert(0, str(ROOT / "tools"))

import flowgen                                          # noqa: E402
from gen_scenes import full_prompt                      # noqa: E402

SHOT = ROOT / "experiments" / "uitest" / "flow" / "diag-genrun.png"
PROJECT = "https://flow.google.com/project/2423a8a2-2219-4dd5-83ea-563fd00a79fb"
SCENE = "一个男孩坐在书桌前，一只手把一部手机反扣着推到桌子另一头，手指还搭在手机上；桌上只剩一盏台灯从侧面照着，其余很暗，主体占画面中部"

BTN_STATE = (
    "(()=>{const b=[...document.querySelectorAll('button')]"
    ".find(x=>/start generation|开始生成/i.test((x.getAttribute('aria-label')||x.textContent||'')));"
    "if(!b)return {found:false};"
    "const r=b.getBoundingClientRect();"
    "return {found:true,disabled:!!b.disabled,aria:b.getAttribute('aria-label')||'',"
    "x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)};})()"
)


def main():
    f = flowgen.Flow(log=lambda *a: print("   ", *a, flush=True))
    try:
        f.enter(PROJECT)
        print("== attach ==")
        f.attach_character("小树")
        print("== type ==")
        t = f._type_prompt(full_prompt(SCENE))
        print("typed:", json.dumps(t, ensure_ascii=False)[:200])
        print("btn after type:", f._run(BTN_STATE))

        # 若按钮还是 disabled：补一个 React 认的 input 事件
        st = f._run(BTN_STATE)
        if isinstance(st, dict) and st.get("disabled"):
            print("!! 按钮是 disabled —— 补 input 事件")
            fix = f._run(
                "(()=>{const els=[...document.querySelectorAll('[contenteditable=true]')];"
                "const el=els[els.length-1];if(!el)return 'no input';el.focus();"
                "el.dispatchEvent(new InputEvent('input',{bubbles:true,inputType:'insertText',data:'x'}));"
                "return 'fired';})()"
            )
            print("fix:", fix)
            time.sleep(2)
            print("btn after fix:", f._run(BTN_STATE))

        print("== click generate ==")
        c = f._click_generate()
        print("click:", json.dumps(c, ensure_ascii=False)[:300])

        base = len(f._image_bases())
        print("images now:", base)
        t0 = time.time()
        while time.time() - t0 < 240:
            time.sleep(10)
            n = len(f._image_bases())
            st = f._run(BTN_STATE)
            tail = f._run("(()=>{const t=document.body.innerText||'';return t.slice(-300);})()")
            print(f"  {int(time.time() - t0):>3}s imgs={n} btn={json.dumps(st, ensure_ascii=False)}")
            if n > base:
                print("  >>> 出了新图！")
                break
            if isinstance(tail, str) and tail.strip():
                print("  tail:", tail.replace("\n", " | ")[-260:])
        flowgen._bsk("screenshot", "--session", f.sid, "--out", str(SHOT), timeout=180)
        print("shot:", SHOT)
    finally:
        f.close()


if __name__ == "__main__":
    main()
