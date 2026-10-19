"""26 页画面代码的生成器。

为什么不手写 26 个文件：一页里真正"创作"的只有四样 —— **处境图、机位、光、屏上字**，
其余都是同一套骨架（GRAMMAR 的规矩）。把四样写成表，代码由表生成：
**改哪页改哪行**，一眼能对比 26 页的节奏安排。

表在下面的 PAGES（照 `docs/页-处境映射.md` 施工）。跑：
    python tools/make_pages.py            # 生成 projects/emotion-full/pages/*.js
    python tools/make_pages.py --check    # 只打印表
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "projects" / "emotion-full" / "pages"

# 机位预设：**停 — 推 — 停**（GRAMMAR 要求：不做整页匀速慢推）
CAM = {
    "push40": "[[0, 1], [T * 0.38, 1], [T * 0.38 + 0.7, 1.09], [T, 1.09]]",
    "push55": "[[0, 1], [T * 0.55, 1], [T * 0.55 + 0.7, 1.07], [T, 1.07]]",
    "push70": "[[0, 1], [T * 0.7, 1], [T * 0.7 + 0.7, 1.05], [T, 1.05]]",
    "pull":   "[[0, 1.09], [T * 0.34, 1.09], [T * 0.34 + 0.9, 1], [T, 1]]",
    "hold":   "[[0, 1.03], [T, 1.03]]",
    "tight55": "[[0, 1.22], [T * 0.55, 1.22], [T * 0.55 + 0.7, 1.30], [T, 1.30]]",   # 主体太小的图用它（裁进来）
}

# 一页 = 图 / 主题 / 机位 / 明暗（reveal: from,to,at,dur）/ 调色 / 灯 / 字
# 灯 = (x, y, r, kind, at, color, k)；字 = (文字, x, y, 字号, 对齐, 颜色, at)
PAGES = [
    dict(id="p01", title="背叛之后，还会不会爱老婆", asset="p01-paper-fold.png", theme="day",
         cam="push40", reveal=(0.30, 1, 0.2, 1.5),
         lights=[(520, 240, 760, "window", 0.4, "", "PV.clamp(lt / 2)")],
         texts=[("还会爱吗", 260, 240, 44, "l", "ink", 1.4)]),

    dict(id="p02", title="不捅破这层窗户纸，妻子会一直蒙在鼓里", asset="p02-paper-window.png",
         theme="day", cam="push55", reveal=(0.32, 1, 0.2, 1.4),
         lights=[(1190, 330, 430, "window", 0.9, "blue", "PV.clamp((lt - 0.9) / 1.6)")],
         texts=[("捅破窗户纸", 250, 230, 44, "l", "ink", 1.2)]),

    dict(id="p03", title="三个真实案例，比任何道理都更能改变理解", asset="p03-cases.png",
         theme="day", cam="push55", reveal=(0.32, 1, 0.2, 1.4),
         lights=[(960, 240, 820, "window", 0.4, "", "PV.clamp(lt / 2)")],
         texts=[("挑出三个", 250, 230, 44, "l", "ink", 1.3)]),

    dict(id="p04", title="暴露往往始于一次意外，他的第一反应是恐惧", asset="male-02-phone-glow.png",
         theme="day", cam="push40", reveal=(0.35, 1, 0.2, 1.4), grade="brightness: 0.92, saturate: 0.94",
         lights=[(1010, 600, 360, "screen", 1.0, "blue", "PV.clamp((lt - 1.0) / 1.2)")],
         texts=[("三年的关系", 250, 230, 44, "l", "ink", 1.5)]),

    dict(id="p05", title="妻子提离婚的当晚，他跪下来认错", asset="p05-kneel.png", theme="day",
         cam="push40", reveal=(0.30, 1, 0.2, 1.5),
         lights=[(500, 250, 720, "window", 0.4, "", "PV.clamp(lt / 2)")],
         texts=[("当场崩塌", 250, 230, 44, "l", "ink", 1.4)]),

    dict(id="p06", title="换副卡、删联系人，他用行动证明要回归", asset="p06-sim-card.png",
         theme="day", cam="push55", reveal=(0.35, 1, 0.2, 1.4),
         lights=[(980, 520, 460, "window", 0.5, "", "PV.clamp(lt / 2)")],
         texts=[("断联消息", 250, 230, 44, "l", "ink", 1.4)]),

    dict(id="p07", title="嘴上答应去讨说法，心里极度抗拒", asset="p07-crease.png", theme="day",
         cam="push55", reveal=(0.35, 1, 0.25, 1.4),
         lights=[(560, 420, 560, "window", 0.6, "", "PV.clamp(lt / 2)")],
         texts=[("追问细节", 250, 230, 44, "l", "ink", 1.4)]),

    dict(id="p08", title="清空账号不等于回归，白天演丈夫夜里睡不着", asset="male-06-bed-edge.png",
         theme="night", cam="push40", reveal=(0.30, 1, 0.2, 1.6),
         grade="brightness: 0.88, saturate: 0.9",
         lights=[(1150, 320, 430, "lamp", 0.4, "orange", "PV.clamp(1 - (lt - 1.5) / 5)")],
         texts=[("白天演，夜里熬", 250, 230, 44, "l", "ink", 1.6)]),

    dict(id="p09", title="婚姻在出事之前，早已无波无澜", asset="male-03-long-table.png", theme="day",
         cam="pull", reveal=(0.30, 1, 0.25, 1.5),
         lights=[(960, 300, 900, "window", 0.5, "", "PV.clamp(lt / 2)")],
         texts=[("无波无澜", 250, 230, 44, "l", "ink", 1.5)]),

    dict(id="p10", title="被关注的感觉太强，让他觉得自己重新活了一次", asset="p10-wine-glass.png",
         theme="day", cam="push55", reveal=(0.35, 1, 0.25, 1.4),
         lights=[(1180, 470, 400, "lamp", 0.8, "orange", "PV.clamp((lt - 0.8) / 1.5)")],
         texts=[("重新活了一次", 250, 230, 44, "l", "ink", 1.3)]),

    dict(id="p11", title="刺激越强，他越要拿婚姻的平淡去做对比", asset="p11-cup-choice.png",
         theme="day", cam="push55", reveal=(0.35, 1, 0.25, 1.4),
         lights=[(1250, 560, 420, "lamp", 0.7, "orange", "PV.clamp((lt - 0.7) / 1.5)")],
         texts=[("拿平淡做对比", 250, 230, 44, "l", "ink", 1.4)]),

    dict(id="p12", title="在外面被需要，回家只剩压力，所以他更爱逃", asset="male-05-door-crack.png",
         theme="day", cam="push55", reveal=(0.35, 1, 0.25, 1.4),
         lights=[(1300, 300, 520, "screen", 0.7, "blue", "PV.clamp((lt - 0.7) / 1.6)")],
         texts=[("更容易逃避", 250, 230, 44, "l", "ink", 1.5)]),

    dict(id="p13", title="愧疚和背叛，可以同时存在", asset="p13-two-lights.png", theme="day",
         cam="push40", reveal=(0.32, 1, 0.2, 1.5),
         lights=[(420, 620, 560, "lamp", 0.5, "orange", "PV.clamp((lt - 0.5) / 1.5)"),
                 (1520, 620, 560, "screen", 1.0, "blue", "PV.clamp((lt - 1.0) / 1.5)")],
         texts=[("愧疚", 250, 230, 40, "l", "orange", 1.4),
                ("背叛", 1500, 230, 40, "l", "blue", 2.2)]),

    dict(id="p14", title="主动断掉外面，并不代表他就轻松了", asset="p14-scissors.png", theme="day",
         cam="push55", reveal=(0.35, 1, 0.25, 1.4),
         lights=[(560, 420, 560, "window", 0.6, "", "PV.clamp(lt / 2)")],
         texts=[("主动断掉", 250, 230, 44, "l", "ink", 1.4)]),

    dict(id="p15", title="白天正常晚上装没事，他连亲密都不敢拒绝", asset="p15-night-door.png",
         theme="night", cam="push40", reveal=(0.35, 1, 0.2, 1.4),
         lights=[(760, 520, 520, "lamp", 0.3, "", "PV.clamp(lt / 1.8)")],
         texts=[("装没事", 250, 230, 44, "l", "ink", 1.6)]),

    dict(id="p16", title="一次回家送钥匙，让他看清这是长期消耗", asset="p16-keys.png", theme="night",
         cam="push40", reveal=(0.30, 1, 0.25, 1.6), grade="brightness: 0.94, saturate: 0.92",
         lights=[(960, 180, 560, "lamp", 0.5, "orange", "PV.clamp((lt - 0.3) / 1.6)")],
         texts=[("来回几小时", 250, 230, 44, "l", "ink", 1.5)]),

    dict(id="p17", title="大多数背叛的男人，不是在享受，而是在撕裂", asset="male-01-paper-fold.png",
         theme="day", cam="push55", reveal=(0.30, 1, 0.2, 1.5),
         lights=[(1900, 180, 700, "window", 0.6, "", "PV.clamp((lt - 0.5) / 2)")],
         texts=[("不是在享受", 250, 230, 44, "l", "ink", 1.4)]),

    dict(id="p18", title="一边要家庭，一边要刺激", asset="p18-two-doors.png", theme="day",
         cam="push40", reveal=(0.35, 1, 0.2, 1.4),
         lights=[(300, 640, 560, "lamp", 0.5, "orange", "PV.clamp((lt - 0.5) / 1.5)"),
                 (1620, 640, 560, "screen", 0.9, "blue", "PV.clamp((lt - 0.9) / 1.5)")],
         texts=[("家里", 260, 230, 40, "l", "orange", 1.6),
                ("外面", 1500, 230, 40, "l", "blue", 2.4)]),

    dict(id="p19", title="不是谁更爱谁，而是他在需求之间失控", asset="p18-two-doors.png", theme="day",
         cam="push55", reveal=(0.30, 1, 0.25, 1.5),
         lights=[(300, 640, 560, "lamp", 0.4, "orange", "PV.clamp(lt / 2)")],
         texts=[("不是谁更爱谁", 250, 230, 44, "l", "ink", 1.4)]),

    dict(id="p20", title="婚外关系更像一种短期的情绪麻醉", asset="p20-anesthesia.png", theme="day",
         cam="tight55", reveal=(0.35, 1, 0.3, 1.5),
         lights=[(960, 240, 700, "lamp", 0.5, "orange", "PV.clamp((lt - 0.5) / 1.5)")],
         texts=[("短期麻醉", 250, 230, 44, "l", "ink", 1.5)]),

    dict(id="p21", title="他可能最想回归，但回归不等于修复", asset="p21-flatten.png", theme="day",
         cam="push40", reveal=(0.35, 1, 0.25, 1.4),
         lights=[(960, 240, 780, "window", 0.5, "", "PV.clamp(lt / 2)")],
         texts=[("回归≠修复", 250, 230, 44, "l", "ink", 1.5)]),

    dict(id="p22", title="第一步不是向外补偿，而是先看清两个点", asset="p22-two-points.png",
         theme="day", cam="push55", reveal=(0.35, 1, 0.25, 1.4),
         lights=[(960, 300, 760, "window", 0.5, "", "PV.clamp(lt / 2)")],
         texts=[("先看清两点", 250, 230, 44, "l", "ink", 1.4)]),

    dict(id="p23", title="要问的是能不能面对关系里的真实代价", asset="p23-shreds.png", theme="day",
         cam="pull", reveal=(0.30, 1, 0.25, 1.5),
         lights=[(960, 250, 780, "window", 0.5, "", "PV.clamp(lt / 2)")],
         texts=[("别两边都要", 250, 230, 44, "l", "ink", 1.4)]),

    dict(id="p24", title="妻子这端最危险的，不是哭，而是只剩情绪", asset="p24-clench.png",
         theme="day", cam="push40", reveal=(0.35, 1, 0.25, 1.4),
         lights=[(1500, 500, 620, "screen", 0.6, "blue", "PV.clamp((lt - 0.6) / 1.6)")],
         texts=[("只剩情绪", 250, 230, 44, "l", "ink", 1.5)]),

    dict(id="p25", title="要不要继续，看对方有没有承担后果", asset="p25-ruler.png", theme="day",
         cam="push55", reveal=(0.35, 1, 0.25, 1.4),
         lights=[(620, 420, 560, "window", 0.6, "", "PV.clamp(lt / 2)")],
         texts=[("看承担后果", 250, 230, 44, "l", "ink", 1.4)]),

    dict(id="p26", title="真正的修复，是重新建立规则和边界", asset="p26-smooth-refold.png",
         theme="day", cam="push40", reveal=(0.35, 1, 0.25, 1.4),
         lights=[(960, 300, 780, "window", 0.5, "orange", "PV.clamp(lt / 2)")],
         texts=[("重建边界", 250, 230, 44, "l", "ink", 1.5)]),
]


def render(p):
    L = []
    L.append(f'/* {p["id"]} · {p["title"]}')
    L.append(" * 图：../scene-library/" + p["asset"] + "（处境图库，图不复制）")
    if p.get("lights"):
        L.append(" * 光：" + "、".join(f'{x[3]}' for x in p["lights"]) + "（光就是情绪）")
    if p.get("texts"):
        L.append(" * 屏上字：" + "、".join(t[0] for t in p["texts"]) + "（只做标签）")
    L.append(" */")
    L.append(f'ENGINE.visual(\'{p["id"]}\', (P) => {{')
    L.append(f'  STYLE.setTheme(\'{p["theme"]}\');')
    L.append('  const T = P.endT;')
    L.append('')
    o = ["at: 0"]
    if p.get("reveal"):
        f, t, a, d = p["reveal"]
        o.append(f'reveal: {{ from: {f}, to: {t}, at: {a}, dur: {d} }}')
    if p.get("cam"):
        L.append('  P.scene(\'../scene-library/' + p["asset"] + '\', {')
        for line in o:
            L.append('    ' + line + ',')
        L.append('    cam: ' + CAM[p["cam"]] + '.map(([t, z]) => ({ t, z })),')
        if p.get("grade"):
            L.append('    grade: { ' + p["grade"] + ' },')
        L.append('  });')
    L.append('')
    for i, (x, y, r, kind, at, color, k) in enumerate(p.get("lights") or [], 1):
        c = (f", color: '{color}'" if color else "")
        L.append(f'  P.light({x}, {y}, {r}, {{ at: {at}, kind: \'{kind}\'{c}, k: (lt) => {k} }});')
    for (txt, x, y, size, align, color, at) in p.get("texts") or []:
        L.append(f'  P.text({json.dumps(txt, ensure_ascii=False)}, '
                 f'{{ x: {x}, y: {y}, size: {size}, align: \'{align}\', color: \'{color}\', at: {at} }});')
    L.append('});')
    L.append('')
    return "\n".join(L)


def main():
    if "--check" in sys.argv:
        print(f'{"页":<5}{"主题":<7}{"机位":<8}{"灯":<4}{"字":<4}局面')
        for p in PAGES:
            print(f'{p["id"]:<5}{p["theme"]:<7}{p.get("cam", "-"):<8}'
                  f'{len(p.get("lights") or []):<4}{len(p.get("texts") or []):<4}{p["asset"]}')
        return
    OUT.mkdir(parents=True, exist_ok=True)
    for p in PAGES:
        (OUT / f'{p["id"]}.js').write_text(render(p), encoding="utf-8")
    print(f"生成 {len(PAGES)} 页 → {OUT.relative_to(ROOT)}")
    for p in PAGES:
        miss = [x for x in [p["asset"]] if not (ROOT / "projects" / "scene-library" / x).exists()]
        if miss:
            print(f'  ⚠ {p["id"]} 的图还没生成：{", ".join(miss)}')


if __name__ == "__main__":
    main()
