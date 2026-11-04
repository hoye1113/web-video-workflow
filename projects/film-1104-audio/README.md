# 夫妻闹到哪一步，就没必要在一起了

## 规格

| 项 | 值 |
|---|---|
| 套版 | **P1**（35 页全部 card） |
| 页数 | 35 页 |
| cue | 143 条 |
| 字数 | 1314 字 |
| 音轨 | 用户原声（`E:\音频素材\1104.mp4`，3:32.79） |
| 成片 | **3:33.8 / 1920×1080 / 60fps** |
| 验收 | 母版 35/35、字幕版 35/35 |

## 文件

- 页表：`page-spec.json`
- 台词：`script-source.json`
- 逐字时间轴：`voice.js`
- 页 → 处境：`docs/页-处境映射.md`
- 图片：`../scene-library/f1104-p01.png` … `f1104-p35.png`
- 成片与交付：`E:\video-factory\1104\`

## 做法

1. 从 `E:\音频素材\1104.mp4` 提取音频，faster-whisper small 转写 → 修同音字
2. `tools/audio_film.py` 按约 37 字 / 6 秒分页，切原音频 → 35 页 / 143 cue
3. 逐页写处境；P1 全部 `card`；Flow 挂 `小树` / `小芽` chip 生成 35 张图
4. `make_pages` → `script.mjs`（字幕）→ `render.mjs --workers 3` → 验收
