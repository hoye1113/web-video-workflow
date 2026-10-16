"""手工试一次 Flow 生图：拿第 01 页的 imagePrompt 真跑一遍。"""
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402
import store    # noqa: E402

PROJ = "marriage_full"
SHOT = sys.argv[1] if len(sys.argv) > 1 else "01"

m = store.load(PROJ)
p = next((s for s in m["shots"] if s["id"] == SHOT), None)
if not p:
    sys.exit(f"没有第 {SHOT} 页")
prompt = (p.get("imagePrompt") or "").strip()
if not prompt:
    sys.exit(f"第 {SHOT} 页没有 imagePrompt（mode={p.get('mode')}）")

print(f"第 {SHOT} 页　mode={p.get('mode')}")
print(f"提示词：{prompt[:110]}…")
print()

f = flowgen.Flow()
t0 = time.time()
try:
    f.open()
    print("…开始生成")
    blobs = f.generate(prompt)
    print(f"拿到 {len(blobs)} 张，共 {sum(len(b) for b in blobs)//1024} KB，用时 {time.time()-t0:.0f}s")
    names = flowgen.save_images(PROJ, SHOT, blobs)
    print("存到：")
    for n in names:
        print("  projects/%s/assets/%s" % (PROJ, n))
    # 记进项目
    m = store.load(PROJ)
    for s in m["shots"]:
        if s["id"] == SHOT:
            s["images"] = names
    store.save(PROJ, m)
    print("已记进 project.json 的 images 字段")
finally:
    f.close()
    print("bsk 会话已关")
