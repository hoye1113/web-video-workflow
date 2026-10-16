"""从页列表生成字幕（ASS / SRT），拼接时烧进画面。

**为什么现在才做**：成片之前既没字幕也没声音，而每一页画面上又有自己的**屏上字**，
底部再压一层字幕就是两层字叠在一起。

**上游早就留了这个概念**（`clip.js`）：
`const safe = {...}` —— "让开的边（px）：管线烧录字幕、平台角标要用的地方"，
还专门打了一行警告："语法还没接 safe，spec.safe 被忽略：**字幕带可能压在字上**"。
我们从没接上。教训：**上游有的概念，先翻一遍再自己造**。

## 两条规矩

1. **字幕带 = 画面下方 18%**（1920×1080 上就是最下面 194px）。
   字幕居中压在带内，`MarginV` 留够，不贴边。
2. **屏上字、生图里的主体，都不许进这一条带**。屏上字进带 = 和字幕糊在一起；
   主体进带 = 被字幕压住。生图的提示词里也要求"最下面一条留空"。

## 时间轴怎么来的

页的 `dur` 本来就是按真实口播切出来的（26 页 / 349 秒），所以**累加 dur 就是音频时间轴**。
页内按每小句的字数分配时间 —— 说话快的地方，字也出得快，和旁白同步。
"""
import re

SUB_BAND = 0.18          # 下方留出这么多给字幕（相对画面高度）→ 1080 上是 194px
MAX_CUE = 18             # 一条字幕最多这么多字（再长就切）
MIN_CUE = 1.2            # 一条字幕最短显示时间（秒），太短来不及看


def safe_bottom(h=1080, margin=30):
    """屏上字允许画到的最低 y。

    字幕带是画面最下面 18%（1080 上是 194px，从 y=886 起）。
    字有高度：`textBaseline='middle'` 时 52px 的字上下各占约 26px，
    所以 y=860 的文字底边正好压到 886 —— 再往上留 30px，**y 必须 <= 856**。
    （提示词里让模型写到 820 以内，留足余量；这里是硬线，用来做检查。）
    """
    return int(h - h * SUB_BAND - margin)


SAFE_LEFT, SAFE_RIGHT, SAFE_TOP = 120, 1800, 110


def _split(text, n=MAX_CUE):
    """把一段旁白切成字幕条：优先在标点处断，其次凑够字数断。"""
    t = (text or "").strip()
    if not t:
        return []
    # 先按标点切成句子
    parts = [x for x in re.split(r"(?<=[。！？；，、：])", t) if x.strip()]
    out, buf = [], ""
    for p in parts:
        if len(buf) + len(p) <= n:
            buf += p
            continue
        if buf:
            out.append(buf)
        # 单句还是太长：硬切
        while len(p) > n:
            cut = p.rfind("，", 0, n)
            cut = cut + 1 if cut > n * 0.5 else n
            out.append(p[:cut])
            p = p[cut:]
        buf = p
    if buf:
        out.append(buf)
    return [x.strip() for x in out if x.strip()]


def cues(shots, base=0.0):
    """页列表 → [(开始, 结束, 文字)]。累加 dur 当时间轴，页内按字数分。"""
    out = []
    t = base
    for s in shots:
        dur = float(s.get("dur") or 12)
        text = (s.get("narration") or "").strip()
        if text:
            pieces = _split(text)
            total = sum(len(p) for p in pieces) or 1
            cur = t
            for i, p in enumerate(pieces):
                seg = dur * len(p) / total
                # 最后一条吃满页尾，避免累计误差把字幕拖出页外
                end = t + dur if i == len(pieces) - 1 else cur + seg
                if end - cur < MIN_CUE:
                    end = cur + MIN_CUE
                out.append((cur, min(end, t + dur + 0.3), p))
                cur = end
        t += dur
    return _merge(out)


def _merge(cs, gap=0.12):
    """把挨得太近的两条并起来（不然会闪），但不超过 MAX_CUE*1.6。"""
    out = []
    for c in cs:
        if out and c[0] - out[-1][1] < gap and len(out[-1][2]) + len(c[2]) <= MAX_CUE * 1.6:
            out[-1] = (out[-1][0], c[1], out[-1][2] + c[2])
        else:
            out.append(list(c) if isinstance(c, tuple) else c)
    return [tuple(x) for x in out]


def _t(sec, ass=False):
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int(sec % 3600 // 60)
    s = sec % 60
    if ass:
        return f"{h}:{m:02d}:{s:05.2f}"
    ms = int(round((s - int(s)) * 1000))
    return f"{h:02d}:{m:02d}:{int(s):02d},{ms:03d}"


ASS_HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: 字幕,{font},{size},&H00FFFFFF,&H00FFFFFF,&H00202020,&H64000000,-1,0,0,0,100,100,1,0,1,3,1,2,90,90,{margin},{enc}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def write_ass(cs, path, w=1920, h=1080, font="Microsoft YaHei", size=None, margin=None):
    """写 ASS。libass 认这个格式，能指定字体、描边，比 SRT 可控。"""
    size = int(size or round(h * 0.052))               # 1080 上约 56px
    # 字幕带里居中：离底边留带高的 1/3，字不会贴着画面下沿
    margin = int(margin if margin is not None else h * SUB_BAND * 0.34)
    head = ASS_HEAD.format(w=w, h=h, font=font, size=size, margin=margin, enc=134)
    body = "".join(
        f"Dialogue: 0,{_t(a, True)},{_t(b, True)},字幕,,0,0,0,,{text}\n"
        for a, b, text in cs)
    with open(path, "w", encoding="utf-8-sig") as f:   # BOM：libass 在 Windows 上认 UTF-8 BOM
        f.write(head + body)
    return path


def write_srt(cs, path):
    with open(path, "w", encoding="utf-8") as f:
        for i, (a, b, text) in enumerate(cs, 1):
            f.write(f"{i}\n{_t(a)} --> {_t(b)}\n{text}\n\n")
    return path


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
    import store
    name = sys.argv[1] if len(sys.argv) > 1 else "marriage_full"
    m = store.load(name) or {}
    shots = m["shots"]
    cs = cues(shots)
    w, h = int(m.get("width") or 1920), int(m.get("height") or 1080)
    d = store.pdir(name) / "out"
    d.mkdir(parents=True, exist_ok=True)
    write_ass(cs, d / "字幕.ass", w, h)
    write_srt(cs, d / "字幕.srt")
    tot = sum(float(s.get("dur") or 12) for s in shots)
    print(f"{len(cs)} 条字幕，覆盖 {tot:.0f} 秒（{tot/60:.1f} 分钟）")
    print(f"写好了：{d / '字幕.ass'}　和　{d / '字幕.srt'}")
    for a, b, t in cs[:8]:
        print(f"  {_t(a)} → {_t(b)}  {t}")
