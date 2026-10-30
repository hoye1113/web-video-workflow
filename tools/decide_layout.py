"""套版选择：P1 = 原版小图留白；P2 = 70% 处境页铺满 + 30% 情绪特写。

用法：
    python tools/decide_layout.py <片名>                 # 读 brief.json 的 layout_mode，默认 p2
    python tools/decide_layout.py <片名> --mode p1       # 全部 card
    python tools/decide_layout.py <片名> --mode p2       # 自动 70/30
    python tools/decide_layout.py <片名> --check         # 只打印，不写文件

判定不是按页数硬切：先看每页是“交代处境”还是“情绪落点”，
再用 7:3 配额校准。显式写了 layout_manual=true 的页不被覆盖。
"""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import pipeline  # noqa: E402

MODES = {
    "p1": {"label": "P1 · 原版留白", "desc": "所有页小图 + 四周留白，不铺满"},
    "p2": {"label": "P2 · 70/30 混合", "desc": "70% 处境页铺满，30% 情绪特写保留干净背景"},
}

# 处境页（铺满）信号：环境、动作、多个物件、转场
FULL_WORDS = [
    "房间", "客厅", "厨房", "卧室", "走廊", "门口", "玄关", "窗", "窗边", "窗外",
    "桌", "桌上", "桌面", "沙发", "床", "柜", "书架", "绿植", "植物", "窗帘",
    "街", "车", "雨", "夜", "光", "站", "坐", "走", "推", "拿", "放", "背对",
    "铁盒", "碗", "饭", "手机", "照片", "纸", "门", "墙", "地板", "背景",
]
# 情绪特写（干净背景）信号：脸、手、单一物件、内心动作
CLOSE_WORDS = [
    "才知道", "原来", "终于", "沉默", "眼泪", "哭", "笑", "心疼", "后悔",
    "害怕", "孤独", "累", "释然", "舍不得", "等不了", "闭眼", "低头",
    "看着", "想起", "手", "手指", "脸", "眼睛", "嘴角", "抱", "吻",
    "只剩", "一个人", "最后", "这一次", "那一刻",
]
SECTION_CLOSE = {"落点": 3, "结论": 3, "结尾": 3, "转折": 2, "反直觉结论": 2}
SECTION_FULL = {"钩子": 2, "案例": 1, "正文": 1, "习惯": 1}


def _text(page):
    parts = [page.get("title", ""), page.get("section", "")]
    parts += [str(c) for c in page.get("cues", [])]
    return "".join(parts)


def score_page(page, index, total, spec_page=None):
    """返回 (full_score, close_score, why)。分数只用于同一条片内部的相对排序。"""
    text = _text(page)
    full = sum(1 for w in FULL_WORDS if w in text)
    close = sum(2 for w in CLOSE_WORDS if w in text)
    why = []
    sec = page.get("section", "")
    if sec in SECTION_CLOSE:
        close += SECTION_CLOSE[sec]
        why.append(f"章节={sec}")
    if sec in SECTION_FULL:
        full += SECTION_FULL[sec]
        why.append(f"章节={sec}")
    if index == 0:
        full += 2
        why.append("首屏")
    if index == total - 1:
        close += 2
        why.append("落点")
    sp = spec_page or {}
    scene = (sp.get("title") or "") + (sp.get("asset") or "")
    if any(w in scene for w in ("近景", "特写")):
        close += 3
        why.append("近景")
    if any(w in text for w in ("房间", "背景", "周围", "站", "坐", "走")):
        full += 2
        why.append("处境")
    return full, close, "、".join(why) or "无信号"


