# web-video-workflow

给内部剪辑人员用的**本地视频生产工作流**：把口播文案变成 3-5 分钟横屏解说片（带字幕、可交给剪辑二次加工）。

> **路线已经换过一次**（2026-10-16）。第一版是自己搭的 Python + React 管线，实测**画面"图解化"、代入不进去**。
> 现在的做法是**以 FRAMETELL 为骨架**（流水线、界面、检查器、时间轴都是它的），
> 我们的东西以一等公民装进去：**生成图 / 角色 IP / 情感风格包**，外加**免密钥配音**和**字幕切分**。
> 决策的来龙去脉在 `docs/方案.md`（含"哪些实测过、哪些还没验"的标注）。

## 目录

| 路径 | 是什么 |
|---|---|
| `docs/方案.md` | **主文档**：目标、为什么用 FRAMETELL、阶段计划 P0-P5、风险、决策记录 |
| `docs/经验与坑.md` | 27 节实测踩坑（现象→根因→修法→以后怎么防）。这是我们最值钱的一份 |
| `docs/FRAMETELL拆解.md` | 读它源码得到的结论：它怎么做到稳定好看（组件库/时间轴/检查器/编排） |
| `docs/待办.md` | 当前待办（按"能不能独立出片"排序） |
| `experiments/frametell-src/frametell-main/` | **FRAMETELL 源码（我们的 fork）**，见它根目录的 `OURS.md`（我们改了哪 15 个文件、为什么） |
| `experiments/ft-run/` | 验证工程与补丁脚本：`实验-情感`（3 页样片）、`复利`（它的示例片）、`patch-edge-tts*.py`、`diff-fork.py` |
| `experiments/uitest/` | 对比图：成片验收表、配色 A/B、代码 vs 生图 |
| `app/` `web/` `tools/` | **旧管线（冻结留档）**：Python 服务 + React 面板 + 我们的脚本。不再开发，工具按需搬进 fork |
| `projects/marriage_full/` | 主项目：26 页的 `project.json` / 页代码 / 生成的图（`assets/`）。成片 mp4 未入库 |
| `PRD-video-factory.md` | 第一版产品需求（历史文档） |

**没有入库的**（体积/版权原因）：`base-arch/`（上游 huashu-art-motion 引擎，81MB）、
各处 `node_modules/`、`out/`（成片 mp4、抽帧、渲染分块）、`experiments/anatomy-main`（第三方的参考仓库）。
这些都能按本文档重新取到或重新生成。

## 怎么跑起来（新机器）

```bash
# 1. 依赖
node ≥ 22.19 · pnpm（corepack prepare pnpm@10.5.2 --activate）· git · Chrome · ffmpeg

# 2. fork 本体
cd experiments/frametell-src/frametell-main
pnpm install --filter "frametell..."      # 不装 Electron 桌面壳
pnpm --filter "frametell..." build

# 3. 配音（免费、免密钥；给的是逐词时间戳）
uv venv ~/.frametell/edge-venv
uv pip install --python ~/.frametell/edge-venv/Scripts/python.exe edge-tts

# 4. 模型：写 ~/.frametell/config.json（自定义 OpenAI 兼容服务商，见 docs/方案.md §7）
#    本机用的是 OpenCode Go 的端点 + deepseek-v4.1-flash

# 5. 起面板
node apps/cli/dist/cli.js serve
#   → http://127.0.0.1:5317/?token=<~/.frametell/server-token>
```

## 一条片子怎么走

```
说一句话 / 传素材 → 导演 agent 出分镜 → 你签字
  → 写口播 → edge-tts 配音（拿到逐字时间戳）
  → 逐页画面（生成图当底 + 矢量层 + 停-推-停的镜头，跟着旁白的词出现）
  → 自动检查（填充率 / 字幕带 / 出框 / 重叠 / 运行时报错）+ 关键帧拼图给模型看图改（≤3 轮）
  → 出片：干净母版 mp4 + 字幕.srt（8-12 字一行，时间精确到字）+ 口播脚本.md
     （字幕与包装交给剪辑软件做；需要直接发平台时另有烧死字幕的版本）
```

## 当前进度

- **P0 地基 ✅**：fork 编译通过、面板能起（5317）、模型接通（实测 文本/工具调用/看图 三样全通）
- **P1 输入输出可靠 ⏳**
  - ✅ **edge-tts 配音**（免密钥、逐词时间戳）—— 3 页 49.4 秒音频 9.4 秒合成，画面时间轴跟着真语速走
  - ✅ **字幕三件套**：短句切分（≤12 字，时间精确到字）+ 默认不烧 + 可单独重跑
  - ✅ **素材读取把关**：materialVerdict() 判定 + 出片前报警 + ocr-scan.py 视觉兜底（实测 3 页扫描件 → 211 字，一字不差）
  - ⏳ **角色资产化**（两个固定角色的定妆图 → 规范参考图 + 角色卡 + 一致性检查）**等定妆图**
- **P2-P5**：见 `docs/方案.md`。**总验收点是 P2 的 3 页对比**（AI 生成的"处境图"能不能让人代入）

## 许可

- 本仓库里 `experiments/frametell-src/frametell-main/` 是 [FRAMETELL](https://github.com/sitor-ai/frametell) 的副本，
  **AGPL-3.0**，保留其 `LICENSE`；我们对它的改动记录在它的 `OURS.md` 里。
- 其余为本项目自有内容。**本地自用，不对外提供服务。**
