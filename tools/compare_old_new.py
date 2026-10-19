"""新旧并排：从旧片（marriage_full）和新片（emotion-full）各抽一帧，按页拼一张对比图。

这是给"愿不愿意发"那条判据用的 —— 一页一行，左旧右新。

用法：
    python tools/compare_old_new.py                # 默认取 01 05 15 18 21 23
    python tools/compare_old_new.py 01 05 12 18
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OLD = ROOT / "projects" / "marriage_full"
NEW = ROOT / "projects" / "emotion-full"
WORK = ROOT / "experiments" / "compare"


def old_times():
    m = json.loads((OLD / "project.json").read_text(encoding="utf-8"))
    out, t = {}, 0.0
    for s in m["shots"]:
        d = float(s.get("dur") or 12)
        out[s["id"]] = t + d * 0.55
        t += d
    return out


def new_times():
    import tempfile, os
    engine = ROOT / "experiments" / "frametell-src" / "frametell-main" / "packages" / "engine"
    js = (f"import {{ loadEpisode }} from '{(engine / 'tools' / 'lib.mjs').as_uri()}';\n"
          "const { L } = loadEpisode();\n"
          "console.log(JSON.stringify(L.pages.map(p => ({id: p.id, t: p.start + (p.end - p.start) * 0.55}))));\n")
    f = pathlib.Path(tempfile.gettempdir()) / "vf-cmp.mjs"
    f.write_text(js, encoding="utf-8")
    r = subprocess.run(["node", str(f)], cwd=str(NEW), capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env={**os.environ, "PYTHONUTF8": "1"})
    line = [x for x in (r.stdout or "").splitlines() if x.strip().startswith("[")][-1]
    return {d["id"]: d["t"] for d in json.loads(line)}


def grab(film, at, out):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{at:g}", "-i", str(film),
                    "-frames:v", "1", "-vf", "scale=760:-1", str(out)],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
    return out.exists()


def main():
    pages = sys.argv[1:] or ["01", "05", "15", "18", "21", "23"]
    oldfilm = OLD / "out" / "成片.mp4"
    newfilm = NEW / "out" / "emotion-full-无字幕.mp4"
    if not oldfilm.exists() or not newfilm.exists():
        sys.exit(f"缺成片：{oldfilm.exists()=} {newfilm.exists()=}")
    ot, nt = old_times(), new_times()
    WORK.mkdir(parents=True, exist_ok=True)
    from PIL import Image
    rows = []
    for pid in pages:
        a, b = WORK / f"old-{pid}.png", WORK / f"new-{pid}.png"
        if not grab(oldfilm, ot[pid], a) or not grab(newfilm, nt["p" + pid], b):
            print(f"  {pid} 抽帧失败，跳过")
            continue
        ims = [Image.open(a).convert("RGB"), Image.open(b).convert("RGB")]
        w = max(i.width for i in ims)
        h = sum(i.height for i in ims) + 8
        row = Image.new("RGB", (w, h), (25, 25, 25))
        row.paste(ims[0], (0, 0))
        row.paste(ims[1], (0, ims[0].height + 8))
        rows.append(row)
        print(f"  {pid} ✓（旧 {ot[pid]:.1f}s / 新 {nt['p' + pid]:.1f}s）")
    if not rows:
        sys.exit("一张都没拼出来")
    per_row = 3
    cw = max(r.width for r in rows)
    ch = max(r.height for r in rows)
    groups = [rows[i:i + per_row] for i in range(0, len(rows), per_row)]
    W = per_row * cw + 8 * (per_row + 1)
    H = len(groups) * ch + 8 * (len(groups) + 1)
    sheet = Image.new("RGB", (W, H), (25, 25, 25))
    for ri, group in enumerate(groups):
        for ci, r in enumerate(group):
            sheet.paste(r, (8 + ci * (cw + 8), 8 + ri * (ch + 8)))
    out = NEW / "docs" / "新旧对比.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=88)
    print("对比图：", out.relative_to(ROOT))


if __name__ == "__main__":
    main()
