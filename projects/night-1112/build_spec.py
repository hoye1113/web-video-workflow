# -*- coding: utf-8 -*-
"""从 1112 的音频切页生成 night-insight 的页面内容。
49 页与 voice.js / script.js 的 p01-p49 一一对应；改这里，重跑本文件即可。
"""
import json
from pathlib import Path

P = []


def add(layout, chapter, name, **kw):
    P.append(dict(layout=layout, chapter=chapter, name=name, **kw))


# 01 钩子
add("hook", "01", "钩子",
    kicker="婚姻信任 · 6 分钟",
    title=["原谅了", "却放不下"],
    lead="夫妻接纳了犯错的伴侣，<br>却始终放不下怀疑。",
    phone={
        "name": "她", "status": "在线",
        "messages": [
            {"side": "in", "text": "我原谅你了"},
            {"side": "out", "text": "可我还是会查你手机"},
            {"side": "in", "text": "你到底想怎样"},
            {"side": "in", "text": "我已经很努力了", "dim": True},
        ],
        "read": "已读",
        "typing": "对方正在输入…",
    },
    note="最难的，不是原谅，是重新相信")

add("split", "01", "钩子",
    kicker="先说结论",
    title=["这不是你", "小题大做"],
    left={"color": "orange", "tag": "你以为", "icon": "toolbox", "title": "放不下",
          "items": ["不够大度", "揪着过去", "脾气变差"]},
    right={"color": "cyan", "tag": "其实是", "icon": "eye", "title": "信任崩塌",
           "items": ["本能警惕", "安全感丢失", "怕再被伤一次"]},
    wall="信任",
    caption="信任崩塌后的反应，不是矫情。")

# 02 信任崩塌
add("list", "02", "信任崩塌",
    kicker="信任崩塌后",
    title=["信任崩塌后", "人会本能警惕"],
    items=["不是小题大做", "是本能反应", "也是背叛的代价"],
    caption="你防的不是她，是再次受伤。")

add("translate", "02", "信任崩塌",
    kicker="信任是什么",
    title=["失去信任", "= 失去确定性"],
    saidLabel="原本", said="平常的小事",
    heardLabel="现在", heard="处处暗藏风险",
    caption="一个细节，就会被放大。")

add("list", "02", "信任崩塌",
    kicker="一个细节",
    title=["一个细节", "会被放大成什么"],
    items=["敏锐捕捉", "心底放大", "脑补最坏结果"],
    caption="想象力越丰富，内耗越深。")

# 03 内耗
add("heart", "03", "内耗",
    kicker="脑补",
    title=["脑补，会", "先于事实到来"],
    quote={"label": "你脑子里", "text": "“她是不是又在骗我？”"},
    caption="就算什么都没发生，难受也是真的。")

add("wall", "03", "内耗",
    kicker="困住关系的",
    title=["困住关系的", "常常不是事件"],
    leftName="事件", rightName="解读", wall="解读",
    caption="是你对这件事的解读。")

add("heart", "03", "内耗",
    kicker="情绪袭来",
    title=["情绪，会", "席卷整个人"],
    quote={"label": "真实感受", "text": "“我控制不住地<br>往坏处想。”"},
    caption="负面感受，会催生负面行为。")

add("list", "03", "内耗",
    kicker="然后",
    title=["然后，关系开始", "反复拉扯"],
    items=["反复争吵", "刻意冷战", "互相刺伤"],
    caption="一段被击穿信任的婚姻，处处都是雷。")

add("split", "03", "内耗",
    kicker="你盯着她",
    title=["你盯着她", "其实在盯着危险"],
    left={"color": "orange", "tag": "她的动作", "icon": "eye", "title": "她的日常",
          "items": ["晚归", "手机", "沉默"]},
    right={"color": "red", "tag": "你的警报", "icon": "warning", "title": "三种警报",
           "items": ["是不是又骗我", "是不是不在乎", "是不是要离开"]},
    wall="警惕",
    caption="长期警惕，消耗的也是你。")

# 04 追问
add("heart", "04", "追问",
    kicker="你不停追问",
    title=["你不停追问", "只是想安心"],
    quote={"label": "你想问的", "text": "“你还爱我吗？”<br>“你还会骗我吗？”"},
    caption="你要的不是道歉，是确定感。")

add("list", "04", "追问",
    kicker="你一次次要的",
    title=["你一次次要的", "不是为难"],
    items=["一个道歉", "一个承诺", "一个还能走下去的信号"],
    caption="你只是想找回，丢失的安全感。")

add("translate", "04", "追问",
    kicker="你想找回的",
    title=["你想找回的", "是安全感"],
    saidLabel="你听到", said="“对不起”",
    heardLabel="你想确认", heard="“还能走下去吗”",
    caption="反复确认，是在确认关系还活着。")

# 05 原则
add("wall", "05", "原则",
    kicker="修复的前提",
    title=["一个人", "修不好两个人的信任"],
    leftName="你", rightName="她", wall="一起",
    caption="两个人都想守住，才叫修复。")

