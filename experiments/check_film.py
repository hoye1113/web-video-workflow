"""片子交付前的自查（只读，不改东西）。

用法：python experiments/check_film.py <片名>
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

LIB = ROOT / "projects" / "scene-library"


def main():
    proj = sys.argv[1] if len(sys.argv) > 1 else "film-1020-1522"
    d = ROOT / "projects" / proj
    ok = True

    # ① 台词
    src = json.loads((d / "script-source.json").read_text(encoding="utf-8"))
    cues = [c for p in src["pages"] for c in p["cues"]]
    chars = sum(len(c) for c in cues)
    print(f"台词：{len(src['pages'])} 页 / {len(cues)} cue / {chars} 字 "
          f"(≈{chars / 194:.2f} 分钟) / 最长 cue {max(len(c) for c in cues)} 字")
    if chars < 1100 or chars > 1230:
        print("   [!] 字数偏离 6 分钟的目标区间（1100–1230）")
        ok = False
    hard = 0
    for p in src["pages"]:
        for c in p["cues"]:
            for i in range(1, len(c) + 1):
                if i == len(c) or c[i - 1] in "，。！？；：、" or i - 0 >= 12:
                    break
            if len(c) > 12 and not any(ch in c[:12] for ch in "，。！？；：、"):
                hard += 1
    print(f"   cue 超 12 字且第 12 字前无标点：{hard} 条")
    ok = ok and hard == 0

    # ② 页表
    spec = json.loads((d / "page-spec.json").read_text(encoding="utf-8"))
    print(f"页表：{len(spec)} 页")
    miss = [p["id"] for p in spec if not (LIB / (p.get("asset") or "")).exists()]
    empty = [p["id"] for p in spec if not p.get("asset")]
    print(f"   asset 留空：{empty or '无'}   图不存在：{miss or '无'}")
    ok = ok and not miss and not empty
    if len(spec) != len(src["pages"]):
        print(f"   [!] 页表 {len(spec)} 页 ≠ 台词 {len(src['pages'])} 页")
        ok = False
    ids_spec = [p["id"] for p in spec]
    ids_src = [p["id"] for p in src["pages"]]
    if ids_spec != ids_src:
        print(f"   [!] 页号对不上：{ids_spec} vs {ids_src}")
        ok = False
    bad_text = [p["id"] for p in spec for t in p.get("texts", []) if len(t[0]) > 8]
    print(f"   屏上字超 8 字：{bad_text or '无'}")
    ok = ok and not bad_text
    low = [p["id"] for p in spec for t in p.get("texts", []) if t[2] > 380]
    print(f"   屏上字掉进下方字幕带（y>380）：{low or '无'}")

    # ③ 页代码
    pages = sorted((d / "pages").glob("p*.js"))
    print(f"页代码：{len(pages)} 个")
    if len(pages) != len(spec):
        print("   [!] 页代码数量对不上")
        ok = False

    # ④ 分镜表（用**面板自己的解析逻辑**数行，别自己数表格 —— 文档里还有好几张表）
    md = d / "docs" / "页-处境映射.md"
    if md.exists():
        sys.path.insert(0, str(ROOT / "apps" / "intern"))
        import server as intern                               # noqa: PLC0415
        rows = intern.map_rows(proj)
        print(f"分镜表：面板读到 {len(rows)} 行（页 | 论点 | 处境 | 主角）")
        if len(rows) != len(spec):
            print("   [!] 分镜表行数 ≠ 页数")
            ok = False
        if len({r[0] for r in rows}) != len(rows):
            print("   [!] 分镜表有重复页号")
            ok = False
    else:
        print("分镜表：缺 docs/页-处境映射.md")
        ok = False

    # ⑤ 队列
    q = json.loads((d / "gen-queue.json").read_text(encoding="utf-8"))
    st = {}
    for t in q["tasks"]:
        st[t["status"]] = st.get(t["status"], 0) + 1
    print(f"队列：{st}")

    # ⑥ 事件
    ev = (d / "events.jsonl").read_text(encoding="utf-8").splitlines()
    print(f"事件：{len(ev)} 条")
    print("\n=> " + ("全部通过" if ok else "有问题，看上面 [!] 的行"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
