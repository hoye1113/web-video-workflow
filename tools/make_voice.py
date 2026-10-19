"""给 emotion-full 配音：逐条 cue 合成 → audio/*.wav + voice.js。

产物契约（`packages/engine/runtime/timing.js` 读的就是这个）：
    SCRIPT.VOICE = { speaker, provider, pages: [[{t, f, d, o, k}, …], …] }
      t = 这条 cue 的文字（**必须和 script.js 里一字不差**）
      f = 音频文件（相对工程目录）
      d = 这条音频的长度（秒）—— **含我在末尾补的停顿**，页内节奏全靠它
      o = 开头那点静音（speech 真正起声的位置）→ 引擎用它算 cue.start
      k = 逐字起声时间（相对音频开头，一个字一个数）→ 字幕精确到字就靠它

每条 cue 是**独立一段音频**（和 `experiments/ft-run/实验-情感` 的做法一致），
末尾按标点补停顿：句号 0.5s / 逗号 0.28s / 页末 0.25s —— 引擎在"有 o"这条路里
**不再自己加停顿**，所以停顿必须我补。

跑法：
    python tools/make_voice.py                # 全部（已有音频的跳过）
    python tools/make_voice.py p05 p06        # 只做指定页
    python tools/make_voice.py --check        # 只对一遍 script.js 与源数据
"""
import json
import os
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
EP = ROOT / "projects" / "emotion-full"
SRC = EP / "script-source.json"
AUDIO = EP / "audio"
VOICEJS = EP / "voice.js"
BRIDGE = (ROOT / "experiments" / "frametell-src" / "frametell-main" / "packages"
          / "voice" / "tools" / "edge-tts.py")
PY = pathlib.Path.home() / ".frametell" / "edge-venv" / "Scripts" / "python.exe"
LOCALBIN = pathlib.Path.home() / ".local" / "bin"

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = -8          # 慢一点，像"讲给你听"
PITCH = -2         # 压低一点，稳
TAIL = {"。": 0.5, "！": 0.5, "？": 0.5, "，": 0.28, "、": 0.24, "；": 0.34, "：": 0.30}


def env():
    e = os.environ.copy()
    e["PATH"] = str(LOCALBIN) + os.pathsep + e.get("PATH", "")
    e["PYTHONUTF8"] = "1"
    e["PYTHONIOENCODING"] = "utf-8"
    return e


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", env=env(), **kw)


def synth(text: str, mp3: pathlib.Path):
    """调桥：文本 → mp3 + 逐词时间戳。"""
    reqf = pathlib.Path(tempfile.gettempdir()) / "vf-tts-req.json"
    reqf.write_text(json.dumps({"text": text, "voice": VOICE, "rate": RATE,
                                "pitch": PITCH, "out": str(mp3)}, ensure_ascii=False),
                    encoding="utf-8")
    r = run([str(PY), str(BRIDGE), str(reqf)], timeout=180)
    raw = (r.stdout or "").strip().splitlines()
    try:
        d = json.loads([x for x in raw if x.startswith("{")][-1])
    except Exception:                                          # noqa: BLE001
        raise RuntimeError(f"桥没吐 JSON：{r.stdout[:200]} / {r.stderr[:200]}") from None
    if "error" in d:
        raise RuntimeError(f"合成失败：{d['error']}")
    return d["words"]


def dur_of(f: pathlib.Path) -> float:
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(f)])
    return round(float((r.stdout or "0").strip() or 0), 3)


def to_wav(mp3: pathlib.Path, wav: pathlib.Path, pad: float):
    """转 48k 双声道 wav，并在末尾补 `pad` 秒静音（停顿就靠它）。"""
    af = f"apad=pad_dur={pad:.3f}" if pad > 0 else "anull"
    r = run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp3),
             "-af", af, "-ar", "48000", "-ac", "2", str(wav)])
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg 转 wav 失败：{(r.stderr or '')[:200]}")