add("list", "05", "原则",
    kicker="李安的原则",
    title=["修复原则", "谁破坏，谁修复"],
    items=["过错方扛起责任", "不推卸、不躲闪", "先拿出诚意"],
    caption="这是第一步，也是最关键的一步。")

add("split", "05", "原则",
    kicker="认错",
    title=["认错，", "不能找借口"],
    left={"color": "cyan", "tag": "可以解释", "icon": "toolbox", "title": "解释",
          "items": ["当时的处境", "犯错的动机"]},
    right={"color": "red", "tag": "不能推卸", "icon": "warning", "title": "推卸",
           "items": ["躲闪逃避", "含糊敷衍", "倒打一耙"]},
    wall="责任",
    caption="解释不是免罪，认错才是开始。")

# 06 过错方
add("list", "06", "过错方",
    kicker="第一步",
    title=["第一步", "老老实实认错"],
    items=["错了就是错了", "不找借口", "踏踏实实改"],
    caption="弯弯绕绕的认错，等于没认。")

add("wall", "06", "过错方",
    kicker="受伤的人",
    title=["受伤的人", "难免反复"],
    leftName="你", rightName="她", wall="情绪",
    caption="上一秒平静，下一秒崩溃，都是正常反应。")

add("list", "06", "过错方",
    kicker="她需要",
    title=["她需要接住", "你的情绪"],
    items=["足够耐心", "安抚不安", "陪你慢慢平复"],
    caption="不是让你别想，是陪你一起想。")

add("heart", "06", "过错方",
    kicker="修复也要放下",
    title=["放下一点", "自由和体面"],
    quote={"label": "过错方", "text": "“接受合理监督，<br>主动给安心。”"},
    caption="陪着你平复，也接受你的不安。")

add("split", "06", "过错方",
    kicker="透明",
    title=["透明，", "不是监控"],
    left={"color": "cyan", "tag": "主动给安心", "icon": "eye", "title": "主动",
          "items": ["分享日常", "同步行踪", "主动报备"]},
    right={"color": "red", "tag": "被迫交代", "icon": "warning", "title": "被动",
           "items": ["查手机", "逼问", "审犯人"]},
    wall="透明",
    caption="主动，才叫安心；被动，只叫应付。")

add("list", "06", "过错方",
    kicker="用行动",
    title=["用行动", "一点点攒回信任"],
    items=["稳定的回应", "持续的陪伴", "一点点攒回"],
    caption="信任不是一次原谅，是很多次验证。")

add("list", "06", "过错方",
    kicker="别困在回忆里",
    title=["别长时间", "困在负面回忆里"],
    items=["一起短途出行", "看场电影", "见见共同的朋友"],
    caption="共同经历，比反复解释更有用。")

add("wall", "06", "过错方",
    kicker="归属感",
    title=["找回", "“我们是一体”的感觉"],
    leftName="你", rightName="她", wall="一起",
    caption="这是过错方要付出的努力。")

# 07 受伤方
add("choice", "07", "受伤方",
    kicker="受伤方",
    title=["受伤方", "也不能只剩防备"],
    left={"color": "red", "icon": "warning", "title": "受害者心态", "sub": "反复怀疑、验证、报复"},
    right={"color": "cyan", "icon": "eye", "title": "修复心态", "sub": "看见改变、理性判断、给回应"},
    quote="“你可以警惕，但别把自己困死。”")

add("list", "07", "受伤方",
    kicker="看见改变",
    title=["看见她", "实实在在的改变"],
    items=["主动早归", "留意你的情绪", "愿意敞开沟通"],
    caption="这些都是她想修复关系的信号。")

add("heart", "07", "受伤方",
    kicker="别让报复",
    title=["别让报复", "毁掉修复的机会"],
    quote={"label": "记住", "text": "“想宣泄是人之常情，<br>但别抱着报复的心态。”"},
    caption="你的目标，是修复，不是摧毁。")

add("heart", "07", "受伤方",
    kicker="记住目标",
    title=["记住你的目标", "修复，不是摧毁"],
    quote={"label": "提醒自己", "text": "“你的目标是修复婚姻，<br>不是彻底摧毁<br>这段关系。”"},
    caption="宣泄情绪可以，但别忘方向。")

add("wall", "07", "受伤方",
    kicker="配合",
    title=["缺少你的配合", "她也修不好"],
    leftName="她", rightName="你", wall="配合",
    caption="信任，是两个人一起重建的。")

# 08 警觉
add("split", "08", "警觉",
    kicker="两种极端",
    title=["绝对信任", "和绝对猜忌，都危险"],
    left={"color": "cyan", "tag": "全然信任", "icon": "eye", "title": "全然信任",
          "items": ["失去风险意识", "忽略问题"]},
    right={"color": "red", "tag": "无休止猜忌", "icon": "warning", "title": "无休止猜忌",
           "items": ["困在焦虑", "耗尽情谊"]},
    wall="适度",
    caption="更好的状态，是保持适度警觉。")

add("heart", "08", "警觉",
    kicker="无休止猜忌",
    title=["无休止的猜忌", "会耗尽所有情谊"],
    quote={"label": "结果", "text": "“你困在焦虑里，<br>她也越来越远。”"},
    caption="猜忌不会保护你，只会消耗你。")

