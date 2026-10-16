"""静态检查一页场景代码。真正的逻辑在 app/checks.py。

    python tools/scene_lint.py <项目> <页号> [--json]
"""
import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "app"))
import checks  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("project")
ap.add_argument("shot")
ap.add_argument("--json", action="store_true")
a = ap.parse_args()

r = checks.scene_lint(a.project, a.shot)
if a.json:
    print(json.dumps(r, ensure_ascii=False, indent=2))
    sys.exit(len(r["problems"]) > 0)

print(f"页 {a.shot}　{r['chars']} 字　色板 {len(r['palette'])} 色　"
      f"显式线宽 {', '.join(f'{x:g}' for x in r.get('lineWidths') or []) or '（无）'}")
print()
for p in r["problems"] or ["（无）"]:
    print("  ✗" if r["problems"] else "   ", p)
if r["warnings"]:
    print("黄灯：")
    for p in r["warnings"]:
        print("  !", p)
print()
print(f"结论：{'有红灯，先改' if r['problems'] else '可以通过'}")
sys.exit(1 if r["problems"] else 0)
