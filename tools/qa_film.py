#!/usr/bin/env python3
"""成片体检：渲染前查 page-spec，渲染后查 mp4，输出 report.md + 证据图。

用法：
    python tools/qa_film.py film-1108-audio
    python tools/qa_film.py film-1108-audio --skip-motion     # 跳过逐页运动分析，快一些
    python tools/qa_film.py film-1108-audio --out E:/video-factory/1108/qa

检查分两段：
  pre   渲染前：缺图、无运镜、字太小、页长异常、cue 覆盖、素材文件、开场规则
  post  渲染后：尺寸/帧率/时长/帧数/音轨/黑帧/响度/真峰值 + 逐页运动 + 手机尺寸图

结果分四级：PASS / WARN / FAIL / INFO。只有 FAIL 会让退出码变成 1。
WARN 是“值得看一眼”的问题，不阻塞交付。
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ENGINE = ROOT / "experiments" / "frametell-src" / "frametell-main" / "packages" / "engine"
SCENE_LIB = ROOT / "projects" / "scene-library"
STAGE_W, STAGE_H = 1440, 1080
TARGET_LUFS = -14.0
LUFS_TOL = 1.5


def find_tool(name):
    env = os.environ.get(name.upper())
    if env and Path(env).exists():
        return str(env)
    hit = shutil.which(name)
    if hit:
        return hit
    pats = [
        rf"C:\Users\*\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_*\ffmpeg-*\bin\{name}.exe",
        rf"C:\Program Files\ffmpeg*\bin\{name}.exe",
        rf"C:\ffmpeg\bin\{name}.exe",
    ]
    for pat in pats:
        hits = sorted(glob.glob(pat))
        if hits:
            return hits[-1]
    return name


FFMPEG = find_tool("ffmpeg")
FFPROBE = find_tool("ffprobe")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_CN = Path(r"C:\Windows\Fonts\msyhbd.ttc")


def run(cmd, timeout=600, cwd=None):
    r = subprocess.run([str(x) for x in cmd], capture_output=True, timeout=timeout, cwd=cwd)
    return r.returncode, r.stdout, r.stderr.decode("utf-8", "replace") if isinstance(r.stderr, bytes) else str(r.stderr)


def probe(film):
    code, out, err = run([FFPROBE, "-v", "error", "-print_format", "json",
                          "-show_format", "-show_streams", "-count_packets", str(film)])
    if code != 0:
        raise RuntimeError(f"ffprobe 读不了 {film}: {err.strip().splitlines()[-1] if err.strip() else code}")
    j = json.loads(out.decode("utf-8", "replace"))
    vs = next((s for s in j["streams"] if s.get("codec_type") == "video"), None)
    if not vs:
        raise RuntimeError(f"{film} 没有视频流")
    num, den = (vs.get("r_frame_rate") or "0/1").split("/")
    fps = float(num) / float(den) if float(den) else 0.0
    frames = int(vs.get("nb_read_packets") or vs.get("nb_frames") or 0)
    return {
        "duration": float(j["format"]["duration"]),
        "w": int(vs["width"]),
        "h": int(vs["height"]),
        "fps": fps,
        "frames": frames,
        "audio": any(s.get("codec_type") == "audio" for s in j["streams"]),
    }


def page_times(ep):
    """从引擎拿真实页时间；失败则返回 None。"""
    js = """
import { loadEpisode } from '%s';
const { L } = loadEpisode();
console.log(JSON.stringify({ duration: L.duration,
  pages: L.pages.map((p) => ({ id: p.id, start: p.start, end: p.end })) }));
