"""生图执行器：读 `gen-queue.json`，逐张在 Flow 上生成，写状态与事件。

**它是"干活的人"，面板是"遥控器"** —— 所以：
  · 队列在文件里（面板/人/agent 都能往里写），执行器崩了再起就接着跑（跳过已完成的）
  · 每张一条事件（面板的"过程列表"读它）+ 一条 jsonl 记录（留档）
  · 失败不连坐：这一张记下原因标 failed，继续下一张

2026-10-20 加的三道保险（都是实测踩出来的，见 `docs/经验与坑.md`）：
  ① **「生成」按钮必须先变亮**。Flow 的提示框是 React contenteditable，
     `execCommand('insertText')` 把字塞进 DOM 了，React 不一定收到 —— 按钮还是灰的，
     这时候点下去**什么都不会发生**，然后白等 300 秒（今天实测踩到：一张没出）。
     所以：写完提示词 → 等按钮 enabled → 还灰着就**重写一遍**再等。
  ② **点了要确认真的开始出图**（页面上出现 stop 按钮）。
     没开始就再点一次（最多 3 次），别闷头等。
  ③ **控制台不许崩**：Windows 控制台是 GBK，打印 '✓'/'✗' 会抛 UnicodeEncodeError，
     一崩整批就停了。所以 stdout 一律降级输出，标记用 ASCII。

用法：
    python tools/gen_worker.py <片名>              # 把队列里 queued/retry 的都做掉
    python tools/gen_worker.py <片名> --dry-run    # 只看要做哪些
    python tools/gen_worker.py <片名> --once       # 只做一张（调试用）
"""
import argparse
import base64
import io
import pathlib
import sys
import time
import warnings

warnings.filterwarnings("ignore")

# Windows 控制台是 GBK：中文/符号会直接抛 UnicodeEncodeError（会带走整批任务）
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:                                            # noqa: BLE001
    pass

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

# 页面状态：生成按钮亮了没 / 有没有开始出图（stop 按钮）/ 提示框里还有没有字
_STATE = (
    "(()=>{const A=x=>((x.getAttribute&&x.getAttribute('aria-label'))||x.textContent||'').trim();"
    "const g=[...document.querySelectorAll('button')]"
    ".find(x=>/start generation|开始生成/i.test(A(x)));"
    "const s=[...document.querySelectorAll('button')]"
    ".find(x=>/^(stop|stop generation|停止|停止生成)$/i.test(A(x)));"
    "const ed=[...document.querySelectorAll('[contenteditable=true]')];"
    "const el=ed[ed.length-1];"
    "return {gen:!!g,disabled:g?!!g.disabled:null,stopping:!!s,"
    "len:el?((el.innerText||'').trim().length):-1};})()"
)


def log(rec):
    LIB.mkdir(parents=True, exist_ok=True)
    with LOGF.open("a", encoding="utf-8") as fh:
        fh.write(__import__("json").dumps(rec, ensure_ascii=False) + "\n")


def say(proj, msg):
    """往事件流里写一句（面板看得到），控制台上也打一句（打崩了也不能带倒整批）。"""
    try:
        pipeline.emit(proj, "log", text=msg)
    except Exception:                                         # noqa: BLE001
        pass
    try:
        print(msg, flush=True)
    except Exception:                                         # noqa: BLE001
        try:
            print(msg.encode("gbk", "replace").decode("gbk"), flush=True)
        except Exception:                                     # noqa: BLE001
            pass


def _state(f):
    st = f._run(_STATE)
    return st if isinstance(st, dict) else {}


def wait_ready(f, tries=10, gap=5):
    """等「生成」按钮变亮。返回 True = 可以点了。"""
    for i in range(tries):
        st = _state(f)
        if st.get("gen") and st.get("disabled") is False:
            return True
        if i < tries - 1:
            time.sleep(gap)
    return False


def wait_started(f, tries=8, gap=6):
    """点完生成之后，确认 Flow **真的开始出图**（页面上出现 stop 按钮）。"""
    for i in range(tries):
        st = _state(f)
        if st.get("stopping"):
            return True
        # 出图时提示框会被清空 —— 也算一个信号
        if st.get("len") == 0 and st.get("gen"):
            return True
        if i < tries - 1:
            time.sleep(gap)
    return False


