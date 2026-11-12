# noir-intro · 4 章风格样片

用 `noir-editorial` 风格包做的 17.7 秒 proof：深色电影感排版、章节 HUD、细线稿图示。

| 项 | 值 |
|---|---|
| 成片 | `out/noir-intro-无字幕.mp4`（1920×1080 / 30fps / 17.7s） |
| 720p 测试 | `out/noir-intro-720p.mp4` |
| 风格包 | `experiments/frametell-src/frametell-main/packages/engine/styles/noir-editorial/` |
| 页面 | `pages/p01.js` … `p04.js` |
| 配音 | 占位：edge-tts `zh-CN-YunjianNeural`，+8% |
| 字幕 | `out/字幕.srt`（本片母版不烧字幕） |

## 跑法（在工程目录）

```powershell
node engine/tools/snap.mjs 2.2 7.3 12.3 17.6
node engine/tools/render.mjs --fps 30 --workers 4 --skip-subs --name noir-intro
```

## 换用户音频（时长跟音频走）

`voice.js` 是唯一时间轴：每条 cue 的 `f/d/o/k` 来自音频切段。把用户音频按 cue 切成
`audio/pNN-i.wav`，重写 `voice.js`（或用 `tools/audio_film.py` 的切音频思路），页面时长就会自动
变成音频长度，不套固定 17.7 秒。文案和 cue 顺序必须与音频一致。

> `node engine/tools/lint.mjs` 会对本片报「字幕带 / 小字」警告：这是风格选择——
> HUD 微标签就是 11–18px，画面内旁白本来就压在最下面。母版不烧字幕；
> 如果要烧字幕，把 `noirNarration` 上移到 y<860，或改用引擎的 `.subs` 层。

## 还没有做的

- BGM / whoosh / 低频音效（参考片的声音设计占很大比重）。
- 商用宋体（当前用系统 SimSun 做 proof；交付前换有授权的宋体）。
- 用户音频进来后的章节映射（哪些句子放哪一页、用哪种页面原型）。
