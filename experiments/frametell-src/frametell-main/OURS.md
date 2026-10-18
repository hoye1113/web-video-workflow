# OURS.md — 我们对 FRAMETELL 做了什么（fork 记录）

> 上游：`sitor-ai/frametell`，本地版本 **v0.7.1**（zip 快照，见 `../ft-main.zip`）。
> 本文是**我们改动与上游的唯一对照表** —— 上游更新时照这份 rebase，别靠记忆。
> 生成方式：拿原始 zip 与工作树逐文件比哈希（`experiments/ft-run/diff-fork.py`）。

## 改动总览（截至 2026-10-16）

**新增 1 个 · 改动 14 个 · 删除 0 个**

### 新增

| 文件 | 干什么 |
|---|---|
| `packages/voice/tools/edge-tts.py` | edge-tts 的 Python 桥：JSON 请求文件进 → mp3 + 逐词时间戳出。**必须 `boundary='WordBoundary'`**（否则中文只有整句时间戳）；请求走 UTF-8 文件不走管道（Windows 控制台会按 GBK 编码）；带退避重试并区分"可重试/不可重试" |
| `packages/engine/styles/warm-emotion/` | **我们的情感叙事风格包（自包含，4 个文件）**：`GRAMMAR.md`（宪法，页面 agent 与评审 agent 都读它）· `style.js`（日/夜两套色板 + `setTheme`）· `style.css`（纸面/暗角/字幕）· `kit.js`（**8 个情感组件**：门/手机/照片/背影/纸/光/距离/空位）。放在 `styles/<风格>/` 下，**不改引擎运行时**。坑：逐页换色板必须改 `PV.C`（运行时在加载时把 palette 拷进了自己的 `C`，改 `STYLE.palette` 无效）；背景只在片级算一次，夜间页要自己用 `P.light(..., { full: true, ground: 'paper' })` 铺底 |

### 素材读取把关（扫描件别再静默地读成空）

| 文件 | 改了什么 |
|---|---|
| packages/core/src/materials.ts | 新增 materialVerdict()：把读到了多少判成 ok / empty / sparse（每页少于 40 字 = 疑似扫描件）；警告文案改成**可照抄的补救命令** |
| packages/core/src/runner.ts | 出片前**把这条判定报给用户**（以前只在解析彻底失败时才吭声，扫描件读成 0 字一声不响） |
| packages/engine/tools/ocr-scan.py | **新增**：扫描件 → 逐页渲图 → **视觉模型转写** → 写成同格式的 <名>.pdf.md。模型与密钥读 ~/.frametell/config.json |

### 改动（按模块）

**配音：加一个免密钥的 provider —— edge-tts**

| 文件 | 改了什么 |
|---|---|
| `packages/voice/src/tts.ts` | `TtsProvider.id` 联合加 `'edge'`；新增 `edgeTts()`（spawn 桥，`~/.frametell/edge-venv` 优先、退回 `uv`）与 `EDGE_VOICES`（8 个音色） |
| `packages/voice/src/index.ts` | 导出 `edgeTts, EDGE_VOICES` |
| `packages/core/src/types.ts` | `VoiceChoice.provider` / `Voice.provider` 加 `'edge'`；`VoicesView.configured` 加 `edge` |
| `packages/core/src/refs.ts` | 音色引用的判定认 `edge` |
| `packages/core/src/runner.ts` | `voiceFor()`：edge **免密钥**（另两家仍要）；"先连配音服务"的预检对 edge 跳过 |
| `packages/core/src/studio.ts` | `voicePreview()` 认 edge；`voices()` 把 EDGE_VOICES 列进去；`configured.edge = true` |
| `packages/agent/src/events.ts` | 事件里的 provider 联合加 `'edge'` |
| `packages/agent/src/prompts.ts` | `Brief.voice` 联合加 `'edge'` |
| `apps/cli/src/cli.ts` | 没有云服务 key 时用 edge；默认音色按语言选 |
| `apps/cli/src/server.ts` | 试听路由的 provider 类型 |
| `apps/desktop/src/main.ts` | IPC 里的试听 provider 类型（桌面壳我们不用，但类型要一致） |

**界面：把 edge 显示出来**

| 文件 | 改了什么 |
|---|---|
| `packages/ui/src/components/VoicePicker.tsx` | `PROVIDER_NAME` 加 `edge: () => 'edge-tts'`；音色分组加 `edge` |
| `packages/ui/src/components/FilmSettings.tsx` | "未配置 key"的提示不把 edge 算进去（它永远可用） |

**字幕：短句切分（短视频惯例 8-12 字一行）**

| 文件 | 改了什么 |
|---|---|
| `packages/engine/tools/script.mjs` | 写 `字幕.srt` 时把一条 cue 切成多行：切在标点处、上限 12 字（`FRAMETELL_SUB_MAX` 可调）；**时间从 cue 的 `k`（逐字起点）取，精确到字**；没有 k 就按字数比例。`口播脚本.md` 不变（给人读，一句一行） |

## 我们**没有**改的（有意为之）

- 渲染内核、组件库、检查器、流水线、studio 的交互 —— 一律不碰，上游怎么走我们就怎么用
- 已放弃：自建 Electron 壳（它已有桌面壳，我们只用浏览器面板）

## 约定（改动纪律）

1. **改动集中在这几处**：`packages/voice/`（新 provider）、`packages/core`+`packages/agent`+`apps` 的**类型与调用点**、`packages/ui` 的**列表显示**、`packages/engine/tools/` 的**工具增强**。
2. 往后我们的**风格包与组件**一律放 `packages/engine/styles/<我们的风格>/` 和 `packages/engine/lib/`（新文件），不改引擎运行时。
3. 每次改完：`pnpm --filter "frametell..." build` 必须过；再跑一遍 `experiments/ft-run/diff-fork.py` 更新本文的清单。
4. 上游更新时：解压新的 zip → 跑 `diff-fork.py`（把 `ft-main.zip` 换成新版）→ 看本文列出的文件在新版里有没有冲突，逐个合并。

## 本地环境（新机器要照做）

```
node ≥ 22.19 · pnpm（corepack prepare pnpm@10.5.2 --activate）· git · Chrome · ffmpeg
pnpm install --filter "frametell..."      # 不装 Electron 桌面壳
pnpm --filter "frametell..." build
uv venv ~/.frametell/edge-venv && uv pip install --python ~/.frametell/edge-venv/Scripts/python.exe edge-tts
~/.frametell/config.json                  # 自定义 OpenAI 兼容服务商（见 docs/方案.md）
node apps/cli/dist/cli.js serve           # 面板：http://127.0.0.1:5317/?token=<~/.frametell/server-token>
```
