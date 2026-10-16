import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "app"))
import store  # noqa: E402

m = store.load(sys.argv[1] if len(sys.argv) > 1 else "marriage_full")
shots = m["shots"]
from collections import Counter
c = Counter(s.get("mode") or "code" for s in shots)

print(f"片型 {m.get('filmType') or '未定'}　骨架 {len(m.get('skeleton') or [])} 段　{len(shots)} 页")
print(f"做法分布：生图 {c['image']}　混合 {c['mixed']}　代码 {c['code']}")
print()
print("页号  位置        时长  做法   论点 / 生图提示词")
print("─" * 118)
for s in shots:
    mode = s.get("mode") or "code"
    tag = {"image": "生图", "mixed": "混合", "code": "代码"}[mode]
    print(f"  {s['id']}  {s['role']:<8} {s['dur']:>3}s  {tag}  {s.get('title','')}")
    ip = (s.get("imagePrompt") or "").strip()
    if ip:
        print(f"           └─ {ip}")
