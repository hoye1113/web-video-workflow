# -*- coding: utf-8 -*-
"""从 1115 的音频切页生成 night-insight 的页面内容（4:3 版）。
29 页与 voice.js / script.js 的 p01-p29 一一对应；改这里，重跑本文件即可。
"""
import json
from pathlib import Path

P = []


def add(layout, chapter, name, **kw):
    P.append(dict(layout=layout, chapter=chapter, name=name, **kw))


add("hook", "01", "钩子",
    kicker="婚姻信任 · 5 步",
    title=["出轨之后", "还能继续吗？"],
    lead="如果你还想守住这个家，<br>花几分钟，把这段话听完。",
    phone={
        "name": "她", "status": "在线",
        "messages": [
            {"side": "in", "text": "我原谅你了"},
            {"side": "out", "text": "可我忘不掉"},
            {"side": "in", "text": "你到底想怎样"},
            {"side": "in", "text": "我已经很努力了", "dim": True},
        ],
        "read": "已读",
        "typing": "对方正在输入…",
    },
    note="五步，走出信任危机")

add("list", "01", "钩子",
    kicker="先说结论",
    title=["五步", "走出信任危机"],
    items=["先听进去", "再落到生活里", "一步一步来"],
    caption="能不能走顺，看你们能不能一起做。")

# 01 重建信任
add("list", "02", "重建信任",
    kicker="第一步",
    title=["第一步", "重建信任"],
    items=["犯错方和受伤方都要明白", "信任像摔碎的瓷碗", "拼回去也回不到原样"],
    caption="裂纹会一直留在那里。")

add("heart", "02", "重建信任",
    kicker="摔碎的信任",
    title=["信任像", "摔碎的瓷碗"],
    quote={"label": "现实", "text": "“就算小心翼翼拼回去，<br>也回不到原来的样子。”"},
    caption="裂纹会一直留在那里。")

add("list", "02", "重建信任",
    kicker="谁来修",
    title=["谁打碎的", "谁扛修复"],
    items=["断掉外面的联系", "不留任何余地", "生活、社交、行程透明"],
    caption="修复的责任，必须由犯错方扛。")

add("split", "02", "重建信任",
    kicker="边界",
    title=["透明", "不是查岗"],
    left={"color": "cyan", "tag": "透明", "icon": "eye", "title": "主动",
          "items": ["主动报备", "行程可见", "社交公开"]},
    right={"color": "red", "tag": "查岗", "icon": "warning", "title": "控制",
           "items": ["逼问", "翻手机", "审犯人"]},
    wall="边界",
    caption="信任的地基被砸烂了，代价只能你担。")

add("list", "02", "重建信任",
    kicker="机会",
    title=["机会只给一次", "看行动"],
    items=["别只看怎么说", "看之后怎么做", "日复一日的改变"],
    caption="留下来，不代表这件事没发生过。")

add("heart", "02", "重建信任",
    kicker="不是道歉",
    title=["想重新赢得信任", "靠的不是道歉"],
    quote={"label": "而是", "text": "“一句对不起，<br>换不回日复一日的安心。”"},
    caption="日复一日的改变，才是答案。")

# 02 允许情绪
add("list", "03", "允许情绪",
    kicker="第二步",
    title=["第二步", "允许情绪被看见"],
    items=["别把情绪憋着", "别硬装大度", "坦白告诉他：我没走"],
    caption="不是不痛，是舍不得这个家。")

add("heart", "03", "允许情绪",
    kicker="我没走",
    title=["我没走", "不是软弱"],
    quote={"label": "真实", "text": "“不是不痛，<br>是舍不得这么多年的感情。”"},
    caption="别把她的留下，当成理所当然。")

add("split", "03", "允许情绪",
    kicker="翻篇",
    title=["一句对不起", "不能立刻翻篇"],
    left={"color": "orange", "tag": "你以为", "icon": "eye", "title": "该过去了",
          "items": ["道歉了就该过去", "提了就是矫情"]},
    right={"color": "red", "tag": "真实感受", "icon": "warning", "title": "刺还在",
           "items": ["一看见你就想起画面", "像一根刺扎在心里"]},
    wall="翻篇",
    caption="情绪反复，不是故意为难。")

add("list", "03", "允许情绪",
    kicker="反复",
    title=["情绪反复", "不是故意为难"],
    items=["会难过", "会委屈", "会莫名发脾气"],
    caption="是你留下的伤还没长好。")

add("heart", "03", "允许情绪",
    kicker="越在乎",
    title=["真不爱了", "反而不会在意"],
    quote={"label": "所以", "text": "“越是在乎，<br>情绪才越反复。”"},
    caption="请多一点理解，多一点耐心。")

