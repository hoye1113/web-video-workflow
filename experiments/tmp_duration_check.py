import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = json.loads((ROOT / "projects/emotion-full/script-source.json").read_text(encoding="utf-8"))
pages = src["pages"]
cues = [c for p in pages for c in p["cues"]]
raw = (ROOT / "projects/emotion-full/voice.js").read_bytes()
txt = raw.decode("utf-8")

# voice.js: {"f":..., "d":..., "o":..., "k":[...], "t":"..."}
items = re.findall(r'\{"f":\s*"([^"]+)",\s*"d":\s*([0-9.]+).*?"t":\s*"((?:[^"\\]|\\.)*)"\}', txt)
print("parsed", len(items), "of", len(cues))


def unesc(s):
    return json.loads('"' + s + '"')


rows = []
for (f, d, t) in items:
    rows.append((unesc(t), float(d)))

# fit: d = c/SPEED + tail(type)
type_of = lambda c: "p" if c.rstrip()[-1] in "。！？" else ("c" if c.rstrip()[-1] in "，、；" else "o")
buckets = {}
for t, d in rows:
    buckets.setdefault(type_of(t), []).append((len(t), d))
for k, v in buckets.items():
    print(k, "n=", len(v), "avg chars", round(sum(x for x, _ in v) / len(v), 2),
          "avg d", round(sum(d for _, d in v) / len(v), 3))

# least squares fit d = c/S + tail, separately per type: solve S by regression on d = a*c + b
def reg(v):
    n = len(v)
    sx = sum(c for c, _ in v); sy = sum(d for _, d in v)
    sxx = sum(c * c for c, _ in v); sxy = sum(c * d for c, d in v)
    a = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    b = (sy - a * sx) / n
    return a, b

for k, v in buckets.items():
    a, b = reg(v)
    print(f"{k}: d = {a:.4f}*chars + {b:.3f}   -> SPEED={1/a:.2f} chars/s, tail={b:.3f}s")

# global model with one speed and per-type tails: iterate
S = 4.13
for _ in range(60):
    tails = {}
    for k, v in buckets.items():
        tails[k] = sum(d - len(t) / S for t, d in v) / len(v)
    # then re-fit speed given tails
    num = sum((len(t) - 0) * (d - tails[type_of(t)]) for t, d in rows)
    den = sum(len(t) ** 2 for t, _ in rows)
    S = den / num
print("SPEED", round(S, 3), "tails", {k: round(v, 3) for k, v in tails.items()})

def predict(pages_):
    tot = 0.0
    for p in pages_:
        for c in p["cues"]:
            tot += len(c) / S + tails.get(type_of(c), 0.2)
        tot += 0.8
    return tot

print("emotion-full predicted", round(predict(pages), 1), "s ; actual audio", round(sum(d for _, d in rows), 1))
print("chars/sec effective", round(sum(len(t) for t, _ in rows) / sum(d for _, d in rows), 3))
