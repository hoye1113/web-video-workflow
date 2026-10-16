"""把 edge-tts 接进 FRAMETELL 的四个调用点（改动最小化，逐处核对）。

改的原文件（他们的仓库）：
  packages/core/src/types.ts      两个 provider 联合类型加 'edge'
  packages/core/src/refs.ts       引用里的音色判定
  packages/core/src/runner.ts     voiceFor()（选 provider）+ 「需要先连配音服务」的预检
  packages/core/src/studio.ts     voicePreview()（试听）
  apps/cli/src/cli.ts             命令行那条路的 provider 选择
"""
import io
import pathlib
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = pathlib.Path(r"D:\WorkSpace\video-factory\experiments\frametell-src\frametell-main")

EDITS = [
    # ── 1. 联合类型 ─────────────────────────────────────────────
    ("packages/core/src/types.ts",
     "export interface VoiceChoice { provider: 'volcengine' | 'elevenlabs'; id: string; name?: string }",
     "export interface VoiceChoice { provider: 'volcengine' | 'elevenlabs' | 'edge'; id: string; name?: string }"),
    ("packages/core/src/types.ts",
     "export interface Voice { provider: 'volcengine' | 'elevenlabs'; id: string; name: string;",
     "export interface Voice { provider: 'volcengine' | 'elevenlabs' | 'edge'; id: string; name: string;"),

    # ── 2. 引用里的音色 ─────────────────────────────────────────
    ("packages/core/src/refs.ts",
     "if (x.kind === 'voice') return (x.provider === 'volcengine' || x.provider === 'elevenlabs')",
     "if (x.kind === 'voice') return (x.provider === 'volcengine' || x.provider === 'elevenlabs' || x.provider === 'edge')"),

    # ── 3. voiceFor：选 provider（edge 免密钥） ─────────────────
    ("packages/core/src/runner.ts",
     """    const key = meta.voice?.provider === 'elevenlabs' ? cfg.tts.elevenlabs : cfg.tts.volcengine;
    const tts = meta.voice && key ? (meta.voice.provider === 'elevenlabs'
      ? elevenLabsTts(key, undefined, { baseUrl: cfg.ttsBaseUrls?.elevenlabs })
      : volcengineTts(key, { baseUrl: cfg.ttsBaseUrls?.volcengine })) : undefined;""",
     """    // edge-tts 免费免密钥：选了它就不再要求配 key（另外两家仍然要）
    const tts = !meta.voice ? undefined
      : meta.voice.provider === 'edge' ? edgeTts()
      : meta.voice.provider === 'elevenlabs' ? (cfg.tts.elevenlabs
          ? elevenLabsTts(cfg.tts.elevenlabs, undefined, { baseUrl: cfg.ttsBaseUrls?.elevenlabs }) : undefined)
      : (cfg.tts.volcengine ? volcengineTts(cfg.tts.volcengine, { baseUrl: cfg.ttsBaseUrls?.volcengine }) : undefined);"""),

    # ── 4. 「需要先在设置里连接配音服务」的预检：edge 跳过 ──────
    ("packages/core/src/runner.ts",
     "    if (!(v.provider === 'elevenlabs' ? cfg.tts.elevenlabs : cfg.tts.volcengine)) {",
     "    if (v.provider !== 'edge' && !(v.provider === 'elevenlabs' ? cfg.tts.elevenlabs : cfg.tts.volcengine)) {"),

    # ── 5. studio 试听 ──────────────────────────────────────────
    ("packages/core/src/studio.ts",
     "  async voicePreview(provider: 'volcengine' | 'elevenlabs', id: string): Promise<string> {",
     "  async voicePreview(provider: 'volcengine' | 'elevenlabs' | 'edge', id: string): Promise<string> {"),
    ("packages/core/src/studio.ts",
     """    const key = provider === 'elevenlabs' ? cfg.tts.elevenlabs : cfg.tts.volcengine;
    if (!key) throw new Error(tr('先在设置里连接配音服务', 'Connect a voice service in Settings first'));
    const tts = provider === 'elevenlabs' ? elevenLabsTts(key) : volcengineTts(key);
    const text = provider === 'elevenlabs' ? 'Hi, I will narrate your video, one clear idea at a time.' : '你好，我来给你的视频配音。我们一句一句，把道理讲清楚。';""",
     """    // edge-tts 免密钥，试听直接合成
    const key = provider === 'elevenlabs' ? cfg.tts.elevenlabs : cfg.tts.volcengine;
    if (provider !== 'edge' && !key) throw new Error(tr('先在设置里连接配音服务', 'Connect a voice service in Settings first'));
    const tts = provider === 'edge' ? edgeTts() : provider === 'elevenlabs' ? elevenLabsTts(key) : volcengineTts(key);
    const text = provider === 'volcengine' ? '你好，我来给你的视频配音。我们一句一句，把道理讲清楚。'
      : provider === 'edge' ? '你好，我来给你的视频配音。我们一句一句，把道理讲清楚。' : 'Hi, I will narrate your video, one clear idea at a time.';"""),

    # ── 6. 命令行那条路：没有 key 时用 edge ─────────────────────
    ("apps/cli/src/cli.ts",
     """    const volc = process.env.VOLCENGINE_TTS_API_KEY ? volcengineTts(process.env.VOLCENGINE_TTS_API_KEY) : undefined;
    const eleven = process.env.ELEVENLABS_API_KEY ? elevenLabsTts(process.env.ELEVENLABS_API_KEY) : undefined;
    const tts = lang === 'en' ? eleven ?? volc : volc ?? eleven;
    const voice = tts ? { speaker: o.voice || (tts.id === 'volcengine' ? 'zh_male_yuanboxiaoshu_uranus_bigtts' : 'JBFqnCBsd6RMkjVDRZzb'), rate: 0, instruction: '像跟朋友分享一个实用的发现，语气轻松、真诚、自然，有轻重缓急' } : undefined;""",
     """    const volc = process.env.VOLCENGINE_TTS_API_KEY ? volcengineTts(process.env.VOLCENGINE_TTS_API_KEY) : undefined;
    const eleven = process.env.ELEVENLABS_API_KEY ? elevenLabsTts(process.env.ELEVENLABS_API_KEY) : undefined;
    // 两家云服务都没有 key 时用 edge-tts（免费、免密钥、有逐词时间戳）
    const edge = edgeTts();
    const tts = (lang === 'en' ? eleven ?? volc : volc ?? eleven) ?? edge;
    const voice = tts ? { speaker: o.voice || (tts.id === 'volcengine' ? 'zh_male_yuanboxiaoshu_uranus_bigtts' : tts.id === 'edge' ? (lang === 'en' ? 'en-US-AriaNeural' : 'zh-CN-XiaoxiaoNeural') : 'JBFqnCBsd6RMkjVDRZzb'), rate: 0, instruction: '像跟朋友分享一个实用的发现，语气轻松、真诚、自然，有轻重缓急' } : undefined;"""),
]


