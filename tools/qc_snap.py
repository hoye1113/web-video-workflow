"""抽帧验收：把整片按页抽 3 帧，拼成对照表（一张 13 页，好一眼过）。

用的是引擎自己的 snap.mjs（时间轴是真的：带配音时按真实语速算）。

用法：
    python tools/qc_snap.py            # 出 out/snap/qc1.jpg qc2.jpg（13 页一张）
    python tools/qc_snap.py --subs     # 带上字幕一起看（核字幕带有没有被挡）
"""
import json
import os
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
EP = ROOT / "projects" / "emotion-full"
ENGINE = ROOT / "experiments" / "frametell-src" / "frametell-main" / "packages" / "engine"

TIMES_JS = """
import { loadEpisode } from '%s';
const { L } = loadEpisode();
const rows = L.pages.map((p) => ({ id: p.id, start: p.start, end: p.end }));
console.log(JSON.stringify({ duration: L.duration, pages: rows }));
""" % (str(ENGINE / "tools" / "lib.mjs").replace("\\", "/"))


def page_times():
    f = pathlib.Path(tempfile.gettempdir()) / "vf-pg-times.mjs"
    f.write_text(TIMES_JS, encoding="utf-8")
    r = subprocess.run(["node", str(f)], cwd=str(EP), capture_output=True, text=True,
                       encoding="utf-8", errors="replace",
                       env={**os.environ, "PYTHONUTF8": "1"})
    lines = [x for x in (r.stdout or "").splitlines() if x.strip().startswith("{")]
    if not lines:
        raise SystemExit(f"拿不到时间轴：\n{r.stdout}\n{r.stderr}")
    return json.loads(lines[-1])


def main():
    d = page_times()
    print(f'片长 {d["duration"]:.1f}s，{len(d["pages"])} 页')
    for i, half in enumerate((d["pages"][:13], d["pages"][13:]), 1):
        times = []
        for p in half:
            span = p["end"] - p["start"]
            times += [round(p["start"] + span * f, 2) for f in (0.22, 0.55, 0.85)]
        sheet = f"qc{i}"
        cmd = ["node", str(ENGINE / "tools" / "snap.mjs"), "--sheet", sheet]
        if "--subs" in sys.argv:
            cmd.append("--subs")
        cmd += [str(t) for t in times]
        print(f'  抽 {len(times)} 帧 → out/snap/{sheet}.jpg（{len(half)} 页）')
        r = subprocess.run(cmd, cwd=str(EP), capture_output=True, text=True,
                           encoding="utf-8", errors="replace",
                           env={**os.environ, "PYTHONUTF8": "1"})
        tail = (r.stdout or "").strip().splitlines()[-2:]
        print("   ", " / ".join(tail) or (r.stderr or "").strip()[-200:])


if __name__ == "__main__":
    main()
