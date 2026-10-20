"""用面板自己的解析逻辑读分镜表（apps/intern/server.py 的 map_rows）→ 看实习生在页面上看到几行。

用法：python experiments/check_map_rows.py <片名>
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "apps" / "intern"))
sys.path.insert(0, str(ROOT / "tools"))

import pipeline                                            # noqa: E402
import server as intern                                   # noqa: E402


def main():
    proj = sys.argv[1] if len(sys.argv) > 1 else "film-1020-1522"
    rows = intern.map_rows(proj)
    print(f"面板看到的分镜行数：{len(rows)}")
    for r in rows:
        print(f"  {r[0]:<5} {r[1][:34]:<36} {r[2][:40]:<42} {r[3]}")
    spec = json.loads((pipeline.proj_dir(proj) / "page-spec.json").read_text(encoding="utf-8"))
    print(f"\n页表页数：{len(spec)}  → {'一致' if len(rows) == len(spec) else '不一致'}")
    return 0 if len(rows) == len(spec) else 1


if __name__ == "__main__":
    sys.exit(main())
