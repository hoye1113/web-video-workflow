# harness 与分工：谁"准备素材"、谁"出片"

> 用户的问题：**要不要加 OpenCode CLI 来承载素材准备阶段（bsk 操作等），最后生视频才走 frametell？**
> 结论先给：**方向对**，但边界不要按"运行时"划，要按**活的种类**划；而且这个形状是三个现成先例的共同答案。

---

## 一、先看先例（都是开源、都能查到）

### ① OpenMontage（agentic 视频生产系统）—— 形状几乎一模一样

它的官方流程图（GitHub README）逐句翻译：

```
你："做一条讲黑洞怎么形成的科普视频"
 → Agent 读 pipeline manifest（YAML：阶段 / 工具 / 评审标准 / 成功闸门）
 → Agent 读 stage director skill（Markdown：每个阶段"怎么做"）
 → Agent 调 Python 工具（100+，"agent 的手"）
 → Agent 用自己的 reviewer skill 自检（schema 校验 / 流程合规 / 质量）
 → Agent 存 checkpoint（JSON：可断点续跑 / 决策日志 / 花费快照）
 → Agent 交给你确认（"每个创作决定你都在场"）
 → 合成前校验闸门 → 渲染（Remotion 或 FFmpeg）
 → 渲染后自检（ffprobe / 抽帧 / 音频分析 / 承诺核对）→ 才给你成品
```

**它把"素材与创作"交给 agent，把"渲染"交给确定性渲染器**，中间用 manifest/checkpoint 管状态。
我们的 frametell 引擎，正好对应它那张图里的 **Remotion/FFmpeg** 那一格。

### ② MoneyPrinterTurbo（确定性流水线）—— 入口多，流水线只一条

主题 → LLM 写稿 → 关键词 → 素材（Pexels）→ edge-tts → 字幕（whisper）→ ffmpeg 合成。
对外有 **WebUI / API / CLI / Agent** 四种入口，**底下是同一条流水线**。
→ 启示：**入口可以多，流水线只该有一条**；面板不该是流水线本身。

### ③ frametell 自己 —— 本来就是"agent + engine"两半

`packages/agent`（导演 / 画页）+ `packages/engine`（页 DSL / 时间轴 / 渲染 / 字幕 / 混音）。
它那个 agent **没有浏览器工具** —— 这正是"用 Flow 生成有 IP 的处境图"这一步的空缺。
→ 所以问题不是"要不要加 harness"，而是**用哪个 harness 去填它 agent 那一格**。

**bsk 本身就是为 agent harness 设计的**（本机实测）：
`bsk install-skill` 支持 12 种 harness —— Codex / Claude Code / Cursor / OpenClaw / CodeBuddy /
WorkBuddy / Pi / Hermes / Kimi Code …，也能用 `--source` 装我们自己的 skill。

---

## 二、建议的架构（四层 + 一条接缝）

```
① 前台（人）    面板：首页 / 工作台 / 审批 / 素材库        ← 剪辑人员只用这一层
                （它只做两件事：调 agent、读文件状态；不实现编排逻辑）
      ↓
② 编排（判断）  agent harness（OpenCode CLI/server + bsk skill）
                职责：写词 · 页→处境映射 · 挑图/看图 · 失败修复 · 按审批意见改片
                工具：bsk（浏览器→Flow 生图）· 文件/脚本 · 读图（模型能看图）
      ↓
③ 执行（机械）  确定性脚本：gen_worker（生图队列）· make_voice · make_pages · lib_index
      ↓
④ 引擎（出片）  frametell engine：页 DSL → 时间轴 → 渲染 → 字幕 → 混音 → 导出
                这里**不许有 LLM**（保证可复现、能查错）
```

**接缝就是文件**（谁写、谁读，写清楚）：

