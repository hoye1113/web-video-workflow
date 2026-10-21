"""把旧片分镜的口播稿洗成"短句 cue"，产出 emotion-full 的源数据与 script.js。

为什么要洗：
  ① 旧稿是**视频转写**，带着大量口水词（啊 / 呢 / 对 / 嗯 / 对吧）—— 口播听着糊；
  ② cue 是 TTS 的**分段单位**，太长（25 字以上）断句难听，太碎（5 字以下）又一顿一顿；
  ③ 字幕一行 8–12 字，**cue 本身就短**就不需要"硬切"，也就不会把词切开
     （`script.mjs` 的 12 字硬切是兜底，源头短才是根治）。

产出：
  projects/emotion-full/script-source.json   ← 源数据（可手改；改完重跑本脚本）
  projects/emotion-full/script.js            ← 引擎要的
用法：
  python tools/make_script_js.py            # 生成 + 打印校对表
  python tools/make_script_js.py --check    # 只打印校对表
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "projects" / "marriage_full" / "project.json"
PROJ = next((a for a in sys.argv[1:] if not a.startswith("-")), "emotion-full")
OUTDIR = ROOT / "projects" / PROJ
SRCJSON = OUTDIR / "script-source.json"
SCRIPTJS = OUTDIR / "script.js"

# 口水词：单独成词（或紧跟标点）时才删，避免把"对话"里的"对"删掉意思
FILLERS = ["啊", "呀", "呢", "吧", "嗯", "哦", "嘛", "对吧", "对的", "就是", "其实", "然后呢"]

CUE_MAX = 18          # 一条 cue 的字数上限（TTS 断句舒服、字幕好切）
CUE_MIN = 6           # 太短的相邻 cue 会合起来（避免一顿一顿）
ENDERS = "。！？"

# 段落内的章节（骨架）—— 旧片的 role 就是骨架名，这里统一成短名
SECTION = {
    "钩子": "钩子",
    "自述入口": "自述入口",
    "案例一·周先生": "案例一",
    "案例二·刘先生": "案例二",
    "案例三·李先生": "案例三",
    "反直觉结论": "反直觉结论",
    "真相拆解": "真相拆解",
    "行动与落点": "行动与落点",
}


def clean(t: str) -> str:
    """去掉转写的口水，但保住句子的意思。"""
    t = re.sub(r"\s+", "", t)
    for f in ["然后呢", "对吧", "对的", "就是", "其实"]:
        t = t.replace(f, "")
    t = re.sub(r"^[嗯呃哦]+", "", t)                      # 句首的语气词
    t = re.sub(r"^那么(?=[第是他她我你这也])", "", t)      # "那么第一个" → "第一个"
    t = t.replace("后来呢", "后来")
    # 句末/句中的语气词（它们在转写里几乎都是口水）
    t = re.sub(r"[啊呀呢吧嗯哦嘛]+(?=[，。！？、；]|$)", "", t)
    t = re.sub(r"[，、]{2,}", "，", t)
    t = re.sub(r"^[，。、；：]+", "", t)
    return t.strip()


def tidy(c: str) -> str:
    """切完之后再收拾一遍：句首的标点一律去掉（切点处会留下逗号）。"""
    c = re.sub(r"^[，。、；：！？]+", "", c)
    c = re.sub(r"[，、]{2,}", "，", c)
    return c.strip()


def hard_wrap(c: str, max_len: int = CUE_MAX):
    """整句没有标点可切时，硬切 —— 但**优先切在"的/了/是"之后**，尽量少切开词。"""
    if len(c) <= max_len:
        return [c]
    out, rest = [], c
    while len(rest) > max_len:
        cut = max_len
        for i in range(max_len, max(CUE_MIN, max_len - 6), -1):
            if rest[i - 1] in "的了是和与跟对给把被在就都也还只才":
                cut = i
                break
        out.append(rest[:cut])
        rest = rest[cut:]
    if rest:
        out.append(rest)
    return out


def split_cues(text: str):
    """先按句末切，再把长句按逗号切，短的合起来。"""
    sents, buf = [], ""
    for ch in text:
        buf += ch
        if ch in ENDERS:
            sents.append(buf)
            buf = ""
    if buf:
        sents.append(buf)

    cues = []
    for s in sents:
        s = s.strip()
        if not s:
            continue
        if len(s) <= CUE_MAX:
            cues.append(s)
            continue
        # 长句：按逗号/顿号切，再合并到 CUE_MAX 以内
        parts = re.split(r"(?<=[，、；：])", s)
        cur = ""
        for p in parts:
            if not p:
                continue
            if cur and len(cur) + len(p) > CUE_MAX:
                cues.append(cur)
                cur = p
            else:
                cur += p
        if cur:
            cues.append(cur)
    # 太短的相邻两块合起来（但别跨过句末）
    merged = []
    for c in cues:
        c = tidy(c)
        if not c:
            continue
        if merged and len(c) < CUE_MIN and not merged[-1].endswith(tuple(ENDERS)) \
                and len(merged[-1]) + len(c) <= CUE_MAX:
            merged[-1] += c
        else:
            merged.append(c)
    # 还是太长的硬切（整句没标点可切的情况）
    out = []
    for c in merged:
        out += hard_wrap(c)
    return [x for x in out if x.strip()]


def build():
    m = json.loads(SRC.read_text(encoding="utf-8"))
    pages = []
    for i, shot in enumerate(m["shots"], 1):
        narration = clean(shot.get("narration") or "")
        if not narration:
            continue
        pages.append({
            "id": "p%02d" % i,
            "section": SECTION.get(shot.get("role") or "", shot.get("role") or ""),
            "title": (shot.get("title") or "").strip(),
            "cues": split_cues(narration),
        })
    return m.get("title") or "成片", pages


def write(pages, title):
    OUTDIR.mkdir(parents=True, exist_ok=True)
    SRCJSON.write_text(json.dumps({"title": title, "gap": 0.8, "pages": pages},
                                  ensure_ascii=False, indent=1), encoding="utf-8")
    lines = [
        "/* emotion-full · 26 页口播稿（由 tools/make_script_js.py 从 script-source.json 生成）。",
        " * 改文案：改 script-source.json 再重跑，别手改这个文件。 */",
        "(function (root) {",
        "  const META = {",
        "    style: 'warm-emotion',",
        f"    title: {json.dumps(title, ensure_ascii=False)},",
        "    name: " + json.dumps(PROJ) + ",",
        "    gap: 0.8,",
        "    voice: { speaker: 'zh-CN-XiaoxiaoNeural', provider: 'edge' },",
        "    extras: ['engine/styles/warm-emotion/kit.js'],",
        "  };",
        "  const PAGES = [",
    ]
    for p in pages:
        lines.append("    { id: %s, section: %s, title: %s, cues: [" %
                     (json.dumps(p["id"]), json.dumps(p["section"], ensure_ascii=False),
                      json.dumps(p["title"], ensure_ascii=False)))
        for c in p["cues"]:
            lines.append("      %s," % json.dumps(c, ensure_ascii=False))
        lines.append("    ] },")
    lines += ["  ];", "  root.SCRIPT = { META, PAGES };",
              "})(typeof window !== 'undefined' ? window : globalThis);", ""]
    SCRIPTJS.write_text("\n".join(lines), encoding="utf-8")


def report(pages):
    tot = 0
    print(f"=== 校对表（{len(pages)} 页）===")
    for p in pages:
        n = sum(len(c) for c in p["cues"])
        tot += n
        print(f'\n【{p["id"]}】{p["section"]} · {p["title"][:26]}　{n} 字 / {len(p["cues"])} 句')
        for c in p["cues"]:
            flag = "  ⚠长" if len(c) > CUE_MAX else ("  ⚠短" if len(c) < 4 else "")
            print(f'   {len(c):>3} {c}{flag}')
    print(f"\n合计 {tot} 字，按 4.3 字/秒约 {tot / 4.3 / 60:.1f} 分钟")


if __name__ == "__main__":
    if "--check" in sys.argv:
        d = json.loads(SRCJSON.read_text(encoding="utf-8"))
        report(d["pages"])
    elif "--from-source" in sys.argv or (SRCJSON.exists() and "--rebuild" not in sys.argv):
        # 源数据已经手改过 → 直接用它生成 script.js（**不要再从旧项目重洗一遍**）
        d = json.loads(SRCJSON.read_text(encoding="utf-8"))
        write(d["pages"], d.get("title") or "成片")
        print(f"从 {SRCJSON.name} 生成：{SCRIPTJS.relative_to(ROOT)}")
        report(d["pages"])
    else:
        title, pages = build()
        write(pages, title)
        print(f"写好：{SRCJSON.relative_to(ROOT)}")
        print(f"写好：{SCRIPTJS.relative_to(ROOT)}")
        report(pages)
