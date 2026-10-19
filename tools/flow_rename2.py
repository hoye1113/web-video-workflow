"""改名（正确姿势）：bsk fill --value … --ref @e3 然后 Enter，再刷新确认真的存住了。"""
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

PROJECT = "https://flow.google.com/project/2423a8a2-2219-4dd5-83ea-563fd00a79fb"
NEW = "video-factory"
SID = sys.argv[1] if len(sys.argv) > 1 else None


def bsk(*a, timeout=180, json_out=False):
    return flowgen._bsk(*a, timeout=timeout, json_out=json_out)


f = flowgen.Flow()
if SID:
    f.sid = SID
    print("用已有会话:", f.sid)
else:
    out, _, _ = bsk("session", "start", json_out=True)
    f.sid = json.loads(out).get("session_id")
    bsk("window", "resize", "--session", f.sid, "--width", "1600", "--height", "900")
    print("新会话:", f.sid)

try:
    bsk("navigate", PROJECT, "--session", f.sid)
    time.sleep(7)
    bsk("reload", "--session", f.sid)
    time.sleep(6)

    out, _, _ = bsk("observe", "--session", f.sid, "--max-tokens", "16000", timeout=300)
    m = re.search(r'@(e\d+)\s+textbox\s+"[^"]*" *="Oct 16', out or "")
    print("标题 ref:", "@" + m.group(1) if m else "(没找到，试 Editable text)")
    if not m:
        m = re.search(r'@(e\d+)\s+textbox\s+"Editable text"', out or "")
    ref = "@" + m.group(1)

    o, e, c = bsk("fill", "--value", NEW, "--ref", ref, "--session", f.sid)
    print("fill:", ((o or "") + (e or "")).strip()[:200] or "(ok)")
    bsk("press", "Enter", "--session", f.sid)
    time.sleep(4)
    print("改后标题区：", f._run("(document.querySelector('header,[role=banner]')||document.body).innerText.replace(/\\n+/g,' | ').slice(0,70)"))

    # 刷新，确认存住了（没存住刷新就回旧名）
    bsk("reload", "--session", f.sid)
    time.sleep(6)
    after = f._run("(()=>{const e=document.querySelector('.editable-text-input');"
                   "return e?(e.value||e.textContent||'').trim():'(找不到标题输入框)';})()")
    print("刷新后标题：", repr(after))
    print("存住了：" , after == NEW)
finally:
    print("会话:", f.sid)
