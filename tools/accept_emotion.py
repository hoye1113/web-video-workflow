"""整片验收：逐页抽帧 + 机器体检 + 拼验收表（emotion-full / 引擎时间轴版）。

和旧管线那版（`accept_film.py`）的区别：时间轴**从引擎的 layout 拿**（带配音时是真实语速），
不是从 project.json 的 dur 累加。

判据（机器能判的三条）：
  ① 黑页：平均亮度太低
  ② 空页：细节量太低（一页什么都没画）
  ③ 字幕带：**母版必须干净**（下方 18% 不该有东西）；有字幕版必须**有字**
人还要看的两条（在验收表上扫）：认得出角色 / 愿意发。

用法：
    python tools/accept_emotion.py                 # 看母版（默认 out/emotion-full.mp4）
    python tools/accept_emotion.py --subs          # 看有字幕版
"""
import json
import os
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJ = next((a for a in sys.argv[1:] if not a.startswith("-")), "emotion-full")
EP = ROOT / "projects" / PROJ
ENGINE = ROOT / "experiments" / "frametell-src" / "frametell-main" / "packages" / "engine"
WORK = ROOT / "experiments" / "accept"

TIMES_JS = """
import { loadEpisode } from '%s';
const { L } = loadEpisode();
console.log(JSON.stringify({ duration: L.duration,
  pages: L.pages.map((p) => ({ id: p.id, start: p.start, end: p.end, section: p.section, title: p.title })) }));
""" % (ENGINE / "tools" / "lib.mjs").as_uri()


def page_times():
    f = pathlib.Path(tempfile.gettempdir()) / "vf-acc-times.mjs"
    f.write_text(TIMES_JS, encoding="utf-8")
    r = subprocess.run(["node", str(f)], cwd=str(EP), capture_output=True, text=True,
                       encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONUTF8": "1"})
    lines = [x for x in (r.stdout or "").splitlines() if x.strip().startswith("{")]
    if not lines:
        raise SystemExit(f"拿不到时间轴：\n{r.stdout}\n{r.stderr}")
    return json.loads(lines[-1])


def grab(film, at, out):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{at:g}", "-i", str(film),
                    "-frames:v", "1", str(out)],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
    return out.exists()


def stats(png):
    import numpy as np
    from PIL import Image
    im = Image.open(png).convert("RGB").resize((320, 180))
    g = np.asarray(im.convert("L")).astype(np.float32)
    mag = np.maximum(np.abs(np.diff(g, axis=1, prepend=g[:, :1])),
                     np.abs(np.diff(g, axis=0, prepend=g[:1, :])))
    band = mag[int(180 * 0.82):]
    return {"bright": round(float(g.mean()), 1),
            "detail": round(float((mag > 12).mean()), 4),
            "band": round(float((band > 12).mean()), 4)}


def main():
    subs = "--subs" in sys.argv
    film = EP / "out" / (f"{EP.name}-有字幕.mp4" if subs else f"{EP.name}-无字幕.mp4")
    if not film.exists():
        cand = sorted((EP / "out").glob("*.mp4")) if (EP / "out").exists() else []
        if not cand:
            sys.exit(f"out/ 里还没有成片（先跑 render.mjs）。找的是 {film.name}")
        film = cand[-1]
        print(f"（用 {film.name}）")

    d = page_times()
    print(f'片长 {d["duration"]:.1f}s / {len(d["pages"])} 页；片子 {film.name}')
    WORK.mkdir(parents=True, exist_ok=True)
    for f in WORK.glob("acc-*.png"):
        f.unlink()

    rows = []
    print("%-5s %7s %7s %8s %7s  %s" % ("页", "时间", "亮度", "细节", "字幕带", "判定"))
    for p in d["pages"]:
        at = p["start"] + (p["end"] - p["start"]) * 0.55
        png = WORK / f'acc-{p["id"]}.png'
        if not grab(film, at, png):
            print(f'{p["id"]:<5} {at:>7.1f}  抽帧失败')
            continue
        st = stats(png)
        flag = []
        if st["bright"] < 18:
            flag.append("黑页")
        if st["detail"] < 0.004:
            flag.append("空页")
        if subs and st["band"] < 0.004:
            flag.append("字幕带没字")
        if not subs and st["band"] > 0.02:
            flag.append("字幕带不干净")
        rows.append(dict(pid=p["id"], at=at, title=p.get("title", ""), **st, flag=flag))
        print("%-5s %6.1fs %7.1f %8.4f %7.4f  %s"
              % (p["id"], at, st["bright"], st["detail"], st["band"],
                 "、".join(flag) or "OK"))

    bad = [r for r in rows if r["flag"]]
    print(f'\n体检：{len(rows)} 页抽到帧，{len(bad)} 页有疑点'
          + ("：" + "、".join(f'{r["pid"]}({"、".join(r["flag"])})' for r in bad) if bad else ""))
    print("表：" + " ".join(str(WORK / f'acc-{r["pid"]}.png') for r in rows[:3]) + " …")


if __name__ == "__main__":
    main()
