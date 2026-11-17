import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAST = json.loads((ROOT / "cast.json").read_text(encoding="utf-8"))
SCENES = json.loads((ROOT / "tests" / "scene-prompts.json").read_text(encoding="utf-8"))

STYLE = CAST["style"]
YIER = "一二：白色圆润熊猫，黑色耳朵与眼圈，脸颊粉色腮红，颈间深棕色小领结；身体和四肢都是白色，不要黑色手脚。"
BUBU = "布布：浅焦糖棕色小熊，圆耳，杏黄色腮红，身后一颗小圆尾巴。"

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
