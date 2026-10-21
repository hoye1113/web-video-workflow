# 为什么越懂事的人，越容易被忽视 —— 讲给总在委

> 目标片长 **3 分钟** ≈ **582 字**（实测 194 字/分钟）。

照 `docs/新题材开工手册.md` 走：
1. 写词 `script-source.json`（cue ≤12 字、第 12 字前有标点）→ `tools/check_cues.py`
2. 出图 `tools/gen_scenes.py`（先翻 `projects/scene-library/` 有没有能复用的）
3. 排页 改本工程的 `page-spec.json` → `python tools/make_pages.py --project film-1021-1604`
4. 配音 `python tools/make_voice.py` → 字幕/渲染（见手册第 4 节）
5. 验收 `tools/qc_snap.py` + `tools/accept_emotion.py`
