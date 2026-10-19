"""接着已设置好的会话：改提示词 → 点生成 → 等新图 → 抓回来。

前提（上一轮已验证）：参考图已挂在提示框里，基线 17 张已知。
这次要验证的核心是：**生成的新图能不能被稳定认出来并抓下来**。
"""
import json
import pathlib
import re
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

SID = sys.argv[1] if len(sys.argv) > 1 else "yldy"
NAME = sys.argv[2] if len(sys.argv) > 2 else "test"
PROMPT = "画面里只出现这一个角色本人：**近景半身**，表情是「忍住不哭」（眼眶含泪、嘴唇抿住、眉微皱）；纯白底、无道具、无文字、无边框；画风与参考图完全一致。"
OUT = ROOT / "experiments" / "cast-views"

f = flowgen.Flow()
f.sid = SID
print("会话:", SID)

# 清空输入框里之前的文字，写新的
before = f._image_urls()
print(f"生成前，已知 {len(before)} 张")

t = f._run("(()=>{const vis=(e)=>e.offsetParent!==null;"
           "const e=[...document.querySelectorAll('[contenteditable=true]')].filter(vis).pop();"
           "if(!e)return 'no input';e.focus();document.execCommand('selectAll',false,null);"
           "document.execCommand('delete',false,null);return 'cleared';})()")
print("清空输入框：", t)
time.sleep(1)
w = f._type_prompt(PROMPT)
print("写提示词：", json.dumps(w, ensure_ascii=False)[:120])
back = f._run("(()=>{const vis=(e)=>e.offsetParent!==null;"
              "const e=[...document.querySelectorAll('[contenteditable=true]')].filter(vis).pop();"
              "return e?(e.textContent||'').trim().slice(0,60):'';})()")
print("读回：", repr(back))

print("\n=== 点生成 ===")
c = f._click_generate()
print("  ", json.dumps(c, ensure_ascii=False)[:200])

print("=== 等新图 ===")
blobs = []
deadline = time.time() + 300
last = 0
while time.time() < deadline:
    time.sleep(6)
    new = f._image_urls() - before
    if len(new) != last:
        print(f"  +{len(new)} 张")
        last = len(new)
    if len(new) >= 1:
        time.sleep(8)
        new = f._image_urls() - before
        break
new = sorted(f._image_urls() - before)
print(f"  新图 {len(new)} 张")
if new:
    blobs = f._fetch(new)
for i, b in enumerate(blobs, 1):
    OUT.mkdir(parents=True, exist_ok=True)
    webp = OUT / f"{NAME}-{i}.webp"
    webp.write_bytes(b)
    png = OUT / f"{NAME}-{i}.png"
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(webp), str(png)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode == 0:
        webp.unlink()
        print("  存:", png.relative_to(ROOT), f"({len(b)//1024} KB)")
    else:
        print("  存:", webp.relative_to(ROOT), f"({len(b)//1024} KB)")
