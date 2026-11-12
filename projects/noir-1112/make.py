# -*- coding: utf-8 -*-
"""Build the noir-1112 project from the user's own narration.

Input:  experiments/transcribe/1112.json (faster-whisper segments)
Output: script-source.json, script.js, cue-audio-map.json, pages/pNN.js
The audio cutter (tools/voice_from_map.py) turns cue-audio-map.json into voice.js.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
PROJ = pathlib.Path(__file__).resolve().parent
TR = json.loads((ROOT / "experiments/transcribe/1112.json").read_text(encoding="utf-8"))

# obvious ASR corrections; the audio is unchanged, only the subtitle text is cleaned
FIX = [
    ("无数个王坏处踩车的理由", "无数个草木皆兵的理由"),
    ("逼得你时刻进崩", "逼得你时刻紧绷"),
    ("想象里有多丰富", "想象力有多丰富"),
    ("伤害就多深", "伤害就有多深"),
    ("谦恶的人同样是你自己", "煎熬的人同样是你自己"),
    ("渴望达到安心的信号", "渴望得到一个安心的信号"),
    ("想要回到从简安稳的生活", "想要回到从前安稳的生活"),
    ("一次次所要道歉", "一次次索要道歉"),
    ("所要承诺", "索要承诺"),
    ("首先要拿出始足的诚意", "首先要拿出十足的诚意"),
    ("没有任何借口可以该多", "没有任何借口可以推脱"),
    ("可以试图成熟当时的处境", "可以试图陈述当时的处境"),
    ("夺闪逃避", "躲闪逃避"),
    ("弯弯整整认错", "坦坦荡荡认错"),
    ("上一秒伤起瓶颈", "上一秒伤春悲秋"),
    ("修复其理", "修复信任"),
    ("收知情况主动报备", "有事主动报备"),
    ("用一张庄看得见的行动", "用看得见的行动"),
    ("或是约熟悉的好友小巨", "或是约熟悉的好友小聚"),
    ("是这理性看待当下的相处", "试着理性看待当下的相处"),
    ("请那往正向的方向思考", "多往正向的方向思考"),
    ("是人之长情", "是人之常情"),
    ("感心里", "在心理上"),
    ("绝对的信任和绝对的补信任", "绝对的信任和绝对的不信任"),
    ("保持试度警觉", "保持适度警觉"),
    ("白彰自己的心态", "摆正自己的心态"),
    ("做好心理愿", "做好心理准备"),
    ("这份惊醒才是对家庭", "这份警觉才是对家庭"),
    ("草木皆病的多疑", "草木皆兵的多疑"),
    ("习惯性补风捉影", "习惯性捕风捉影"),
    ("就认定就错重业", "就认定旧情复燃"),
    ("它会向外寻求未解", "他会向外寻求慰藉"),
    ("那你形式就要尽量谈当透明", "那你的行动就要尽量坦荡透明"),
    ("人天生对伴侣有情感独占于", "人天生对伴侣有情感独占欲"),
    ("在安全感之间世上", "在安全感这件事上"),
    ("家和万事心", "家和万事兴"),
    ("至上痛苦", "至深的痛苦"),
    ("会向九汉逢甘陵的草木", "会像久旱逢甘霖的草木"),
    ("完成褪变", "完成蜕变"),
    ("变得劳不可破", "变得牢不可破"),
    ("李安向来劝何不劝离", "李安向来劝和不劝离"),
    ("曾经你堵定她是好人", "曾经你笃定她是好人"),
    ("这本真心被她辜负", "这份真心被她辜负"),
    ("这不是你小题大作", "这不是你小题大做"),
    ("原本悉松平常的日常小事", "原本稀松平常的日常小事"),
    ("甚至互相慈伤", "甚至互相刺伤"),
    ("逼得你时刻进崩", "逼得你时刻紧绷"),
]


def clean(t):
    t = (t or "").strip()
    for a, b in FIX:
        t = t.replace(a, b)
    return re.sub(r"\s+", "", t)


segs = []
for s in TR["segments"]:
    t = clean(s["text"])
    if t:
        segs.append({"start": float(s["start"]), "end": float(s["end"]), "text": t})

(PROJ / "segments-clean.json").write_text(json.dumps(segs, ensure_ascii=False, indent=1), encoding="utf-8")

# ── page map: from / to are 0-based segment indices, inclusive ─────────────
P = [
    dict(t="chapter", ch=1, en="TRUST / COLLAPSE", title="信任崩塌", sub="夫妻接纳了犯错的伴侣，却始终放不下怀疑", ghost="信", a=0, b=2),
    dict(t="statement", ch=1, en="THE BEGINNING", title="笃定", sub="曾经你笃定她是好人，毫无保留交出真心", ghost="信", a=3, b=6),
    dict(t="split", ch=1, en="THE REFLEX", title="防备", sub="不是小题大做，是信任崩塌后的本能反应", ghost="防", viz="crack", a=7, b=12),
    dict(t="split", ch=1, en="CERTAINTY", title="失去确定性", sub="失去信任，本质是失去了对这段感情的确定性", ghost="定", viz="curveDown", a=13, b=15),
    dict(t="list", ch=1, en="RISK", title="暗藏风险", sub="稀松平常的小事，在你眼里都暗藏风险", ghost="险", key="风险", items=["一次负面细节", "被你敏锐捕捉", "在心底无限放大"], a=16, b=21),
    dict(t="statement", ch=1, en="THE MIND", title="脑补", sub="想象力有多丰富，脑补带来的内耗和伤害就有多深", ghost="念", a=22, b=25),
    dict(t="statement", ch=1, en="INTERPRETATION", title="解读", sub="困住关系的，早已不是事件本身，而是人的解读", ghost="解", a=26, b=28),
    dict(t="split", ch=1, en="THE WAVE", title="情绪", sub="一旦认定对方还会伤害你，情绪会瞬间席卷而来", ghost="情", viz="wave", a=29, b=32),
    dict(t="list", ch=1, en="NEGATIVE LOOP", title="负面行为", sub="负面情绪，一定会催生负面行为", ghost="伤", key="行为", items=["反复争吵", "刻意冷战", "互相刺伤"], a=33, b=36),
    dict(t="statement", ch=1, en="THE COST", title="煎熬", sub="长期处在警惕里，煎熬的人同样是你自己", ghost="熬", a=37, b=43),
    dict(t="chapter", ch=2, en="THE NEED", title="追问", sub="你不停追问、反复确认，只想要一个安心的信号", ghost="问", a=44, b=47),
    dict(t="list", ch=2, en="SAFETY", title="安全感", sub="你要的不是道歉，是找回丢失的安全感", ghost="安", key="安心", items=["确认还能走下去", "回到从前的生活", "找回丢失的安全感"], a=48, b=54),
    dict(t="statement", ch=2, en="REBUILD", title="一起重建", sub="这条路再难，也需要两个人一起努力", ghost="建", a=55, b=59),
    dict(t="chapter", ch=3, en="WHO REPAIRS", title="谁破坏，谁修复", sub="李安一直认同一个原则", ghost="修", a=60, b=62),
    dict(t="statement", ch=3, en="HER RESPONSIBILITY", title="她的责任", sub="是她亲手摧毁信任，就理应由她扛起修复的责任", ghost="责", a=63, b=65),
    dict(t="statement", ch=3, en="SINCERITY", title="诚意", sub="错了就是错了，没有任何借口可以推脱", ghost="诚", a=66, b=71),
    dict(t="steps", ch=3, en="THE FIRST STEP", title="第一步", sub="这是修复信任、重建亲密关系最关键的一步", ghost="改", items=["坦荡认错", "踏实改正", "重建信任"], a=72, b=77),
    dict(t="statement", ch=3, en="THE RELAPSE", title="反复", sub="你难免猜疑、情绪起伏；这都是受伤后的正常反应", ghost="复", a=78, b=84),
    dict(t="split", ch=3, en="PATIENCE", title="耐心", sub="她需要接住你的情绪，陪你慢慢平复", ghost="耐", viz="twoNodes", a=85, b=90),
    dict(t="list", ch=3, en="TRANSPARENCY", title="透明", sub="放下一部分自由和体面，接受合理监督", ghost="透", key="行动", items=["分享日常", "同步行踪", "有事报备"], a=91, b=99),
    dict(t="list", ch=3, en="TOGETHER", title="一起向外走", sub="一同感受生活，找回“我们是一体的”归属感", ghost="同", key="一起", items=["短途出行", "看一场电影", "约好友小聚"], a=100, b=111),
    dict(t="chapter", ch=4, en="THE INJURED SIDE", title="受伤的一方", sub="也不能一直困在受害者心态里", ghost="伤", a=112, b=115),
    dict(t="list", ch=4, en="THE SIGNALS", title="看见改变", sub="这些，都是她想要修复关系的信号", ghost="见", key="信号", items=["主动早归", "留意情绪", "敞开心扉"], a=116, b=122),
    dict(t="twoPaths", ch=4, en="TWO PATHS", title="正向", sub="理性看待当下，多往正向的方向思考", left="修复婚姻", right="摧毁关系", ghost="标", a=123, b=132),
    dict(t="statement", ch=4, en="COOPERATION", title="配合", sub="缺少你的配合，单凭她一个人，信任无法重建", ghost="合", a=133, b=138),
    dict(t="twoPaths", ch=4, en="TWO EXTREMES", title="两种极端", sub="都暗藏隐患", left="绝对信任", right="绝对不信任", ghost="衡", viz="scale", a=139, b=147),
    dict(t="split", ch=4, en="VIGILANCE", title="适度警觉", sub="清楚风险、摆正心态，才是对关系负责", ghost="警", viz="eye", a=148, b=155),
    dict(t="chapter", ch=5, en="VIGILANCE / PARANOIA", title="警觉与多疑", sub="理性的警觉，和草木皆兵的多疑，完全是两回事", ghost="疑", a=156, b=157),
    dict(t="list", ch=5, en="THE SHADOW", title="捕风捉影", sub="过度多疑，大多源于内心的自卑", ghost="影", key="多疑", items=["正常相处 → 关系越界", "吃顿饭 → 旧情复燃", "不够认可自己 → 难以信任"], a=158, b=168),
    dict(t="statement", ch=5, en="THE MIND AGAIN", title="想象", sub="不要困在主观想象里；无端猜忌只会把对方推远", ghost="想", a=169, b=177),
    dict(t="list", ch=5, en="REASSURANCE", title="安心信号", sub="如果伴侣敏感多疑，你的行动要尽量坦荡透明", ghost="安", key="安心", items=["多肯定，多赞美", "释放安心信号", "帮他建立底气"], a=178, b=187),
    dict(t="chapter", ch=6, en="TRUST IS AIR", title="信任是空气", sub="没有信任，就没有真正的安全感", ghost="空", a=188, b=191),
    dict(t="statement", ch=6, en="NO TRUST", title="没有信任", sub="和睦的亲密关系，也就无从谈起", ghost="信", a=192, b=196),
    dict(t="split", ch=6, en="AIR", title="空气", sub="拥有时被忽略，消失时让人窒息", ghost="气", viz="wave", a=197, b=203),
    dict(t="split", ch=6, en="FOUNDATION", title="地基", sub="没有信任的婚姻，如同没有地基的房子", ghost="基", viz="house", a=204, b=210),
    dict(t="chapter", ch=7, en="REBUILD", title="重塑", sub="危机，也是感情重塑的契机", ghost="塑", a=211, b=214),
    dict(t="statement", ch=7, en="STRONGER", title="更稳固", sub="度过难关之后的感情，往往会比从前更稳固", ghost="固", a=215, b=219),
    dict(t="split", ch=7, en="TRANSFORMATION", title="蜕变", sub="像久旱逢甘霖的草木，完成蜕变，牢不可破", ghost="生", viz="sprout", a=220, b=229),
    dict(t="closing", ch=7, en="STAY / TOGETHER", title="劝和不劝离", sub="无论遇上什么困惑，都可以来找李安聊聊", ghost="聊", a=230, b=236),
]

# sanity: every segment covered exactly once, in order
cursor = 0
for p in P:
    assert p["a"] == cursor, f"{p['title']} starts at {p['a']}, expected {cursor}"
    cursor = p["b"] + 1
assert cursor == len(segs), f"covered {cursor} of {len(segs)} segments"

# page ids, chapter page counter, cues
pages = []
ch_count = {}
for i, p in enumerate(P, 1):
    pid = f"p{i:02d}"
    raw = segs[p["a"]:p["b"] + 1]
    cues = []
    for s in raw:
        t = s["text"]
        if cues and len(t) <= 2:
            cues[-1]["text"] += t
            cues[-1]["end"] = s["end"]
        else:
            cues.append({"text": t, "start": s["start"], "end": s["end"]})
    if len(cues) > 1 and len(cues[0]["text"]) <= 2:
        cues[1]["text"] = cues[0]["text"] + cues[1]["text"]
        cues[1]["start"] = cues[0]["start"]
        cues.pop(0)
    ch = p["ch"]
    ch_count[ch] = ch_count.get(ch, 0) + 1
    pages.append({**p, "id": pid, "no": i, "pageInCh": ch_count[ch], "cues": cues})

# script-source.json
src = {
    "title": "裂痕之后",
    "gap": 0,
    "voice": {"speaker": "audio", "provider": "audio"},
    "pages": [
        {"id": p["id"], "section": f"第{p['ch']}章", "title": p["title"], "cues": [c["text"] for c in p["cues"]]}
        for p in pages
    ],
}
(PROJ / "script-source.json").write_text(json.dumps(src, ensure_ascii=False, indent=1), encoding="utf-8")

# cue map for the audio cutter
cmap = []
for p in pages:
    cmap.append({"page": p["id"], "cues": [{"index": i, "start": c["start"], "end": c["end"], "text": c["text"]} for i, c in enumerate(p["cues"])]})
(PROJ / "cue-audio-map.json").write_text(json.dumps(cmap, ensure_ascii=False, indent=1), encoding="utf-8")

# script.js
def js(s):
    return json.dumps(s, ensure_ascii=False)

lines = [
    f"/* noir-1112 · generated by make.py from the user's audio (do not hand-edit the page blocks) */",
    "(function (root) {",
    "  const META = {",
    "    style: 'noir-editorial',",
    f"    title: {js('裂痕之后')},",
    "    name: 'noir-1112',",
    "    gap: 0,",
    "    pageMotion: false,",
    "    voice: { speaker: 'audio', provider: 'audio' },",
    "    extras: ['engine/styles/noir-editorial/kit.js'],",
    "    // exact user-audio timeline: no lead, no gap, no tail padding",
    "    pace: { lead: 0, gap: 0, maxHold: 0, comma: 0, stop: 0, pageEnd: 0, tail: 0 },",
    "  };",
    "  const PAGES = [",
]
for p in pages:
    lines.append(f"    {{ id: {js(p['id'])}, section: {js('第'+str(p['ch'])+'章')}, title: {js(p['title'])}, cues: [")
    for c in p["cues"]:
        lines.append(f"      {js(c['text'])},")
    lines.append("    ] },")
lines += ["  ];", "  root.SCRIPT = { META, PAGES };", "})(typeof window !== 'undefined' ? window : globalThis);", ""]
(PROJ / "script.js").write_text("\n".join(lines), encoding="utf-8")

# storyboard for reference
(PROJ / "storyboard.json").write_text(json.dumps([
    {"id": p["id"], "chapter": p["ch"], "type": p["t"], "title": p["title"], "sub": p["sub"], "viz": p.get("viz"), "from": p["a"], "to": p["b"], "cues": len(p["cues"])}
    for p in pages
], ensure_ascii=False, indent=1), encoding="utf-8")

# ── page code ───────────────────────────────────────────────────────────────
def header(p):
    return f"""  const H = P.hud;
  H.noirHeader({p['ch']}, 7, {js(p['en'])}, {{ at: 0.04, right: 'NOIR / {p['ch']:02d}' }});
  H.noirLabel('{p['ch']:02d}.{p['pageInCh']:02d}', 1700, 140, {{ size: 11, color: 'faint', at: 0.7 }});"""

def base(p, size=86, color="orange", y=220):
    return f"""  P.noirGhost({js(p['ghost'])}, {{ x: 1270, y: 205, size: 300, opacity: 0.07 }});
  P.noirReveal({js(p['title'])}, {{ x: 148, y: {y}, size: {size}, color: '{color}', at: 0.26, dur: 0.65, stagger: 0.045 }});
  P.text({js(p['sub'])}, {{ x: 152, y: {y + 118}, size: 31, font: 'serif', color: 'soft', at: 0.8, mode: 'fade', dur: 0.5, w: 760, lh: 1.38 }});
  P.noirHairline(150, 760, {y + 174}, {{ color: 'faint', sw: 1, at: 0.95, dur: 0.7, opacity: 0.72 }});"""

def viz(p, at=1.0):
    v = p.get("viz")
    if v == "crack":
        return f"""  P.noirCrack(1180, 270, 380, 470, {{ color: 'red', at: {at} }});
  P.noirLabel('TRUST / BROKEN', 1160, 750, {{ size: 12, color: 'muted', at: {at + 0.6} }});"""
    if v == "curveDown":
        return f"""  P.noirCurve('M980 360 C1180 360 1380 560 1720 720', {{ color: 'blue', sw: 2.4, glow: 7, at: {at} }});
  P.noirHairline(980, 1720, 600, {{ color: 'faint', sw: 1, at: {at + 0.2}, dur: 0.7, opacity: 0.4 }});
  P.noirLabel('CERTAINTY / LOST', 1530, 760, {{ size: 12, color: 'muted', at: {at + 0.7} }});"""
    if v == "wave":
        return f"""  P.noirWave(1060, 400, 600, 150, {{ bars: 42, gap: 5, color: 'blue', at: {at} }});
  P.noirLabel('EMOTION / SIGNAL', 1060, 370, {{ size: 12, color: 'muted', at: {at + 0.1} }});"""
    if v == "eye":
        return f"""  P.noirEye(1300, 430, 170, {{ color: 'blue', at: {at} }});
  P.noirLabel('WATCH / NOT FEAR', 1160, 650, {{ size: 12, color: 'muted', at: {at + 0.5} }});"""
    if v == "twoNodes":
        return f"""  P.noirTwoNodes(1100, 520, 1600, 520, {{ color: 'blue', r: 10, at: {at} }});
  P.noirLabel('YOU', 1080, 470, {{ size: 12, color: 'muted', at: {at + 0.35} }});
  P.noirLabel('HER', 1580, 470, {{ size: 12, color: 'muted', at: {at + 0.45} }});"""
    if v == "house":
        return f"""  P.noirHouse(1160, 300, 420, {{ color: 'orange', at: {at} }});
  P.noirLabel('FOUNDATION / TRUST', 1160, 720, {{ size: 12, color: 'muted', at: {at + 0.8} }});"""
    if v == "sprout":
        return f"""  P.noirSprout(1320, 320, 390, {{ color: 'green', at: {at} }});
  P.noirLabel('AFTER / THE RAIN', 1210, 740, {{ size: 12, color: 'muted', at: {at + 0.6} }});"""
    if v == "scale":
        return f"""  P.noirScale(1300, 300, 430, {{ color: 'orange', at: {at} }});
  P.noirLabel({js(p['left'])}, 1020, 520, {{ size: 18, color: 'blue', at: {at + 0.5} }});
  P.noirLabel({js(p['right'])}, 1450, 520, {{ size: 18, color: 'red', at: {at + 0.6} }});"""
    return ""

def page_code(p):
    head = header(p)
    if p["t"] == "chapter":
        body = f"""  P.noirGhost('{p['ch']:02d}', {{ x: 1230, y: 170, size: 310, opacity: 0.08 }});
  P.noirReveal({js(p['title'])}, {{ x: 148, y: 250, size: 96, color: 'orange', at: 0.3, dur: 0.7, stagger: 0.055 }});
  P.text({js(p['sub'])}, {{ x: 152, y: 392, size: 34, font: 'serif', color: 'soft', at: 0.9, mode: 'fade', dur: 0.55, w: 780, lh: 1.4 }});
  P.noirHairline(150, 780, 452, {{ color: 'faint', sw: 1, at: 1.0, dur: 0.8, opacity: 0.72 }});
  P.noirLabel('CHAPTER {p['ch']:02d} / 07', 150, 820, {{ size: 12, color: 'muted', at: 0.8 }});
  P.box(1120, 170, 560, 500, {{ r: 0, fill: null, color: 'faint', sw: 1, rough: 0, single: true, at: 0.55, dur: 1.0, pen: false }});
  P.line(1120, 170, 1200, 170, {{ color: 'orange', sw: 1.2, at: 0.8, dur: 0.4, pen: false }});
  P.line(1120, 170, 1120, 250, {{ color: 'orange', sw: 1.2, at: 0.86, dur: 0.4, pen: false }});
  P.noirLabel('SPECIMEN / {p['ch']:02d}', 1120, 700, {{ size: 11, color: 'muted', at: 1.2 }});"""
    elif p["t"] == "statement":
        body = base(p, size=88, color="orange") + f"""
  P.box(1120, 220, 560, 460, {{ r: 0, fill: null, color: 'faint', sw: 1, rough: 0, single: true, at: 0.6, dur: 0.9, pen: false }});
  P.line(1120, 220, 1200, 220, {{ color: 'orange', sw: 1.2, at: 0.9, dur: 0.35, pen: false }});
  P.line(1120, 220, 1120, 300, {{ color: 'orange', sw: 1.2, at: 0.95, dur: 0.35, pen: false }});
  P.noirLabel('SPECIMEN / {p['ch']:02d}.{p['pageInCh']:02d}', 1120, 700, {{ size: 11, color: 'muted', at: 1.25 }});
  P.noirLabel('STATEMENT / {p['ch']:02d}.{p['pageInCh']:02d}', 150, 820, {{ size: 12, color: 'muted', at: 1.0 }});"""
    elif p["t"] == "split":
        body = base(p, size=84, color="ink") + "\n" + viz(p, at=1.05) + f"""
  P.noirLabel('NOTE / {p['ch']:02d}.{p['pageInCh']:02d}', 150, 820, {{ size: 12, color: 'muted', at: 1.1 }});"""
    elif p["t"] == "list":
        body = base(p, size=82, color="ink")
        body += f"""
  P.noirCard(1140, 440, 400, 190, {{ fill: '#0A1214', color: 'soft', sw: 1.0, at: 1.25, dur: 0.7 }});
  P.line(1140, 440, 1182, 440, {{ color: 'orange', sw: 1.2, at: 1.45, dur: 0.3, pen: false }});
  P.line(1140, 440, 1140, 484, {{ color: 'orange', sw: 1.2, at: 1.5, dur: 0.3, pen: false }});
  P.text({js(p.get('key', p['ghost']))}, {{ x: 1330, y: 492, w: 300, align: 'c', size: 34, font: 'serif', color: 'ink', at: 1.5, mode: 'fade', dur: 0.5 }});
  P.noirLabel('THE / LIST', 1340, 570, {{ size: 12, color: 'muted', at: 1.7 }});"""
        for i, item in enumerate(p.get("items", [])[:4]):
            y = 480 + i * 92
            body += f"""
  H.noirLabel('{i + 1:02d}', 150, {y}, {{ size: 13, color: 'orange', at: {0.95 + i * 0.25}, track: '0.1em' }});
  P.text({js(item)}, {{ x: 210, y: {y - 12}, size: 31, font: 'serif', color: 'ink', at: {1.0 + i * 0.25}, mode: 'fade', dur: 0.45, w: 760 }});
  P.noirHairline(150, 760, {y + 38}, {{ color: 'faint', sw: 1, at: {1.05 + i * 0.25}, dur: 0.55, opacity: 0.6 }});"""
        body += f"""
  P.noirLabel('INDEX / {p['ch']:02d}.{p['pageInCh']:02d}', 150, 820, {{ size: 12, color: 'muted', at: 1.2 }});"""
    elif p["t"] == "steps":
        body = base(p, size=82, color="ink")
        xs = [300, 960, 1620]
        body += f"""
  P.noirConnector(360, 580, 900, 580, {{ color: 'soft', sw: 1, dashed: true, dash: '4 8', at: 1.0, dur: 0.7, opacity: 0.4 }});
  P.noirConnector(1020, 580, 1560, 580, {{ color: 'soft', sw: 1, dashed: true, dash: '4 8', at: 1.2, dur: 0.7, opacity: 0.4 }});"""
        for i, (x, item) in enumerate(zip(xs, p.get("items", []))):
            body += f"""
  P.noirNode({x}, 580, 12, {{ color: 'orange', at: {1.1 + i * 0.15}, dur: 0.45 }});
  H.noirLabel('{i + 1:02d}', {x - 12}, 528, {{ size: 13, color: 'muted', at: {1.2 + i * 0.15} }});
  P.text({js(item)}, {{ x: {x}, y: 620, w: 360, align: 'c', size: 30, font: 'serif', color: 'ink', at: {1.3 + i * 0.15}, mode: 'fade', dur: 0.45 }});"""
        body += f"""
  P.noirLabel('STEPS / {p['ch']:02d}.{p['pageInCh']:02d}', 150, 820, {{ size: 12, color: 'muted', at: 1.2 }});"""
    elif p["t"] == "twoPaths":
        body = base(p, size=84, color="ink")
        if p.get("viz") == "scale":
            body += "\n" + viz(p, at=1.05)
        else:
            body += f"""
  P.noirCurve('M960 720 C900 620 780 500 640 380', {{ color: 'blue', sw: 2.2, glow: 6, at: 1.05, dur: 1.0 }});
  P.noirCurve('M960 720 C1020 620 1140 500 1280 380', {{ color: 'red', sw: 2.2, glow: 5, at: 1.2, dur: 1.0 }});
  P.noirLabel({js(p['left'])}, 620, 340, {{ size: 20, color: 'blue', at: 1.7 }});
  P.noirLabel({js(p['right'])}, 1240, 340, {{ size: 20, color: 'red', at: 1.8 }});
  P.noirNode(960, 720, 6, {{ at: 1.0, dur: 0.4 }});"""
        body += f"""
  P.noirLabel('PATHS / {p['ch']:02d}.{p['pageInCh']:02d}', 150, 820, {{ size: 12, color: 'muted', at: 1.2 }});"""
    else:  # closing
        body = f"""
  P.noirGhost({js(p['ghost'])}, {{ x: 1280, y: 180, size: 300, opacity: 0.07 }});
  P.noirReveal({js(p['title'])}, {{ x: 960, y: 240, w: 1300, align: 'c', size: 74, color: 'orange', at: 0.3, dur: 0.7, stagger: 0.05 }});
  P.text({js(p['sub'])}, {{ x: 960, y: 360, w: 1100, align: 'c', size: 32, font: 'serif', color: 'soft', at: 0.9, mode: 'fade', dur: 0.55, lh: 1.4 }});
  P.noirWave(680, 500, 560, 105, {{ bars: 36, gap: 5, color: 'blue', at: 1.0, dur: 0.7 }});
  P.path('M928 660 Q928 640 952 640 Q976 640 976 660 L976 724 Q976 748 952 748 Q928 748 928 724 Z', {{ color: 'orange', sw: 1.5, at: 1.3, dur: 0.6 }});
  P.line(938, 674, 966, 674, {{ color: 'orange', sw: 1, at: 1.5, dur: 0.3, pen: false }});
  P.line(938, 690, 966, 690, {{ color: 'orange', sw: 1, at: 1.56, dur: 0.3, pen: false }});
  P.line(938, 706, 966, 706, {{ color: 'orange', sw: 1, at: 1.62, dur: 0.3, pen: false }});
  P.line(952, 748, 952, 790, {{ color: 'orange', sw: 1.2, at: 1.7, dur: 0.3, pen: false }});
  P.line(920, 790, 984, 790, {{ color: 'orange', sw: 1.2, at: 1.8, dur: 0.3, pen: false }});
  P.noirLabel('李安 · 情感修复', 960, 830, {{ size: 13, color: 'muted', at: 1.6, track: '0.2em' }});
  P.noirLabel('STAY / TOGETHER', 1650, 140, {{ size: 11, color: 'faint', at: 0.8 }});"""
    return f"""/* {p['id']} · {p['title']} · generated */
ENGINE.visual({js(p['id'])}, (P) => {{
{head}
{body}
}});
"""

for p in pages:
    (PROJ / "pages" / f"{p['id']}.js").write_text(page_code(p), encoding="utf-8")

print(f"{len(pages)} pages · {len(segs)} segments · cues {sum(len(p['cues']) for p in pages)}")
print("last segment ends", segs[-1]["end"])
