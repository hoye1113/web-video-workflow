#!/usr/bin/env python
"""edge-tts bridge: JSON on stdin → mp3 + 逐词时间戳（JSON 打到 stdout）。

为什么要个桥：edge-tts 是 Python 包，而配音层其余部分是 TypeScript。
契约照抄 TtsProvider.synth：

    in : {"text": "...", "voice": "zh-CN-XiaoxiaoNeural",
          "rate": -8, "pitch": -2, "out": "C:/.../take.mp3"}
    out: {"audio": "C:/.../take.mp3",
          "words": [{"word": "反而", "startTime": 0.10, "endTime": 0.40}, ...]}

rate / pitch 用 provider 侧的数值（rate 是百分比，pitch 约按"一个半音 ≈ 2Hz"折算），
越界的值在这里夹住 —— 别让上层为了迁就一个 TTS 改自己的类型。

**必须用 boundary='WordBoundary'**：edge-tts 7.x 默认只发 SentenceBoundary，
中文就只剩"整句一个时间戳"，画面就没法按字对齐（实测过）。
"""
import asyncio
import io
import json
import sys

import edge_tts


def _pct(v, default="+0%"):
    if v is None:
        return default
    v = max(-50, min(100, int(round(float(v)))))
    return f"{'+' if v >= 0 else ''}{v}%"


def _hz(v, default="+0Hz"):
    if v is None:
        return default
    hz = max(-50, min(50, int(round(float(v) * 2))))
    return f"{'+' if hz >= 0 else ''}{hz}Hz"


async def run(req: dict) -> dict:
    text = (req.get("text") or "").strip()
    if not text:
        raise ValueError("text 是空的")
    voice = req.get("voice") or "zh-CN-XiaoxiaoNeural"
    out = req["out"]

    comm = edge_tts.Communicate(
        text, voice,
        boundary="WordBoundary",          # ← 关键：不写这句就只有整句时间戳
        rate=_pct(req.get("rate")),
        pitch=_hz(req.get("pitch")),
    )
    audio = bytearray()
    words = []
    async for ch in comm.stream():
        if ch["type"] == "audio":
            audio.extend(ch["data"])
        elif ch["type"] == "WordBoundary":
            words.append({
                "word": ch["text"],
                "startTime": round(ch["offset"] / 10_000_000, 4),
                "endTime": round((ch["offset"] + ch["duration"]) / 10_000_000, 4),
            })
    if not audio:
        raise RuntimeError("edge-tts 没吐音频（网络或音色名不对？）")
    with open(out, "wb") as f:
        f.write(bytes(audio))
    return {"audio": out, "words": words, "bytes": len(audio)}


async def run_with_retry(req: dict, tries: int = 4) -> dict:
    """重试。

    为什么要：edge-tts 走的是微软的朗读接口，**偶发抖动是常态**（实测一次失败、紧接着两次成功）。
    但要区分两类错误：音色名写错 / 文本为空 —— 重试也没用，直接抛。
    """
    last = ""
    for i in range(tries):
        try:
            return await run(req)
        except Exception as e:                              # noqa: BLE001
            msg = f"{type(e).__name__}: {e}"
            if isinstance(e, (ValueError, FileNotFoundError)) or "text 是空的" in msg:
                raise
            last = msg
            if i < tries - 1:
                await asyncio.sleep(1.5 * (i + 1))          # 退避，别把对面打烦
    raise RuntimeError(last or "edge-tts 连续失败")


def main():
    # 请求来源，按优先级：
    #   1) argv[1] 是 .json 文件 → 读它（**推荐**：文件是 UTF-8，路径是 ASCII，绕开 Windows 控制台编码）
    #   2) stdin → **必须按字节读再 UTF-8 解码**（PowerShell 管道会把中文按 GBK 塞进来，实测踩过）
    #   3) 调试用：argv = 文本 voice out
    if len(sys.argv) >= 2 and sys.argv[1].endswith(".json"):
        with open(sys.argv[1], "rb") as f:
            req = json.loads(f.read().decode("utf-8"))
    elif len(sys.argv) >= 4:
        req = {"text": sys.argv[1], "voice": sys.argv[2], "out": sys.argv[3]}
    else:
        raw = sys.stdin.buffer.read()
        req = json.loads(raw.decode("utf-8", "replace") or "{}")
    try:
        print(json.dumps(asyncio.run(run_with_retry(req)), ensure_ascii=False))
    except Exception as e:                                  # noqa: BLE001
        # retryable=true：上层可以再试（网络抖动）；false：输入的问题，别白试
        retryable = isinstance(e, RuntimeError) and "连续失败" in str(e)
        print(json.dumps({"error": f"{type(e).__name__}: {e}", "retryable": retryable}, ensure_ascii=False))
        sys.exit(2 if retryable else 1)


if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    main()
