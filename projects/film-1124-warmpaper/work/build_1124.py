import json
from pathlib import Path

ROOT = Path(r"C:\Users\QWQ\web-video-workflow")
PROJ = "film-1124-warmpaper"
D = ROOT / "projects" / PROJ
OUT_ROOT = Path(r"E:\video-factory\1124")

STYLE = "暖色纸本插画，平涂加细铅笔线，一支笔的笔触，不描粗边不发光。"
TAIL = ("米白纸底留白多，主体在画面中部偏左，画面下方 20% 完全留空，"
        "左上留出一小块干净纸面放短标签；不要任何文字、图表、箭头、圆圈、边框。")

# id, cast, scene, label, theme, cam, reveal
FRAMES = [
    ("p01", "小树+小芽",
     "男孩和女孩坐在同一张沙发上，中间隔着一小段距离；男孩身体微微后仰，双手放在膝上；女孩身体前倾，手里捧着一只杯子想递给他；两人都看着对方，男孩的眼神有些躲",
     "焦虑吸引回避", "day", "push40", [0.32, 1, 0.2, 1.45]),
    ("p02", "小芽",
     "女孩独自坐在沙发一角，双腿蜷起来，手里握着一部手机，头低着；旁边放着一只没动的杯子，米白纸底留白很多",
     "多么煎熬", "day", "push55", [0.36, 1, 0.22, 1.5]),
    ("p03", "小树+小芽",
     "男孩坐在女孩旁边，身体前倾，手里拿着一杯热饮递给她；女孩双手接过，抬头看他；两人靠得比上一页近，男孩头顶的嫩芽立着",
     "最初动心", "day", "push40", [0.32, 1, 0.2, 1.45]),
    ("p04", "小树+小芽",
     "两人坐在小餐桌两侧，男孩给女孩倒茶，女孩双手捧着杯子；桌上只有一只茶壶和两只杯子，暖色侧光",
     "事事体贴", "day", "push55", [0.34, 1, 0.22, 1.5]),
    ("p05", "小树+小芽",
     "两人坐在沙发上，女孩身体明显倾向男孩，手伸向他的手臂；男孩身体后仰，双手放在膝上，视线偏向一边；两人之间出现一小段距离",
     "高开低走", "day", "pull", [0.34, 1, 0.22, 1.5]),
    ("p06", "小树+小芽",
     "男孩独自坐在书桌前，一只手撑着额头，桌上摊着几本书；女孩站在门口，手里握着手机，看着他，没有走进去",
     "情感需求", "day", "push40", [0.36, 1, 0.22, 1.5]),
    ("p07", "小树+小芽",
     "女孩拿着手机靠近男孩，身体前倾，像在追问；男孩后退到门边，一只手已经搭在门把上，视线避开她",
     "越追越逃", "day", "push55", [0.36, 1, 0.22, 1.5]),
    ("p08", "小树+小芽",
     "女孩坐在桌边，面前摊着笔记本，双手比划着想沟通；男孩背对她坐在沙发另一端，戴着耳机，身体缩着",
     "闭口不谈", "day", "push40", [0.34, 1, 0.22, 1.5]),
    ("p09", "小树+小芽",
     "女孩把一条毯子轻轻递向男孩，男孩坐在沙发上双臂抱在胸前，身体往旁边让了一点；两人都没有笑",
     "爱意索取", "day", "push55", [0.36, 1, 0.22, 1.5]),
    ("p10", "小树+小芽",
     "男孩坐在沙发前的地上，背靠沙发，头低着；女孩站在他身后，手里端着一只杯子，安静看着他",
     "一味躲避", "day", "pull", [0.34, 1, 0.22, 1.5]),
    ("p11", "小树+小芽",
     "女孩坐在桌边，手里拿着手机和一支笔，像在追问一个答案；男孩站在门口，穿着外套，手放在门把上，准备离开",
     "刨根问底", "day", "push40", [0.36, 1, 0.22, 1.5]),
    ("p12", "小树",
     "男孩独自坐在昏暗房间的角落，抱着膝盖，头低着；头顶的嫩芽有一点下垂，米白纸底留白很多",
     "故作冷漠", "day", "push55", [0.4, 1, 0.24, 1.6]),
    ("p13", "小树+小芽",
     "两人坐在同一张沙发两端，各自低头看着自己的手；中间放着一只小杯子，谁都没有先开口",
     "真心喜欢", "day", "pull", [0.34, 1, 0.22, 1.5]),
    ("p14", "小树+小芽",
     "女孩坐在桌边，看着一个空白的旧相框和一把空椅子；男孩站在窗边，背对着她，窗外是柔和的纸色",
     "依恋人格", "day", "push40", [0.36, 1, 0.22, 1.5]),
    ("p15", "小树+小芽",
     "男孩站在窗前，双臂抱在胸前，看着窗外；女孩站在门口，手里拿着一条毯子，没有走近",
     "压抑情绪", "day", "push55", [0.36, 1, 0.22, 1.5]),
    ("p16", "小树+小芽",
     "两人坐在餐桌两侧，桌上堆着几只没收拾的杯子和一叠纸；男孩低头，女孩看着他，气氛安静",
     "真实本性", "day", "push40", [0.34, 1, 0.22, 1.5]),
    ("p17", "小树+小芽",
     "女孩坐在沙发上，手里拿着一个空白相框，低头看；男孩站在门口，身体已经转向外面，像要离开",
     "完美爱人", "day", "pull", [0.34, 1, 0.22, 1.5]),
    ("p18", "小树+小芽",
     "女孩坐在书桌前，面前摊着笔记本，手里拿着笔；男孩站在窗边，把窗户推开一条缝，光透进来",
     "重塑心态", "day", "push55", [0.34, 1, 0.22, 1.5]),
    ("p19", "小树+小芽",
     "女孩坐在桌边，面前摊着笔记本和笔，桌上并排放着三只小杯子；男孩站在旁边，看着她写",
     "三件事", "day", "push40", [0.36, 1, 0.22, 1.5]),
    ("p20", "小树+小芽",
     "两人坐在餐桌两侧，桌上摊着一本空白笔记本、两只杯子和三颗小石子；男孩和女孩都看着桌面",
     "值得携手", "day", "push55", [0.34, 1, 0.22, 1.5]),
    ("p21", "小树+小芽",
     "两人并肩站在窗边，窗外是米白的纸色晨光；窗台上放着一盆小植物，两人都看着窗外",
     "再决定", "day", "hold", [0.34, 1, 0.22, 1.5]),
]

