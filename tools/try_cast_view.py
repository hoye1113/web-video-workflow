"""端到端验证：挂参考图 + 生成一张"女主的背面"。

这一步回答两件事：
  ① 参考图这条路通不通（attach 能不能挂上、挂上后生成还成不成功）
  ② **形象锁不锁得住**（生成出来的还是不是那个女孩）
"""
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

REF = ROOT / "cast" / "girl.jpg"
OUT_DIR = ROOT / "experiments" / "cast-views"
PROMPT = (
    "同一张角色设定图里的那个 Q 版女孩，画她的**背面全身**："
    "浅栗灰粉齐肩微卷短发、**头顶一片两叶嫩芽**、穿米白色超大号连帽卫衣（袖子长到手背）、下摆盖过胯、"
    "光腿、深棕色小短靴。构图：人物居中，占画面高度约七成，白色纯底，无背景、无道具、无文字。"
    "画风与设定图完全一致：Q 版三头身、大头、平涂 + 细线（深棕不纯黑）、低饱和浅色。"
)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    f = flowgen.Flow()
    t0 = time.time()
    try:
        f.open()
        f.attach(REF)
        blobs = f.generate(PROMPT, timeout=300)
        names = flowgen.save_images("cast", {"id": "girl-back"}, blobs) if False else None
        # 存到 cast-views/（不塞进 projects）
        saved = []
        for i, b in enumerate(blobs, 1):
            p = OUT_DIR / f"girl-back-{i}.png"
            p.write_bytes(b)
            saved.append(p)
        print(f"拿到 {len(blobs)} 张，用时 {time.time()-t0:.0f}s：")
        for p in saved:
            print("   ", p.relative_to(ROOT))
    finally:
        f.close()


if __name__ == "__main__":
    main()
