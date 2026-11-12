# 夜读 · 信任重建（night-trust-1112）

用 `E:\音频素材\1112.mp4` 的原音频做的横屏深色心理图解。

## 规格

| 项 | 值 |
|---|---|
| 画幅 | 1920×1080 / 30fps |
| 时长 | 06:18.2（49 页） |
| 音频 | 用户原声，未改语速、未补静音；约 -16.3 LUFS / -1.3 dBTP |
| 风格 | `night-insight`（独立套版，不和 warm-emotion / noir-editorial 冲突） |
| 成片 | `out/night-1112-无字幕.mp4` |
| 交付 | `E:\video-factory\night-1112\`（mp4 + 字幕.srt + 口播脚本.md + night-spec.js） |

## 结构

- 01 钩子：原谅了，却放不下
- 02 信任崩塌：失去信任 = 失去确定性
- 03 内耗：事件 → 解读 → 情绪 → 行为
- 04 追问：要的不是道歉，是安全感
- 05 原则：谁破坏，谁修复
- 06 过错方：认错、耐心、透明、共同活动
- 07 受伤方：看见改变、别报复、别把自己困死
- 08 警觉：适度警觉，不是草木皆兵
- 09 敏感伴侣：透明、肯定、给底气
- 10 信任：像空气，也像地基
- 11 收尾：危机也是重塑的契机，劝和不劝离

## 文件

| 文件 | 用途 |
|---|---|
| `script-source.json` | 音频切页后的 cue 源数据 |
| `script.js` | 页 / cue 时间轴（由 `audio_film.py` 生成） |
| `voice.js` | 每页/每条 cue 的原音频切片 |
| `pages/p01.js` … `p49.js` | 一页一行，调用 `NIGHT.render` |
| `night-spec.js` | 49 页的内容 + 版式（主要改这个） |
| `build_spec.py` | 从内容表生成 `night-spec.js` |
| `out/` | 成片、字幕、口播脚本、抽帧 |

## 重建

```powershell
# 改完页面内容后
python projects/night-1112/build_spec.py

cd projects/night-1112
node engine/tools/render.mjs --skip-subs --fps 30 --workers 4
```

## 说明

- 音频不改：成片音轨就是原音频的连续切片；ASR 的错字只影响转写，不影响声音。
- 屏上字是按内容重写的短句，不是逐字字幕；完整字幕在 `out/字幕.srt`。
- 没有额外加 BGM；如果原音频没有 BGM，成片就是纯口播。
- `check.mjs` 的 sparse/empty 是 SVG 口径，这套 HTML 组件会误报；验收以抽帧和人眼审片为准。