# 03 说不安
add("list", "04", "说出不安",
    kicker="第三步",
    title=["第三步", "把不安说出口"],
    items=["别把委屈全憋着", "别总说都过去了", "别假装忘记"],
    caption="有些事，不是不提就不存在。")

add("heart", "04", "说出不安",
    kicker="反复提起",
    title=["反复提起", "是因为害怕"],
    quote={"label": "她怕", "text": "“怕你回来只是一时愧疚，<br>怕新鲜感过了你才回来。”"},
    caption="不是不提就不存在。")

add("list", "04", "说出不安",
    kicker="怕改变",
    title=["怕你的改变", "只是一阵子"],
    items=["时间一长又重蹈覆辙", "反复提起不是羞辱", "只是想确认你想回头"],
    caption="她想确认的，是你真的想好好过日子。")

add("heart", "04", "说出不安",
    kicker="说给彼此",
    title=["“我是真的", "想好好过日子。”"],
    quote={"label": "这句话", "text": "“要说给彼此听。”"},
    caption="别让不安，烂在心里。")

# 04 新规则
add("list", "05", "新规则",
    kicker="第四步",
    title=["第四步", "建立新的安全感规则"],
    items=["减少没必要的社交", "避免单独和异性接触", "去哪、和谁、做什么，主动说"],
    caption="把修复，落到具体的生活细节里。")

add("split", "05", "新规则",
    kicker="安全感",
    title=["透明", "不是控制"],
    left={"color": "cyan", "tag": "主动", "icon": "eye", "title": "给安心",
          "items": ["报备", "商量", "公开"]},
    right={"color": "red", "tag": "控制", "icon": "warning", "title": "逼交代",
           "items": ["查手机", "逼问", "限制自由"]},
    wall="安全感",
    caption="她需要时间，把安全感找回来。")

add("heart", "05", "新规则",
    kicker="看得见",
    title=["你的每一分努力", "她都看得见"],
    quote={"label": "慢慢来", "text": "“只要你真的在改变，<br>我也会慢慢放下戒备。”"},
    caption="一点点靠近，而不是一步到位。")

add("list", "05", "新规则",
    kicker="回归的人",
    title=["回归家庭的人", "也怕看不到头"],
    items=["不是不想补偿", "怕一辈子被钉在背叛者位置", "说出口，是给他一点希望"],
    caption="补偿，不该是无期徒刑。")

add("heart", "05", "新规则",
    kicker="还有机会",
    title=["只要真心弥补", "还有机会修好"],
    quote={"label": "别让", "text": "“补偿，<br>变成无期徒刑。”"},
    caption="两个人都要看到希望。")

# 05 给时间
add("list", "06", "给时间",
    kicker="第五步",
    title=["第五步", "给时间"],
    items=["重建信任很长", "伤口愈合也会留疤", "千万不能急"],
    caption="这是一件很长很长的事。")

add("heart", "06", "给时间",
    kicker="那道疤",
    title=["每次看见那道疤", "都会想起当初的疼"],
    quote={"label": "她不是", "text": "“说忘就能忘的人。”"},
    caption="感情碎过一次，不可能马上复原。")

add("list", "06", "给时间",
    kicker="慢慢消化",
    title=["她需要时间", "慢慢消化"],
    items=["一点点拼回信任", "别怪她总翻旧账", "爱得越深，伤得越重"],
    caption="不是她太执着，是伤太深。")

add("heart", "06", "给时间",
    kicker="深夜的痛",
    title=["那些深夜里的痛", "你没经历过"],
    quote={"label": "所以", "text": "“别指望我很快<br>像以前那样毫无保留。”"},
    caption="我们都需要时间，需要耐心。")

add("list", "06", "给时间",
    kicker="要多久",
    title=["背叛之后", "重建信任要多久"],
    items=["两年", "三年", "甚至更久"],
    caption="这很正常。")

# 收尾
add("wall", "07", "收尾",
    kicker="最后",
    title=["这条路", "一个人走不完"],
    leftName="她", rightName="你", wall="一起",
    caption="需要持续悔改，也需要慢慢释怀。")

add("end", "07", "收尾",
    kicker="李安 · 夜读",
    title=["从废墟里", "重新长出来"],
    note="两个人一起使劲，感情才有机会。",
    sub="先接住，再往前走。")

assert len(P) == 29, f"expected 29 pages, got {len(P)}"
spec = {f"p{i + 1:02d}": p for i, p in enumerate(P)}
out = Path(__file__).with_name("night-spec.js")
out.write_text("window.NIGHT_SPEC = " + json.dumps(spec, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
print(f"wrote {out} · {len(spec)} pages")
