"""把口播转成带时间轴的文本。输出三个文件：

    <名>.txt    纯文本
    <名>.srt    字幕
    <名>.json   分段（每段起止秒 + 文字）—— V2 的页面时长对齐要用这个

用法：
    python tools/transcribe.py 片子.mp4
    python tools/transcribe.py 片子.mp4 --model medium --lang zh

两处环境适配（这台机器上踩过的）：
  - 音频解码不走 PyAV（faster-whisper 自带的解码器和装上的 av 版本接口对不上），
    改用 ffmpeg 解成 16k 单声道 float32，直接喂 numpy 数组。
  - 模型要下 HuggingFace，这台机器必须走系统代理（Chrome 用的那个），
    这里自动把系统代理读进环境变量。
"""
import argparse
import json
import os
import subprocess
import sys
import wave
from pathlib import Path


def use_system_proxy():
    """把 Windows 系统代理读进环境变量（命令行默认不读，浏览器读）。"""
    if os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy"):
        return os.environ.get("HTTPS_PROXY")
    try:
        import winreg
        k = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                           r"Software\Microsoft\Windows\CurrentVersion\Internet Settings")
        enable = winreg.QueryValueEx(k, "ProxyEnable")[0]
        server = winreg.QueryValueEx(k, "ProxyServer")[0]
        if enable and server:
            url = server if "://" in server else f"http://{server}"
            os.environ["HTTP_PROXY"] = os.environ["HTTPS_PROXY"] = url
            os.environ.setdefault("NO_PROXY", "127.0.0.1,localhost,::1")
            return url
    except Exception:                                          # noqa: BLE001
        pass
    return None


def decode_audio(path, sr=16000):
    """用 ffmpeg 解成 16k 单声道 float32 numpy 数组，绕开 PyAV。"""
    import numpy as np
    r = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path),
         "-f", "f32le", "-ac", "1", "-ar", str(sr), "-"],
        capture_output=True,
    )
    if r.returncode != 0 or not r.stdout:
        raise RuntimeError("ffmpeg 解码失败：" + (r.stderr.decode("utf-8", "replace")[:400]))
    return np.frombuffer(r.stdout, dtype=np.float32)


def fmt_ts(sec, comma=True):
    h = int(sec // 3600); m = int(sec % 3600 // 60); s = sec % 60
    ms = int(round((s - int(s)) * 1000))
    sep = "," if comma else "."
    return f"{h:02d}:{m:02d}:{int(s):02d}{sep}{ms:03d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("media")
    ap.add_argument("--model", default="small", help="tiny/base/small/medium/large-v3")
    ap.add_argument("--lang", default="zh")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    src = Path(a.media)
    if not src.exists():
        sys.exit(f"找不到文件：{src}")
    out = Path(a.out) if a.out else src.with_suffix("")
    out.parent.mkdir(parents=True, exist_ok=True)

    px = use_system_proxy()
    if px:
        print(f"走系统代理 {px}", flush=True)

    from faster_whisper import WhisperModel
    print(f"载入模型 {a.model}（第一次会下载）…", flush=True)
    model = WhisperModel(a.model, device="cpu", compute_type="int8")

    print("解码音频…", flush=True)
    audio = decode_audio(src)
    dur = len(audio) / 16000

    print(f"转写中（{dur:.1f} 秒）…", flush=True)
    segs, info = model.transcribe(audio, language=a.lang, vad_filter=True, beam_size=5)
    rows = []
    for s in segs:
        rows.append({"start": round(s.start, 3), "end": round(s.end, 3), "text": s.text.strip()})
        print(f"  [{fmt_ts(s.start)} → {fmt_ts(s.end)}] {s.text.strip()}", flush=True)

    (out.with_suffix(".json")).write_text(
        json.dumps({"file": str(src), "language": info.language,
                    "duration": round(dur, 2), "segments": rows},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    (out.with_suffix(".txt")).write_text("".join(r["text"] for r in rows), encoding="utf-8")
    (out.with_suffix(".srt")).write_text(
        "".join(f"{i+1}\n{fmt_ts(r['start'])} --> {fmt_ts(r['end'])}\n{r['text']}\n\n"
                for i, r in enumerate(rows)), encoding="utf-8")

    chars = sum(len(r["text"]) for r in rows)
    if dur:
        print(f"\n完成：{len(rows)} 段 · {dur:.1f} 秒 · {chars} 字 · {chars/dur*60:.0f} 字/分钟")
    print(f"-> {out.with_suffix('.txt')}\n-> {out.with_suffix('.srt')}\n-> {out.with_suffix('.json')}")


if __name__ == "__main__":
    main()
