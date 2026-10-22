"""审 cue 的切行：有没有"12 字硬切"（切点没落在标点上就会切开词）。

规则和 `packages/engine/tools/script.mjs` 的 splitCue 一致：
标点处必切、攒到 SUB_MAX（默认 12）也切。

用法：python tools/check_cues.py [--max 12]
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJ = next((a for a in sys.argv[1:] if not a.startswith("-")), "emotion-full")
SRC = ROOT / "projects" / PROJ / "script-source.json"
PUNCT = re.compile(r"[，。！？；：、,.!?;:—…]")

MAX = 12


def split(cue):
    out, frm = [], 0
    for i in range(1, len(cue) + 1):
        if i == len(cue) or PUNCT.match(cue[i - 1]) or i - frm >= MAX:
            out.append((frm, cue[frm:i]))
            frm = i
    return out


def main():
    mx = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else MAX
    d = json.loads(SRC.read_text(encoding="utf-8"))
    hard, long_ok = [], 0
    total = 0
    for p in d["pages"]:
        for c in p["cues"]:
            total += 1
            parts = split(c)
            bad = [t for _, t in parts if len(t) >= mx and not PUNCT.search(t[-1:])]
            if len(parts) == 1:
                continue                     # 不用切
            if bad:
                hard.append((p["id"], c, [t for _, t in parts]))
            else:
                long_ok += 1
    print(f"{total} 条 cue：要切行的 {long_ok + len(hard)} 条，其中**硬切**（会切开词）{len(hard)} 条\n")
    for pid, c, parts in hard:
        print(f'  {pid}  {c}   →   {" ｜ ".join(parts)}')
    print(f"\n（把硬切处加个逗号就行：cue 里第 12 个字前要有标点）")

    # ── 节奏检查：用户要求 **6 秒一屏**（1.4 倍速 ≈ 5.5 字/秒 → 一页 30–36 字）──
    long_pages, short_pages, chars_all = [], [], 0
    for p in d["pages"]:
        n = sum(len(c) for c in p["cues"])
        chars_all += n
        if n > 45:
            long_pages.append((p["id"], n))
        elif n < 20:
            short_pages.append((p["id"], n))
    pages = len(d["pages"])
    print(f"\n节奏：{pages} 页 / 共 {chars_all} 字 / 估时 {chars_all / 5.5 / 60:.1f} 分钟"
          f"（6 秒一屏时，一页 30–36 字）")
    if long_pages:
        print("  偏长（>45 字，≈8 秒以上）：" + "、".join(f"{i}({n})" for i, n in long_pages))
    if short_pages:
        print("  偏短（<20 字，≈3.6 秒以下）：" + "、".join(f"{i}({n})" for i, n in short_pages))
    if not long_pages and not short_pages:
        print("  ✓ 每页节奏都在 6 秒附近")


if __name__ == "__main__":
    main()
