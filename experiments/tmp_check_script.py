import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUNCT = re.compile(r"[，。！？；：、,.!?;:—…]")
MAX = 12

proj = sys.argv[1] if len(sys.argv) > 1 else "infidelity-1021"
p = ROOT / "projects" / proj / "script-source.json"
d = json.loads(p.read_text(encoding="utf-8"))
pages = d["pages"]
cues = [(pg["id"], c) for pg in pages for c in pg["cues"]]

bad_len = [(pid, c, len(c)) for pid, c in cues if len(c) > MAX]
no_punct = [(pid, c) for pid, c in cues if len(c) >= MAX and not PUNCT.search(c[-1:])]
total = sum(len(c) for _, c in cues)
print(f"[{proj}] pages={len(pages)} cues={len(cues)} chars={total}")
print(f"  超 12 字的 cue: {len(bad_len)}  {bad_len}")
print(f"  第 12 字前没标点的: {len(no_punct)}  {no_punct}")
print(f"  页数在 50-60 之间: {50 <= len(pages) <= 60}")
print(f"  短于 4 字的 cue: {[(pid, c) for pid, c in cues if len(c) < 4]}")

# 引擎的切行逻辑（和 packages/engine 的 splitCue 一致）：标点处切，攒满 12 也切
def split(cue):
    out, frm = [], 0
    for i in range(1, len(cue) + 1):
        if i == len(cue) or PUNCT.match(cue[i - 1]) or i - frm >= MAX:
            out.append(cue[frm:i])
            frm = i
    return out

hard = []
for pid, c in cues:
    parts = split(c)
    if len(parts) == 1:
        continue
    for t in parts:
        if len(t) >= MAX and not PUNCT.search(t[-1:]):
            hard.append((pid, c, parts))
print(f"  硬切（会切开词）: {len(hard)}  {hard}")

# 每页字数
sizes = [(pg["id"], len(pg["cues"]), sum(len(c) for c in pg["cues"])) for pg in pages]
print(f"  每页 cue 数 min/max: {min(s[1] for s in sizes)}/{max(s[1] for s in sizes)}")
print(f"  每页字数 min/max: {min(s[2] for s in sizes)}/{max(s[2] for s in sizes)}")
print(f"  平均每页 {total/len(pages):.1f} 字")

# 字幕行数（每条 cue 就是一行字幕）
print(f"  字幕总行数 = cue 数 = {len(cues)}")
