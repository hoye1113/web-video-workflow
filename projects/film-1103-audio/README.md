# 别等她攒够失望，才懂得珍惜

## 规格

| 项 | 值 |
|---|---|
| 套版 | **P1**（19 页全部 card） |
| 页数 | 19 页 |
| cue | 81 条 |
| 字数 | 606 字 |
| 音轨 | 用户原声（`E:\音频素材\1103.mp4`，1:58.47） |
| 成片 | **1:59.5 / 1920×1080 / 60fps** |
| 验收 | 母版 19/19、字幕版 19/19 |

## 文件

- 页表：`page-spec.json`
- 台词：`script-source.json`
- 逐字时间轴：`voice.js`
- 页 → 处境：`docs/页-处境映射.md`
- 图片：`../scene-library/f1103-p01.png` … `f1103-p19.png`
- 成片与交付：`E:\video-factory\1103\`

## 做法

1. 从 `E:\音频素材\1103.mp4` 提取音频，faster-whisper small 转写 → 修同音字
2. `tools/audio_film.py` 按约 31 字 / 6 秒分页，切原音频 → 19 页 / 81 cue
3. 逐页写处境；P1 全部 `card`；Flow 挂 `小树` / `小芽` chip 生成 19 张图
4. `make_pages` → `script.mjs`（字幕）→ `render.mjs --workers 3` → 验收
