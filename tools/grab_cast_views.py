"""抓生成图（用 flowgen._fetch：它在浏览器里 fetch + 按尺寸过滤，缩略图会被丢掉）。"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

SID = sys.argv[1] if len(sys.argv) > 1 else "zylj"
PREFIX = sys.argv[2] if len(sys.argv) > 2 else "back"
OUT = ROOT / "experiments" / "cast-views"
OUT.mkdir(parents=True, exist_ok=True)

f = flowgen.Flow()
f.sid = SID
urls = sorted(f._image_urls())
print(f"候选 {len(urls)} 张（含素材缩略图），按宽度 ≥900 过滤后：")
blobs = f._fetch(urls)
print(f"   留下 {len(blobs)} 张")
for i, b in enumerate(blobs, 1):
    webp = OUT / f"{PREFIX}-{i}.webp"
    webp.write_bytes(b)
    png = OUT / f"{PREFIX}-{i}.png"
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(webp), str(png)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode == 0:
        webp.unlink()
        print("   ", png.relative_to(ROOT), f"({len(b)//1024} KB)")
    else:
        print("   ", webp.relative_to(ROOT), f"({len(b)//1024} KB, 转换失败留着原文件)")