add("heart", "08", "警觉",
    kicker="更好的状态",
    title=["更好的状态", "是适度警觉"],
    quote={"label": "分清", "text": "“清楚风险，<br>但不预设罪名。”"},
    caption="理性的警觉，和草木皆兵是两回事。")

add("translate", "08", "警觉",
    kicker="理性警觉",
    title=["理性警觉", "≠ 草木皆兵"],
    saidLabel="理性", said="“有风险”",
    heardLabel="多疑", heard="“她一定会越界”",
    caption="一个是判断，一个是想象。")

add("list", "08", "警觉",
    kicker="过度多疑",
    title=["过度多疑", "常常来自哪里"],
    items=["捕风捉影", "预设罪名", "把正常相处当越界"],
    caption="你防的，可能不是她。")

add("list", "08", "警觉",
    kicker="过度多疑",
    title=["过度多疑", "常来自内心的自卑"],
    items=["不够认可自己", "怕自己留不住对方", "提前预设她会离开"],
    caption="你防的不是她，是自己不被爱的恐惧。")

add("heart", "08", "警觉",
    kicker="你怕的",
    title=["你怕的", "不是她变心"],
    quote={"label": "是", "text": "“你觉得自己，<br>留不住任何人。”"},
    caption="先认可自己，才更容易信任别人。")

add("wall", "08", "警觉",
    kicker="别困在想象里",
    title=["别困在", "主观想象里"],
    leftName="想象", rightName="事实", wall="证据",
    caption="婚姻有裂痕，但未必会持续恶化。")

# 09 敏感伴侣
add("heart", "09", "敏感伴侣",
    kicker="如果她敏感多疑",
    title=["如果她敏感多疑", "你就主动给安心"],
    quote={"label": "透明", "text": "“我会让你知道，<br>你在哪里、我在哪里。”"},
    caption="透明，是给敏感的人最好的定心丸。")

add("list", "09", "敏感伴侣",
    kicker="多肯定",
    title=["多肯定，多赞美", "帮她建立底气"],
    items=["看见她的付出", "说出你的需要", "让她感到被需要"],
    caption="被肯定的人，才更容易相信关系。")

# 10 信任
add("heart", "10", "信任",
    kicker="学着信任",
    title=["学着信任", "是一种能力"],
    quote={"label": "人都会", "text": "“期待另一半忠诚，<br>但信任需要练习。”"},
    caption="没有信任，就没有真正的安全感。")

add("wall", "10", "信任",
    kicker="没有信任",
    title=["没有信任", "就没有安全感"],
    leftName="信任", rightName="安全感", wall="连接",
    caption="亲密的亲密关系，也就无从谈起。")

add("list", "10", "信任",
    kicker="家和",
    title=["家和，", "万事才兴"],
    items=["猜忌不断", "争执不休", "消耗生活"],
    caption="人很难把精力，投入工作和生活。")

add("heart", "10", "信任",
    kicker="信任像空气",
    title=["信任像空气", "失去才知窒息"],
    quote={"label": "拥有时", "text": "常常忽略，<br>失去才知窒息。"},
    caption="没有信任的婚姻，走不远。")

add("wall", "10", "信任",
    kicker="地基",
    title=["没有信任的婚姻", "像没有地基的房子"],
    leftName="信任", rightName="婚姻", wall="地基",
    caption="摇摇欲坠，幸福无从谈起。")

# 11 收尾
add("list", "11", "收尾",
    kicker="但换个角度",
    title=["但危机", "也是重塑的契机"],
    items=["两个人愿意", "坚持往前走", "难关之后更稳固"],
    caption="痛苦会催生改变，也会暴露问题。")

add("heart", "11", "收尾",
    kicker="痛苦",
    title=["痛苦，", "会催生改变的决心"],
    quote={"label": "也看清", "text": "“婚姻里原本藏着的<br>那些问题。”"},
    caption="看见问题，才有机会修。")

add("list", "11", "收尾",
    kicker="走出伤痛",
    title=["走出伤痛", "重新建立连接"],
    items=["化解隔阂", "重新连接", "完成蜕变"],
    caption="像久旱逢甘霖的草木，重新长出来。")

add("heart", "11", "收尾",
    kicker="变得牢不可破",
    title=["变得牢不可破", "劝和不劝离"],
    quote={"label": "先修复", "text": "“再决定。”"},
    caption="婚姻感情里，别在情绪里做终局。")

add("end", "11", "收尾",
    kicker="李安 · 夜读",
    title=["李安愿意", "认真听你的故事"],
    note="陪你梳理出路。",
    sub="给你温暖的陪伴，和坚定的支撑。")

assert len(P) == 49, f"expected 49 pages, got {len(P)}"
spec = {f"p{i + 1:02d}": p for i, p in enumerate(P)}
out = Path(__file__).with_name("night-spec.js")
out.write_text("window.NIGHT_SPEC = " + json.dumps(spec, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
print(f"wrote {out} · {len(spec)} pages")