def build_k(text: str, words, lead: float):
    """逐字起声：把词级时间戳摊到字上（词内线性插值，标点跟后一个字）。"""
    chars = list(text)
    k = [None] * len(chars)
    pos = 0
    for w in words:
        wd = (w.get("word") or "")
        if not wd:
            continue
        idx = text.find(wd, pos)
        if idx < 0:
            continue
        n = len(wd)
        s, e = float(w["startTime"]), float(w["endTime"])
        for j in range(n):
            ci = idx + j
            if ci < len(chars):
                k[ci] = round(s + (e - s) * (j / max(n, 1)), 4)
        pos = idx + n
    # 剩下的（标点等）：跟上一个已定的字
    last = lead
    for i, v in enumerate(k):
        if v is None:
            k[i] = last
        else:
            last = v
    for i in range(1, len(k)):
        if k[i] < k[i - 1]:
            k[i] = k[i - 1]
    return k


def one_cue(text: str, pid: str, i: int):
    """合成一条 cue → 返回 {f, d, o, k}。**不管文件在不在都重做**（元数据只能从这次合成里来）。"""
    wav = AUDIO / f"{pid}-{i}.wav"
    mp3 = AUDIO / f"{pid}-{i}.mp3"
    words = synth(text, mp3)
    lead = round(min([float(w["startTime"]) for w in words] or [0]), 3)
    pad = TAIL.get(text.strip()[-1:], 0.25)
    to_wav(mp3, wav, pad)
    mp3.unlink(missing_ok=True)
    return {"f": f"audio/{wav.name}", "d": dur_of(wav), "o": lead,
            "k": build_k(text, words, lead)}


def main(argv):
    d = json.loads(SRC.read_text(encoding="utf-8"))
    pages = d["pages"]
    want = [a for a in argv[1:] if not a.startswith("-")]
    if "--check" in argv:
        tot = 0
        for p in pages:
            n = len(p["cues"])
            tot += n
        print(f'{len(pages)} 页 / {tot} 条 cue；音色 {VOICE} rate {RATE} pitch {PITCH}')
        return

    AUDIO.mkdir(parents=True, exist_ok=True)
    cache = json.loads(VOICEJS.with_suffix(".cache.json").read_text(encoding="utf-8")) \
        if VOICEJS.with_suffix(".cache.json").exists() else {}
    todo = 0
    for p in pages:
        fresh = bool(want) and p["id"] in want
        if not fresh:
            continue
        for i, text in enumerate(p["cues"]):
            key = f'{p["id"]}:{i}'
            if key in cache and not force_all(argv):
                continue
            todo += 1
            print(f'  {p["id"]} [{i + 1}/{len(p["cues"])}] {text}')
            v = one_cue(text, p["id"], i)
            v["t"] = text
            cache[key] = v
            print(f'      {v["d"]}s 起声{v["o"]}s 首字k={v["k"][:4]}')

    # 组装：**按页对齐**；缺的页给空数组 —— 引擎对没配音的页会退回按字数估算（timing.js 里那条兜底）
    out_pages, missing = [], []
    for p in pages:
        cues = [cache.get(f'{p["id"]}:{i}') for i in range(len(p["cues"]))]
        if all(cues):
            out_pages.append(cues)
        else:
            out_pages.append([])
            missing.append(p["id"])

    VOICEJS.write_text(
        "/* 由 tools/make_voice.py 生成（音色 " + VOICE + "）：真实语速的时间轴。\n"
        " * 改了 cue 文字**必须重跑配音**，否则 t 对不上就不会生效。 */\n"
        "SCRIPT.VOICE = " + json.dumps({"speaker": VOICE, "provider": "edge",
                                        "pages": out_pages}, ensure_ascii=False) + ";\n",
        encoding="utf-8")
    VOICEJS.with_suffix(".cache.json").write_text(json.dumps(cache, ensure_ascii=False),
                                                  encoding="utf-8")
    total = sum(c["d"] for pg in out_pages for c in pg)
    print(f"写好 {VOICEJS.relative_to(ROOT)}：{len(out_pages)} 页 / 已配音 "
          f"{sum(1 for p in out_pages if p)} 页 / 语音共 {total / 60:.1f} 分钟（本轮新做 {todo} 条）")
    if missing:
        print("还没配音的页：" + " ".join(missing))


def force_all(argv):
    return "--force" in argv


if __name__ == "__main__":
    main(sys.argv)
