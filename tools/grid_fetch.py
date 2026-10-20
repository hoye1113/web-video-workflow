"""把 Flow 项目网格里**最新的几张图**取回本地（网格按新到旧排，所以前 N 张就是刚出的）。

用法：
    python tools/grid_fetch.py <片名> <张数> <前缀>
    python tools/grid_fetch.py film-1020-1522 4 rescue

产物：projects/scene-library/rescue-01.png、rescue-02.png…（按网格顺序，1 = 最新）
"""
import io
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))

import flowgen                                          # noqa: E402

from PIL import Image                                   # noqa: E402

# Windows 的控制台是 GBK，中文/符号会直接抛 UnicodeEncodeError —— 一律降级输出
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:                                        # noqa: BLE001
    pass

LIB = ROOT / "projects" / "scene-library"
PROJECT = "https://flow.google.com/project/2423a8a2-2219-4dd5-83ea-563fd00a79fb"


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 1
    n = int(sys.argv[2])
    prefix = sys.argv[3]
    LIB.mkdir(parents=True, exist_ok=True)
    f = flowgen.Flow(log=lambda *a: print("   ", *a, flush=True))
    try:
        f.enter(PROJECT)
        bases = f._run(
            "(()=>{const H=['flow-content.google','flow.google.com/asb','/asb/'];"
            "const out=[];for(const i of document.querySelectorAll('img')){"
            "const u=i.src||'';if(!H.some(h=>u.includes(h)))continue;"
            "out.push(u.replace(/=s\\d+(-rw)?$/,''));}return out;})()"
        )
        if not isinstance(bases, list):
            print("no bases:", bases)
            return 1
        seen, uniq = set(), []
        for b in bases:
            if b not in seen:
                seen.add(b)
                uniq.append(b)
        print(f"网格里 {len(uniq)} 张，取最新 {min(n, len(uniq))} 张")
        got = f._fetch_raw(uniq[:n], min_w=900)
        for i, x in enumerate(got, 1):
            import base64
            blob = base64.b64decode(x["b64"])
            out = LIB / f"{prefix}-{i:02d}.png"
            Image.open(io.BytesIO(blob)).convert("RGB").save(out)
            print(f"  [ok] {out.name}  {x['w']}x{x['h']}")
        if len(got) < n:
            print(f"  （只取到 {len(got)} 张）")
    finally:
        f.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
