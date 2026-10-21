import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
b = json.loads((ROOT / "projects/infidelity-1021/brief.json").read_text(encoding="utf-8"))
print("keys:", list(b.keys()))
print("topic:", b.get("topic"))
print("minutes:", b.get("minutes"))
m = b.get("materials", "")
print("materials chars:", len(m))
print("---- tail 600 ----")
print(m[-600:])
