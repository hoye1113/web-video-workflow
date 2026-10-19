# video-factory

给内部剪辑人员用的**本地视频生产工作流**：把一段口播文案，变成 3–10 分钟的横屏 1080p 解说片
（**情绪/婚姻题材**为主），产出**干净母版 mp4 + 字幕.srt + 口播脚本.md**，交给剪辑在剪辑软件里包装。

> **路线**：以 [FRAMETELL](https://github.com/sitor-ai/frametell) 的**引擎**为骨架（页 DSL / 时间轴 / 渲染 / 字幕 / 混音），
> 我们的差异以一等公民装进去：**Flow 生成的"处境图" · 两个角色 IP（小树/小芽）· 暖纸本情感风格包 · 免密钥配音（edge-tts）**。
> 素材阶段（生图/挑图）交给一个**会开浏览器的 agent**（OpenCode + bsk），出片阶段是**确定性脚本**，两头用**文件**交接。

---

## 一、交接：现在到哪了（2026-10-19 收工）

### 已经跑通、实测过的

| 东西 | 在哪 | 状态 |
|---|---|---|
| **第一部整片**（26 页 / 9:52 / 1080p）| `projects/emotion-full/out/emotion-full-{无字幕,有字幕}.mp4` | ✅ 已出片（未入库，`out/` 本地生成）|
| 台词（手写，26 页 184 条 cue）| `projects/emotion-full/script-source.json` | ✅ 字幕 0 条硬切 |
| 配音（edge-tts，逐字时间戳）| `projects/emotion-full/audio/*.wav` + `voice.js` | ✅ 语音 9.6 分钟 |
| 处境图库（37 张，含一致性指标）| `projects/scene-library/` + `index.json` | ✅ 小树 26 / 小芽 11；2 张有标记（p02 留白带、p23 留白带）|
| 角色 IP | Flow 项目里 `小树`/`小芽` + `projects/character-assets/character-cards.md` | ✅ 形象锁住（嫩芽 `#DEF0A8` 是最强识别符）|
| **面板**（人在网页上生成）| `python tools/panel/server.py` → `127.0.0.1:8899` | ✅ P1 完成：首页/工作台/素材库 + 审批 + 自动推进 |
| 生图执行器（队列→Flow→落盘）| `tools/gen_worker.py` | ✅ 串行、失败不连坐、断点续跑 |
| **material agent**（素材阶段）| `tools/opencode/agents/material.md` + `skills/new-film/` | ✅ 已装进本机 OpenCode，实测能读手册回答、待它跑图 |
| 剪辑人员手册 | `docs/剪辑操作手册.md` | ✅ 初版 |

### 还没做完的（下一步就接这儿）

1. **P1.5 收尾**：agent 的**权限卡**（面板上"允许一次/总是允许/拒绝"已画好，还没在真实生图里验过）；
   让 agent 真跑一次完整生图（`gen_worker` 走队列）。
2. **P2 改片闭环**：引用（把某一页/某一句/某一帧"加到对话"）、**只重做受影响的页**（图换了只重渲那几页）、排队与暂停。
3. **P3**：加角色的流程（上传定妆图 → bsk 走 Flow 建 Character → 自动量色板）、素材库搜索/标签、一句话开工。
4. 第一部片子的**用户验收**：与旧片并排过 5 条判据（认得出角色 / 不违和 / 有处境感 / 无图表味 / 愿意发）。

---

## 二、怎么跑起来

### 0) 环境（新机器一次性）

```powershell
# git / node ≥22 / pnpm / Python 3.12 / ffmpeg / Chrome（登录 Flow 的那个 Profile 装 bsk 扩展）
cd experiments/frametell-src/frametell-main
pnpm install --filter "frametell..." ; pnpm --filter "frametell..." build   # 不装 Electron 壳
uv venv ~/.frametell/edge-venv ; uv pip install --python ~/.frametell/edge-venv/Scripts/python.exe edge-tts
# 模型：写 ~/.frametell/config.json（OpenAI 兼容；本机走 OpenCode Go 的端点，见 docs/方案.md §7）
# 浏览器自动化：bsk daemon + Chrome 扩展（扩展要装在**登录 Flow 的那个 Profile**）
```

### 1) 面板（人和片子打交道的地方）

```powershell
python tools/panel/server.py            # → http://127.0.0.1:8899
```

- **首页**：写一句话 → 定片长/配音/角色 → 「开始制作」（建工程、挂引擎、给骨架）
- **工作台**：左"对话/过程"、右"画面"；**流程自动往下走**，人只做三件事：**说**（消息框 → material agent）、
  **点头**（三张审批卡：页→处境映射表 / 逐张的图 / 成片）、**看**（成片、逐页、抽帧表）
- **素材库**：37 张按角色分组，带一致性指标与"用在哪几页"；可「指定给页」（改页表并重生成该页代码）
- **环境自检**在右上角（bsk daemon / 扩展 / edge-tts / ffmpeg / 引擎；「深检」会开浏览器验 Flow 项目与角色）

### 2) 素材阶段交给 agent（P1.5）

```powershell
python tools/opencode/install.py        # 把 agent 与 skill 装进 ~/.config/opencode/
# 装完 OpenCode 里会有 agent `material` 与 skill `new-film`；面板消息框发的每句话都交给它
```

### 3) 出片（引擎，机械活）

```powershell
cd projects/emotion-full
node <engine>/tools/script.mjs          # → out/口播脚本.md + out/字幕.srt
node <engine>/tools/render.mjs          # → out/*.mp4（分段并行，约 20 分钟）
python tools/accept_emotion.py          # 机器判据：黑页/空页/字幕带
python tools/qc_snap.py                 # 逐页抽帧对照表（看图用）
```

---

## 三、文档地图（**读哪份做什么**）

| 你想 | 读这份 |
|---|---|
| **开工一条新片**（换题材） | `docs/新题材开工手册.md` —— 五步：定片长 → 写词 → 出图 → 排页 → 出片验收；**片长换算 194 字/分钟** |
| **踩过的坑**（最值钱） | `docs/经验与坑.md` —— 六十（Flow 取图四坑）/ 六一（工程挂载·字幕·voice.js 契约）/ 六二（片长是**先定的**） |
| **界面该怎么长** | `docs/面板优化方案.md` —— 照 frametell 的交互（首页/工作台/审批/素材库）+ 第七节实施进度 |
| **架构分工**（谁干什么） | `docs/harness-架构建议.md` —— 素材交给 agent、出片交给引擎；依据 OpenMontage / MoneyPrinterTurbo / frametell 三个先例 |
| **总方案与决策记录** | `docs/方案.md`（v2.1） |
| **当前待办** | `docs/待办.md` |
| **剪辑人员怎么用** | `docs/剪辑操作手册.md` |
| **角色资产** | `projects/character-assets/character-cards.md`（实测色板、禁令） |
| **页 → 处境映射（第一部）** | `projects/emotion-full/docs/页-处境映射.md` |
| **FRAMETELL 怎么做到稳定好看** | `docs/FRAMETELL拆解.md`；fork 的改动清单在 `experiments/frametell-src/frametell-main/OURS.md` |

**历史文档（已被取代，只作留档）**：`docs/P2-待拍板.md`、`docs/P3-P4-方案.md`、`PRD-video-factory.md`。

---

## 四、目录地图

| 路径 | 是什么 |
|---|---|
| `projects/emotion-full/` | **第一部整片**（26 页）：`script-source.json`（台词唯一出处）· `page-spec.json`（页表）· `pages/`（逐页代码）· `out/`（成片，未入库）|
| `projects/scene-library/` | **处境图库**（37 张）+ `index.json`（面板读它渲染素材库）|
| `projects/character-assets/` | 角色卡与定妆图锚点 |
| `projects/marriage_full/` | **旧片**（349 秒）：对比基线，**一行不改** |
| `tools/` | `panel/`（面板）· `gen_worker.py`（生图执行器）· `conductor.py`（自动推进）· `pipeline.py`（队列/事件/审批/自检）· `agent_bridge.py`（面板↔agent）· `gen_scenes.py`/`make_voice.py`/`make_pages.py`/`lib_index.py`/`qc_snap.py`/`accept_emotion.py` |
| `tools/opencode/` | agent 与 skill 的**源**（用 `install.py` 装到 `~/.config/opencode/`）|
| `experiments/frametell-src/frametell-main/` | **FRAMETELL fork**（AGPL-3.0）：引擎 `packages/engine`、studio、agent；我们的改动记录在它的 `OURS.md` |
| `app/` `web/` `base-arch/` | **冻结留档**（旧管线 / 上游引擎），不再开发；工具按需搬进 fork |
| `docs/` | 上面第三节的文档 |

**没入库的**（体积）：各处 `node_modules/`、所有 `out/`（成片/抽帧/渲染分块）、`audio/`、`voice.js`、
`base-arch/`、`experiments/anatomy-main`。都能按文档重新生成。

---

## 五、纪律（别犯的错）

1. **只用 Flow 生图，绝不用它生视频**（生图不花积分；视频花积分）
2. **角色靠挂 chip**（`Add ingredients → Characters → 小树/小芽 → Add to prompt`），**绝不把角色写进提示词**；不许摘嫩芽
3. **先定片长再写字**（194 字/分钟）；一条 cue ≤12 字且**第 12 字前要有标点**（否则字幕切开词）
4. **素材阶段 = agent**（要判断的活）· **出片 = 脚本**（机械活）· **引擎里不许有 LLM**
5. 面板是遥控器、执行器是干活的人、**约定就是文件**（`gen-queue.json` / `events.jsonl` / `docs/审批.json`）
6. `base-arch/`、`app/`、`web/`、`projects/marriage_full/` **只读**

---

## 六、许可

- `experiments/frametell-src/frametell-main/` 是 [FRAMETELL](https://github.com/sitor-ai/frametell) 的副本，**AGPL-3.0**，保留其 `LICENSE`；
  我们对它的改动记录在它的 `OURS.md` 里。
- 其余为本项目自有内容。**本地自用，不对外提供服务**（仓库为 private）。
