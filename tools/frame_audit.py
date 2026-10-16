"""量渲染帧。真正的逻辑在 app/checks.py。

    python tools/frame_audit.py <项目> <页号> [--json]
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

r = checks.frame_audit(a.project, a.shot)
if a.json:
    print(json.dumps(r, ensure_ascii=False, indent=2))
    sys.exit(len(r.get("problems", [])) > 0)
if r.get("error"):
    print("✗", r["error"])
    sys.exit(2)

print(f"页 {a.shot}　色板 {len(r['palette'])} 色（色相 {len(r['palette_hues'])} 个）"
      f"　镜头 {r.get('camera')}　{len(r['frames'])} 帧")
print()
print("帧号            新色相(最脏格) 色相差  内容框 w×h    重心        帧差")
for f in r["frames"]:
    b, c = f["box"], f["centroid"]
    print(f"  {f['frame']:<14} {f['newhue_cell']*100:>9.1f}%   {f['max_gap']:>5.0f}°  "
          f"{b[0]:>4.0%}×{b[1]:<4.0%}  ({c[0]:.2f},{c[1]:.2f})  "
          + (f"{f['diff']:>6.2f}" if "diff" in f else "     —"))
print()
if r["problems"]:
    print("红灯：")
    for p in r["problems"]:
        print("  ✗", p)
else:
    print("红灯：无")
if r["warnings"]:
    print("黄灯：")
    for p in r["warnings"]:
        print("  !", p)
print()
print(f"结论：{'有问题，先改' if r['problems'] else '可以通过'}")
sys.exit(1 if r["problems"] else 0)
