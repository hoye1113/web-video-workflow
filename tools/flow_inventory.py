"""盘点：项目里现在有哪些素材、哪些角色（用户已经用 Characters 建了"小树"）。"""
import json
import pathlib
import re
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

PROJECT = "https://flow.google.com/project/2423a8a2-2219-4dd5-83ea-563fd00a79fb"
SHOT = ROOT / "experiments" / "uitest" / "flow" / "assets.png"

f = flowgen.Flow()
try:
    out, _, _ = flowgen._bsk("session", "start", json_out=True, timeout=180)
    f.sid = json.loads(out).get("session_id")
    flowgen._bsk("window", "resize", "--session", f.sid, "--width", "1600", "--height", "900", timeout=60)
    flowgen._bsk("navigate", PROJECT, "--session", f.sid, timeout=180)
    time.sleep(8)
    print("会话:", f.sid)

    # 左侧栏切到 Characters
    out2, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "16000", timeout=300)
    mc = re.search(r'@(e\d+)\s+button\s+"Characters"', out2 or "")
    print("左侧 Characters:", "@" + mc.group(1) if mc else "没找到")
    if mc:
        flowgen._bsk("click", "@" + mc.group(1), "--session", f.sid, timeout=120)
        time.sleep(4)
        print("\n=== Characters 视图里的内容 ===")
        print(f._run("(document.body.innerText||'').replace(/\\n+/g,' | ').slice(0,700)"))

    # 左侧栏 Images（看生成了哪些图）
    out3, _, _ = flowgen._bsk("observe", "--session", f.sid, "--max-tokens", "16000", timeout=300)
    mi = re.search(r'@(e\d+)\s+button\s+"Images"', out3 or "")
    if mi:
        flowgen._bsk("click", "@" + mi.group(1), "--session", f.sid, timeout=120)
        time.sleep(4)
        print("\n=== Images 视图里的内容（素材名） ===")
        print(f._run("(document.body.innerText||'').replace(/\\n+/g,' | ').slice(0,900)"))

    flowgen._bsk("screenshot", "--session", f.sid, "--out", str(SHOT), timeout=180)
    print("\n截图:", SHOT.relative_to(ROOT))
finally:
    print("会话:", f.sid)
