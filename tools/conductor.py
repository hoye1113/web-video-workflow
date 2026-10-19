"""自动推进器：按顺序把"没做完的下一件事"做掉 —— 人不需要点阶段按钮。

照 frametell 的分工：**阶段是自动往下走的**，人只做三件事 ——
①说（消息框）②点头（审批卡：分镜/图/成片）③看（画面）。
所以"下一步做什么"由这个脚本判断，不由人点。

它在面板里以一个后台线程跑（每 5 秒看一眼），也可以单独跑：
    python tools/conductor.py emotion-full --watch      # 前台看它怎么判
    python tools/conductor.py emotion-full --once       # 只判一次（不干活，打印结论）

判断顺序（每一步都只在"该做且没在做"时才动）：
    台词齐 → 【等确认分镜】→ 出图（队列）→ 【等看图】→ 素材索引 → 排页 → 配音 → 字幕 → 渲染 → 验收/抽帧
"""
import argparse
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import pipeline                                       # noqa: E402

STALE = 60          # 两个文件的 mtime 差在这个秒数内算"一样新"


def newest(d, pat):
    fs = [f for f in d.glob(pat) if f.is_file()]
    return max((f.stat().st_mtime for f in fs), default=0)


def oldest(d, pat):
    fs = [f for f in d.glob(pat) if f.is_file()]
    return min((f.stat().st_mtime for f in fs), default=0)


def step_for(proj):
    """返回 (阶段名, 理由) 或 (None, 状态说明)。"""
    d = pipeline.proj_dir(proj)
    src = d / "script-source.json"
    if not src.exists():
        return None, "等你写台词（script-source.json）"
    q = pipeline.queue(proj)
    todo = [t for t in q["tasks"] if t["status"] in ("queued", "retry")]
    review = [t for t in q["tasks"] if t["status"] == "review"]
    gates = pipeline.gate_state(proj)
    spec = d / "page-spec.json"
    voice = d / "voice.js"
    srt = d / "out" / "字幕.srt"
    index = ROOT / "projects" / "scene-library" / "index.json"
    film = sorted((d / "out").glob("*.mp4"))

    # 0) 台词本身要能过（硬切/格式）
    if not (d / "script.js").exists() or (d / "script.js").stat().st_mtime < src.stat().st_mtime:
        return "剧本", "台词有新改动，先把剧本编出来"
    if not spec.exists():
        return None, "等排页表（page-spec.json，可由 agent 或模板生成）"

    # 1) 分镜闸门：确认之前不出图
    if gates.get("map") != "ok":
        return None, "等你确认分镜（页 → 处境映射表）"

    # 2) 出图：队列里有活就干
    if todo:
        return "出图", f"队列里还有 {len(todo)} 张要出"
    # 3) 出了图要人看（看图闸门）
    if review and gates.get("img") != "ok":
        return None, f"等你看看刚出的 {len(review)} 张图"

    # 4) 素材索引 → 5) 排页 → 6) 配音 → 7) 字幕 → 8) 渲染
    if not index.exists() or (q["tasks"] and index.stat().st_mtime < newest(d.parent / "scene-library", "*.png")):
        return "素材", "素材库索引该更新了"
    # 排页看的是"页代码有没有落后于页表/素材" —— 要拿**页文件的 mtime**比。
    # 拿页表去比索引（素材）会死循环：索引更新一次，页表永远比它旧，就会每 5 秒重排一次。
    if newest(d / "pages", "p*.js") < max(spec.stat().st_mtime, index.stat().st_mtime if index.exists() else 0):
        return "排页", "页表/素材更新了，重排一次页代码"
    if not voice.exists() or voice.stat().st_mtime < src.stat().st_mtime:
        return "配音", "台词有新改动，重配一次"
    if not srt.exists() or srt.stat().st_mtime < voice.stat().st_mtime:
        return "字幕", "配音改了，字幕要跟着重出"
    if not film or film[-1].stat().st_mtime < max(spec.stat().st_mtime, voice.stat().st_mtime):
        return "渲染", "画面/声音有新改动，重渲一版"

    # 9) 出片后的验收（机器判据 + 抽帧表）
    if film and (d / "out" / "snap").exists() and newest(d / "out" / "snap", "qc*.jpg") < film[-1].stat().st_mtime:
        return "抽帧", "成片更新了，重新抽帧"
    return None, "都做完了 —— 等你确认成片" if gates.get("film") != "ok" else "已完成"


def advance(proj, say=print):
    """看一步、做一步（一次只做一件事，做完就返回，让下一次调用继续）。"""
    step, why = step_for(proj)
    if not step:
        return None, why
    say(f"[推进] {step}：{why}")
    pipeline.emit(proj, "stage", stage=step, status="start", detail=f"自动：{why}")
    _, cmd, cwd, txt = pipeline.STEP[step]
    cmd = [str(x).replace("{proj}", proj) for x in cmd]
    cwd = pipeline.proj_dir(proj) if cwd == "PROJ" else ROOT
    r = pipeline.run(cmd, cwd=cwd, timeout=7200)
    ok = r.returncode == 0
    for line in (r.stdout or "").splitlines()[-40:]:
        pipeline.emit(proj, "log", text=line, step=step)
    pipeline.emit(proj, "stage", stage=step, status="done" if ok else "failed",
                  detail=txt["done"] if ok else (r.stderr or "没成")[-200:])
    return step, why


def paused(proj):
    f = pipeline.proj_dir(proj) / "paused"
    return f.exists()


def set_paused(proj, on):
    f = pipeline.proj_dir(proj) / "paused"
    if on:
        f.write_text(time.strftime("%Y-%m-%d %H:%M:%S"), encoding="utf-8")
        pipeline.emit(proj, "stage", stage="暂停", status="done", detail="已暂停（做好的不会重做）")
    else:
        f.unlink(missing_ok=True)
        pipeline.emit(proj, "stage", stage="继续", status="done", detail="继续制作")
    return on


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--pause", action="store_true")
    ap.add_argument("--resume", action="store_true")
    a = ap.parse_args()
    if a.pause or a.resume:
        print("已暂停" if set_paused(a.project, a.pause) else "已继续")
        return
    if a.once:
        step, why = step_for(a.project)
        print(f"下一步：{step or '（不动）'} —— {why}")
        return
    if a.watch:
        while True:
            step, why = advance(a.project)
            print(f"  {time.strftime('%H:%M:%S')} {step or '·'} {why}")
            if not step:
                time.sleep(5)
        return
    advance(a.project)


if __name__ == "__main__":
    main()
