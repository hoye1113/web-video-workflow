"""看 Flow 页面上的「生成」按钮到底是什么、有没有 disabled、有没有会报错的气泡。

用法：python experiments/diag_gen_btn.py
"""
import json
import pathlib
import re
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECT = "https://flow.google.com/project/2423a8a2-2219-4dd5-83ea-563fd00a79fb"
SHOT = ROOT / "experiments" / "uitest" / "flow" / "diag-genbtn.png"


def bsk(*args, timeout=180, json_out=False):
    cmd = ["bsk", *[str(a) for a in args]]
    if json_out:
        cmd.append("--json")
    p = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    return p.stdout or "", p.stderr or "", p.returncode


def main():
    out, err, _ = bsk("session", "start", json_out=True)
    sid = re.search(r'"session_id"\s*:\s*"([^"]+)"', out).group(1)
    print("session", sid)
    try:
        bsk("window", "resize", "--session", sid, "--width", "1600", "--height", "900")
        bsk("navigate", PROJECT, "--session", sid)
        time.sleep(12)
        js = r"""(()=>{
          const bs=[...document.querySelectorAll('button')];
          const rows=bs.map((b,i)=>({
            i, label:(b.getAttribute('aria-label')||b.textContent||'').trim().slice(0,40),
            disabled:!!b.disabled, title:(b.getAttribute('title')||'').slice(0,30),
            cls:(b.className||'').toString().slice(0,50),
            x:Math.round(b.getBoundingClientRect().x), y:Math.round(b.getBoundingClientRect().y)
          }));
          const ed=[...document.querySelectorAll('[contenteditable=true]')];
          const edInfo=ed.map(e=>({text:(e.innerText||'').slice(0,60), x:Math.round(e.getBoundingClientRect().x), y:Math.round(e.getBoundingClientRect().y)}));
          return JSON.stringify({buttons:rows, editables:edInfo});
        })()"""
        out, err, _ = bsk("evaluate", js, "--session", sid, json_out=True, timeout=300)
        try:
            val = json.loads(out).get("value")
            if isinstance(val, str):
                val = json.loads(val)
        except Exception as e:                                      # noqa: BLE001
            print("parse fail", out[:400], err[:300])
            return 1
        print("--- editables ---")
        for e in val.get("editables", []):
            print("  ", e)
        print("--- buttons (x>900 or generation-ish) ---")
        for b in val.get("buttons", []):
            lbl = b["label"].lower()
            if "generation" in lbl or "generate" in lbl or b["x"] > 900 or b["y"] > 500:
                print("  ", b)
        bsk("screenshot", "--out", str(SHOT), "--session", sid, timeout=180)
        print("shot:", SHOT)
    finally:
        bsk("session", "stop", sid)
    return 0


if __name__ == "__main__":
    sys.exit(main())
