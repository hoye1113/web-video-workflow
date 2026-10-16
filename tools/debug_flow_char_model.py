"""核实：Flow 的 Characters 面板是"生图"还是"生视频"。

用户的问题：如果角色是给视频生成用的（Veo 要花积分），那对我们没用 ——
我们只要生图（Nano Banana 不生视频、不花积分）。

做法：进 Characters 面板，把"模型/家族"下拉打开，看里面列的是什么。
"""
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
    f.open()
    out, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "14000", timeout=300)
    m = re.search(r'@(e\d+)\s+button\s+"Characters"', out or "")
    flowgen._bsk("click", "@" + m.group(1), "--session", f.sid, timeout=120)
    time.sleep(3)

    print("=== Characters 面板上的模型/格式入口 ===")
    out2, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "14000", timeout=300)
    for line in (out2 or "").splitlines():
        if re.search(r"model|family|banana|veo|video|image|crop|format|arrow_forward|Start", line, re.I):
            print("  " + line.strip()[:130])

    # 打开模型家族下拉，看选项
    m2 = re.search(r'@(e\d+)\s+button\s+"Select model family', out2 or "")
    if not m2:
        m2 = re.search(r'@(e\d+)\s+button\s+"[^"]*(model|family)[^"]*"', out2 or "", re.I)
    print("\n模型下拉 ref：", "@" + m2.group(1) if m2 else "没找到")
    if m2:
        flowgen._bsk("click", "@" + m2.group(1), "--session", f.sid, timeout=120)
        time.sleep(2)
        opts = f._run("(()=>{const vis=(e)=>e.offsetParent!==null;"
                      "const t=[...document.querySelectorAll('[role=menuitem],[role=option],[role=menuitemradio],li,div')]"
                      ".filter(vis).map(e=>(e.textContent||'').trim()).filter(x=>x && x.length<60);"
                      "return [...new Set(t)].slice(0,30);})()")
        print("=== 下拉里有什么 ===")
        print(json.dumps(opts, ensure_ascii=False, indent=1)[:1200])
finally:
    print("\n会话:", f.sid)
