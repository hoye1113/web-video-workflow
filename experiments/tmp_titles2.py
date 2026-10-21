import json
import pathlib
import re

P = pathlib.Path(__file__).resolve().parent.parent / "projects/infidelity-1021"
src = json.loads((P / "script-source.json").read_text(encoding="utf-8"))
md = (P / "docs/页-处境映射.md").read_text(encoding="utf-8")
rows = [l for l in md.splitlines() if re.match(r"^\|\s*p\d\d\s*\|", l)]
out = []
for pg, row in zip(src["pages"], rows):
    cols = [c.strip() for c in row.split("|")]
    if cols[2] != pg["title"]:
        out.append(f"{pg['id']}\tTABLE: {cols[2]}\tSCRIPT: {pg['title']}")
(pathlib.Path(__file__).resolve().parent / "tmp_titles2.txt").write_text("\n".join(out), encoding="utf-8")
print("讲什么 与 title 不一致的页数:", len(out))