src = json.loads((D / "script-source.json").read_text(encoding="utf-8"))
assert len(FRAMES) == len(src["pages"]), (len(FRAMES), len(src["pages"]))


def prompt(scene):
    return STYLE + scene + "。" + TAIL


queue = []
genq = {"tasks": []}
md = ["# 页 → 处境映射（film-1124-warmpaper）", "",
      "> 小树 / 小芽 · 暖色纸本 16:9；小树=回避型男孩，小芽=焦虑型女孩；21 页；只交无字幕。", ""]
md.append("| 页 | 讲什么 | 场景 | 屏上标签 | 角色 | 机位 |")
md.append("|---|---|---|---|---|---|")

for pid, cast, scene, label, theme, cam, reveal in FRAMES:
    page = next(p for p in src["pages"] if p["id"] == pid)
    asset = f"f1124-{pid}.png"
    queue.append({"id": pid, "cast": cast, "prompt": prompt(scene),
                  "out": str((ROOT / "projects" / "scene-library" / asset).resolve()).replace("\\", "/")})
    genq["tasks"].append({"id": f"{pid}-1", "page": pid, "cast": cast, "scene": scene,
                          "out": asset, "layout": "card", "status": "queued", "tries": 0,
                          "error": "", "img": "", "metrics": {}, "at": "2026-11-24 10:00:00"})
    md.append(f"| {pid} | {page.get('title','')} | {scene} | {label} | {cast} | {cam} |")

spec = []
for pid, cast, scene, label, theme, cam, reveal in FRAMES:
    page = next(p for p in src["pages"] if p["id"] == pid)
    spec.append({
        "id": pid,
        "title": page.get("title", ""),
        "asset": f"f1124-{pid}.png",
        "theme": theme,
        "cam": cam,
        "reveal": reveal,
        "lights": [],
        "texts": [[label, 250, 230, 44, "l", "ink", 1.4]] if label else [],
    })

(D / "docs").mkdir(exist_ok=True)
(D / "docs" / "页-处境映射.md").write_text("\n".join(md) + "\n", encoding="utf-8")
(D / "page-spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
(D / "gen-queue.json").write_text(json.dumps(genq, ensure_ascii=False, indent=1), encoding="utf-8")

W = OUT_ROOT / "work"
W.mkdir(parents=True, exist_ok=True)
for i in range(2):
    chunk = queue[i * 11:(i + 1) * 11]
    (W / f"queue-{i+1}.json").write_text(json.dumps(chunk, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"queue-{i+1}: {len(chunk)}")
(W / "queue-all.json").write_text(json.dumps(queue, ensure_ascii=False, indent=1), encoding="utf-8")

print(f"pages={len(FRAMES)} specs={len(spec)}")
