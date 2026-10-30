# 最后一块糖 · 14.7 秒样片（P2 70/30 混合套版）

> 这是为了验证整条链路临时跑的一条短样片：**4 页 / 70 字 / 14.7 秒 / 1920×1080 / 60fps**。
> 不是正式长片，但走的是和正片完全相同的流程：写词 → Flow 生图（小芽 chip）→ 配音 → 字幕 → 渲染 → 验收。
> 这一版是 **P2**：p01–p03 处境页全铺满 + 房间背景；p04 情绪落点保留干净纸面特写。
> 底部 18% 用纸色渐变压成字幕带。P1 原版仍可在工作台“套版”里切换。

## 文案

```
她总把最后一块糖，留到化了才吃。
她笑着说，好东西要留到最后，才不算浪费。
后来她才知道，有些甜，等不了那么久。
直到那天，她把糖放进嘴里，笑了。
```

## 看片

- 有字幕版：`out/demo-candy-1029-有字幕.mp4`
- 无字幕母版：`out/demo-candy-1029-无字幕.mp4`
- 字幕：`out/字幕.srt`
- 口播稿：`out/口播脚本.md`
- 四页图（P2）：`out/contact-sheet-p2.jpg`
- 四页图（全铺满参考）：`out/contact-sheet-v2.jpg`
- 铺满前后对比：`out/p01-before-after.jpg`
- 网页预览：`review.html`

## 四页

| 页 | 套版 | 画面 | 主题 |
|---|---|---|---|
| p01 | **full** | 女孩坐在靠窗木桌前，矮柜、书架、相框、窗帘、绿植、糖纸和铁盒 | day |
| p02 | **full** | 女孩把旧铁盒推到桌边，背景是书架、矮柜、绿植和窗 | day |
| p03 | **full** | 女孩站在窗边，看着手心里化开的糖纸，夜色 + 窗帘、矮柜、绿植 | night |
| p04 | **close** | 女孩把糖放进嘴里，闭眼笑，干净纸面 + 一束柔光 | day |

## 体检

- 生图 4/4，0 失败；4 张都由 Flow 挂 `小芽` chip 生成，提示词里没有写角色名。
- 台词 11 条 cue，0 条硬切。
- 成片 14.7s，H.264 1920×1080 60fps + AAC 48kHz 单声道，音轨不是静音。
- **无字幕母版：4/4 页通过**（底部 18% 是纸色字幕带，不再是留白/杂物）。
- **有字幕版：4/4 页通过**。
- 风格包新增：`warm-emotion/style.css` 的 `#frame::after` 字幕带渐变。

## 跑法

```powershell
python tools/check_cues.py demo-candy-1029
python tools/make_script_js.py demo-candy-1029 --from-source
python tools/make_voice.py demo-candy-1029
python tools/gen_worker.py demo-candy-1029          # 在 Flow 里挂小芽 chip 出 4 张图
python tools/make_pages.py --project demo-candy-1029
cd projects/demo-candy-1029
node <engine>/packages/engine/tools/script.mjs
node <engine>/packages/engine/tools/render.mjs --workers 2
python tools/qc_snap.py demo-candy-1029
python tools/accept_emotion.py demo-candy-1029 --subs
```
