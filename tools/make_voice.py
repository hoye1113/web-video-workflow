"""给一条片子配音：**整页连续合成 → 按词边界切成每条 cue** → voice.js。

为什么不是"一条 cue 合成一次"（旧做法，已废弃）：
  每条单独合成会让 **每一句重新起调**，句子之间还会各带一段首尾静音，
  拼起来就是"短句很碎 + 停顿很长"。用户听过成片后的原话：
  "TTS 说话有很明显的错误短句和比较长的说话停顿，希望句子连续读完，
   在逗号或句号处才正常停顿。"

现在的做法（**连续优先**）：
  ① 把一页的 cues **拼成一段连续文本**（标点都在 cue 末尾，拼起来就是自然句子）；
  ② 调一次 edge-tts → 一段自然语调的整页音频 + 逐词时间戳；
  ③ 按"这条 cue 的第一个词"到"下一条 cue 的第一个词"**切**出每条 cue 的音频
     （切点天然包含逗号/句号处那个停顿 → 只在标点处停，不会额外加静音）；
  ④ 每条 cue 记 d（切出来的长度）、o（起声在片段内的位置）、k（逐字起点）。

语速：基准 **+40%（约 1.4 倍）** —— 用户要求"以真人说话语速"，并给了 1.4 倍这个数。
时长拟合保留（±8% 微调），但**不再为了凑时长把语速降到很慢**。

用法：
    python tools/make_voice.py <片名>                 # 全部页（并按目标时长微调）
    python tools/make_voice.py <片名> p05 p06          # 只做指定页
    python tools/make_voice.py <片名> --rate 40        # 指定语速（百分比）
    python tools/make_voice.py <片名> --check
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
SRC = EP / "script-source.json"
AUDIO = EP / "audio"
VOICEJS = EP / "voice.js"
BRIDGE = (ROOT / "experiments" / "frametell-src" / "frametell-main" / "packages"
          / "voice" / "tools" / "edge-tts.py")
PY = pathlib.Path.home() / ".frametell" / "edge-venv" / "Scripts" / "python.exe"
LOCALBIN = pathlib.Path.home() / ".local" / "bin"

VOICE = "zh-CN-XiaoxiaoNeural"
PITCH = -2
RATE = 40          # **1.4 倍**（edge-tts 的 rate 是百分比：+40%）
RATE_MIN, RATE_MAX = 30, 55      # 拟合时允许的语速范围（不再慢到 1.0 倍以下）
LEAD = 0.08        # 切片时往前多留一点，别把字头切掉
FIT_TOL = 0.08     # 目标时长 ±8% 就算合格


def env():
    e = os.environ.copy()
    e["PATH"] = str(LOCALBIN) + os.pathsep + e.get("PATH", "")
    e["PYTHONUTF8"] = "1"
    e["PYTHONIOENCODING"] = "utf-8"
    return e


def run(cmd, timeout=180):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", env=env(), timeout=timeout)


def synth(text: str, mp3: pathlib.Path):
    """整段文本 → mp3 + 逐词时间戳。"""
    reqf = pathlib.Path(tempfile.gettempdir()) / "vf-tts-req.json"
    reqf.write_text(json.dumps({"text": text, "voice": VOICE, "rate": RATE,
                                "pitch": PITCH, "out": str(mp3)}, ensure_ascii=False),
                    encoding="utf-8")
    r = run([str(PY), str(BRIDGE), str(reqf)])
    lines = [x for x in (r.stdout or "").strip().splitlines() if x.startswith("{")]
    if not lines:
        raise RuntimeError(f"桥没吐 JSON：{(r.stdout or r.stderr)[:200]}")
    d = json.loads(lines[-1])
    if "error" in d:
        raise RuntimeError(f"合成失败：{d['error']}")
    return d["words"]


def dur_of(f: pathlib.Path) -> float:
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(f)])
    try:
        return round(float((r.stdout or "0").strip() or 0), 3)
    except Exception:                                          # noqa: BLE001
        return 0.0


def cut(src: pathlib.Path, dst: pathlib.Path, start: float, end: float):
    """从整页音频里切一段（48k 双声道）。"""
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(0.0, start):.3f}",
         "-to", f"{max(start + 0.25, end):.3f}", "-i", str(src),
         "-ar", "48000", "-ac", "2", str(dst)])


def page_entries(pid: str, cues):
    """一页 → 每条 cue 的音频与时间轴（整页合成、再切）。"""
    text = "".join(cues)
    mp3 = AUDIO / f"{pid}.full.mp3"
    words = synth(text, mp3)
    total = dur_of(mp3)
    if total <= 0:
        raise RuntimeError(f"{pid} 合成出来的音频是 0 秒")

    # 词 → 字符区间
    spans, pos = [], 0
    for w in words:
        wd = (w.get("word") or "")
        if not wd:
            continue
        idx = text.find(wd, pos)
        if idx < 0:
            continue
        spans.append((idx, idx + len(wd), float(w["startTime"]), float(w["endTime"])))
        pos = idx + len(wd)

    offs, c = [], 0
    for cu in cues:
        offs.append(c)
        c += len(cu)

    entries = []
    for i, cu in enumerate(cues):
        c0, c1 = offs[i], offs[i] + len(cu)
        starts = [s for (a, b, s, e) in spans if b > c0 and a < c1]
        if starts:
            s0 = min(starts)
        elif entries:                       # 纯标点：接在上一条后面
            s0 = entries[-1]["_end"]
        else:
            s0 = LEAD
        cut_start = max(0.0, s0 - LEAD)
        if i + 1 < len(cues):
            n0 = offs[i + 1]
            nxt = [s for (a, b, s, e) in spans if a >= n0]
            cut_end = min(nxt) if nxt else total
        else:
            cut_end = total
        cut_end = min(total, max(cut_end, cut_start + 0.3))

        wav = AUDIO / f"{pid}-{i}.wav"
        cut(mp3, wav, cut_start, cut_end)

        k = []
        for ci in range(c0, c1):
            w = next((x for x in spans if x[0] <= ci < x[1]), None)
            if w:
                a, b, ws, we = w
                frac = (ci - a) / max(1, (b - a))
                k.append(round(max(0.0, ws - cut_start + (we - ws) * frac), 3))
            else:
                k.append(round(max(0.0, s0 - cut_start), 3))
        entries.append({"t": cu, "f": f"audio/{wav.name}",
                        "d": round(dur_of(wav) or (cut_end - cut_start), 3),
                        "o": round(max(0.0, s0 - cut_start), 3),
                        "k": k, "r": RATE, "_end": cut_end})
    for e in entries:
        e.pop("_end", None)
    mp3.unlink(missing_ok=True)
    return entries


def resolve_voice(ep: pathlib.Path):
    def pick(path):
        try:
            d = json.loads(path.read_text(encoding="utf-8"))
        except Exception:                                      # noqa: BLE001
            return ""
        if path.name == "brief.json":
            return (d.get("speaker") or "").strip()
        v = d.get("voice") or {}
        return (v.get("speaker") or "").strip() if isinstance(v, dict) else ""

    for f in ("brief.json", "script-source.json"):
        s = pick(ep / f)
        if s:
            return s
    return VOICE


def target_seconds(ep: pathlib.Path):
    try:
        b = json.loads((ep / "brief.json").read_text(encoding="utf-8"))
        m = float(b.get("minutes") or 0)
        return m * 60 if m > 0 else None
    except Exception:                                          # noqa: BLE001
        return None


def main(argv):
    global VOICE, RATE
    if "--voice" in argv:
        VOICE = argv[argv.index("--voice") + 1]
    else:
        VOICE = resolve_voice(EP)
    if "--rate" in argv:
        RATE = float(argv[argv.index("--rate") + 1])
    raw = [a for a in argv[1:] if not a.startswith("-")]
    for flag in ("--voice", "--rate"):
        if flag in argv:
            v = argv[argv.index(flag) + 1]
            if v in raw:
                raw.remove(v)
    pages_want = raw[1:] if raw else []

    d = json.loads(SRC.read_text(encoding="utf-8"))
    pages = d["pages"]
    if "--check" in argv:
        tot = sum(len(p["cues"]) for p in pages)
        print(f'{len(pages)} 页 / {tot} 条 cue；音色 {VOICE} rate {RATE:+.0f}%（约 {1 + RATE / 100:.1f} 倍）')
        return

    AUDIO.mkdir(parents=True, exist_ok=True)

    def synthesize():
        cache = json.loads(VOICEJS.with_suffix(".cache.json").read_text(encoding="utf-8")) \
            if VOICEJS.with_suffix(".cache.json").exists() else {}
        todo_pages = 0
        for p in pages:
            if pages_want and p["id"] not in pages_want:
                continue
            keys = [f'{p["id"]}:{i}' for i in range(len(p["cues"]))]
            valid = all(k in cache and cache[k].get("t") == t and cache[k].get("r") == RATE
                        and (AUDIO / cache[k]["f"].split("/")[-1]).exists()
                        for k, t in zip(keys, p["cues"]))
            if valid and "--force" not in argv:
                continue
            todo_pages += 1
            print(f'  {p["id"]}（{len(p["cues"])} 条）整页合成…', flush=True)
            try:
                entries = page_entries(p["id"], p["cues"])
            except Exception as e:                             # noqa: BLE001
                print(f'    ✗ {p["id"]} 失败：{e}（这一页先跳过）', flush=True)
                continue
            for k, en in zip(keys, entries):
                cache[k] = en

        out_pages, missing = [], []
        for p in pages:
            cues = [cache.get(f'{p["id"]}:{i}') for i in range(len(p["cues"]))]
            if all(cues):
                out_pages.append(cues)
            else:
                out_pages.append([])
                missing.append(p["id"])
        VOICEJS.write_text(
            "/* 由 tools/make_voice.py 生成（音色 " + VOICE + "，语速 " + f"{RATE:+.0f}%"
            + "）：整页连续合成后按词边界切分。\n"
            " * 改了 cue 文字**必须重跑配音**，否则 t 对不上就不会生效。 */\n"
            "SCRIPT.VOICE = " + json.dumps({"speaker": VOICE, "provider": "edge",
                                            "pages": out_pages}, ensure_ascii=False) + ";\n",
            encoding="utf-8")
        VOICEJS.with_suffix(".cache.json").write_text(json.dumps(cache, ensure_ascii=False),
                                                      encoding="utf-8")
        total = sum(c["d"] for pg in out_pages for c in pg)
        print(f"写好 {VOICEJS.relative_to(ROOT)}：{len(out_pages)} 页 / 已配音 "
              f"{sum(1 for p in out_pages if p)} 页 / 语音共 {total / 60:.1f} 分钟"
              f"（本轮重做 {todo_pages} 页）")
        if missing:
            print("还没配音的页：" + " ".join(missing))
        return out_pages, missing, total

    out_pages, missing, total = synthesize()

    # ── 时长拟合：只微调语速（±8% 内），**不再为了凑时长把语速降慢** ──────────────
    target = target_seconds(EP)
    if target and not pages_want and not missing:
        for attempt in range(1, 3):
            ratio = total / target
            print(f"  配时第 {attempt} 轮：{total:.0f}s / 目标 {target:.0f}s（{ratio:.1%}），语速 {RATE:+.0f}%")
            if abs(ratio - 1) <= FIT_TOL:
                print("  ✓ 时长在目标 ±8% 内")
                break
            new_rate = ((1 + RATE / 100.0) * ratio - 1) * 100.0
            new_rate = max(RATE_MIN, min(RATE_MAX, round(new_rate, 1)))
            if abs(new_rate - RATE) < 0.8:
                print(f"  ⚠ 语速已到边界（{RATE:+.0f}%），再调没有意义 —— 想更长/更短要改文案字数")
                break
            print(f"  → 语速 {RATE:+.0f}% 改到 {new_rate:+.0f}%，整页重配")
            RATE = new_rate
            out_pages, missing, total = synthesize()
        try:
            b = json.loads((EP / "brief.json").read_text(encoding="utf-8"))
            b["rate"] = RATE
            b["audio_seconds"] = round(total, 1)
            (EP / "brief.json").write_text(json.dumps(b, ensure_ascii=False, indent=1), encoding="utf-8")
        except Exception:                                      # noqa: BLE001
            pass
    if missing:
        print("还没配音的页：" + " ".join(missing))


if __name__ == "__main__":
    main(sys.argv)
