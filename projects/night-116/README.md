# 夜读 · 追问背后（night-trust-116）

用 `E:\音频素材\116.mp4` 的原音频做的 **米白 4:3 横屏**心理图解。

## 规格

| 项 | 值 |
|---|---|
| 画幅 | **4:3 / 1920×1440（1440p）/ 30fps** |
| 时长 | 03:26.0（26 页） |
| 音频 | 用户原声，未改语速；约 -16.1 LUFS |
| 风格 | `night-insight` 米白 4:3 变体 |
| 成片 | `out/night-116-43-无字幕.mp4` |
| 交付 | `E:\video-factory\night-116\` |

## 结构

1. 钩子：她反复追问，不是折磨你
2. 三个真相
3. 真相一：她是在自救
4. 真相二：切断再次犯错的退路
5. 真相三：判断这段婚姻值不值得
6. 收尾：满目疮痍之后，再重新出发

## 文件

| 文件 | 用途 |
|---|---|
| `script-source.json` | 音频切页后的 cue 源数据 |
| `script.js` / `voice.js` | 时间轴和原音频切片 |
| `night-spec.js` | 26 页内容 + 版式 |
| `build_spec.py` | 从内容表生成 `night-spec.js` |
| `covers/a.html` / `b.html` | 两张 3:4 米白封面 |
| `covers/render.mjs` | 渲染两张封面 |
| `out/` | 成片、字幕、封面 |

## 重建

```powershell
python projects/night-116/build_spec.py
cd projects/night-116
$env:VF_STAGE="1920x1440"
node engine/tools/render.mjs --skip-subs --fps 30 --workers 4 --name night-116-43
```

米白主题：`script.js` 里的 `META.cream = true`；样式在 `engine/styles/night-insight/` 的 `.ni-cream` 分支。
