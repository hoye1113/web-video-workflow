import pathlib
import re

p = pathlib.Path(r"D:\WorkSpace\video-factory\web\node_modules\react-resizable-panels\dist\react-resizable-panels.d.ts")
t = p.read_text(encoding="utf-8", errors="replace")
for name in ("PanelProps", "GroupProps", "SeparatorProps"):
    i = t.find(f"type {name} =")
    if i < 0:
        i = t.find(f"interface {name} ")
    print(f"=== {name} ===")
    print(t[i:i + 900] if i >= 0 else "没找到")
    print()
