"""生图监督器：盯着一条片子的队列，出问题就修（重启执行器 / 失败重排），直到画完或超时。

用法：python tools/supervise_images.py marriage-1021 [--minutes 60]
"""
import argparse
import json
import pathlib
import subprocess
import sys
import time
import urllib.request
from collections import Counter

BASE = "http://127.0.0.1:8900"


def get(path):
    return json.loads(urllib.request.urlopen(BASE + path, timeout=30).read())


def post(path, body):
    req = urllib.request.Request(BASE + path, json.dumps(body).encode(),
                                 {"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())


def worker_running():
    ps = ("(Get-CimInstance Win32_Process -Filter \"name='python.exe'\" | "
          "Where-Object { $_.CommandLine -match 'gen_worker' } | Measure-Object).Count")
    out = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                         capture_output=True, text=True).stdout.strip()
    return out not in ("0", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("film")
    ap.add_argument("--minutes", type=float, default=60)
    a = ap.parse_args()
    F, deadline = a.film, time.time() + a.minutes * 60
    ROOT = pathlib.Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(ROOT / "tools"))
    import pipeline as pl
    total = None
    last = None
    while time.time() < deadline:
        time.sleep(30)
        try:
            q = pl.queue(F)
            imgs = [{"status": t.get("status"), "file": bool(t.get("img"))} for t in q["tasks"]]
        except Exception as e:                                  # noqa: BLE001
            print("  ✗ 读队列失败：", e, flush=True)
            continue
        total = total or len(imgs) or 0
        c = Counter(x["status"] for x in imgs)
        done = sum(1 for x in imgs if x.get("file"))
        line = "  已出 %d/%d · %s" % (done, total, dict(c))
        if line != last:
            print(line, flush=True)
            last = line
        pending = any(x["status"] in ("queued", "retry", "failed") for x in imgs)
        if pending and not worker_running():
            try:
                q = pl.queue(F)
                for t in q["tasks"]:
                    if t["status"] in ("failed", "browser", "generating", "prompt", "fetching") and not t.get("img"):
                        t["status"] = "retry"
                        t["error"] = ""
                pl.queue_save(F, q)
            except Exception:                               # noqa: BLE001
                pass
            try:
                logf = ROOT / "logs" / f"gen-{F}.log"
                logf.parent.mkdir(parents=True, exist_ok=True)
                subprocess.Popen([sys.executable, str(ROOT / "tools" / "gen_worker.py"), F],
                                 cwd=str(ROOT), stdout=open(logf, "ab"), stderr=subprocess.STDOUT,
                                 stdin=subprocess.DEVNULL,
                                 creationflags=0x00000008 | 0x00000200, close_fds=True)
                print("  ↻ 执行器不在 → 已重启（直接起 gen_worker，不依赖面板）", flush=True)
            except Exception as e:                              # noqa: BLE001
                print("  ✗ 重启失败：", e, flush=True)
        if total and done >= total:
            print("  ✓ 全部出完", flush=True)
            return 0
    print("  ⏰ 监督到时（还有没画完的）", flush=True)
    return 1


if __name__ == "__main__":
    sys.exit(main())
