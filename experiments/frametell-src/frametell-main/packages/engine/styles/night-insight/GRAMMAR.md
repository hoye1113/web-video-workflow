# Night insight · grammar card

> 深色心理图解。不是插画，也不是口播背景：画面本身就是内容。
> 独立于 `warm-emotion` / `tech-dark`，项目用 `META.style = 'night-insight'` 拉进来。

## In one sentence

一块近黑的屏幕，用青色的“正确/冷静”和橙色的“情绪/重点”，把一段关系里的机制拆成聊天框、卡片、墙体、人物圆点和一句话。

## Picture

- **Ground**: `#07090C`，中心微微提亮，64px 网格，四周压暗。
- **Palette**: 青 `#35E0D0` 是主色（正确/冷静/主线）；橙 `#FFA23A` 是强调（情绪/重点）；红 `#FF5A6A` 只给“错误/雷区”。
- **Type**: 粗黑体。大标题 76–104px，正文 32–44px，单行 ≤14 字。屏上字是标题和结论，不写完整口播。
- **Components**: `phone` / `bubble` / `card` / `wall` / `avatar` / `heart` / `ring` / `quote` / `choice` / `switch` / `end`.
- **Space**: 四边 120px 安全区；底部 180px 留给 caption 和平台 UI；主图不压字幕带。
- **Chrome**: 左上角 `01 钩子` 章节号，右上角留空或放系列名；不要抢主标题。

## Layouts (`kit.js` → `NIGHT.render`)

`hook` · `split` · `translate` · `wall` · `heart` · `choice` · `list` · `end`

每页只选一个；字段见 `projects/night-insight-template/night-spec.js`。

## Motion

- **Hard cut between pages.** 不要整页淡入淡出；用页面切换本身当节拍。
- 页内元素 0.3–0.6 秒淡入 + 上浮 20–30px；卡片可带 0.96→1 的轻微缩放。
- 一页最多 3 个入场事件；聊天框逐条弹出，每条间隔 0.4–0.6 秒。
- 线条/箭头从左向右生长 0.4–0.5 秒；不做粒子、发光爆炸、3D 翻转。

## Pacing

- 30 秒 6–8 页；60 秒 12–16 页；3–4 分钟 24–32 页。
- 一页一个观点；每页至少一个“画面变化”，不要连续两页同一构图。
- 音频优先：页面切换点落在句号/问号/停顿处，不切在句子中间。

## Never

- 不用实拍、AI 插画、人物正脸；人物只用无名圆点。
- 不把整段口播铺满屏；屏上只留标题、关键词、一句结论。
- 不在同一屏用第三种强调色；红色只表示错误。
- 不照抄对标账号的文案、分镜和配色比例；结构可以学，内容必须原创。