""" % (ENGINE / "tools" / "lib.mjs").as_uri()
    f = Path(tempfile.gettempdir()) / "vf-qa-times.mjs"
    f.write_text(js, encoding="utf-8")
    try:
        code, out, err = run(["node", str(f)], timeout=120, cwd=str(ep))
    except Exception:
        return None
    lines = [x for x in out.decode("utf-8", "replace").splitlines() if x.strip().startswith("{")]
    if code != 0 or not lines:
        return None
    return json.loads(lines[-1])


def parse_voice(ep):
    p = ep / "voice.js"
    if not p.exists():
        return None
    raw = p.read_text(encoding="utf-8")
    a = raw.find("SCRIPT.VOICE")
    a = raw.find("{", a if a >= 0 else 0)
    b = raw.rfind("}")
    if a < 0 or b < 0:
        return None
    try:
        return json.loads(raw[a:b + 1])
    except Exception:
        return None


def extract_frame(film, t, out, width):
    code, _, err = run([FFMPEG, "-y", "-v", "error", "-ss", f"{max(0.0, t):.3f}",
                        "-i", str(film), "-frames:v", "1",
                        "-vf", f"scale={width}:-2", str(out)])
    return code == 0 and out.exists()


def make_grid(film, times, out, cell_w, cols, labels=None, title=None):
    rows = (len(times) + cols - 1) // cols
    cell_h = round(cell_w * 9 / 16)
    pad = 6
    header = 34 if title else 0
    sheet = Image.new("RGB", (cols * cell_w + (cols + 1) * pad, header + rows * cell_h + (rows + 1) * pad), (24, 24, 24))
    dr = ImageDraw.Draw(sheet)
    font_path = FONT_CN if FONT_CN.exists() else FONT_BOLD
    font = ImageFont.truetype(str(font_path), 16) if font_path.exists() else ImageFont.load_default()
    if title:
        dr.text((pad, 8), title, font=font, fill=(240, 236, 228))
    tmp = out.parent / "_tmp_frame.png"
    for i, t in enumerate(times):
        if not extract_frame(film, t, tmp, cell_w):
            continue
        im = Image.open(tmp).convert("RGB")
        im = im.resize((cell_w, cell_h), Image.LANCZOS)
        x = pad + (i % cols) * (cell_w + pad)
        y = header + pad + (i // cols) * (cell_h + pad)
        sheet.paste(im, (x, y))
        if labels:
            txt = labels[i]
            tb = dr.textbbox((0, 0), txt, font=font)
            tw = tb[2] - tb[0]
            dr.rectangle([x, y, x + tw + 8, y + 24], fill=(24, 24, 24))
            dr.text((x + 4, y + 3), txt, font=font, fill=(255, 214, 120))
    tmp.unlink(missing_ok=True)
    sheet.save(out, quality=92)
    return out


def black_frames(film):
    code, out, err = run([FFMPEG, "-hide_banner", "-nostats", "-i", str(film),
                          "-vf", "blackdetect=d=0.04:pix_th=0.06", "-an", "-f", "null", "NUL"])
    txt = (out or b"").decode("utf-8", "replace") + err
    return [(float(a), float(b)) for a, b in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", txt)]


def loudness(film):
    code, out, err = run([FFMPEG, "-hide_banner", "-nostats", "-i", str(film), "-vn",
                          "-af", "ebur128=peak=true", "-f", "null", "NUL"], timeout=900)
    txt = (out or b"").decode("utf-8", "replace") + err
    summary = txt[txt.rfind("Summary:"):] if "Summary:" in txt else txt
    m = re.search(r"I:\s+(-?[\d.]+)\s+LUFS", summary)
    p = re.search(r"Peak:\s+(-?(?:[\d.]+|inf))\s+dBFS", summary)
    i = float(m.group(1)) if m else float("nan")
    tp = float(p.group(1).replace("inf", "Infinity")) if p else float("nan")
    return i, tp


def page_frames(film, start, dur, fps=4, w=320):
    code, out, err = run([FFMPEG, "-v", "error", "-ss", f"{max(0.0, start):.3f}",
                          "-t", f"{max(0.1, dur):.3f}", "-i", str(film),
                          "-vf", f"fps={fps},scale={w}:180:flags=area,format=gray",
                          "-f", "rawvideo", "-pix_fmt", "gray", "-"], timeout=120)
    size = w * 180
    n = len(out) // size if out else 0
    if n <= 0:
        return None
    return np.frombuffer(out[:n * size], dtype=np.uint8).reshape(n, 180, w)


def motion_one(film, start, dur):
    frames = page_frames(film, start, dur)
    if frames is None or len(frames) < 3:
        return None
    a = frames.astype(np.int16)
    # 0.5s window (fps=4 -> lag 2)
    lag2 = [float((np.abs(a[i + 2] - a[i]) > 8).mean()) for i in range(len(a) - 2)]
    # 0.25s window for still runs
    lag1 = [float((np.abs(a[i + 1] - a[i]) > 8).mean()) for i in range(len(a) - 1)]
    still = sum(1 for x in lag1 if x < 0.001)
    runmax = cur = 0
    for x in lag1:
        cur = cur + 1 if x < 0.001 else 0
        runmax = max(runmax, cur)
    flashes = 0
    for i in range(1, len(a) - 1):
        dp = float((np.abs(a[i] - a[i - 1]) > 8).mean())
        dn = float((np.abs(a[i + 1] - a[i]) > 8).mean())
        ds = float((np.abs(a[i + 1] - a[i - 1]) > 8).mean())
        if dp > 0.02 and dn > 0.02 and ds < 0.01:
            flashes += 1
    return {
        "max": max(lag2) if lag2 else 0.0,
        "median": float(np.median(lag2)) if lag2 else 0.0,
        "still_steps": still,
        "still_sec": round(runmax * 0.25, 2),
        "flashes": flashes,
        "frames": len(frames),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--out", default=None)
    ap.add_argument("--skip-motion", action="store_true")
    args = ap.parse_args()

    proj = args.project.strip().strip("/\\")
    ep = ROOT / "projects" / proj
    if not ep.exists():
        sys.exit(f"工程不存在：{ep}")
    qa = Path(args.out) if args.out else ep / "qa"
    qa.mkdir(parents=True, exist_ok=True)

    spec_p = ep / "page-spec.json"
    if not spec_p.exists():
        sys.exit(f"找不到 {spec_p}")
    spec = json.loads(spec_p.read_text(encoding="utf-8"))

    times = page_times(ep)
    voice = parse_voice(ep)
    film = ep / "out" / f"{proj}-无字幕.mp4"
    if not film.exists():
        cands = sorted((ep / "out").glob("*.mp4")) if (ep / "out").exists() else []
        film = cands[-1] if cands else None
    film_exists = film is not None and film.exists()

    rows = []  # {level, area, name, detail}
    def add(level, area, name, detail=""):
        rows.append({"level": level, "area": area, "name": name, "detail": detail})

    # ── pre ──────────────────────────────────────────────
    n_pages = len(spec)
    tl_pages = (times or {}).get("pages") or []
    if tl_pages:
        add("PASS" if len(tl_pages) == n_pages else "FAIL", "pre", "页数",
            f"spec {n_pages} / 时间轴 {len(tl_pages)}")
    else:
        add("WARN", "pre", "页数", "拿不到引擎时间轴，只能按 spec 检查")

    missing, wrong_size, no_cam, bad_theme = [], [], [], []
    text_small, text_out = [], []
    dark_starts = 0
    for p in spec:
        pid = p.get("id", "?")
        asset = p.get("asset") or ""
        apath = SCENE_LIB / asset if asset else None
        if not apath or not apath.exists():
            missing.append(f"{pid}:{asset or '(空)'}")
        else:
            try:
                with Image.open(apath) as im:
                    if im.size != (STAGE_W, STAGE_H):
                        wrong_size.append(f"{pid}:{im.size[0]}x{im.size[1]}")
            except Exception:
                wrong_size.append(f"{pid}:读不了")
        cam = p.get("cam")
        if not cam:
            no_cam.append(pid)
        theme = p.get("theme", "day")
        if theme not in ("day", "night"):
            bad_theme.append(f"{pid}:{theme}")
        rv = p.get("reveal") or [1, 1]
        if float(rv[0]) < 0.5:
            dark_starts += 1
        for t in p.get("texts") or []:
            if len(t) < 7:
                continue
            txt, x, y, size = t[0], float(t[1]), float(t[2]), float(t[3])
            if size < STAGE_H * 0.04:
                text_small.append(f"{pid}:{txt}:{size:g}px")
            if not (0 <= x <= STAGE_W and 0 <= y <= STAGE_H):
                text_out.append(f"{pid}:{txt}@({x:g},{y:g})")

    add("FAIL" if missing else "PASS", "pre", "图片齐全",
        f"缺 {len(missing)} 张" + ("：" + "、".join(missing[:6]) if missing else ""))
    add("WARN" if wrong_size else "PASS", "pre", "图片尺寸",
        f"{len(wrong_size)} 张不是 1440×1080" + ("：" + "、".join(wrong_size[:6]) if wrong_size else "") +
        ("；渲染时会放大" if wrong_size else ""))
    add("FAIL" if no_cam else "PASS", "pre", "每页有运镜",
        f"{len(no_cam)} 页没写 cam" + ("：" + "、".join(no_cam) if no_cam else ""))
    beat_pages = [p for p in spec if p.get("cam") == "beat"]
    if beat_pages:
        missing_beat = [p["id"] for p in beat_pages if p.get("beatAt") is None]
        bad_beat = []
        for p in beat_pages:
            if p.get("beatAt") is None:
                continue
            dur = next((x["end"] - x["start"] for x in tl_pages if x["id"] == p["id"]), None)
            if dur is not None and not (0 <= float(p["beatAt"]) < dur):
                bad_beat.append(f'{p["id"]}:{float(p["beatAt"]):.2f}s/{dur:.1f}s')
        beat_times = " / ".join(f'{p["id"]} {float(p["beatAt"]):.2f}s' for p in beat_pages if p.get("beatAt") is not None)
        add("WARN" if missing_beat or bad_beat else "PASS", "pre", "重拍时间",
            (f"{len(beat_pages)} 页重拍" + (f"：{beat_times}" if beat_times else "")) +
            ("；缺 beatAt：" + "、".join(missing_beat) if missing_beat else "") +
            ("；落点超出页长：" + "、".join(bad_beat) if bad_beat else ""))
    else:
        add("INFO", "pre", "重拍时间", "没有 cam=beat 的页面")
    add("WARN" if bad_theme else "PASS", "pre", "主题值",
        f"{len(bad_theme)} 页主题不认识" + ("：" + "、".join(bad_theme) if bad_theme else "（day/night 合法）"))
    visuals = [p.get("visual") for p in spec]
    if any(visuals):
        runs = [f'{spec[i]["id"]}–{spec[i+2]["id"]}:{visuals[i]}' for i in range(len(visuals) - 2)
                if visuals[i] and visuals[i] == visuals[i + 1] == visuals[i + 2]]
        counts = {}
        for v in visuals:
            if v:
                counts[v] = counts.get(v, 0) + 1
        top = " / ".join(f"{k} {v}" for k, v in sorted(counts.items(), key=lambda x: -x[1]))
        add("WARN" if runs else "PASS", "pre", "画面类型",
            f"连续 3 页同类型 {len(runs)} 处" + ("：" + "、".join(runs) if runs else f"（{top}）"))
    else:
        add("INFO", "pre", "画面类型", "page-spec 没有 visual 字段，跳过类型轮换检查")
    add("WARN" if text_small else "PASS", "pre", "标签字号",
        f"{len(text_small)} 处 < 4% 画面高（43.2px）" + ("：" + "、".join(text_small[:6]) if text_small else "（全部 ≥43.2px）"))
    add("WARN" if text_out else "PASS", "pre", "文字位置",
        f"{len(text_out)} 处出画" + ("：" + "、".join(text_out[:6]) if text_out else "（都在画面内）"))

    dark_ratio = dark_starts / n_pages if n_pages else 0
    add("WARN" if dark_ratio > 0.8 else "PASS", "pre", "页间亮度起点",
        f"{dark_starts}/{n_pages} 页 reveal 从 <0.5 起" + ("；硬切时新页会先暗后亮" if dark_ratio > 0.8 else ""))

    if spec:
        p1 = spec[0]
        rv = p1.get("reveal") or [1, 1]
        first_text = min([float(t[6]) for t in (p1.get("texts") or []) if len(t) >= 7], default=999)
        hook_bad = float(rv[0]) < 0.6 or first_text > 0.8
        add("WARN" if hook_bad else "PASS", "pre", "开场 1 秒",
            f"p01 亮度从 {float(rv[0]):g} 起，首字 {first_text:g}s" +
            ("；前 1 秒偏暗/无字" if hook_bad else "；有画面有字"))

    if tl_pages:
        durs = [p["end"] - p["start"] for p in tl_pages]
        short = [f'{p["id"]}:{d:.1f}s' for p, d in zip(tl_pages, durs) if d < 3.0]
        long = [f'{p["id"]}:{d:.1f}s' for p, d in zip(tl_pages, durs) if d > 10.0]
        add("WARN" if short or long else "PASS", "pre", "页长",
            f"最短 {min(durs):.1f}s / 最长 {max(durs):.1f}s" +
            ("；短页 " + "、".join(short[:5]) if short else "") +
            ("；长页 " + "、".join(long[:5]) if long else ""))

    if voice and isinstance(voice.get("pages"), list):
        vp = voice["pages"]
        if tl_pages and len(vp) != len(tl_pages):
            add("FAIL", "pre", "cue 页数", f"voice {len(vp)} / 时间轴 {len(tl_pages)}")
        bad_sum, missing_audio = [], []
        for i, cues in enumerate(vp):
            pid = tl_pages[i]["id"] if i < len(tl_pages) else f"p{i+1:02d}"
            s = sum(float(c.get("d", 0)) for c in cues)
            if tl_pages and i < len(tl_pages):
                want = tl_pages[i]["end"] - tl_pages[i]["start"]
                if abs(s - want) > 0.35:
                    bad_sum.append(f"{pid}:{s:.1f}/{want:.1f}")
            for c in cues:
                f = c.get("f")
                if f and not (ep / f).exists():
                    missing_audio.append(f"{pid}:{f}")
        total_cue = sum(float(c.get("d", 0)) for cues in vp for c in cues)
        add("PASS" if not bad_sum else "WARN", "pre", "cue 与页长",
            f"{len(bad_sum)} 页对不上" + ("：" + "、".join(bad_sum[:6]) if bad_sum else f"（总 cue {total_cue:.1f}s）"))
        if tl_pages and vp:
            last, last_cues = tl_pages[-1], vp[-1]
            tail = (last["end"] - last["start"]) - sum(float(c.get("d", 0)) for c in last_cues)
            if tail > 0.5:
                add("INFO", "pre", "结尾留白",
                    f'{last["id"]} 末尾 {tail:.1f}s 无口播，确认是否刻意留白')
        add("FAIL" if missing_audio else "PASS", "pre", "切音频齐全",
            f"缺 {len(missing_audio)} 段" + ("：" + "、".join(missing_audio[:5]) if missing_audio else "全部存在"))
    else:
        add("WARN", "pre", "cue 检查", "读不到 voice.js")

    # ── post ─────────────────────────────────────────────
    info = None
    if not film_exists:
        add("INFO", "post", "成片", "out/ 里还没有 mp4，这次只跑 pre 检查")
    else:
        try:
            info = probe(film)
            add("PASS", "post", "可解码", f'{info["frames"]} 帧 / {info["duration"]:.2f}s')
            ok_size = (info["w"], info["h"]) == (STAGE_W, STAGE_H)
            add("PASS" if ok_size else "FAIL", "post", "尺寸", f'{info["w"]}×{info["h"]}（期望 1440×1080）')
            ok_fps = abs(info["fps"] - 60) < 0.01
            add("PASS" if ok_fps else "FAIL", "post", "帧率", f'{info["fps"]:.2f}fps（期望 60）')
            if times:
                want = float(times["duration"])
                ok_dur = abs(info["duration"] - want) <= 0.15
                add("PASS" if ok_dur else "FAIL", "post", "时长", f'{info["duration"]:.2f}s（时间轴 {want:.2f}s）')
                want_frames = round(want * info["fps"])
                ok_frames = abs(info["frames"] - want_frames) <= 2
                add("PASS" if ok_frames else "FAIL", "post", "帧数",
                    f'{info["frames"]}（期望 {want_frames}）')
            add("PASS" if info["audio"] else "FAIL", "post", "音轨", "有" if info["audio"] else "没有")
            blacks = black_frames(film)
            add("PASS" if not blacks else "FAIL", "post", "黑帧",
                "无" if not blacks else "、".join(f"{a:.2f}-{b:.2f}s" for a, b in blacks[:6]))
            i, tp = loudness(film)
            if np.isnan(i):
                add("WARN", "post", "响度", "测不出来")
            else:
                ok = (TARGET_LUFS - LUFS_TOL) <= i <= (TARGET_LUFS + LUFS_TOL)
                far = i < TARGET_LUFS - 4 or i > TARGET_LUFS + 4
                add("PASS" if ok else ("FAIL" if far else "WARN"), "post", "响度",
                    f"{i:.1f} LUFS（目标 {TARGET_LUFS:g}±{LUFS_TOL:g}）" +
                    ("" if ok else ("；建议 gain " + f"{TARGET_LUFS - i:+.1f} dB")))
            if not np.isnan(tp):
                add("PASS" if tp <= -1.0 else "FAIL", "post", "真峰值", f"{tp:.1f} dBTP（≤ -1）")
        except Exception as e:
            add("FAIL", "post", "成片检查", f"{type(e).__name__}: {e}")

    # ── motion ───────────────────────────────────────────
    motion = []
    if film_exists and times and not args.skip_motion:
        for p in times["pages"]:
            m = motion_one(film, p["start"], p["end"] - p["start"])
            if m:
                m["id"] = p["id"]
                m["dur"] = p["end"] - p["start"]
                motion.append(m)
        if motion:
            for m in motion:
                if m["max"] < 0.001:
                    m["grade"] = "static"
                elif m["max"] < 0.005:
                    m["grade"] = "low"
                elif m["median"] < 0.001 and m["still_sec"] >= 2.0:
                    m["grade"] = "pulse"
                else:
                    m["grade"] = "moving"
            static = [m for m in motion if m["grade"] == "static"]
            pulse = [m for m in motion if m["grade"] == "pulse"]
            low = [m for m in motion if m["grade"] == "low"]
            moving = [m for m in motion if m["grade"] == "moving"]
            flashes = [m for m in motion if m["flashes"] > 0]
            add("WARN" if (len(static) / len(motion) > 0.25 or flashes) else "PASS", "post", "逐页运动",
                f"完全不动 {len(static)}/{len(motion)} 页；单次推镜+长静止 {len(pulse)} 页；"
                f"连续运动 {len(moving)} 页；闪帧 {len(flashes)} 页")
            if pulse:
                stills = sorted(m["still_sec"] for m in pulse)
                add("INFO", "post", "运动结构",
                    f"多数页是「一次推镜 + {stills[len(stills)//2]:.1f}s 静止」；"
                    "不是连续运动，确认是否符合这种讲述节奏")
            with (qa / "motion.csv").open("w", encoding="utf-8-sig", newline="") as f:
                f.write("page,dur_s,max_change_pct,median_pct,still_steps,longest_still_s,flashes,grade\n")
                for m in motion:
                    f.write(f'{m["id"]},{m["dur"]:.2f},{m["max"]*100:.2f},{m["median"]*100:.2f},'
                            f'{m["still_steps"]},{m["still_sec"]:.2f},{m["flashes"]},{m["grade"]}\n')

    # ── evidence images ──────────────────────────────────
    arts = []
    if film_exists:
        dur = info["duration"] if info else (times or {}).get("duration", 0)
        if dur:
            if times:
                pages = times["pages"]
                times_cs = [p["start"] + (p["end"] - p["start"]) * 0.55 for p in pages]
                labels = [p["id"] for p in pages]
            else:
                n = 48 if len(spec) >= 40 else 24
                times_cs = [dur * (i + 0.5) / n for i in range(n)]
                labels = [f"{i+1:02d}" for i in range(n)]
            arts.append(make_grid(film, times_cs, qa / "contact-sheet.png", 300, 6,
                                  labels=labels, title=f"{proj} · {dur:.1f}s · {len(times_cs)} 格"))
            phone_n = 12
            if times and len(times["pages"]) >= phone_n:
                pages = times["pages"]
                idx = sorted(set(round(i * (len(pages) - 1) / (phone_n - 1)) for i in range(phone_n)))
                phone_times = [pages[j]["start"] + (pages[j]["end"] - pages[j]["start"]) * 0.55 for j in idx]
                phone_labels = [pages[j]["id"] for j in idx]
            else:
                phone_times = [dur * (i + 0.5) / phone_n for i in range(phone_n)]
                phone_labels = [f"{t:.0f}s" for t in phone_times]
            arts.append(make_grid(film, phone_times, qa / "phone-sheet.png", 320, 4,
                                  labels=phone_labels,
                                  title="手机尺寸预览（320px 宽）"))
            open_n = 16
            open_times = [i * 0.1 for i in range(open_n)]
            arts.append(make_grid(film, open_times, qa / "opening-strip.png", 240, 4,
                                  labels=[f"{t:.1f}s" for t in open_times],
                                  title="开场 0–1.5s（每 0.1s 一帧）"))
            if times and len(times["pages"]) > 1:
                b0 = max(0, times["pages"][1]["start"] - 0.6)
                btimes = [b0 + i * 0.1 for i in range(16)]
                arts.append(make_grid(film, btimes, qa / "boundary-strip.png", 240, 4,
                                      labels=[f"{t:.1f}s" for t in btimes],
                                      title="p01→p02 接缝（每 0.1s 一帧）"))

    # ── report ───────────────────────────────────────────
    fails = [r for r in rows if r["level"] == "FAIL"]
    warns = [r for r in rows if r["level"] == "WARN"]
    passes = [r for r in rows if r["level"] == "PASS"]
    infos = [r for r in rows if r["level"] == "INFO"]
    lines = []
    lines.append(f"# 成片体检 · {proj}")
    lines.append("")
    lines.append(f"- 成片：`{film}`" if film_exists else "- 成片：还没渲染（只跑 pre 检查）")
    lines.append(f"- 规格：{STAGE_W}×{STAGE_H} / 60fps / {n_pages} 页")
    if info:
        lines.append(f'- 实测：{info["w"]}×{info["h"]} / {info["fps"]:.0f}fps / '
                     f'{info["duration"]:.1f}s / {info["frames"]} 帧')
    tail = f" / {len(infos)} INFO" if infos else ""
    lines.append(f"- 结论：**{len(passes)} PASS / {len(warns)} WARN / {len(fails)} FAIL{tail}**")
    lines.append("")
    if fails:
        lines.append("## 先修这些（FAIL）")
        lines.append("")
        for r in fails:
            lines.append(f"- **{r['name']}**：{r['detail']}")
        lines.append("")
    if warns:
        lines.append("## 值得看一眼（WARN）")
        lines.append("")
        for r in warns:
            lines.append(f"- **{r['name']}**：{r['detail']}")
        lines.append("")
    if infos:
        lines.append("## 信息")
        lines.append("")
        for r in infos:
            lines.append(f"- **{r['name']}**：{r['detail']}")
        lines.append("")

    advice = []
    names = {r["name"] for r in warns} | {r["name"] for r in infos}
    if "图片尺寸" in names:
        advice.append("图片先放大到 1440×1080 再渲染（Lanczos 或 Real-ESRGAN），不要在浏览器里直接放大。")
    if "页间亮度起点" in names:
        advice.append("中间页 reveal 起点从 0.3 提到 0.65；只有段落切换保留 0.3，避免每 6 秒暗一下。")
    if "开场 1 秒" in names:
        advice.append("p01 直接满亮度起，首字 0.2–0.4s，推镜 0.3s 起；前 1 秒是短视频最贵的一秒。")
    if "cue 与页长" in names or "结尾留白" in names:
        last_id = spec[-1].get("id", "最后一页") if spec else "最后一页"
        advice.append(f"{last_id} 末尾约 1s 无口播，确认是否刻意留白；不是就补内容或缩短页长。")
    if "响度" in names:
        advice.append("最终封装加 +2 dB，或用 loudnorm 归一到 -14 LUFS / -1 dBTP。")
    if "运动结构" in names:
        advice.append("现在是「一次推镜 + 2.8–3.8s 静止」；要更活，把推镜对齐该页关键词，或关键页用 inset/alt 图加第二拍。")
    if "逐页运动" in names:
        advice.append("有整页完全不动或闪帧，先看 motion.csv 和连续帧，再决定补运动还是修穿帮。")
    if advice:
        lines.append("## 下一步建议")
        lines.append("")
        for a in advice:
            lines.append(f"- {a}")
        lines.append("")

    lines.append("## 检查明细")
    lines.append("")
    lines.append("| 段 | 项 | 结果 | 说明 |")
    lines.append("|---|---|---|---|")
    for r in rows:
        lines.append(f"| {r['area']} | {r['name']} | {r['level']} | {r['detail']} |")
    lines.append("")
    if motion:
        worst = sorted(motion, key=lambda m: (-m["still_sec"], m["median"]))[:12]
        lines.append("## 运动最静的 12 页")
        lines.append("")
        lines.append("| 页 | 页长 | 0.5s 最大变化 | 中位变化 | 最长静止 | 判定 |")
        lines.append("|---|---:|---:|---:|---:|---|")
        for m in worst:
            lines.append(f'| {m["id"]} | {m["dur"]:.1f}s | {m["max"]*100:.2f}% | '
                         f'{m["median"]*100:.2f}% | {m["still_sec"]:.1f}s | {m["grade"]} |')
        lines.append("")
        lines.append("> `pulse` = 有一次明显运动，但中位变化 0%、最长静止 ≥2s（停-推-停）；"
                     "`static` = 整页 0.5s 窗口内变化 <0.1%；`low` = 最大变化 <0.5%；`moving` = 其余。"
                     f"完整 {len(motion)} 页数据在 `motion.csv`。")
        lines.append("")
    if arts:
        lines.append("## 证据图")
        lines.append("")
        for a in arts:
            lines.append(f"- `{a.name}`")
        lines.append("")
    lines.append("## 说明")
    lines.append("")
    lines.append("- FAIL 必须修；WARN 是建议，不阻塞交付。")
    lines.append("- 运动指标按 0.5 秒窗口算，适配 60fps 慢推，不会把缓慢运镜误判成冻结。")
    lines.append("- 这项检查看的是文件、节奏、可读性和运动，不判断故事和角色好不好。")
    lines.append("")
    report = qa / "report.md"
    report.write_text("\n".join(lines), encoding="utf-8")

    print(f"报告：{report}")
    print(f"结论：{len(passes)} PASS / {len(warns)} WARN / {len(fails)} FAIL" +
          (f" / {len(infos)} INFO" if infos else ""))
    for r in fails:
        print(f"  FAIL  {r['name']}: {r['detail']}")
    for r in warns:
        print(f"  WARN  {r['name']}: {r['detail']}")
    if motion:
        counts = {g: sum(1 for m in motion if m["grade"] == g) for g in ("static", "pulse", "low", "moving")}
        print(f'运动：static {counts["static"]} / pulse {counts["pulse"]} / '
              f'low {counts["low"]} / moving {counts["moving"]} / '
              f'闪帧 {sum(1 for m in motion if m["flashes"])} 页')
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