def do_one(f, proj, t):
    """生成一张。返回 metrics，失败抛异常。"""
    pipeline.queue_set(proj, t["id"], status="browser", tries=t.get("tries", 0) + 1)
    pipeline.emit(proj, "page", id=t["page"], status="browser", detail=f"挂角色 {t['cast']}")
    # cast 可以是 "小树+小芽"：双人同框页要两个 chip 都挂，另一个角色才不会被模型乱画
    for _name in str(t["cast"]).split("+"):
        if _name.strip():
            f.attach_character(_name.strip())

    prompt = full_prompt(t["scene"], t.get("layout", "full"))
    pipeline.queue_set(proj, t["id"], status="prompt")
    pipeline.emit(proj, "page", id=t["page"], status="prompt", detail="写提示词（会读回核对）")
    back = f._type_prompt(prompt)
    if not (isinstance(back, dict) and back.get("ok")):
        raise RuntimeError(f"提示词没输进去：{back}")

    # ① 按钮得先亮（React 认了这次输入才行）
    if not wait_ready(f):
        f._type_prompt(prompt)                     # 再写一遍
        if not wait_ready(f, tries=6):
            raise RuntimeError("提示词写进去了，但「生成」按钮一直是灰的（Flow 没认这次输入）")

    # ② 点生成 + 确认真的开始出图
    started = False
    for attempt in range(3):
        c = f._click_generate()
        if not isinstance(c, dict) or not c.get("ok"):
            raise RuntimeError(f"点不到生成按钮：{c}")
        if wait_started(f):
            started = True
            break
        say(proj, f"    生成没启动（第 {attempt + 1} 次点击），再点一次")
    if not started:
        raise RuntimeError("点了生成，Flow 一直没进入出图状态")

    pipeline.queue_set(proj, t["id"], status="generating")
    pipeline.emit(proj, "page", id=t["page"], status="generating", detail="生成中（约 60–100 秒）")

    # ③ 等新图：网格里**新冒出来的 base**（老图都在基线里，不会被当成新的）
    before = set(f.known) | f._image_bases()
    deadline = time.time() + 300
    got = []
    while time.time() < deadline:
        time.sleep(6)
        cur = f._image_bases()
        fresh = [b for b in sorted(cur - before) if b not in f._rejected]
        if fresh:
            time.sleep(8)                          # 等原图就位
            try:
                cand = f._fetch_raw(fresh[:6], min_w=900)
            except Exception as e:                 # noqa: BLE001
                cand = []
                say(proj, f"    取图没成（还在生成）：{e}")
            for x in cand:
                blob = base64.b64decode(x["b64"])
                old, _why = f._is_old(blob)
                if old:
                    f._rejected.add(x.get("b") or "")
                    continue
                got = [blob]
                break
            if got:
                break
    if not got:
        st = _state(f)
        raise RuntimeError(f"300 秒内没等到新图（页面状态 {json.dumps(st, ensure_ascii=False)}）")

    b = got[0]
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
    import json                                              # noqa: PLC0415
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    proj = a.project

    q = pipeline.queue(proj)
    todo = [t for t in q["tasks"] if t.get("status") in ("queued", "retry")]
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
            say(proj, f'[!] {c["name"]}：{c["hint"]}')
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
                f = flowgen.Flow(log=lambda *a: print("   ", *a, flush=True))
                f.enter(PROJECT_URL)
                cur = t.get("cast")
            say(proj, f'[{i}/{len(todo)}] {t["id"]} · {t["page"]} · {t["cast"]}：{t["scene"][:24]}…')
            t0 = time.time()
            try:
                m = do_one(f, proj, t)
                ok.append(t["id"])
                say(proj, f'    [ok] {m["w"]}x{m["h"]} 芽{m["sprout_px"]} 带{m["band_std"]} '
                          f'（{time.time() - t0:.0f}s）')
            except Exception as e:                              # noqa: BLE001
                msg = f"{type(e).__name__}: {e}"[:160]
                pipeline.queue_set(proj, t["id"], status="failed", error=msg)
                pipeline.emit(proj, "page", id=t["page"], status="failed", detail=msg)
                failed.append(t["id"])
                say(proj, f"    [x] {msg}")
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
    print(f"\n=== 出图结束：成功 {len(ok)}，失败 {len(failed)}"
          + (f"（{', '.join(failed)}）" if failed else ""))
    print("    去面板上看图 → 通过 / 写句改法打回（打回的会重新排队）")
    return 0


if __name__ == "__main__":
    import json                                              # noqa: E402,PLC0415
    sys.exit(main())
