import pathlib

root = pathlib.Path(r"D:\WorkSpace\video-factory\experiments\aui-test\node_modules\@assistant-ui\react-data-stream")
print("=== protocol.d.ts ===")
print((root / "dist" / "protocol.d.ts").read_text(encoding="utf-8", errors="replace")[:2500])
print()
print("=== index.d.ts ===")
print((root / "dist" / "index.d.ts").read_text(encoding="utf-8", errors="replace")[:1200])
print()
print("=== useDataStreamRuntime.d.ts ===")
print((root / "dist" / "useDataStreamRuntime.d.ts").read_text(encoding="utf-8", errors="replace")[:1500])
