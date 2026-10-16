"""成片验收：逐页抽帧 + 自动体检 + 拼验收表。

为什么要有这个：成片是 349 秒的 mp4，人不可能从头一秒一秒看完。
但要验收"每一页都对"，就得**每页都看一眼** —— 折中做法是每页抽中间那一帧，
26 页拼成一张表，一眼扫完。

顺手做三件机器能判的事（省得人眼去看）：
  ① 有没有**黑页/空页**（平均亮度、细节量都低到不像画面）
  ② 页数对不对（每页都抽到了）
  ③ 字幕在不在（下方字幕带里有没有字）

用法：python tools/accept_film.py <项目> [成片文件名]
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
sys.path.insert(0, str(ROOT / "tools"))


def page_times(shots):
    """每页的 (页号, 开始秒, 时长)，用来知道"什么时候该抽帧"。"""
    out, t = [], 0.0
    for s in shots:
        d = float(s.get("dur") or 12)
        out.append((s["id"], t, d))
        t += d
    return out


def grab(film, at, out):
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{at:g}", "-i", str(film),
                        "-frames:v", "1", str(out)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return out.exists()


def stats(png):
    """一帧的体检：平均亮度、细节量、下方字幕带的细节量。"""
    import numpy as np
    from PIL import Image
    im = Image.open(png).convert("RGB").resize((320, 180))
    a = np.asarray(im).astype(np.float32)
    g = np.asarray(im.convert("L")).astype(np.float32)
    mag = np.maximum(np.abs(np.diff(g, axis=1, prepend=g[:, :1])),
                     np.abs(np.diff(g, axis=0, prepend=g[:1, :])))
    band = mag[int(180 * 0.82):]                     # 字幕带
    return {"bright": round(float(g.mean()), 1),
            "detail": round(float((mag > 12).mean()), 4),
            "sub_band": round(float((band > 12).mean()), 4)}


if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "marriage_full"
    filmname = sys.argv[2] if len(sys.argv) > 2 else "成片.mp4"
    m = json.loads((ROOT / "projects" / name / "project.json").read_text(encoding="utf-8"))
    shots = m["shots"]
    film = ROOT / "projects" / name / "out" / filmname
    if not film.exists():
        sys.exit(f"没有这个成片：{film}")

    work = ROOT / "experiments" / "accept"
    work.mkdir(parents=True, exist_ok=True)
    for f in work.glob("*.png"):
        f.unlink()

    rows = []
    print(f"逐页抽帧（{len(shots)} 页）")
    print("%-4s %8s %7s %7s %8s %s" % ("页", "时间", "亮度", "细节", "字幕带", "判定"))
    for sid, t0, dur in page_times(shots):
        at = t0 + dur * 0.55                       # 一页的中间偏后，避开开头的揭示
        png = work / f"p{sid}.png"
        if not grab(film, at, png):
            print(f"{sid:<4} {at:>7.1f} 抽帧失败")
            continue
        st = stats(png)
        flag = []
        if st["bright"] < 18:
            flag.append("黑页")
        if st["detail"] < 0.004:
            flag.append("空页")
        if st["sub_band"] < 0.004:
            flag.append("字幕带没字")
        rows.append({"shot": sid, "at": at, **st, "flag": flag})
        print("%-4s %7.1fs %7.1f %7.4f %8.4f %s"
              % (sid, at, st["bright"], st["detail"], st["sub_band"],
                 "、".join(flag) or "OK"))

    bad = [r for r in rows if r["flag"]]
    print()
    print(f"体检：{len(rows)} 页抽到帧，{len(bad)} 页有疑点"
          + ("：" + "、".join(f'{r["shot"]}({"、".join(r["flag"])})' for r in bad) if bad else ""))

    # 拼验收表：每页一帧，4 列，帧上标页号
    fs = [str(work / f"p{r['shot']}.png") for r in rows]
    from contact_sheet import sheet
    out = ROOT / "experiments" / "uitest" / "80_成片验收表.png"
    sheet(out, fs, cols=4, cell=470)
    print(f"验收表：{out}")
