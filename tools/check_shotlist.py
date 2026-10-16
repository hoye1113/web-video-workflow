"""校验「切页」的产出：旁白有没有丢、每页时长、页内节奏。"""
import pathlib
import re
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "app"))
import store  # noqa: E402

SRC = pathlib.Path(r"E:\user_pasted_clipboard_long_content_as_file_站在男人角度告诉你，犯错的男人还会不会爱 (2).txt")
PROJ = sys.argv[1] if len(sys.argv) > 1 else "marriage_full"

clean = lambda t: re.sub(r"[\s\u3000]", "", t or "")

src = clean(SRC.read_text(encoding="utf-8"))
m = store.load(PROJ)
pages = m["shots"]
nar = clean("".join(p.get("narration", "") for p in pages))

print(f"骨架：{'  →  '.join(m.get('skeleton', []))}")
print(f"页数 {len(pages)}　总时长 {sum(p['dur'] for p in pages)} 秒　"
      f"≈ {sum(p['dur'] for p in pages)/60:.1f} 分钟")
print()
print(f"原文 {len(src)} 字　页旁白合计 {len(nar)} 字　覆盖率 {len(nar)/len(src)*100:.1f}%")
print()

print("=== 原文每个自然段有没有被分配掉 ===")
paras = [p for p in SRC.read_text(encoding="utf-8").split("\n") if clean(p)]
miss = 0
for i, para in enumerate(paras, 1):
    head = clean(para)[:14]
    hit = clean(para) in nar
    if not hit:
        miss += 1
    print(f"  段{i:>2}  {len(clean(para)):>4} 字  {head}…  {'OK' if hit else '★ 没进旁白'}")
print(f"  -> {len(paras)} 段里 {miss} 段没进去")
print()

print("=== 每页 ===")
for p in pages:
    n = p.get("narration", "")
    print(f"  {p['id']}  {p['role']:<5}  {p['dur']:>2}s  旁白 {len(clean(n)):>3} 字  {p['title']}")
print()

print("=== 统计 ===")
print("  镜头动作：", dict(Counter(p.get("camera", "?") for p in pages)))
durs = [p["dur"] for p in pages]
print(f"  时长：最短 {min(durs)}s  最长 {max(durs)}s  平均 {sum(durs)/len(durs):.1f}s")
lens = [len(clean(p.get("narration", ""))) for p in pages]
print(f"  旁白：最短 {min(lens)} 字  最长 {max(lens)} 字  平均 {sum(lens)/len(lens):.0f} 字")
rate = [len(clean(p.get("narration", ""))) / p["dur"] * 60 for p in pages]
print(f"  语速：最慢 {min(rate):.0f}  最快 {max(rate):.0f}  平均 {sum(rate)/len(rate):.0f} 字/分钟（实测真人 403）")
