import json
import pathlib

p = pathlib.Path(__file__).with_name("1112.json")
d = json.loads(p.read_text(encoding="utf-8"))
lines = []
for s in d["segments"]:
    t = float(s["start"])
    lines.append(f"[{int(t // 60):02d}:{t % 60:05.2f}] {s['text']}")
pathlib.Path(__file__).with_name("1112-lines.txt").write_text("\n".join(lines), encoding="utf-8")
print(len(lines), "lines")
