"""素材库索引：扫图 + 量指标 + 标"用在哪些页"，写成 `projects/scene-library/index.json`。

为什么要它：面板上"选图/选角色/看一致性"全靠这份索引 —— 现在这些信息散在
README 手写表、批量生成日志、各片的 page-spec 里。**索引是素材库模块的地基。**

每张图一条：
    file / cast（小树|小芽|不定）/ scene（处境一句话，从生成日志来）/
    w h / band_std（下方留白带越平越好）/ sprout_px（嫩芽色像素，0 = 可能丢了识别符号）/
    used_by（哪部片子的哪一页）/ status（等审批|已通过|打回）

用法：
    python tools/lib_index.py            # 写索引 + 打印概况
    python tools/lib_index.py --check    # 只打印
"""
import json
import pathlib
import sys
import warnings

warnings.filterwarnings("ignore")

# Windows 控制台是 GBK：打印 '⚠'/'✓' 会抛 UnicodeEncodeError（会带倒整批活）
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:                                        # noqa: BLE001
    pass

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIB = ROOT / "projects" / "scene-library"
OUT = LIB / "index.json"

SPROUT = (0xDE, 0xF0, 0xA8)          # 嫩芽色 #DEF0A8
# 嫩芽判据（2026-10-20 与 tools/gen_scenes.py 对齐）：老窗口只认最亮的嫩芽，
# 暗一点的橄榄绿嫩芽会被判成 0。**这是提示不是判决 —— 头顶有没有芽要人眼看。**
SPROUT_MIN = 12                      # 低于这个数 → 提示"看一眼头顶"


def metrics(f: pathlib.Path):
    from PIL import Image
    im = Image.open(f).convert("RGB")
    w, h = im.size
    band = im.crop((0, int(h * 0.82), w, h)).resize((60, 12))
    px = list(band.getdata())
    mean = tuple(sum(c[i] for c in px) // len(px) for i in range(3))
    var = sum((c[i] - mean[i]) ** 2 for c in px for i in (0, 1, 2)) // (len(px) * 3)
    small = im.resize((160, 90))
    sprout = sum(1 for c in small.getdata()
                 if c[1] > 150 and c[0] > 110 and c[2] < 190 and (c[1] - c[2]) > 25)
    return {"w": w, "h": h, "band_std": int(var ** 0.5), "sprout_px": sprout}


def gen_log():
    """批量生成日志 → {文件名: {char, scene}}（这是"这张图是谁、画的是什么"的出处）。

    两个日志都读：
      · batch-c-log.jsonl   —— 批次 C（tools/gen_scenes.py）
      · gen-worker.log.jsonl —— 队列执行器（tools/gen_worker.py），字段名是 cast/scene/file
    """
    d = {}
    f = LIB / "batch-c-log.jsonl"
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except Exception:                                  # noqa: BLE001
                continue
            if r.get("file"):
                d[r["file"]] = {"cast": r.get("char", ""), "scene": r.get("scene", ""),
                                "at": r.get("at", "")}
    f2 = LIB / "gen-worker.log.jsonl"
    if f2.exists():
        for line in f2.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except Exception:                                  # noqa: BLE001
                continue
            if r.get("file"):
                d.setdefault(r["file"], {"cast": r.get("cast", ""), "scene": r.get("scene", ""),
                                         "at": r.get("at", "")})
    return d


def used_by():
    """扫每部片子的 page-spec.json（页表）→ {文件名: [(片, 页), …]}。"""
    out = {}
    for spec in (ROOT / "projects").glob("*/page-spec.json"):
        proj = spec.parent.name
        try:
            pages = json.loads(spec.read_text(encoding="utf-8"))
        except Exception:                                      # noqa: BLE001
            continue
        for p in pages:
            a = p.get("asset") or ""
            if a:
                out.setdefault(a, []).append(f'{proj}:{p.get("id")}')
    return out


def approvals():
    """各片的 docs/审批.json → {library/文件名: 判定}。"""
    out = {}
    for f in (ROOT / "projects").glob("*/docs/审批.json"):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:                                      # noqa: BLE001
            continue
        for k, v in d.items():
            if k.startswith("library/"):
                out[k[len("library/"):]] = v.get("verdict")
    return out


def main():
    log, used, appr = gen_log(), used_by(), approvals()
    # 没进生成日志的三张（另一台机器做的）：名字对不上，按图的内容标角色
    CAST_FIX = {"p05-kneel.png": "小树", "p15-night-door.png": "小树", "p18-two-doors.png": "小树"}
    rows = []
    for f in sorted(LIB.glob("*.png")):
        if "sheet" in f.name:                 # 拼版对照图不是素材，不进库
            continue
        m = metrics(f)
        # 谁：生成日志优先；其次命名（male-/female- 前缀）；再不行查手工表
        cast = (log.get(f.name, {}).get("cast") or CAST_FIX.get(f.name)
                or ("小树" if f.name.startswith("male-") else
                    "小芽" if f.name.startswith("female-") else ""))
        rows.append({
            "file": f.name, "cast": cast,
            "scene": log.get(f.name, {}).get("scene", ""),
            "kind": "专用" if f.name.startswith("p") else "通用",
            **m,
            "used_by": used.get(f.name, []),
            "status": {"ok": "已通过", "no": "打回"}.get(appr.get(f.name, ""), "等审批"),
            "at": log.get(f.name, {}).get("at", ""),
        })
    if "--check" not in sys.argv:
        OUT.write_text(json.dumps({"at": __import__("time").strftime("%Y-%m-%d %H:%M:%S"),
                                   "count": len(rows), "images": rows},
                                  ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"素材库：{len(rows)} 张")
    for r in rows:
        flag = []
        if r["band_std"] > 12:
            flag.append("留白带不净")
        if r["sprout_px"] < SPROUT_MIN:
            flag.append("嫩芽少，看一眼头顶")
        used = ("→ " + " ".join(r["used_by"])) if r["used_by"] else ""
        print(f'  {r["file"]:<26} {r["cast"] or "-":<4} {r["status"]:<4} '
              f'{r["w"]}x{r["h"]} 芽{r["sprout_px"]:>3} 带{r["band_std"]:>2} '
              f'{"[!] " + "、".join(flag) if flag else ""} {used}')
    print(f"\n写好了：{OUT.relative_to(ROOT)}" if "--check" not in sys.argv else "（--check，没写）")


if __name__ == "__main__":
    main()
