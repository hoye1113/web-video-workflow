import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
P = ROOT / "projects/infidelity-1021"

src = json.loads((P / "script-source.json").read_text(encoding="utf-8"))
spec = json.loads((P / "page-spec.json").read_text(encoding="utf-8"))
md = (P / "docs/页-处境映射.md").read_text(encoding="utf-8")

ok = True


def chk(cond, msg):
    global ok
    print(("  OK   " if cond else "  FAIL ") + msg)
    if not cond:
        ok = False


print("=== script-source.json ===")
ids = [p["id"] for p in src["pages"]]
chk(len(src["pages"]) == 54, f"页数 = {len(src['pages'])}（要 50-60）")
chk(ids == [f"p{i:02d}" for i in range(1, len(ids) + 1)], "id 连续 p01..pNN")
chk(src["voice"]["speaker"] == "zh-CN-XiaoxiaoNeural", "voice.speaker 用 brief 里的")
tot = sum(len(c) for p in src["pages"] for c in p["cues"])
chk(2200 <= tot <= 2350, f"总字数 = {tot}（目标 ≈2300）")
bad = [(p["id"], c, len(c)) for p in src["pages"] for c in p["cues"] if len(c) > 12]
chk(not bad, f"每条 cue ≤12 字（超标 {len(bad)}）{bad}")
PUNCT = re.compile(r"[，。！？；：、,.!?;:—…]")
nop = [(p["id"], c) for p in src["pages"] for c in p["cues"]
       if len(c) >= 12 and not PUNCT.search(c[-1:])]
chk(not nop, f"第 12 字前有标点（缺 {len(nop)}）")
secs = [len(p["cues"]) for p in src["pages"]]
chk(min(secs) >= 4 and max(secs) <= 8, f"每页 cue 数 {min(secs)}-{max(secs)}（4-8）")

print("=== page-spec.json ===")
chk(len(spec) == len(src["pages"]), f"页数与台词一致：{len(spec)} vs {len(src['pages'])}")
chk([s["id"] for s in spec] == ids, "id 与台词逐页一致")
chk([s["title"] for s in spec] == [p["title"] for p in src["pages"]], "title 与台词一致")
chk(all(s["asset"] == "" for s in spec), "asset 全为空（等出图后回填）")
chk(all(s["theme"] in ("day", "night") for s in spec), "theme 只有 day/night")
chk(all(s["cam"] in ("push40", "push55", "pull", "tight55") for s in spec),
    "cam 只有 push40/push55/pull/tight55")
chk(all(len(s["reveal"]) == 4 for s in spec), "reveal 是 [from,to,at,dur]")
chk(all(isinstance(s["lights"], list) and all(len(l) == 7 for l in s["lights"]) for s in spec),
    "lights 每条 7 项")
chk(all(len(t) == 7 for s in spec for t in s["texts"]), "texts 每条 7 项")
long_txt = [(s["id"], t[0], len(t[0])) for s in spec for t in s["texts"] if len(t[0]) > 8]
chk(not long_txt, f"屏上字 ≤8 字（超标 {long_txt}）")
low = [(s["id"], t[1], t[2]) for s in spec for t in s["texts"] if t[2] > 260]
chk(not low, f"屏上字 y ≤260（下方留字幕带）（越界 {low}）")
no_l = [s["id"] for s in spec if not s["lights"]]
chk(not no_l, f"每页都有光（缺 {no_l}）")
print("  主题分布：", {t: sum(1 for s in spec if s["theme"] == t) for t in ("day", "night")})
print("  机位分布：", {c: sum(1 for s in spec if s["cam"] == c)
                        for c in ("push40", "push55", "pull", "tight55")})

print("=== docs/页-处境映射.md ===")
lines = md.splitlines()
head = [l for l in lines if l.strip().startswith("| 页")]
chk(len(head) == 1 and head[0].strip() == "| 页 | 讲什么 | 画面 | 主角 |",
    f"表头严格一致：{head[0].strip() if head else '（没有）'}")
rows = [l for l in lines if re.match(r"^\|\s*p\d\d\s*\|", l)]
chk(len(rows) == 54, f"表里 {len(rows)} 行（要 54）")
row_ids = [re.match(r"^\|\s*(p\d\d)\s*\|", l).group(1) for l in rows]
chk(row_ids == ids, "表里的页号与台词逐页一致")
bad_cast = [r[:12] for r in rows if not re.search(r"\|\s*(小树|小芽)\s*\|\s*$", r)]
chk(not bad_cast, f"主角列只有 小树/小芽（异常 {bad_cast}）")
empty = [r[:12] for r in rows if len([c for c in r.split("|") if c.strip()]) < 4]
chk(not empty, f"每行四列都有内容（空 {empty}）")
short_scene = [r[:12] for r in rows if len(r.split("|")[3].strip()) < 15]
chk(not short_scene, f"画面列是一句处境（太短 {short_scene}）")

print("\n结果：", "全部通过" if ok else "有 FAIL")