def choose(pages, spec, mode="p2"):
    """返回 {page_id: layout}，layout = card | full | close。"""
    if mode == "p1":
        return {p.get("id"): "card" for p in pages}
    n = len(pages)
    if n == 0:
        return {}
    by_id = {p.get("id"): p for p in (spec or [])}
    rows = []
    for i, p in enumerate(pages):
        pid = p.get("id")
        sp = by_id.get(pid) or {}
        full, close, why = score_page(p, i, n, sp)
        rows.append({"id": pid, "full": full, "close": close, "delta": close - full, "why": why,
                     "manual": bool(sp.get("layout_manual")),
                     "layout": sp.get("layout") if sp.get("layout_manual") else None})
    # 手工指定的页先锁定；剩下的按 7:3 配额选
    locked = {r["id"]: r["layout"] for r in rows if r["manual"] and r["layout"] in ("full", "close", "card")}
    free = [r for r in rows if r["id"] not in locked]
    target = max(1, round(n * 0.3)) if n >= 2 else 0
    target = min(target, n - 1) if n >= 2 else 0
    already_close = sum(1 for v in locked.values() if v == "close")
    need = max(0, target - already_close)
    # 先按“情绪分”排；同分时后面的页优先（落点更可能是特写），避免首屏被选成特写
    ranked = sorted(free, key=lambda r: (r["delta"], r["close"], 1 if r["id"] == rows[-1]["id"] else 0), reverse=True)
    close_ids = {r["id"] for r in ranked[:need]}
    out = {}
    for r in rows:
        if r["id"] in locked:
            out[r["id"]] = locked[r["id"]]
        elif r["id"] in close_ids:
            out[r["id"]] = "close"
        else:
            out[r["id"]] = "full"
    return out


def explain(pages, spec, mode="p2"):
    by_id = {p.get("id"): p for p in (spec or [])}
    rows = []
    n = len(pages)
    for i, p in enumerate(pages):
        pid = p.get("id")
        full, close, why = score_page(p, i, n, by_id.get(pid) or {})
        rows.append((pid, p.get("title", ""), full, close, close - full, why))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("project")
    ap.add_argument("--mode", choices=sorted(MODES), default=None)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    proj = a.project
    d = pipeline.proj_dir(proj)
    brief = pipeline.read_json(d / "brief.json", {}) or {}
    mode = a.mode or brief.get("layout_mode") or "p2"
    if mode not in MODES:
        mode = "p2"
    src = pipeline.read_json(d / "script-source.json", {}) or {}
    pages = src.get("pages", [])
    spec = pipeline.read_json(d / "page-spec.json", []) or []
    rows = explain(pages, spec, mode)
    chosen = choose(pages, spec, mode)
    print(f"{proj} · {MODES[mode]['label']} · {len(pages)} 页")
    print(f"{'页':<5}{'布局':<7}{'full':>5}{'close':>6}{'差':>5}  为什么")
    for pid, title, full, close, delta, why in rows:
        print(f"{pid:<5}{chosen.get(pid, '-'):<7}{full:>5}{close:>6}{delta:>5}  {why}  {title[:24]}")
    n = len(pages)
    c = sum(1 for v in chosen.values() if v == "close")
    f = sum(1 for v in chosen.values() if v == "full")
    card = sum(1 for v in chosen.values() if v == "card")
    print(f"\n合计：full {f} / close {c} / card {card}" +
          (f"（close {c/n:.0%}，目标约 30%）" if n else ""))
    if a.check:
        return
    # 写回 page-spec
    for p in spec:
        pid = p.get("id")
        if pid in chosen:
            p["layout"] = chosen[pid]
    (d / "page-spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    # 只改还没开始画的任务，不碰 review / 已画好的
    q = pipeline.queue(proj)
    touched = 0
    for t in q["tasks"]:
        if t.get("status") in ("queued", "retry") and t.get("page") in chosen:
            t["layout"] = chosen[t["page"]]
            touched += 1
    if touched:
        pipeline.queue_save(proj, q)
    # 把模式写进 brief，下次不用再传
    brief["layout_mode"] = mode
    (d / "brief.json").write_text(json.dumps(brief, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"已写回 page-spec.json（layout），队列里更新了 {touched} 个待做任务")


if __name__ == "__main__":
    main()