| 交接物 | 谁写 | 谁读 |
|---|---|---|
| `script-source.json`（台词，每条 cue ≤12 字带标点）| agent（人可改）| make_voice / 引擎 |
| `page-spec.json`（每页：图/主题/机位/光/屏上字）| agent（人可改）| make_pages |
| `scene-library/`（图 + `index.json` 索引 + 审批）| gen_worker | 面板 / 页表 |
| `gen-queue.json`（生图队列）| 面板 / agent | gen_worker |
| `out/*.mp4`、`字幕.srt` | 引擎 | 人 / 剪辑软件 |

**三条分工纪律**（避免走两个极端）：
1. **不让 agent 干机械活**：一张张点 Flow 可以由 agent 发起，但**循环由脚本跑**（便宜、可重试、可断点）
2. **不让脚本干判断活**："这段词怎么写""这张图能不能用"必须 agent 或人
3. **引擎里不许有 LLM**（frametell 的 engine 本来就没有，保持）

---

## 三、落地分期

### P1（现在）：面板 + 确定性执行器
- 面板（已有雏形）→ 照 frametell 交互重做：首页 / 工作台 / 审批 / 素材库（见 `docs/面板优化方案.md`）
- `tools/lib_index.py`（素材库索引，**已做**）+ `tools/gen_worker.py`（生图队列执行器）
- **环境自检**（bsk daemon / 扩展装在哪个 Chrome Profile / 能否进 Flow / 是不是 Nano Banana 2.1）

### P1.5：把"素材阶段"交给 agent（就是你说那一步）
- 建一个 **material agent**（OpenCode 的 agent 定义），只给这些能力：
  - `bash`：白名单（`bsk` / `python tools/*` / `ffmpeg` / `node <engine>/tools/*`）
  - 文件读写：限定在 `projects/`、`cast/`、`experiments/`
  - 读图：看生成结果，判断形象一致性
- 给它两个 skill：**我们的开工手册**（`new-film`）+ **bsk 自带的 `browser-skill`**
- 面板通过 OpenCode 的 **HTTP API / SDK** 起会话、发指令、收事件流
  → **事件流直接喂面板的"过程列表"**（正好是 frametell 工作台那套）

### P2：引擎接上 + 审批闭环
- agent 交出的文件 → 引擎渲染 → 前后自检（`accept_emotion` / `qc_snap`）→ 结果回面板
- 三个审批点：页→处境映射表 / 每张图 / 成片
- "只重做受影响页"

### P3（可选）：直接把 frametell 的 studio 当面板
- 若将来走"全自动 agent 写页"那条路线，studio（React UI + Studio 契约）可以直接用；
  我们的契约已照它对齐（`say` / `approve` / `subscribe` / `timeline` / `frames`）

---

## 四、为什么不选另外两条路

| 方案 | 代价 |
|---|---|
| **全 agent**（连渲染也交给 agent 调工具）| 贵、慢、不可复现、出错难查；渲染是纯机械活，加 agent 只增加不确定性 |
| **全脚本**（像 MoneyPrinterTurbo 全定死）| "这段词改一下""这张图重画"就要人肉；而这类活占素材阶段八成 |
| **直接用 frametell studio 走它自带路线** | 它的 agent 没有浏览器工具、画面是"agent 写页代码"；我们要的是"处境图 + 角色 IP" |

**一句话**：把 frametell 当**渲染引擎**，把 OpenCode 当**会开浏览器的导演**，把面板当**剪辑人员的前台**；
三者之间用**文件**交接，用**审批点**把关。

---

## 五、要拍板的两件事

1. **素材阶段的 harness 用谁**：
   - 建议 **OpenCode**（本机已在用、模型走 opencode-go、不产生额外成本）
   - 备选：bsk 原生支持的 Codex / Claude Code / Cursor / Kimi Code 等（换 harness 只需重装 skill）
2. **P1 与 P1.5 的先后**：
   - 建议**先把 P1 的审批点 + 素材库做扎实**（没有审批点，agent 的输出没人把关，返工更贵）
   - 再做 P1.5 把素材阶段交给 agent
