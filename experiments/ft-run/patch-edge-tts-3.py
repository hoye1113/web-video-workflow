"""把剩下的窄类型也放宽（agent 的事件类型 + cli 的 server 路由 + desktop 的 IPC）。"""
import io
import pathlib
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
R = pathlib.Path(r"D:\WorkSpace\video-factory\experiments\frametell-src\frametell-main")

EDITS = [
    ("packages/agent/src/events.ts",
     "| { kind: 'voice'; label: string; provider: 'volcengine' | 'elevenlabs'; id: string; name: string };",
     "| { kind: 'voice'; label: string; provider: 'volcengine' | 'elevenlabs' | 'edge'; id: string; name: string };"),
    ("packages/agent/src/events.ts",
     "| { type: 'voice'; voice: { provider: 'volcengine' | 'elevenlabs'; id: string; name?: string } }",
     "| { type: 'voice'; voice: { provider: 'volcengine' | 'elevenlabs' | 'edge'; id: string; name?: string } }"),
    ("apps/cli/src/server.ts",
     "'volcengine' | 'elevenlabs'",
     "'volcengine' | 'elevenlabs' | 'edge'"),
    ("apps/desktop/src/main.ts",
     "'volcengine' | 'elevenlabs'",
     "'volcengine' | 'elevenlabs' | 'edge'"),
]

for rel, old, new in EDITS:
    p = R / rel
    s = p.read_text(encoding="utf-8")
    if new in s and old not in s:
        print(f"  · {rel} 已改过")
        continue
    n = s.count(old)
    if n == 0:
        print(f"  ✗ {rel}：没找到")
        continue
    p.write_text(s.replace(old, new), encoding="utf-8")
    print(f"  ✓ {rel}：{n} 处")

# studio.ts：key 的类型因为三元变成 string|undefined 了，收窄一下写法
p = R / "packages/core/src/studio.ts"
s = p.read_text(encoding="utf-8")
old = """    const tts = provider === 'edge' ? edgeTts() : provider === 'elevenlabs' ? elevenLabsTts(key) : volcengineTts(key);"""
new = """    const tts = provider === 'edge' ? edgeTts()
      : provider === 'elevenlabs' ? elevenLabsTts(key ?? '') : volcengineTts(key ?? '');"""
if new in s:
    print("  · studio.ts tts 已改过")
elif s.count(old) == 1:
    p.write_text(s.replace(old, new), encoding="utf-8")
    print("  ✓ studio.ts tts 收窄")
else:
    print(f"  ✗ studio.ts tts 匹配 {s.count(old)} 处")
