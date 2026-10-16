"""导演回路：确定性检查打头阵，模型看图收尾，每轮存档，最后只保留得分最高的那版。

顺序就是成本顺序 —— 先跑便宜的，贵的放最后：

    第 N 轮
      ├─ 静态检查（读代码，秒级）          红灯 → 带着问题去改，不进渲染、不进评审
      ├─ 渲帧（~10s）                      渲不出来 = 代码坏了，记 0 分，回滚
      ├─ 像素检查（量帧，秒级）            红灯 → 带着问题去改，不进评审
      ├─ 模型看图评审（~40s，花钱）        打分 + 给具体改法
      └─ 存档、达标就停、否则按意见改

为什么要有「比稿」：实测同一个模型、同一套提示词，一次把画面改好了（7→8 分），
另一次改坏了（把主体改到出画）。所以不能信任单次修改，只能每轮存档 + 打分 + 留最高分。
"""
import json
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENGINE = ROOT / "base-arch" / "scripts" / "engine"
UV = shutil.which("uv") or str(Path.home() / ".local" / "bin" / "uv.exe")

import checks      # noqa: E402
import prompts     # noqa: E402
import store       # noqa: E402
import text as T   # noqa: E402


def _env():
    e = os.environ.copy()
    e["PYTHONUTF8"] = "1"
    e["PYTHONIOENCODING"] = "utf-8"
    return e


def _render_stills(project, shot, dur, job):
    """同步渲几个关键帧。旧帧先清掉，免得看到上一轮的。"""
    out = ROOT / "projects" / project / "out" / f"{shot}_still"
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob("t*.png"):
        f.unlink()
    at = [0.3, round(float(dur) * 0.4, 2), round(float(dur) * 0.85, 2)]
    cmd = [
        UV, "run", "--offline", "--with", "playwright", "python", str(ENGINE / "render.py"),
        "--film", f"demos/{project}", "--solo", shot,
        "--stills", ",".join(f"{t:g}" for t in at), "--no-counter", "--out", str(out),
    ]
    r = subprocess.run(cmd, cwd=str(ENGINE), env=_env(), capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=600)
    frames = sorted(out.glob("t*.png"))
    if r.returncode != 0 or not frames:
        tail = "\n".join((r.stdout or r.stderr or "").strip().splitlines()[-6:])
        raise RuntimeError("渲染失败，代码可能写坏了：\n" + tail)
    return frames


def _review(ai, project, shot, frames):
    m = store.load(project) or {}
    s = next((x for x in m.get("shots", []) if x["id"] == shot), {})
    st = m.get("style") or {}
    prompt = prompts.REVIEW.format(
        title=s.get("title", ""), note=s.get("note", ""), camera=s.get("camera", "停"),
        look=st.get("look") or "扁平矢量线稿",
        palette="、".join(st.get("palette") or []),
    )
    return T.parse_review(ai.generate(prompt, files=[str(f) for f in frames[-6:]]))


def _revise(ai, src, problems, fixes, shot, say=print):
    issues = "\n".join(f"- {x}" for x in problems) or "- （没提问题）"
    fx = "\n".join(f"- {x}" for x in fixes) or "- （没给改法）"
    out = T.strip_fence(ai.generate(prompts.REVISE.format(issues=issues, fixes=fx, source=src),
                                    timeout=420))
    out, renamed = T.fix_scene_id(out, shot)
    if renamed:
        say(f"改完注册名写错了，已改回 SCENES['{shot}']")
    import scene_check
    out = scene_check.fix_syntax(ai, out, shot, say=say)   # 改坏了也不许存盘
    return out, renamed


