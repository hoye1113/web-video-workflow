"""批量生成处境图（批次 C：emotion-full 那 12 张）。

流程（另一台机器验证过、本机也用同一套）：
    进项目 → 挂角色 chip → 清空+写提示词（读回核对）→ 点生成 → 等新图 → 取原图 → 落盘 → 量一眼

用法（可断点续跑：已存在的文件自动跳过）：
    python tools/gen_scenes.py            # 全部
    python tools/gen_scenes.py 01 02      # 只跑指定页（先跑 01 试路）
    python tools/gen_scenes.py --list     # 只看清单

产物：
    projects/scene-library/pNN-*.png      图
    projects/scene-library/batch-c-log.jsonl   记录（提示词、耗时、量出来的数）
"""
import io
import json
import pathlib
import sys
import time
import warnings

warnings.filterwarnings("ignore")          # Pillow 的 getdata 弃用提示会污染 stderr

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

from PIL import Image  # noqa: E402          # noqa: E402

PROJECT = "https://flow.google.com/project/2423a8a2-2219-4dd5-83ea-563fd00a79fb"
LIB = ROOT / "projects" / "scene-library"
LOG = LIB / "batch-c-log.jsonl"
SHOTS = ROOT / "experiments" / "uitest" / "flow"

STYLE = "暖色纸本插画，平涂加细铅笔线，一支笔的笔触，不描粗边不发光。"
TAIL = "米白纸底留白多，画面下方 20% 完全留空，不要任何文字、不要图表、不要箭头、不要圆圈、不要边框。"

# 顺序有讲究：**同一个角色连做**，最后才换角色（换角色要清 chip，重启会话最稳）
ITEMS = [
    # ---- 小树（男）----
    dict(page="01", file="p01-paper-fold.png", char="小树",
         scene="一个男孩独自坐在桌前，双手正把一张纸沿中线折下去，纸折到一半，顶光把纸面照亮，桌面干净"),
    dict(page="06", file="p06-sim-card.png", char="小树",
         scene="近景：一个男孩低头，双手拿着一部旧手机，拇指正把一张小小的电话卡从手机侧边顶出来，卡片刚弹起一点，看得清卡和手，桌面上有一支笔，侧顶光。只画这一组动作（半身），主体占画面中部"),
    dict(page="07", file="p07-crease.png", char="小树",
         scene="一个男孩低着头，一根食指反复掐着纸上同一道折痕，纸面看得见压痕，侧光打在手和纸上"),
    dict(page="10", file="p10-wine-glass.png", char="小树",
         scene="一个男孩独自坐着，一只举着酒杯的手从画面外伸进来停在半空，酒杯还没落到桌上，暖色侧光"),
    dict(page="13", file="p13-two-lights.png", char="小树",
         scene="一个男孩站在走廊中间，左侧照来一片暖黄的光、右侧照来一片冷青的光，两种光在他身上叠在一起，脚下两道方向不同的影子，正面看镜头"),
    dict(page="14", file="p14-scissors.png", char="小树",
         scene="一个男孩手持一把剪刀，停在一条绷紧的细线前面，没有剪下去，桌面和手被侧光照亮"),
    dict(page="16", file="p16-keys.png", char="小树",
         scene="夜里，一个男孩站在玄关，一根食指勾着一串钥匙垂在身侧，钥匙微微晃动，头顶只有一盏灯照着"),
    dict(page="21", file="p21-flatten.png", char="小树",
         scene="一个男孩把一团揉皱的纸放回桌面，手还停在纸上方，纸的褶皱清清楚楚，顶光照着桌面"),
    dict(page="23", file="p23-shreds.png", char="小树",
         scene="一个男孩的背影踩着一地碎纸片朝门口走去，门口逆光，影子被拉长，纸片散落一地"),
    dict(page="03", file="p03-cases.png", char="小树",
         scene="近景：桌面上摊着一大叠纸，男孩的手从中间抽出三张，那三张放在最上面，顶光照着纸面"),
    dict(page="11", file="p11-cup-choice.png", char="小树",
         scene="男孩坐在桌前，面前左边是一碗饭和一杯清水，右边放着一杯酒，他正看着那杯酒，暖色顶光"),
    dict(page="25", file="p25-ruler.png", char="小树",
         scene="近景：男孩的手把一把尺子压在纸上，纸上有一道折痕，尺子的刻度朝向镜头，侧光"),
    dict(page="20", file="p20-anesthesia.png", char="小树",
         scene="男孩坐在房间里，一束温暖的顶光落在他身上，他闭着眼睛仰起头，神情放松，四周是米白的墙面"),
    dict(page="22", file="p22-two-points.png", char="小树",
         scene="近景：男孩低头看着桌上一张纸，手里拿着一支笔，笔尖停在纸面上方，纸上有两个小墨点，侧顶光"),
    # ---- 小芽（女）----
    dict(page="02", file="p02-paper-window.png", char="小芽",
         scene="一个女孩背对镜头站着，面前是一扇糊着白纸的木窗，她的一根手指从屋里这侧把纸窗顶出一个小洞，洞外透进一线冷光，屋里昏暗"),
    dict(page="24", file="p24-clench.png", char="小芽",
         scene="一个女孩低头站着，双手把一张纸攥得越来越紧，纸被攥出褶皱，指节发白，冷色侧光照着她的侧脸和手"),
    dict(page="26", file="p26-smooth-refold.png", char="小芽",
         scene="一个女孩坐在桌前，双手把一张揉皱的纸抚平，又用指腹压出一道新的折痕，暖光照着桌面、手和她的侧脸"),
]


