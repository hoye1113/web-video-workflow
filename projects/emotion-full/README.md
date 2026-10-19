# emotion-full · 整片（26 页 · warm-emotion）

> 用 `warm-emotion` 风格包 + 处境图库，把原片（`projects/marriage_full`，349 秒）**整片重做**。
> 原片是**对比基线**，一行不改；这一部是**新做法**的成品。

## 现在到哪了

| 步 | 内容 | 状态 |
|---|---|---|
| 1 | 页 → 处境映射表（9 复用 + 12 新生成 + 5 代码画） | ✅ 已拍板（`docs/页-处境映射.md`） |
| 2 | 新生成 12 张处境图 | 🔄 10/12（p13 / p24 重跑中，见 `../scene-library/`） |
| 3 | 26 页场景代码 | ⬜ 未开始（模板：`../warm-emotion-3pages/pages/*.js`） |
| 4 | 配音 + 字幕 | ⬜ 台词已定稿（`script-source.json`），待跑 TTS |
| 5 | 整片渲染 + 逐页验收 | ⬜ |
| 6 | 剪辑人员手册 | ⬜ |

## 文件

| 文件 | 是什么 |
|---|---|
| `script-source.json` | **口播稿的唯一出处**（手写，每条 cue ≤18 字）。改文案改这里 |
| `script.js` | 引擎读的（由 `tools/make_script_js.py` 从上面生成，别手改） |
| `pages/pNN.js` | 逐页画面（照 `../warm-emotion-3pages/pages/p05.js` 写） |
| `assets/` | **不复制图**：页面里直接写 `../scene-library/xxx.png`（图库是唯一出处） |
| `out/` | 渲染产物（不入库） |

## 跑法（在 `experiments/frametell-src/frametell-main` 的 fork 里）

```bash
cd projects/emotion-full            # 注意：要能在 fork 里看到这个目录（junction 已挂）
node <engine>/tools/lint.mjs                                  # 语法/规范
node <engine>/tools/snap.mjs --sheet all 2 6 10 14 18 22      # 抽帧看画面
node <engine>/tools/script.mjs                                # 出口播脚本 + 字幕.srt
node <engine>/tools/render.mjs                                # 出 out/*.mp4
```

## 规矩（来自 `warm-emotion/GRAMMAR.md`，逐条核）

一页**一次有重量的动作**；**光就是情绪**；屏上字只做**标签**（≤8 字，≥36px）；
最下面 **18% 留空**（字幕带）；**不许**图表 / 箭头 / 圆圈 / 三卡；
角色只用 `小芽`（女）`小树`（男），**头顶嫩芽不许丢**。