def make_loop(ai, project, shot, rounds=3, target=8):
    """返回一个可以扔进任务队列跑的 fn(job)。"""

    def run(job):
        m = store.load(project) or {}
        s = next((x for x in m.get("shots", []) if x["id"] == shot), None)
        if not s:
            raise ValueError("没有这个镜头")
        dur = float(s.get("dur") or 15)

        src = store.read_scene(project, shot)
        if not src.strip():
            raise ValueError("这一页还没有代码，先「写场景代码」")

        best = None
        for r in range(1, rounds + 1):
            job.step(r - 1, rounds, f"第 {r} 轮")
            job.say(f"════ 第 {r} 轮")

            # ---- 1. 静态检查（秒级，不花钱）----
            st = checks.scene_lint(project, shot, src)
            if st["problems"]:
                job.say("静态检查红灯：")
                for p in st["problems"]:
                    job.say("   ✗ " + p)
                n = store.save_version(project, shot, src,
                                       {"score": -1, "stage": "lint", "problems": st["problems"]})
                job.say(f"存档 v{n}（静态检查未过，不计分）")
                try:
                    src, rn = _revise(ai, src, st["problems"],
                                      [p for p in st["problems"]], shot, say=job.say)
                except Exception as e:                          # noqa: BLE001
                    job.say(f"改代码失败：{e}")
                    break
                store.write_scene(project, shot, src)
                continue

            for w in st["warnings"]:
                job.say("   ! " + w)

            # ---- 2. 渲帧 ----
            job.say("渲帧…")
            try:
                frames = _render_stills(project, shot, dur, job)
            except Exception as e:                              # noqa: BLE001
                job.say(f"渲染挂了：{e}")
                n = store.save_version(project, shot, src,
                                       {"score": -1, "stage": "render", "problems": [str(e)]})
                job.say(f"存档 v{n}（渲不出来，0 分）")
                break
            job.say(f"渲了 {len(frames)} 帧")

            # ---- 3. 像素检查（秒级，不花钱）----
            fa = checks.frame_audit(project, shot)
            if fa.get("error"):
                job.say("像素检查跳过：" + fa["error"])
            elif fa["problems"]:
                job.say("像素检查红灯：")
                for p in fa["problems"]:
                    job.say("   ✗ " + p)
                n = store.save_version(project, shot, src,
                                       {"score": -1, "stage": "audit", "problems": fa["problems"]})
                job.say(f"存档 v{n}（像素检查未过，不计分）")
                try:
                    src, rn = _revise(ai, src, fa["problems"], fa["problems"], shot, say=job.say)
                except Exception as e:                          # noqa: BLE001
                    job.say(f"改代码失败：{e}")
                    break
                store.write_scene(project, shot, src)
                continue
            else:
                for w in fa.get("warnings") or []:
                    job.say("   ! " + w)

            # ---- 4. 模型看图评审（贵的放最后）----
            job.say("两条确定性检查都过了，送模型看图…")
            try:
                rev = _review(ai, project, shot, frames)
            except Exception as e:                              # noqa: BLE001
                job.say(f"评审失败：{e}")
                break

            n = store.save_version(project, shot, src, rev)
            score = rev.get("score", -1)
            job.say(f"存档 v{n} · 得分 {score}/10 · ok={rev.get('ok')}")
            for p in (rev.get("problems") or [])[:6]:
                job.say("   · " + p)
            if best is None or score > best["score"]:
                best = {"n": n, "score": score, "src": src}
                job.say(f"   ↑ 目前最好的一版（v{n}）")

            if rev.get("ok") or score >= target:
                job.say("达标，提前结束")
                break
            if r == rounds:
                break

            job.say("按意见改（下一轮渲这版）")
            try:
                src, rn = _revise(ai, src, rev.get("problems") or [], rev.get("fixes") or [], shot,
                                  say=job.say)
            except Exception as e:                              # noqa: BLE001
                job.say(f"改代码失败：{e}")
                break
            store.write_scene(project, shot, src)
            job.say(f"改完 {len(src)} 字")

        if best:
            store.write_scene(project, shot, best["src"])
            job.say(f"═══ 回路结束：保留 v{best['n']}（{best['score']} 分），已回写进场景")
        else:
            job.say("没有一版通过确定性检查，场景文件保持原样，等你手工看一眼")

    return run
