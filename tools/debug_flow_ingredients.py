"""探路：Flow 的「Add ingredients to the prompt」点下去会发生什么。

要弄清楚：是不是文件选择器（input[type=file]）、还是素材库弹窗、还是拖放区。
定了这个，才能把"挂参考图"写进 flowgen。
"""
import base64
import json
import pathlib
import re
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

DUMP = (
    "(()=>{const q=(s)=>[...document.querySelectorAll(s)];"
    "const btn=(b)=>((b.getAttribute('aria-label')||'')+' '+((b.textContent||'').trim().slice(0,24))).trim();"
    "return {inputs:q('input').map(i=>i.type+(i.accept?(' accept='+i.accept):'')),"
    " fileInputs:q('input[type=file]').length,"
    " dialogs:q('[role=dialog],[role=menu],[role=listbox]').length,"
    " dropzones:q('[class*=drop],[data-dropzone]').length,"
    " hiddenNote:(document.querySelector('[role=dialog]')||document.body).innerText.slice(0,600),"
    " buttons:q('button').map(btn).slice(0,26)};})()"
)


def show(t, v):
    print(f"--- {t} ---")
    print(json.dumps(v, ensure_ascii=False, indent=1)[:1400] if isinstance(v, (dict, list)) else v)


f = flowgen.Flow()
try:
    f.open()
    show("进入项目后的按钮", f._run(DUMP))
    print()

    # 用 bsk 的真实点击（JS .click() 在这个 UI 上不触发 React，之前踩过）
    out, err, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "8000", timeout=180)
    m = re.search(r'@(e\d+)\s+button\s+"([^"]*ingredient[^"]*)"', out or "", re.I)
    print("observe 里找 ingredients 按钮：", m.group(0) if m else "没找到")
    if not m:
        cand = re.findall(r'@e\d+\s+button\s+"[^"]{0,40}"', out or "")[:24]
        print("候选按钮：", cand)
    else:
        ref = "@" + m.group(1)
        o2, e2, c2 = flowgen._bsk("click", ref, "--session", f.sid, timeout=120)
        print("点击结果：", (o2 or e2 or "").strip()[:160])
        time.sleep(3)
        show("点完之后", f._run(DUMP))
finally:
    print()
    print("（会话留着，方便下一步接着看）")
