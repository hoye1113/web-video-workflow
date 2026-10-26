"""用**用户自己录的音频**做成片：转写 → 分页 → 切音频 → 写 script.js / voice.js。

和 TTS 的 `make_voice.py` 的区别：
  - 不合成，只**切**：每页/每条 cue 的音频都是从原音频里切出来的（音色、语速原样）；
  - 时间轴 = 原音频的时间轴：`META.pace = {lead:0, gap:0, maxHold:0}`，
    所以成片音轨就是原音频（顺序不变、不加静音），字幕按原音频对齐。

用法：
    python tools/audio_film.py <片名> <transcript.json> <audio.wav>
        [--page-chars 33] [--page-sec 6.2] [--max-cue 20]

输入 transcript.json：tools/transcribe.py 的产出（segments: [{start,end,text}]）。
"""
import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUNCT = "，。！？；：、,.!?;:"


def run(cmd, timeout=120):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=timeout)


def dur_of(f):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(f)])
    try:
        return round(float((r.stdout or "0").strip() or 0), 3)
    except Exception:                                          # noqa: BLE001
        return 0.0


def tidy(t):
    t = (t or "").strip()
    t = t.replace(" ", "")
    return t


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("transcript")
    ap.add_argument("audio")
    ap.add_argument("--page-chars", type=int, default=33)
    ap.add_argument("--page-sec", type=float, default=6.2)
    ap.add_argument("--max-cue", type=int, default=20)
    a = ap.parse_args(argv[1:])

    proj = a.project
    d = ROOT / "projects" / proj
    if not d.exists():
        sys.exit(f"没有工程目录：{d}（先 tools/new_film.py {proj}）")

    tr = json.loads(pathlib.Path(a.transcript).read_text(encoding="utf-8"))
    segs = [s for s in tr.get("segments", []) if tidy(s.get("text"))]
    if not segs:
        sys.exit("转写里没有可用段落")

    audio = pathlib.Path(a.audio)
    total = dur_of(audio) or float(tr.get("duration") or 0)
    ADIR = d / "audio"
    ADIR.mkdir(parents=True, exist_ok=True)

    # 段落 → cue（太短的并到前一条，太长的保留——切音频只能按段边界）
    cues = []
    for s in segs:
        t = tidy(s["text"])
        if cues and len(t) <= 3 and not cues[-1]["text"].endswith(tuple("。！？")):
            cues[-1]["text"] += t
            cues[-1]["end"] = float(s["end"])
            continue
        cues.append({"text": t, "start": float(s["start"]), "end": float(s["end"])})

    # cue 的切点：下一条的开始（连续，不留缝）；最后一条到音频结尾
    for i, c in enumerate(cues):
        c["cut_end"] = cues[i + 1]["start"] if i + 1 < len(cues) else total
        if c["cut_end"] <= c["start"]:
            c["cut_end"] = min(total, c["start"] + 1.0)

    # 分页：约 page_chars 字 / page_sec 秒一页
    pages, cur = [], []
    cur_chars = 0.0
    cur_sec = 0.0
    for c in cues:
        n = len(c["text"])
        sec = c["cut_end"] - c["start"]
        if cur and (cur_chars + n > a.page_chars + 6 or cur_sec + sec > a.page_sec + 1.2 or len(cur) >= 5):
            pages.append(cur)
            cur, cur_chars, cur_sec = [], 0.0, 0.0
        cur.append(c)
        cur_chars += n
        cur_sec += sec
    if cur:
        pages.append(cur)

    SPEAKER = "audio"
    voice_pages, src_pages, spec_pages = [], [], []
    for pi, pg in enumerate(pages, 1):
        pid = f"p{pi:02d}"
        vlist, clist = [], []
        for ci, c in enumerate(pg):
            wav = ADIR / f"{pid}-{ci}.wav"
            run(["ffmpeg", "-y", "-loglevel", "error",
                 "-ss", f"{max(0.0, c['start'] - 0.02):.3f}", "-to", f"{c['cut_end']:.3f}",
                 "-i", str(audio), "-ar", "48000", "-ac", "2", str(wav)])
            dd = dur_of(wav) or (c["cut_end"] - c["start"])
            chars = list(c["text"])
            k = [round(min(dd * 0.95, (i + 0.5) / max(1, len(chars)) * dd * 0.95), 3)
                 for i in range(len(chars))]
            vlist.append({"t": c["text"], "f": f"audio/{wav.name}", "d": round(dd, 3),
                          "o": 0, "k": k, "r": 0})
            clist.append(c["text"])
        voice_pages.append(vlist)
        title = pg[0]["text"].rstrip(PUNCT)[:24]
        src_pages.append({"id": pid, "section": "正文" if 2 < pi < len(pages) - 1 else ("钩子" if pi <= 2 else "落点"),
                          "title": title, "cues": clist})
        spec_pages.append({"id": pid, "title": title, "asset": "", "theme": "day",
                           "cam": "push40", "reveal": [0.3, 1, 0.2, 1.5],
                           "lights": [], "texts": []})

    title = (tr.get("title") or d.name)
    (d / "script-source.json").write_text(json.dumps(
        {"title": title, "gap": 0, "voice": {"speaker": SPEAKER, "provider": "audio"},
         "pages": src_pages}, ensure_ascii=False, indent=1), encoding="utf-8")

    # script.js：**pace 全 0** —— 音轨必须和原音频一模一样，不能加静音
    lines = [
        f"/* {proj} · 由 tools/audio_film.py 从用户音频生成（不要手改） */",
        "(function (root) {",
        "  const META = {",
        "    style: 'warm-emotion',",
        f"    title: {json.dumps(title, ensure_ascii=False)},",
        f"    name: {json.dumps(proj)},",
        "    gap: 0,",
        "    voice: { speaker: 'audio', provider: 'audio' },",
        "    extras: ['engine/styles/warm-emotion/kit.js'],",
        "    pace: { lead: 0, gap: 0, maxHold: 0, tail: 1.0 },",
        "  };",
        "  const PAGES = [",
    ]
    for p in src_pages:
        lines.append("    { id: %s, section: %s, title: %s, cues: [" %
                     (json.dumps(p["id"]), json.dumps(p["section"], ensure_ascii=False),
                      json.dumps(p["title"], ensure_ascii=False)))
        for c in p["cues"]:
            lines.append("      %s," % json.dumps(c, ensure_ascii=False))
        lines.append("    ] },")
    lines += ["  ];", "  root.SCRIPT = { META, PAGES };",
              "})(typeof window !== 'undefined' ? window : globalThis);", ""]
    (d / "script.js").write_text("\n".join(lines), encoding="utf-8")

    (d / "voice.js").write_text(
        "/* 由 tools/audio_film.py 生成：音频来自用户的录音，按段切开，未做任何合成 */\n"
        "SCRIPT.VOICE = " + json.dumps({"speaker": SPEAKER, "provider": "audio",
                                        "pages": voice_pages}, ensure_ascii=False) + ";\n",
        encoding="utf-8")

    (d / "page-spec.json").write_text(json.dumps(spec_pages, ensure_ascii=False, indent=1),
                                     encoding="utf-8")

    chars = sum(len(c["text"]) for pg in pages for c in pg)
    print(f"  页数 {len(pages)} · cue {len(cues)} · 字数 {chars} · 音频 {total:.1f}s")
    print(f"  每页字数：{[sum(len(c['text']) for c in pg) for pg in pages][:10]} …")
    print(f"  写好：script-source.json / script.js / voice.js / page-spec.json（{proj}）")


if __name__ == "__main__":
    main(sys.argv)
