# 认错改错没用，对方爱你才有用

> 用户原声：`C:\Users\QWQ\Desktop\彬\1031.mp4`（4:50 / 290 秒）。
> 成片走 **P2 70/30 套版**：32 页处境铺满 + 14 页情绪特写。

## 规格

| 项 | 值 |
|---|---|
| 页数 | 46 页 |
| cue | 156 条 |
| 字数 | 1431 字 |
| 音轨 | 用户原声（切段，不合成） |
| 画幅 | 1920×1080 / 60fps |
| 成片 | 约 4:51 |
| 套版 | P2：full 32 / close 14（约 30% 特写） |

## 文件

- 页 → 处境映射：`docs/页-处境映射.md`
- 页表：`page-spec.json`
- 台词：`script-source.json`
- 逐字时间轴：`voice.js`
- 字幕 / 口播稿：`out/字幕.srt` / `out/口播脚本.md`
- 成片：`out/1031-无字幕.mp4` / `out/1031-有字幕.mp4`

最终交付会复制到：

```
D:\video-factory\1031\out\
```

## 做法

1. 音频转写（faster-whisper small，本地模型）→ 修同音字
2. `tools/audio_film.py` 按 ~33 字 / 6.2 秒分页，切原音频
3. 逐页写处境；`tools/decide_layout.py` 按 P2 判定；人工校准到 32 full / 14 close
4. Playwright 驱动 Flow（`tools/flow_batch.mjs`）批量生图，角色用 `小树` / `小芽` chip
5. `make_pages` → `script.mjs`（字幕）→ `render.mjs --workers 3` → 验收
