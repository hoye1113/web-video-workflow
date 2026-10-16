"""edge-tts 验证：能不能装、能不能合成中文、能不能拿到逐字时间戳。

它的 narrate.ts 需要的就是这两样：mp3 + WordTime[]（中文按字）。
edge-tts 的 WordBoundary 事件正好给这个：offset / duration 单位是 100 纳秒。
"""
import asyncio
import io
import json
import sys
from pathlib import Path

import edge_tts

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

VOICE = sys.argv[1] if len(sys.argv) > 1 else "zh-CN-XiaoxiaoNeural"
TEXT = "反而他更加倾向于用一种补偿心态去维持表面的和平。"
OUT = Path("D:/WorkSpace/video-factory/experiments/edge-tts-test")


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    mp3 = OUT / f"test-{VOICE}.mp3"
    comm = edge_tts.Communicate(TEXT, VOICE, rate="-8%", pitch="-2Hz")
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
    mp3.write_bytes(bytes(audio))
    (OUT / f"words-{VOICE}.json").write_text(
        json.dumps(words, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"音色 {VOICE}")
    print(f"  mp3 {len(audio)//1024} KB → {mp3.name}")
    print(f"  逐字时间戳 {len(words)} 条（原文 {len(TEXT)} 字）")
    for w in words[:6]:
        print(f"    {w['startTime']:>6.2f}s → {w['endTime']:>6.2f}s  {w['word']}")
    if words:
        print(f"  ...末条 {words[-1]['startTime']:.2f}s → {words[-1]['endTime']:.2f}s {words[-1]['word']}")


if __name__ == "__main__":
    asyncio.run(main())
