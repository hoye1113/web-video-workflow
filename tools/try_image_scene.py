"""端到端验证 F2：贴图页写代码 → 抽帧 → 评审。全程走真实服务（跟界面一条路）。

用法：
  python tools/try_image_scene.py 01        # 只写代码
  python tools/try_image_scene.py 01 full   # 写代码 + 抽帧 + 评审
"""
import json
import sys
import time
import urllib.request

BASE = "http://127.0.0.1:8777"
PROJ = "marriage_full"


def post(path, body):
    r = urllib.request.Request(BASE + path, data=json.dumps(body).encode(),
                               headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=120) as f:
        return json.loads(f.read().decode("utf-8"))


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=120) as f:
        return json.loads(f.read().decode("utf-8"))


def wait(job, limit=1200):
    """等一个任务跑完，边等边把它的日志打出来。

    注意：服务端没有 /api/jobs/<id> 这个路由，只有 /api/jobs 列表 —— 从列表里挑。
    """
    jid = job.get("id")
    t0, seen = time.time(), 0
    while time.time() - t0 < limit:
        time.sleep(3)
        j = next((x for x in get("/api/jobs") if x.get("id") == jid), None)
        if j is None:
            raise RuntimeError(f"任务 {jid} 从列表里消失了")
        for line in j.get("log", [])[seen:]:
            print("   ", line, flush=True)
        seen = len(j.get("log", []))
        if j.get("status") in ("done", "failed"):
            print(f"    → {j['status']}　{j.get('elapsed')}s", flush=True)
            if j.get("status") == "failed":
                print("    错误：" + str(j.get("error"))[:400], flush=True)
            return j
    raise TimeoutError(f"任务 {jid} 超过 {limit}s 没结束")


if __name__ == "__main__":
    sid = sys.argv[1] if len(sys.argv) > 1 else "01"
    full = len(sys.argv) > 2 and sys.argv[2] == "full"

    print(f"① 写场景代码（页 {sid}）", flush=True)
    j = wait(post("/api/scene", {"project": PROJ, "shot": sid}))
    if j["status"] == "failed":
        sys.exit(1)
    src = (j.get("result") or {}).get("source") or ""
    print(f"   代码 {len(src)} 字 / {len(src.splitlines())} 行", flush=True)

    if not full:
        sys.exit(0)

    print("② 抽帧", flush=True)
    wait(post("/api/stills", {"project": PROJ, "shot": sid}))

    print("③ 评审", flush=True)
    r = wait(post("/api/review", {"project": PROJ, "shot": sid}))
    print(json.dumps(r.get("result"), ensure_ascii=False, indent=2)[:2500], flush=True)