def main():
    ok = 0
    for rel, old, new in EDITS:
        p = ROOT / rel
        s = p.read_text(encoding="utf-8")
        if new in s and old not in s:
            print(f"  跳过（已改过）：{rel}")
            ok += 1
            continue
        n = s.count(old)
        if n != 1:
            print(f"  ✗ {rel}：匹配到 {n} 处，预期 1 处 —— 没动")
            continue
        p.write_text(s.replace(old, new), encoding="utf-8")
        print(f"  ✓ {rel}：改了 1 处")
        ok += 1

    # 引用：还得把 edgeTts 加进 import
    for rel, old, new in [
        ("packages/core/src/runner.ts",
         "import { elevenLabsTts, volcengineTts } from '@frametell/voice';",
         "import { edgeTts, elevenLabsTts, volcengineTts } from '@frametell/voice';"),
        ("packages/core/src/studio.ts",
         "import { bundledSample, ELEVENLABS_DEFAULT_VOICES, ElevenLabsError, elevenLabsTts, listEl",
         "import { bundledSample, edgeTts, ELEVENLABS_DEFAULT_VOICES, ElevenLabsError, elevenLabsTts, listEl"),
        ("apps/cli/src/cli.ts",
         "import { elevenLabsTts, volcengineTts } from '@frametell/voice';",
         "import { edgeTts, elevenLabsTts, volcengineTts } from '@frametell/voice';"),
    ]:
        p = ROOT / rel
        s = p.read_text(encoding="utf-8")
        if "edgeTts" in s.split("\n\n")[0] or new in s:
            print(f"  跳过 import（已改过）：{rel}")
            continue
        hits = [l for l in s.splitlines() if l.startswith(old[:60])]
        if len(hits) != 1:
            print(f"  ✗ import {rel}：匹配 {len(hits)} 行")
            continue
        p.write_text(s.replace(hits[0], hits[0].replace(old.split(" ")[1], "edgeTts, " + old.split(" ")[1], 1)), encoding="utf-8")
        print(f"  ✓ import {rel}")
    print(f"\n完成 {ok}/{len(EDITS)} 处")


if __name__ == "__main__":
    main()
