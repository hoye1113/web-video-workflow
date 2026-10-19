"""带验证的完整流程（每一步都读回状态，生成前截图）。

要验三件事：
  ① 已知集合取全了吗（素材网格懒加载 → 会把老图当新图）
  ② 参考图挂上的**是哪个**（小树 还是 小芽 还是别的）
  ③ 提示词进没进输入框（读回文本）
"""
import json
import pathlib
import re
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

PROJECT = "https://flow.google.com/project/2423a8a2-2219-4dd5-83ea-563fd00a79fb"
CHAR = "小树"
PROMPT = "画同一个女孩的近景半身头像：忍住不哭的表情（眼睛含着、嘴唇抿住、眉微皱），纯白底、无道具、无文字、无边框。"
SHOT = ROOT / "experiments" / "uitest" / "flow" / "before-generate.png"

f = flowgen.Flow()
try:
    out, _, _ = flowgen._bsk("session", "start", json_out=True, timeout=180)
    f.sid = json.loads(out).get("session_id")
    flowgen._bsk("window", "resize", "--session", f.sid, "--width", "1600", "--height", "900", timeout=60)
    flowgen._bsk("navigate", PROJECT, "--session", f.sid, timeout=180)
    time.sleep(8)
    print("会话:", f.sid)

    # ① 把素材网格滚一遍，取全"已知集合"
    print("\n=== ① 取全已知集合 ===")
    for i in range(6):
        f._run(f"window.scrollTo(0, {i * 900})")
        time.sleep(1.2)
    f._run("window.scrollTo(0, 0)")
    time.sleep(1)
    known = f._image_urls()
    print(f"  已知图片 {len(known)} 张")

    # ② 打开素材面板，挂角色
    out, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "16000", timeout=300)
    m = re.search(r'@(e\d+)\s+button\s+"Add ingredients', out or "")
    flowgen._bsk("click", "@" + m.group(1), "--session", f.sid, timeout=120)
    time.sleep(4)
    print("\n=== ② 素材面板：全部条目（名字|类型） ===")
    print(f._run("(document.body.innerText||'').replace(/\\n+/g,' | ').slice(-900)"))

    # 点 小树
    pick = f._run(
        "(()=>{const all=[...document.querySelectorAll('*')];"
        "const hit=all.filter(e=>(e.textContent||'').trim()==='" + CHAR + "'&&e.children.length<=2);"
        "if(!hit.length)return 'not found';let el=hit[0];"
        "for(let i=0;i<6&&el;i++){if((el.className||'').toString().includes('asset-item'))break;el=el.parentElement;}"
        "if(!el)return 'no asset-item';el.setAttribute('data-pick','1');"
        "return (el.textContent||'').trim().slice(0,40);})()")
    print(f"\n  点中的条目：{pick!r}")
    if pick not in ("not found", "no asset-item"):
        flowgen._bsk("click", "--session", f.sid, "--selector", "[data-pick='1']", timeout=180)
        time.sleep(3)

    add = f._run("(()=>{const b=[...document.querySelectorAll('button')].find(x=>/add to prompt/i.test(x.textContent||''));"
                 "if(!b)return false;b.setAttribute('data-add','1');return {disabled:!!b.disabled};})()")
    print("  Add to prompt：", json.dumps(add, ensure_ascii=False))
    if add:
        flowgen._bsk("click", "--session", f.sid, "--selector", "[data-add='1']", timeout=180)
        time.sleep(4)

    # 挂上之后：看提示词框附近有什么（参考图会以 chip 出现在框上方）
    print("\n  挂后页面尾：", f._run("(document.body.innerText||'').replace(/\\n+/g,' | ').slice(-200)"))

    # ③ 输提示词并读回
    t = f._type_prompt(PROMPT)
    print("\n=== ③ 提示词 ===")
    print("  写入：", json.dumps(t, ensure_ascii=False)[:200])
    time.sleep(1)
    back = f._run("(()=>{const vis=(e)=>e.offsetParent!==null;"
                  "const e=[...document.querySelectorAll('[contenteditable=true]')].filter(vis).pop();"
                  "return e?(e.textContent||'').trim().slice(0,120):'(找不到输入框)';})()")
    print("  读回：", repr(back))
    print("  一致：", PROMPT[:30] in (back or ""))

    flowgen._bsk("screenshot", "--session", f.sid, "--out", str(SHOT), timeout=180)
    print("\n  截图：", SHOT.relative_to(ROOT))
    print("\n（这一轮**不生成** —— 先看截图确认设置对了，再点生成）")
finally:
    print("\n会话:", f.sid)
