"""诊断 Flow：进项目，看页面上的报错/限额提示，数一数项目里有多少张图，截个图。

用法：python experiments/diag_flow.py
"""
import json
import pathlib
import re
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECT = "https://flow.google.com/project/2423a8a2-2219-4dd5-83ea-563fd00a79fb"
SHOT = ROOT / "experiments" / "uitest" / "flow" / "diag-flow.png"

KEYS = ["limit", "quota", "error", "try again", "upgrade", "credit", "fail",
        "not available", "sorry", "out of", "generation", "waiting", "queue"]


def bsk(*args, timeout=180, json_out=False):
    cmd = ["bsk", *[str(a) for a in args]]
    if json_out:
        cmd.append("--json")
    p = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    return p.stdout or "", p.stderr or "", p.returncode


def main():
    out, err, _ = bsk("session", "start", json_out=True)
    m = re.search(r'"session_id"\s*:\s*"([^"]+)"', out)
    if not m:
        print("no session:", out[:200], err[:200])
        return 1
    sid = m.group(1)
    print("session", sid)
    try:
        bsk("window", "resize", "--session", sid, "--width", "1600", "--height", "900")
        bsk("navigate", PROJECT, "--session", sid)
        time.sleep(12)
        js = ("(()=>{const H=['lh3.googleusercontent.com','googleusercontent.com'];"
              "const imgs=[...document.querySelectorAll('img')].filter(i=>(i.src||'').includes('usercontent'));"
              "return JSON.stringify({imgs:imgs.length,"
              " txt:(document.body.innerText||'').replace(/\\n+/g,' | ').slice(0,2500)});})()")
        out, err, _ = bsk("evaluate", js, "--session", sid, json_out=True, timeout=300)
        try:
            val = json.loads(out).get("value")
        except Exception:                                          # noqa: BLE001
            val = out
        if isinstance(val, str):
            try:
                val = json.loads(val)
            except Exception:                                      # noqa: BLE001
                pass
        if isinstance(val, dict):
            print("IMG COUNT:", val.get("imgs"))
            txt = val.get("txt") or ""
            print("--- page text ---")
            print(txt[:2500])
            print("--- keyword hits ---")
            for k in KEYS:
                for hit in re.finditer(k, txt, re.I):
                    s = max(0, hit.start() - 60)
                    print(f"[{k}] ...{txt[s:hit.start() + 90]}...")
        else:
            print("raw:", str(val)[:2000], err[:500])
        SHOT.parent.mkdir(parents=True, exist_ok=True)
        bsk("screenshot", "--out", str(SHOT), "--session", sid, timeout=180)
        print("shot:", SHOT)
    finally:
        bsk("session", "stop", sid)
    return 0


if __name__ == "__main__":
    sys.exit(main())
