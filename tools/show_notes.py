import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "app"))
import store  # noqa: E402

m = store.load(sys.argv[1] if len(sys.argv) > 1 else "marriage_full")
print(f"骨架：{'  →  '.join(m.get('skeleton', []))}\n")
print("页号  位置        时长  屏上字        画面画什么")
print("─" * 92)
for p in m["shots"]:
    t = f"「{p['text']}」" if p.get("text") else "—"
    print(f"  {p['id']}  {p['role']:<8} {p['dur']:>3}s  {t:<12}  {p.get('note') or '(空)'}")
