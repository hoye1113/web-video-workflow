import json
from pathlib import Path

ROOT = Path(r"C:\Users\QWQ\web-video-workflow")
D = ROOT / "projects" / "film-1124-warmpaper"
LIB = ROOT / "projects" / "scene-library"

q = json.loads((D / "gen-queue.json").read_text(encoding="utf-8"))
missing = []
for t in q["tasks"]:
    name = t.get("out") or ""
    p = LIB / name
    if name and p.exists():
        t["img"] = name
        t["status"] = "done"
        t["error"] = ""
    else:
        missing.append(t.get("page"))
(D / "gen-queue.json").write_text(json.dumps(q, ensure_ascii=False, indent=1), encoding="utf-8")
print("tasks", len(q["tasks"]), "missing", missing)
