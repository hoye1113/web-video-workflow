---
name: new-film
description: |
  Use when starting or revising a video-factory film: writing the spoken script
  (script-source.json), generating situation images in Flow with the 小树/小芽
  character chips (bsk + Chrome), building the page table (page-spec.json),
  voicing with edge-tts, or running the engine to render and check the film.
  Covers the length budget (194 chars/minute), cue rules (≤12 chars with
  punctuation), the character禁令, and the tools in tools/.
---

# new-film · 开一部新片（video-factory）

> 完整手册在仓库里：`docs/新题材开工手册.md`（开工五步）、`docs/经验与坑.md` 六十/六一/六二节（坑）。
> 这份 skill 是"最短可执行版"，动手前仍要读那两份。

## 0. 先定片长（别跳过）

```
台账字数 ≈ 194 字/分钟     6 分钟 ≈ 1200 字 · 8 分钟 ≈ 1550 字 · 10 分钟 ≈ 1900 字
```

## 1. 写台词（唯一的创作环节）

`projects/<片>/script-source.json`：每页一组 cue。

- 一条 cue **≤12 字**，且**第 12 个字之前必须有标点**（否则字幕会切开词）
- 一页 4–8 条 = 10–15 秒；骨架：钩子 → 案例 ×2-3 → 反直觉结论 → 拆解 → 行动
- 检查：`python tools/check_cues.py`（目标 **0 条硬切**）→ `python tools/make_script_js.py --from-source`

## 2. 出图（Flow，串行，一张约 60–100 秒）

```bash
python tools/measure_lib.py          # 先看图库有什么（能复用就别生成）
python tools/gen_worker.py <片名>    # 队列执行器：读 gen-queue.json → Flow → 落盘 → 量指标
python tools/gen_scenes.py 07 12     # 或按页批量（改 ITEMS 里的 scene 描述）
```

- 提示词只写处境；**角色不写进提示词**，用 `Add ingredients → Characters → 选角色 → Add to prompt` 挂 chip
- 三件事必须做：**读回核对提示词**、**指纹挡老图**（差 ≤2.5 判同一张）、**生成后量指标**（嫩芽像素 / 留白带 / 尺寸）
- 不对的图挪到 `experiments/rejects/`，改描述重画

## 3. 排页（改工程自己的页表）

`projects/<片>/page-spec.json` → `python tools/make_pages.py --project <片名>`

- 机位只四选：`push40` / `push55` / `pull` / `tight55`（都是"停-推-停"）
- 主题 `day`/`night`（夜景图必须 night，否则深色标签看不见）
- 屏上字只做标签；光要落在主体上（飘在空处会是一团圆圈）

## 4. 配音 → 字幕 → 渲染（机械活，照跑）

```bash
python tools/make_voice.py                     # → audio/*.wav + voice.js（约 10 分钟）
cd projects/<片> && node <engine>/tools/script.mjs && node <engine>/tools/render.mjs
python tools/accept_emotion.py && python tools/qc_snap.py     # 机器判据 + 抽帧表
```

## 5. 交付与验收

- 干净母版 mp4 + `字幕.srt` + `口播脚本.md`（时长/画幅/页数/字幕带四条自查）
- 三个审批点要人点头：**页→处境映射表** · **逐张的图** · **成片**
- 反悔的代价：改词要重配音+重渲；**改图只重渲那几页**（分段有缓存，别整片重来）

## 角色禁令（违背=白干）

| 角色 | 必须 |
|---|---|
| `小树`（男）| 灰蓝短发 `#728A96`、浅灰蓝开襟外套、白 T、**头顶嫩芽 `#DEF0A8`** |
| `小芽`（女）| 暖粉齐肩微卷发、米白连帽衫、**头顶嫩芽** |

不许换衣服、不许换发型、**不许摘嫩芽**；不许临时造脸。
