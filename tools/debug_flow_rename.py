"""进入用户那个项目（Oct 16 - 16:43）→ 记下它的 URL → 改名为 video-factory。

改名后：以后所有生图都在这个项目里做（素材库里有 girl.jpg / boy.jpg）。
"""
import json
import pathlib
import re
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

NEW_NAME = "video-factory"
OLD = "16:43"

f = flowgen.Flow()
try:
    out, err, _ = flowgen._bsk("session", "start", json_out=True, timeout=180)
    f.sid = json.loads(out).get("session_id")
    flowgen._bsk("window", "resize", "--session", f.sid, "--width", "1600", "--height", "900", timeout=60)
    flowgen._bsk("navigate", "https://flow.google.com", "--session", f.sid, timeout=180)
    time.sleep(6)
    print("会话:", f.sid)

    # ① 打开顶栏的项目选择器（combobox "Select project"）
    out2, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "16000", timeout=300)
    m = re.search(r'@(e\d+)\s+combobox\s+"Select project', out2 or "")
    print("Select project ref:", "@" + m.group(1) if m else "没找到")
    if not m:
        raise SystemExit("找不到项目选择器")
    flowgen._bsk("click", "@" + m.group(1), "--session", f.sid, timeout=120)
    time.sleep(3)

    # ② 在新图层里点 "Oct 16 - 16:43"
    out3, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "16000", timeout=300)
    print("=== 选择器展开后 ===")
    target = None
    for line in (out3 or "").splitlines():
        s = line.strip()
        if re.search(r"Oct 16|option|menuitem", s) and len(s) < 140:
            print("  " + s)
            mm = re.search(r'@(e\d+).*' + OLD, s)
            if mm:
                target = "@" + mm.group(1)
    print("目标项 ref:", target)
    if target:
        flowgen._bsk("click", target, "--session", f.sid, timeout=120)
        time.sleep(6)
        print("地址：", f._run("location.href"))
        print("标题：", f._run("(document.querySelector('header,[role=banner]')||document.body).innerText.replace(/\\n+/g,' | ').slice(0,120)"))

    # ③ 改名：标题是个可编辑文本框
    out4, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "16000", timeout=300)
    mt = re.search(r'@(e\d+)\s+textbox\s+"Editable text"', out4 or "")
    print("标题文本框 ref:", "@" + mt.group(1) if mt else "没找到")
    if mt:
        # 先看它是 input 还是 contenteditable
        info = f._run("(()=>{const es=[...document.querySelectorAll('[contenteditable=true],input')];"
                      "const t=es.find(e=>(e.textContent||e.value||'').includes('Oct 16'));"
                      "return t?{tag:t.tagName, ce:t.getAttribute('contenteditable'), val:(t.textContent||t.value||'').slice(0,30)}:'not found';})()")
        print("标题元素：", json.dumps(info, ensure_ascii=False))
        o, e, c = flowgen._bsk("fill", target=mt and ("@" + mt.group(1)), value=None) if False else (None, None, None)
        # 用 bsk fill（它是 input 就成；contenteditable 可能失败 —— 那再退回 execCommand）
        o, e, c = flowgen._bsk("fill", "@" + mt.group(1), NEW_NAME, "--session", f.sid, timeout=120)
        print("fill：", ((o or "") + (e or "")).strip()[:160] or "(ok)")
        flowgen._bsk("press", "Enter", "--session", f.sid, timeout=60)
        time.sleep(3)
        print("改后标题：", f._run("(document.querySelector('header,[role=banner]')||document.body).innerText.replace(/\\n+/g,' | ').slice(0,80)"))
finally:
    print("\n会话留着:", f.sid)
