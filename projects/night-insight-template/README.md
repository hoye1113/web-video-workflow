# Night insight · 独立模板

深色心理图解套版。**和 `warm-emotion` / `tech-dark` 完全分开**：样式在
`engine/styles/night-insight/`，项目用 `META.style = 'night-insight'` 拉进来。

这个目录既是 30 秒 demo，也是以后开新片的模板。

## 目录

| 文件 | 作用 |
|---|---|
| `index.html` | 入口，先加载 `night-spec.js`、`script.js`，再启动引擎 |
| `night-spec.js` | **页面内容 + 版式**（主要改这个） |
| `script.js` | 时间轴：页 / cue / 音频配置 |
| `pages/p01.js` … `p07.js` | 一行调用 `NIGHT.render`，不用改 |
| `engine/` `engine_modules/` | 指向引擎的 junction（不入库） |
| `out/` | 渲染产物（不入库） |

## 版式

`night-spec.js` 里每页写一个 `layout`：

- `hook`：手机聊天 + 大标题 + 心形
- `split`：左右两卡 + 中间墙
- `translate`：一句话 → 另一种翻译
- `wall`：两个人物圆点 + 中间墙
- `heart`：心形 + 保护环 + 话术
- `choice`：两个选择卡 + 开关 + 问题
- `end`：结尾标题 + 两人靠近

字段示例见 `night-spec.js`。

## 跑起来

```powershell
# 预览（Chrome 打开，自动播放）
start projects/night-insight-template/index.html

# 或双击 preview.cmd / render.cmd

# 渲染无字幕母版（30fps，和参考片一致）
cd projects/night-insight-template
node engine/tools/render.mjs --skip-subs --fps 30
```

## 接自己的音频

```powershell
# 1. 开一个独立工程（从本模板复制）
python tools/new_night_film.py night-insight-新片 --title "新片标题"

# 2. 转写 + 按音频切页（自动写 script.js / voice.js / night-spec.js / pages）
python tools/transcribe.py 你的音频.mp4 --model small --lang zh
python tools/audio_film.py night-insight-新片 你的音频.transcript.json 你的音频.mp4 --style night-insight

# 3. 按新 cue 把 night-spec.js 的 layout 从 list 改成 hook / split / ...
# 4. 渲染
cd projects/night-insight-新片
node engine/tools/render.mjs --skip-subs
```

`audio_film.py --style night-insight` 是音频优先：它不合成、不加速，只按原音频切段；
时间轴就是你的原音频。它先给一版可跑的 `list` 页，之后按内容换成正式版式。

## BGM / 音效

引擎支持页面级 `sfx`。在 `script.js` 的页面对象里加：

```js
sfx: [{ f: 'audio/bgm.mp3', at: 0, until: 'end', loop: true, vol: -18 }]
```

`audio/bgm.mp3` 用可商用素材；转场音效可以再加一条短 `sfx`。没有 BGM 时成片就是纯口播/静音。

## 纪律

- 不照抄对标账号的文案和分镜；结构和版式可以复用，内容必须原创。
- 一页一个观点；屏上字不写完整口播。
- 红色只给错误/雷区；一屏最多两种强调色。
