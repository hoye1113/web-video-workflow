# -*- coding: utf-8 -*-
"""从 116 的音频切页生成 night-insight 的页面内容（米白 4:3 版）。
26 页与 voice.js / script.js 的 p01-p26 一一对应；改这里，重跑本文件即可。
"""
import json
from pathlib import Path

P = []


def add(layout, chapter, name, **kw):
    P.append(dict(layout=layout, chapter=chapter, name=name, **kw))


add("hook", "01", "钩子",
    kicker="婚姻信任 · 3 个真相",
    title=["她反复追问", "不是折磨你"],
    lead="出轨之后，她总问细节，<br>到底在问什么？",
    phone={
        "name": "她", "status": "在线",
        "messages": [
            {"side": "in", "text": "那天到底怎么回事"},
            {"side": "out", "text": "都过去了，别问了"},
            {"side": "in", "text": "你是不是早就开始了"},
            {"side": "in", "text": "你告诉我细节", "dim": True},
        ],
        "read": "已读",
        "typing": "对方正在输入…",
    },
    note="三个真相，读懂她的追问")

add("list", "01", "钩子",
    kicker="先说结论",
    title=["她不是", "揪着不放"],
    items=["不是报复你", "不是收集证据", "她是在自救"],
    caption="换个角度，才听得懂她的追问。")

add("list", "02", "三个真相",
    kicker="三个真相",
    title=["三个真相", "读懂她的追问"],
    items=["她要确定", "她要教训", "她要未来"],
    caption="看懂这些，才知道怎么回应。")

add("heart", "02", "三个真相",
    kicker="她一遍遍问",
    title=["她一遍遍问", "到底想要什么？"],
    quote={"label": "不是", "text": "“不是为了让你难受，<br>是想知道还能不能走下去。”"},
    caption="这是她给关系的一次确认。")

# 真相一
add("list", "03", "真相一",
    kicker="真相一",
    title=["真相一", "她是在自救"],
    items=["混乱的思绪需要停下", "痛苦想象需要落地", "她需要一份确定"],
    caption="她不是要折磨你，是要救自己。")

add("heart", "03", "真相一",
    kicker="找一个答案",
    title=["她在给关系", "找一个答案"],
    quote={"label": "她想确认", "text": "“这段关系，<br>到底还能不能继续？”"},
    caption="她问的是细节，要的是确定。")

add("translate", "03", "真相一",
    kicker="心理学上",
    title=["这叫", "创伤后应激反应"],
    saidLabel="重大伤害之后", said="“事情一直模糊”",
    heardLabel="大脑会", heard="“反复回响、内耗、脑补”",
    caption="不是她矫情，是警报停不下来。")

add("list", "03", "真相一",
    kicker="越模糊",
    title=["事情越模糊", "越会反复回响"],
    items=["不受控制地回想", "脑补最坏的画面", "越想越可怕"],
    caption="你越闭口不提，她越往坏处想。")

add("heart", "03", "真相一",
    kicker="越不说",
    title=["你越不说", "她越会猜"],
    quote={"label": "她脑子里", "text": "“是不是早就开始了？<br>是不是一切都是蓄谋已久？”"},
    caption="隐瞒，只会让她更不安。")

add("split", "03", "真相一",
    kicker="她要的是",
    title=["她要的不是", "无限细节"],
    left={"color": "cyan", "tag": "她要", "icon": "eye", "title": "确定",
          "items": ["确定", "边界", "安全感"]},
    right={"color": "red", "tag": "她不要", "icon": "warning", "title": "敷衍",
           "items": ["敷衍", "隐瞒", "一次次猜"]},
    wall="确定",
    caption="细节是入口，确定才是答案。")

add("list", "03", "真相一",
    kicker="具体的事",
    title=["把模糊的噩梦", "变成一件具体的事"],
    items=["用事实替代猜疑", "让想象落地", "自我消耗才能停下"],
    caption="清晰的经过，才能让她停止脑补。")

add("heart", "03", "真相一",
    kicker="不是保护",
    title=["你以为隐瞒", "是在保护她"],
    quote={"label": "其实", "text": "“是把她一个人，<br>丢在痛苦想象里。”"},
    caption="隐瞒不是保护，是让她独自内耗。")

