import json
import pathlib

P = pathlib.Path(__file__).resolve().parent.parent / "projects/infidelity-1021"
src = json.loads((P / "script-source.json").read_text(encoding="utf-8"))
spec = json.loads((P / "page-spec.json").read_text(encoding="utf-8"))
out = []
for a, b in zip(src["pages"], spec):
    if a["title"] != b["title"]:
        out.append(f"{a['id']}\tSCRIPT: {a['title']}\tSPEC: {b['title']}")
(P.parent.parent / "experiments/tmp_titles.txt").write_text("\n".join(out), encoding="utf-8")
print("diffs:", len(out))
