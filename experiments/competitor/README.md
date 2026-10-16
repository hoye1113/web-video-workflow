# 竞品拆解 · FRAMETELL

样片：`E:\ceba897123e33e8c487add3945641ac9_raw.mp4`
规格：1656×1080 / 60fps / 82 秒 / 无音轨 / 82 秒里 **0 个切点**（连续画面，不是镜头拼接）

> 注：这是**屏幕录制**，录的是 FRAMETELL 这个桌面应用的完整使用过程，不是它产出的视频本身。
> 它产出的那条 77 秒视频作为示范嵌在应用里反复播放，所以录屏本身没有切点。

## 一、它是什么

输入一句话或一份材料 → 输出带旁白字幕的解说视频。
样片："Why is the sky blue and sunsets red"，77 秒，5 页。

自述（新建页顶部原文）：

> Say what you want to explain, or attach your material. **The director agent drafts a storyboard for your sign-off**, then writes the narration, voices it, draws every page and **checks its own work**. You get a 1080p video with subtitles.

## 二、新建页：六个控件，全是"选"不是"填"

| 控件 | 形式 | 细节 |
|---|---|---|
| 一句话 | 输入框 | "Say what you want to explain" |
| 附件（可选） | 拖拽 / 选择 | PDF、Word、PowerPoint、EPUB、Markdown、图片 |
| 时长 | **四个档位** | [1 min] [2 min] [5 min] [10 min]，不是精确数字 |
| 声音 | 带试听的预设 | "Bella - Professional, Bright, Warm"，可切性别、可试听 |
| 语言 | 两个档 | [中文] [English] |
| **风格** | **五个命名预设** | 见下 |
| 模型 | 默认选好，可换 | 接用户自己的中转 API（"via your relay api.sub2tok.com"） |

底部：`⏎ to start` + `Start →`，下面接 "Recent videos" 列表。

### 风格那五个预设（最值得抄的一行）

```
Warm storybook ｜ Quiet study ｜ Whiteboard ｜ Chalkboard ｜ Tech dark
```

每个带色板缩略图，选中后下面出一句人话：

> **Warm storybook**：Warm flat illustration with one metaphor carried through the whole film.
> Good for investing, everyday life and psychology.

**用户不需要懂"扁平矢量线稿"这种术语。**

## 三、工作区：内置叙事骨架（最重要的发现）

页面标题是固定修辞骨架，不是自由发挥：

```
1  Hook: same sun, two different skies
2  Intuition: sunlight is …
3  Mechanism: tiny air molecules bounce blue around
4  Numbers: shorter wave, much stronger scattering
5  Sunset: a longer trip through air leaves only red
```

**钩子 → 直觉 → 机制 → 数字 → 结论**

- 每页 = **一个完整的小论点 + 一段完整的话**，不是按秒切
- 页标题就是论点；页正文是旁白原文（一段 4-5 句的完整论述）
- 例：Mechanism 那页的旁白是 "Air is mostly nitrogen and oxygen molecules, far smaller than a light wave. They scatter short waves like blue much more than long waves like red. So blue light bounces all over the sky…"

工作区布局：

- 左：页面列表（标题 + 旁白 + 状态 + 单页"Play voice"试听）
- 右：live preview（当前页动画在跑）+ 五个页面缩略图 + 每页旁白
- 底：对话框 —— "What would you like to change? You can add pages, lines and frames from the right"
- 顶部：项目名 + 完成后显示 "Done"

## 四、普通人友好的三个机制

1. **先出分镜给你签字**："drafts a storyboard for **your sign-off**"
2. **用大白话给意见**：输入框提示 *"give the director a note, like 'slow the pace a little'"*
3. **进度和成本实时可见**："About 9 min left · $0.13"、"✓ Approved"、"Writing the narration…"
   - 完成后："**Your video is ready** / 77s · made in 12m 52s · cost $1.59"
   - 还有一句："Only the pages you change are redrawn, and you can watch the result right away."

## 五、它的画面长什么样

每页一个 flat 插画风的代码绘制动画，暖色扁平（米色底 / 陶土橙 / 深青 / 奶油黄）：

- Page 3「Mechanism」：一片点阵（空气分子）里蓝色小球四散弹跳
- Page 4「Numbers」：一条正弦波 + 标签"Blue ~450 nm"
- Page 5「Sunset」：大气层楔形 + 红球直线穿过 + 蓝球被打散 + 两个标签依次出现

**画风高度统一**（一套色板到底），**画面信息密度克制**（一页就一两个元素 + 一两个标签）。

## 六、对我们的三条直接改动

| # | 改动 | 理由 |
|---|---|---|
| 1 | 切页改成**按叙事骨架切**，一页一个论点 | 普通人不会分镜，骨架替他决定结构。我们自由发挥时切出的是 35 个平均 6 秒、节奏全平的镜头 |
| 2 | 风格收成 **5-8 个命名预设**，每个带色板 + 一句人话 | 我们有 43 个选项（35 风格 + 8 语法），对普通人是灾难 |
| 3 | 一页 = **一个知识点**，不是一段时间 | 15 秒一页的底气来自"这页有一个完整论点" |

## 七、画面对不上的地方（它没有而我们有的）

- 它有内置 TTS，我们的声音在 V2（但转写工具已经通了）
- 它的画风固定，我们能用 35 种艺术风格和 8 种解说语法
- 它的"页"是静态构图 + 元素依次出现；我们的 engine 能做真正的逐帧动画（落沙、形变）