# 真相二
add("list", "04", "真相二",
    kicker="真相二",
    title=["真相二", "切断再次犯错的退路"],
    items=["道歉不等于翻篇", "模糊会随时间淡化", "清晰才会记住教训"],
    caption="她要细节，是让教训刻进心里。")

add("heart", "04", "真相二",
    kicker="一句对不起",
    title=["一句对不起", "翻不过这一页"],
    quote={"label": "现实", "text": "“要过细节的道歉，<br>大多只是敷衍。”"},
    caption="真正的悔改，是敢把经过摊开。")

add("list", "04", "真相二",
    kicker="模糊与清晰",
    title=["模糊会淡化", "清晰才会记住"],
    items=["模糊的感受容易过去", "清晰的经过留在心里", "记住痛，才不再犯"],
    caption="她要的不是报复，是让你记住。")

add("heart", "04", "真相二",
    kicker="一根刺",
    title=["清晰的经过", "会像一根刺"],
    quote={"label": "留在心里", "text": "“提醒你这份痛。”"},
    caption="这不是惩罚，是约束。")

add("list", "04", "真相二",
    kicker="长久教训",
    title=["把当下的冲击", "变成长久教训"],
    items=["记住这份痛", "克制再次犯错", "守住这个家"],
    caption="教训越清晰，越不容易重蹈覆辙。")

add("wall", "04", "真相二",
    kicker="约束与守护",
    title=["这既是约束", "也是守护"],
    leftName="你", rightName="她", wall="家",
    caption="她不是在毁这个家，是在守这个家。")

# 真相三
add("list", "05", "真相三",
    kicker="真相三",
    title=["真相三", "判断这段婚姻值不值得"],
    items=["她想知道为什么", "她想知道还能不能修", "她在看你的态度"],
    caption="不是找茬，是在做最后的判断。")

add("split", "05", "真相三",
    kicker="态度",
    title=["你的态度", "就是答案"],
    left={"color": "cyan", "tag": "一时糊涂", "icon": "eye", "title": "愿意",
          "items": ["愿意坦白", "愿意承担", "愿意改"]},
    right={"color": "red", "tag": "没有真心", "icon": "warning", "title": "逃避",
           "items": ["敷衍", "回避", "倒打一耙"]},
    wall="诚意",
    caption="她看的是你有没有诚意。")

add("heart", "05", "真相三",
    kicker="没有勇气",
    title=["如果你连坦诚", "的勇气都没有"],
    quote={"label": "她会明白", "text": "“你只是人回来了，<br>心没有回来。”"},
    caption="看不到诚意，她会对婚姻死心。")

add("list", "05", "真相三",
    kicker="不是惩罚",
    title=["她要的不是惩罚", "是清楚的说法"],
    items=["为什么走到这一步", "这个家还能不能修", "还能不能有未来"],
    caption="她是在给这段婚姻最后一次机会。")

add("heart", "05", "真相三",
    kicker="一起挖根源",
    title=["只要你愿意", "一起挖出问题根源"],
    quote={"label": "哪怕很痛", "text": "“她也愿意再给一次机会。”"},
    caption="坦诚，是接住她的手。")

# 收尾
add("list", "06", "收尾",
    kicker="所以",
    title=["所以当她", "再一次追问"],
    items=["别敷衍", "别回避", "别把她的手推开"],
    caption="那是她在绝望里伸出的手。")

add("heart", "06", "收尾",
    kicker="最后一道考题",
    title=["你的坦诚和担当", "就是答案"],
    quote={"label": "接住她", "text": "“接住这只手，<br>打好这道题。”"},
    caption="这是她给你的最后一道考题。")

add("end", "06", "收尾",
    kicker="李安 · 夜读",
    title=["满目疮痍之后", "再重新出发"],
    note="两个人一起直面，才有机会重建。",
    sub="先接住，再往前走。")

assert len(P) == 26, f"expected 26 pages, got {len(P)}"
spec = {f"p{i + 1:02d}": p for i, p in enumerate(P)}
out = Path(__file__).with_name("night-spec.js")
out.write_text("window.NIGHT_SPEC = " + json.dumps(spec, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
print(f"wrote {out} · {len(spec)} pages")
