"""修上一步：import 写成 default 了，另外两处没匹配上（缩进是 2 空格，不是 4）。逐条精确改。"""
import io
import pathlib
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
R = pathlib.Path(r"D:\WorkSpace\video-factory\experiments\frametell-src\frametell-main")

# ① import 修回来：import edgeTts, { → import { edgeTts,
for rel in ["packages/core/src/runner.ts", "packages/core/src/studio.ts", "apps/cli/src/cli.ts"]:
    p = R / rel
    s = p.read_text(encoding="utf-8")
    if "import edgeTts, {" in s:
        s = s.replace("import edgeTts, {", "import { edgeTts,")
        p.write_text(s, encoding="utf-8")
        line = next(l for l in s.splitlines() if "@frametell/voice" in l)
        print(f"  ✓ import {rel}\n      {line.strip()[:120]}")
    else:
        print(f"  · import {rel} 已经是好的")

# ② runner.ts 的 voiceFor（顶格 2 空格缩进）
p = R / "packages/core/src/runner.ts"
s = p.read_text(encoding="utf-8")
old = """  const key = meta.voice?.provider === 'elevenlabs' ? cfg.tts.elevenlabs : cfg.tts.volcengine;
  const tts = meta.voice && key ? (meta.voice.provider === 'elevenlabs'
    ? elevenLabsTts(key, undefined, { baseUrl: cfg.ttsBaseUrls?.elevenlabs })
    : volcengineTts(key, { baseUrl: cfg.ttsBaseUrls?.volcengine })) : undefined;"""
new = """  // edge-tts 免费免密钥：选了它就不再要求配 key（另外两家仍然要）
  const tts = !meta.voice ? undefined
    : meta.voice.provider === 'edge' ? edgeTts()
    : meta.voice.provider === 'elevenlabs' ? (cfg.tts.elevenlabs
        ? elevenLabsTts(cfg.tts.elevenlabs, undefined, { baseUrl: cfg.ttsBaseUrls?.elevenlabs }) : undefined)
    : (cfg.tts.volcengine ? volcengineTts(cfg.tts.volcengine, { baseUrl: cfg.ttsBaseUrls?.volcengine }) : undefined);"""
if new in s:
    print("  · runner.ts voiceFor 已改过")
elif s.count(old) == 1:
    p.write_text(s.replace(old, new), encoding="utf-8")
    print("  ✓ runner.ts voiceFor")
else:
    print(f"  ✗ runner.ts voiceFor 匹配 {s.count(old)} 处")

# ③ cli.ts 的 provider 选择
p = R / "apps/cli/src/cli.ts"
s = p.read_text(encoding="utf-8")
old = """  const volc = process.env.VOLCENGINE_TTS_API_KEY ? volcengineTts(process.env.VOLCENGINE_TTS_API_KEY) : undefined;
  const eleven = process.env.ELEVENLABS_API_KEY ? elevenLabsTts(process.env.ELEVENLABS_API_KEY) : undefined;
  const tts = lang === 'en' ? eleven ?? volc : volc ?? eleven;
  const voice = tts ? { speaker: o.voice || (tts.id === 'volcengine' ? 'zh_male_yuanboxiaoshu_uranus_bigtts' : 'JBFqnCBsd6RMkjVDRZzb'), rate: 0, instruction: '像跟朋友分享一个实用的发现，语气轻松、真诚、自然，有轻重缓急' } : undefined;"""
new = """  const volc = process.env.VOLCENGINE_TTS_API_KEY ? volcengineTts(process.env.VOLCENGINE_TTS_API_KEY) : undefined;
  const eleven = process.env.ELEVENLABS_API_KEY ? elevenLabsTts(process.env.ELEVENLABS_API_KEY) : undefined;
  // 两家云服务都没配 key 时用 edge-tts（免费、免密钥、带逐词时间戳）
  const edge = edgeTts();
  const tts = (lang === 'en' ? eleven ?? volc : volc ?? eleven) ?? edge;
  const voice = tts ? { speaker: o.voice || (tts.id === 'volcengine' ? 'zh_male_yuanboxiaoshu_uranus_bigtts' : tts.id === 'edge' ? (lang === 'en' ? 'en-US-AriaNeural' : 'zh-CN-XiaoxiaoNeural') : 'JBFqnCBsd6RMkjVDRZzb'), rate: 0, instruction: '像跟朋友分享一个实用的发现，语气轻松、真诚、自然、有轻重缓急' } : undefined;"""
if new in s:
    print("  · cli.ts 已改过")
elif s.count(old) == 1:
    p.write_text(s.replace(old, new), encoding="utf-8")
    print("  ✓ cli.ts provider 选择")
else:
    print(f"  ✗ cli.ts 匹配 {s.count(old)} 处")

# ④ 自检：三处都不该再有裸的 key 判定
for rel in ["packages/core/src/runner.ts", "apps/cli/src/cli.ts", "packages/core/src/studio.ts"]:
    s = (R / rel).read_text(encoding="utf-8")
    print(f"  {rel}: edgeTts 出现 {s.count('edgeTts')} 次，edge 判定 {s.count(chr(39)+'edge'+chr(39))} 次")
