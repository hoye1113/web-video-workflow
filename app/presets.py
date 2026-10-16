"""风格预设：给普通人看的"选一个"，不是让他写画风描述。

一条预设 = 名字 + 一句人话 + 画风一句话 + 一套色板。色板全部来自上游的
references/色板.md（8 套现成的），不另造色，免得踩蓝紫禁区。

选中之后写进项目的是 look / palette / character 三个字段 —— 场景代码由模型按
这三个字段现写，不需要有现成的模板画面。
"""

# 上游色板：6 个键 + 适合什么
PALETTES = {
    "paper":   {"适合": "人文、历史、读书、解释一个道理",
                "bg": "#F3EDE2", "surface": "#FBF8F2", "ink": "#1B1A17", "sub": "#6B655B", "accent": "#C8402F", "accent2": "#2F5D62"},
    "poster":  {"适合": "观点、冲突、要一句话砸进去的科普",
                "bg": "#FFD23F", "surface": "#FFF6D6", "ink": "#111111", "sub": "#4A4433", "accent": "#FF5A36", "accent2": "#14213D"},
    "ink":     {"适合": "科技、夜景、严肃话题",
                "bg": "#121417", "surface": "#1E2226", "ink": "#F2EFE8", "sub": "#A39E93", "accent": "#F2B33D", "accent2": "#5FB3A1"},
    "navy":    {"适合": "产品、数据、手机与电子设备（平涂，不渐变）",
                "bg": "#0D1B2A", "surface": "#16293D", "ink": "#EEF3F6", "sub": "#8FA3B3", "accent": "#5CC8E0", "accent2": "#F2A93B"},
    "bauhaus": {"适合": "设计、结构、几何、流程",
                "bg": "#EFE9DD", "surface": "#FFFFFF", "ink": "#111111", "sub": "#555555", "accent": "#D62828", "accent2": "#1D4E89"},
    "snow":    {"适合": "冬天、医疗、清洁、实验室",
                "bg": "#E9EEF0", "surface": "#FFFFFF", "ink": "#1F2A30", "sub": "#5E6B72", "accent": "#D9482B", "accent2": "#3E7C8C"},
    "wood":    {"适合": "生活、厨房、手作、家里的事",
                "bg": "#EDE3D1", "surface": "#F7F1E6", "ink": "#2B2622", "sub": "#7A6E62", "accent": "#C4552D", "accent2": "#3F5B4B"},
    "chalk":   {"适合": "课堂、推导、公式、讲题",
                "bg": "#23302B", "surface": "#2E3D37", "ink": "#F1EFE6", "sub": "#A9B3AA", "accent": "#F4D35E", "accent2": "#E87D5A"},
}


def palette_list(pid):
    p = PALETTES[pid]
    return [p["bg"], p["surface"], p["ink"], p["sub"], p["accent"], p["accent2"]]


# 六个预设。名字要人能看懂，说明要像人说话，不要术语。
PRESETS = [
    {
        "id": "paper",
        "name": "暖色纸本",
        "hint": "像一本旧书里的插画。适合讲道理、讲人情、讲一段经历。",
        "look": "暖色纸本插画：平涂加细铅笔线，留白多，全片只用一支笔的笔触，不描粗边不发光",
        "palette": "paper",
        "character": "只出手和背影，不画脸",
    },
    {
        "id": "wood",
        "name": "居家暖木",
        "hint": "像下午的客厅。适合家庭、婚姻、日常生活里的那些事。",
        "look": "暖木色平面插画：圆角块面加细线，一束室内光斜切进来，物体有干净的接触阴影",
        "palette": "wood",
        "character": "只出手和背影，不画脸",
    },
    {
        "id": "ink_night",
        "name": "夜灯深墨",
        "hint": "像深夜只开了一盏灯。适合失眠、压力、说不出口的事。",
        "look": "深色底加单一暖光源：硬边平涂，阴影干净，亮部只有一处，其余压暗",
        "palette": "ink",
        "character": "只出手和背影，不画脸",
    },
    {
        "id": "chalk",
        "name": "白板讲题",
        "hint": "像老师在黑板上一句一句讲。适合把一件事拆开讲清楚。",
        "look": "深绿黑板加粉笔线条：手写感，边讲边画，线条允许轻微抖动",
        "palette": "chalk",
        "character": "无人物，用粉笔画的图形和标注",
    },
    {
        "id": "poster",
        "name": "高对比海报",
        "hint": "像一张出版海报。适合观点、冲突、要一句话砸进脑子里的内容。",
        "look": "高对比平涂：大色块、粗黑轮廓、一个画面只有一个焦点，不放细节",
        "palette": "poster",
        "character": "只出手和背影，不画脸",
    },
    {
        "id": "diagram",
        "name": "干净几何",
        "hint": "像一份干净的说明书。适合步骤、流程、结构性的内容。",
        "look": "浅底纯平涂加细黑线框：圆、方、三角的构成，标注用短线引出",
        "palette": "bauhaus",
        "character": "无人物，用图形和标签",
    },
]

BY_ID = {p["id"]: p for p in PRESETS}


def expand(style):
    """把 {preset: 'paper'} 展开成 {preset, look, palette[6], character, name, hint}。"""
    if not style:
        return style
    pid = style.get("preset")
    p = BY_ID.get(pid)
    if not p:
        return style
    out = dict(style)
    out["name"] = p["name"]
    out["hint"] = p["hint"]
    out["look"] = p["look"]
    out["character"] = p["character"]
    out["paletteId"] = p["palette"]
    out["palette"] = palette_list(p["palette"])
    return out


def listing():
    """给界面的列表：带色板缩略图用的三色。"""
    out = []
    for p in PRESETS:
        cols = palette_list(p["palette"])
        out.append({
            "id": p["id"], "name": p["name"], "hint": p["hint"],
            "swatch": [cols[0], cols[4], cols[5]],      # 底 / 主强调 / 副强调
        })
    return out
