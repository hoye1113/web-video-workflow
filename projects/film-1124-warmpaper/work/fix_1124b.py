import json
from pathlib import Path

p = Path(r"E:\video-factory\1124\work\1124-fixed.json")
d = json.loads(p.read_text(encoding="utf-8"))
repl = {
    "发挥自己": "放任自己",
    "积载": "积累",
    "尽数看见": "逐渐看见",
    "分争": "纷争",
}
for s in d["segments"]:
    t = s["text"]
    for a, b in repl.items():
        t = t.replace(a, b)
    s["text"] = t
p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
text = "".join(s["text"] for s in d["segments"])
Path(r"E:\video-factory\1124\work\1124-fixed.txt").write_text(text, encoding="utf-8")
print("chars", len(text))
