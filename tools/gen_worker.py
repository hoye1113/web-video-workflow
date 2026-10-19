"""生图执行器：读 `gen-queue.json`，逐张在 Flow 上生成，写状态与事件。

**它是"干活的人"，面板是"遥控器"** —— 所以：
  · 队列在文件里（面板/人/agent 都能往里写），执行器崩了再起就接着跑（跳过已完成的）
  · 每张一条事件（面板的"过程列表"读它）+ 一条 jsonl 记录（留档）
  · 失败不连坐：这一张记下原因标 failed，继续下一张

用法：
    python tools/gen_worker.py <片名>              # 把队列里 queued/retry 的都做掉
    python tools/gen_worker.py <片名> --dry-run    # 只看要做哪些
    python tools/gen_worker.py <片名> --once       # 只做一张（调试用）
"""
import argparse
import io
import pathlib
import sys
import time
import warnings

warnings.filterwarnings("ignore")

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
sys.path.insert(0, str(ROOT / "tools"))
import flowgen                                  # noqa: E402
import pipeline                                 # noqa: E402
from gen_scenes import full_prompt, metrics     # noqa: E402

from PIL import Image                           # noqa: E402

LIB = ROOT / "projects" / "scene-library"
PROJECT_URL = "https://flow.google.com/project/2423a8a2-2219-4dd5-83ea-563fd00a79fb"
LOGF = LIB / "gen-worker.log.jsonl"


def log(rec):
    LIB.mkdir(parents=True, exist_ok=True)
    with LOGF.open("a", encoding="utf-8") as fh:
        fh.write(__import__("json").dumps(rec, ensure_ascii=False) + "\n")


def say(proj, msg):
    print(msg, flush=True)
    pipeline.emit(proj, "log", text=msg)


def do_one(f, proj, t):
    """生成一张。返回 metrics，失败抛异常。"""
    pipeline.queue_set(proj, t["id"], status="browser", tries=t.get("tries", 0) + 1)
    pipeline.emit(proj, "page", id=t["page"], status="browser", detail=f"挂角色 {t['cast']}")
    f.attach_character(t["cast"])
    pipeline.queue_set(proj, t["id"], status="prompt")
    pipeline.emit(proj, "page", id=t["page"], status="prompt", detail="写提示词（会读回核对）")
    pipeline.queue_set(proj, t["id"], status="generating")
    pipeline.emit(proj, "page", id=t["page"], status="generating", detail="生成中（约 60–100 秒）")
    blobs = f.generate(full_prompt(t["scene"]), timeout=300, settle=8, keep=1)
    b = blobs[0]
    pipeline.queue_set(proj, t["id"], status="fetching")
    m = metrics(b)
    out = LIB / t["out"]
    Image.open(io.BytesIO(b)).convert("RGB").save(out)
    pipeline.queue_set(proj, t["id"], status="review", img=t["out"], metrics=m, error="")
    pipeline.emit(proj, "page", id=t["page"], status="review",
                  detail=f"{m['w']}x{m['h']} 芽{m['sprout_px']} 带{m['band_std']} → 等你看看")
    log({"task": t["id"], "page": t["page"], "cast": t["cast"], "file": t["out"],
         "scene": t["scene"], "metrics": m, "at": time.strftime("%Y-%m-%d %H:%M:%S")})
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    proj = a.project

    q = pipeline.queue(proj)
    todo = [t for t in q["tasks"] if t["status"] in ("queued", "retry")]
    if not todo:
        print("队列里没有待做的（queued/retry）")
        pipeline.emit(proj, "stage", stage="出图", status="done", detail="队列是空的")
        return 0
    # 同一角色的连做（换角色要重开会话，chip 才不串）
    todo.sort(key=lambda t: t.get("cast", ""))

    print(f"要做 {len(todo)} 张：" + "、".join(f'{t["id"]}({t["cast"]})' for t in todo))
    if a.dry_run:
        for t in todo:
            print(f'  {t["id"]:<10} {t["page"]:<5} {t["cast"]:<4} {t["scene"][:40]}')
        return 0

    bad = [c for c in pipeline.env_check() if not c["ok"]]
    if bad:
        for c in bad:
            say(proj, f'✗ {c["name"]}：{c["hint"]}')
        pipeline.emit(proj, "stage", stage="出图", status="failed",
                      detail="环境没准备好：" + "、".join(c["name"] for c in bad))
        return 2

    pipeline.emit(proj, "stage", stage="出图", status="start", detail=f"{len(todo)} 张")
    ok, failed = [], []
    cur, f = None, None
    try:
        for i, t in enumerate(todo, 1):
            if cur != t.get("cast"):
                if f:
                    f.close()
                    time.sleep(2)
                f = flowgen.Flow(log=print)
                f.enter(PROJECT_URL)
                cur = t.get("cast")
            say(proj, f'[{i}/{len(todo)}] {t["id"]} · {t["page"]} · {t["cast"]}：{t["scene"][:24]}…')
            t0 = time.time()
            try:
                m = do_one(f, proj, t)
                ok.append(t["id"])
                say(proj, f'    ✓ {m["w"]}x{m["h"]} 芽{m["sprout_px"]} 带{m["band_std"]} '
                          f'（{time.time() - t0:.0f}s）')
            except Exception as e:                              # noqa: BLE001
                msg = f"{type(e).__name__}: {e}"[:160]
                pipeline.queue_set(proj, t["id"], status="failed", error=msg)
                pipeline.emit(proj, "page", id=t["page"], status="failed", detail=msg)
                failed.append(t["id"])
                say(proj, f"    ✗ {msg}")
                # 会话可能死了：下次重开
                try:
                    f.close()
                except Exception:                               # noqa: BLE001
                    pass
                f = None
                cur = None
            if a.once:
                break
    finally:
        if f:
            f.close()

    # 顺手把素材库索引更新了（面板读它渲染素材库）
    pipeline.run([pipeline.PY, "tools/lib_index.py"], timeout=600)
    pipeline.emit(proj, "stage", stage="出图",
                  status="done" if not failed else "failed",
                  detail=f"成功 {len(ok)} 张" + (f"，失败 {len(failed)} 张" if failed else ""))
    print(f"\n═══ 出图结束：成功 {len(ok)}，失败 {len(failed)}"
          + (f"（{', '.join(failed)}）" if failed else ""))
    print("    去面板上看图 → ✓ 通过 / ✗ 写句改法打回（打回的会重新排队）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
