import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAST = json.loads((ROOT / "cast.json").read_text(encoding="utf-8"))
SCENES = json.loads((ROOT / "tests" / "scene-prompts.json").read_text(encoding="utf-8"))

STYLE = CAST["style"]
YIER = "1布布（一二，女）：白色圆润熊猫，黑色实心圆耳朵，脸部纯白、没有黑眼圈，深棕色小圆眼，粉色腮红，颈间黑色小领结，白色小短手，黑色小圆脚；女性。"
BUBU = "2布布（布布，男）：暖棕色小熊，圆耳朵，内耳深棕，脸部纯棕、没有黑眼圈，深棕色小圆眼，杏黄色腮红，身后一颗小圆尾巴；男性，比1布布略大一点。"

def build(item):
    individual = item["id"] in {"yier-hero", "bubu-hero"}
    if item["id"] == "yier-hero":
        chars = YIER + "画面只出现一二这一只角色，全身入镜。"
    elif item["id"] == "bubu-hero":
        chars = BUBU + "画面只出现布布这一只角色，全身入镜。"
    else:
        chars = YIER + BUBU + "两只角色外形与参考图完全一致，各只出现一次、全身入镜。"
    return (
        STYLE["prompt"] + chars +
        f'【场景】{item["scene"]}。'
        f'【情绪】布布在「够」：{item["bubu_action"]}；一二在「挡」：{item["yier_action"]}。'
        f'【光】{item["light"]}。'
        f'【道具】{item["props"]}。'
        f'【文字】{item["text_rule"]}。'
        + STYLE["tail"]
    )

queue = []
for item in SCENES:
    queue.append({
        "id": item["id"],
        "cast": "",
        "prompt": build(item),
        "out": str((ROOT / "refs" / item["out"]).resolve()).replace("\\", "/"),
    })

(ROOT / "tests" / "refs-queue.json").write_text(
    json.dumps(queue, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"queue: {len(queue)}")
for q in queue:
    print(q["id"], "->", q["out"])
