"""收尾：让"配音服务是否可用"这张表认 edge（免费免密钥，永远可用），并把它列进音色列表。"""
import io
import pathlib
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
R = pathlib.Path(r"D:\WorkSpace\video-factory\experiments\frametell-src\frametell-main")

EDITS = [
    # ── 后端：把 edge 音色列出来 + configured 里永远为 true ──
    ("packages/core/src/studio.ts",
     "import { edgeTts, bundledSample,",
     "import { EDGE_VOICES, edgeTts, bundledSample,"),
    ("packages/core/src/studio.ts",
     "    const voices: Voice[] = [...mine, ...VOLCENGINE_VOICES.filter((v) => !mine.some((m) => m.id === v.id))];",
     """    // edge-tts 免费免密钥：永远可用，音色直接列出来
    const edgeVoices: Voice[] = EDGE_VOICES.map((v) => ({ provider: 'edge' as const, id: v.id, name: v.name, gender: v.gender, lang: v.lang }));
    const voices: Voice[] = [...mine, ...edgeVoices, ...VOLCENGINE_VOICES.filter((v) => !mine.some((m) => m.id === v.id))];"""),
    ("packages/core/src/studio.ts",
     "return { voices, configured: { volcengine: !!cfg.tts.volcengine, elevenlabs: !!cfg.tts.elevenlabs }",
     "return { voices, configured: { volcengine: !!cfg.tts.volcengine, elevenlabs: !!cfg.tts.elevenlabs, edge: true }"),

    # ── 类型 ──
    ("packages/core/src/types.ts",
     "    configured: { volcengine: boolean; elevenlabs: boolean };",
     "    configured: { volcengine: boolean; elevenlabs: boolean; edge: boolean };"),

    # ── 前端：三处 ──
    ("packages/ui/src/components/VoicePicker.tsx",
     "const PROVIDER_NAME: Record<Voice['provider'], () => string> = { volcengine: () => t('home.voice.volcengine'), elevenlabs: () => 'ElevenLabs' };",
     "const PROVIDER_NAME: Record<Voice['provider'], () => string> = { volcengine: () => t('home.voice.volcengine'), elevenlabs: () => 'ElevenLabs', edge: () => 'edge-tts' };"),
    ("packages/ui/src/components/VoicePicker.tsx",
     "(['volcengine', 'elevenlabs'] as const).map((provider) => ({",
     "(['edge', 'volcengine', 'elevenlabs'] as const).map((provider) => ({"),
    ("packages/ui/src/components/FilmSettings.tsx",
     "(['volcengine', 'elevenlabs'] as const).filter((x) => !voices.data!.configured[x])",
     "(['volcengine', 'elevenlabs'] as const).filter((x) => !voices.data!.configured[x])   // edge 永远可用，不用提示配 key"),
]

for rel, old, new in EDITS:
    p = R / rel
    s = p.read_text(encoding="utf-8")
    if new in s and old not in s:
        print(f"  · {rel} 已改过")
        continue
    n = s.count(old)
    if n != 1:
        print(f"  ✗ {rel}：匹配 {n} 处 —— 跳过")
        continue
    p.write_text(s.replace(old, new), encoding="utf-8")
    print(f"  ✓ {rel}")