def full_prompt(scene):
    return STYLE + scene + "。" + TAIL


def metrics(png):
    """量一眼：尺寸 / 下方留白带 / 嫩芽色在不在。"""
    im = Image.open(io.BytesIO(png)).convert("RGB")
    w, h = im.size
    band = im.crop((0, int(h * 0.82), w, h)).resize((60, 12))
    px = list(band.getdata())
    mean = tuple(sum(c[i] for c in px) // len(px) for i in range(3))
    var = sum((c[i] - mean[i]) ** 2 for c in px for i in (0, 1, 2)) // (len(px) * 3)
    small = im.resize((160, 90))
    sprout = sum(1 for c in small.getdata()
                 if c[1] > 190 and c[0] > 160 and c[2] < 200 and (c[1] - c[2]) > 30)
    return {"w": w, "h": h, "band_mean": mean, "band_std": int(var ** 0.5), "sprout_px": sprout}


def main(argv):
    want = [a for a in argv[1:] if not a.startswith("-")]
    if "--list" in argv:
        for it in ITEMS:
            print(f'  {it["page"]}  {it["char"]}  {it["file"]}')
        return
    LIB.mkdir(parents=True, exist_ok=True)

    todo = [it for it in ITEMS
            if (not want or it["page"] in want) and not (LIB / it["file"]).exists()]
    skip = [it for it in ITEMS if it not in todo]
    print(f"要做 {len(todo)} 张，跳过 {len(skip)} 张（已存在或没选中）")
    for it in todo:
        print(f'  · {it["page"]} {it["char"]} {it["file"]}')
    if not todo:
        return

    done, failed = [], []
    # 按角色分组（同一角色连做；换角色 = 重启会话，免得 chip 串味）
    for char in dict.fromkeys(it["char"] for it in todo):
        group = [it for it in todo if it["char"] == char]
        f = flowgen.Flow(log=lambda *a: print("   ", *a, flush=True))
        try:
            f.enter(PROJECT)
            chips = f.attach_character(char)        # 挂不上会直接抛
            print(f"  chip：{json.dumps(chips, ensure_ascii=False)[:150]}")
            SHOTS.mkdir(parents=True, exist_ok=True)
            shot = SHOTS / f"attach-{char}.png"
            flowgen._bsk("screenshot", "--session", f.sid, "--out", str(shot), timeout=180)
            print(f"  截图存档（事后核对挂的是谁）：{shot.relative_to(ROOT)}")
            for it in group:
                prompt = full_prompt(it["scene"])
                if (LIB / it["file"]).exists():
                    continue
                t0 = time.time()
                print(f'\n[{it["page"]}] {it["file"]}（{char}）')
                blobs = None
                for attempt, wait_s in ((1, 300), (2, 420)):
                    try:
                        blobs = f.generate(prompt, timeout=wait_s, settle=8, keep=1)
                        break
                    except Exception as e:                      # noqa: BLE001
                        print(f"    第 {attempt} 次没成：{e}")
                        if attempt == 1:
                            time.sleep(5)
                if not blobs:
                    failed.append({"page": it["page"], "error": "两次都没等到"})
                    continue
                b = blobs[0]
                try:
                    m = metrics(b)
                except Exception as e:                          # noqa: BLE001
                    m = {"metrics_error": str(e)[:80]}
                # 存图（fetch 回来的是 webp，转成 png 跟图库一致）
                im = Image.open(io.BytesIO(b)).convert("RGB")
                im.save(LIB / it["file"])
                rec = dict(it, w=m.get("w"), h=m.get("h"),
                           band_mean=m.get("band_mean"), band_std=m.get("band_std"),
                           sprout_px=m.get("sprout_px"),
                           seconds=round(time.time() - t0, 1),
                           at=time.strftime("%Y-%m-%d %H:%M:%S"))
                with LOG.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                print(f'    ✓ {m.get("w")}x{m.get("h")} 留白带均值{m.get("band_mean")} '
                      f'std{m.get("band_std")} 嫩芽色像素{m.get("sprout_px")} '
                      f'（{rec["seconds"]}s）')
                done.append(it["page"])
        finally:
            f.close()
            time.sleep(2)

    print(f"\n═══ 批次 C：成功 {len(done)} 张（{' '.join(done)}），失败 {len(failed)}")
    for x in failed:
        print("   ✗", x)


if __name__ == "__main__":
    main(sys.argv)
