# 参考 · huashu-design

> 链接：https://github.com/alchaincyf/huashu-design
> 作者：花叔（alchaincyf）· MIT · 2026-10-30 存档，**先不接入生产**。

## 它是什么

一个给 agent 用的 **HTML 设计 skill**：在 Claude Code / Codex / Cursor / OpenCode 等 agent 里说话，
产出网页、App 原型、可编辑 PPTX、信息图、短动画。不是视频引擎，也不替代 FRAMETELL。

核心能力：

- 84 种 HTML 原生风格库（网页 / PPT / 信息图 / App / 中文与东亚）
- 三方向门：六个候选 → 六张缩略图 → 挑三版做真稿
- 品牌资产协议（问 → 搜官方 → 下载 → grep 色值 → 写 `brand-spec.md`）
- 设计体检 + 外观账本（只量事实；三版撞车 / 和最近项目撞车）
- HTML → MP4/GIF、可编辑 PPTX、PDF/PNG/SVG

安装（如果以后要用）：

```powershell
npx skills add alchaincyf/huashu-design
# 或
git clone https://github.com/alchaincyf/huashu-design.git ~/.claude/skills/huashu-design
```

## 可以借鉴的（按价值排序）

### 1. 经验分层：preference / observed / verified / superseded

它的 `scripts/learn.py` 把经验分成四类，每条带 topics、evidence、下次怎么做：

| 类型 | 含义 |
|---|---|
| `preference` | 用户亲口说的原话，直到他改口都成立 |
| `observed` | 只在一个项目里见过，是线索不是规则 |
| `verified` | 两个以上项目复现，或测量过 |
| `superseded` | 已经不成立，保留条目并写明被什么取代 |

**对我们的启发**：`docs/经验与坑.md` 现在 82 节混在一起，
“6 秒一屏”是用户偏好，“--workers 6”是实测规则，“小树变树人”是一次观察。
以后新经验按四类记；旧经验先挑最常用的迁，不必一次全改。

### 2. 外观账本 + 撞车检测

它记录每次交付的底色、色板、字体、版式骨架，下个项目主动避开。

**对我们的启发**：我们的片子都是 `warm-emotion`，很容易“每部都一个样”。
可以落成 `tools/look_ledger.py`：

- 读 `page-spec.json` + `pages/*.js` + `out/snap/qc*.jpg`
- 记：底色、主色板、theme 比例、机位分布、屏上字位置、标题版式
- 新片和最近 3 部比，太像就提醒换方向

它的 `design_lint.py` 里可借鉴的数值：

- 色板距离
- 版式骨架相关性
- 底色类 + 标题字体是否相同

这正好可以补我们“重画比稿只看分数、不看是否换皮”的缺口。

### 3. 只量事实的设计体检：红 / 黄 / 提示

- **红灯**：图裂、字太小、对比度不够、控制台报错 → 必修
- **黄灯**：模板装饰（全大写小标签、`A · B · C`、圆角卡片套件、标题只给一个词换色）
- **提示**：外观家族（暖纸衬线、深底单点缀、细线报纸）——本身不是错，三版都落进去才是问题

**对我们的启发**：我们已有 `scene_lint` / `frame_audit` / `accept_emotion`，
方向是对的；缺的是“黄灯”和“重画比稿的换皮检测”。
可以把“色板距离 + 构图相关性”加到图片比稿里。

### 4. 能力探测不阻塞

它的 `scripts/capabilities.py` 只报告“手里有什么”，缺了给安装建议，不崩：

- `shutil.which` 查 node / ffmpeg / npx
- 查 skills 目录
- 只报告 key 是否存在，不打印值
- JSON 输出

**对我们的启发**：`tools/pipeline.py` 的 `env_check()` 在 bsk 缺失时直接
`FileNotFoundError` 崩掉。应该改成“返回 ok:false + hint”，工作台能渲染，不阻塞启动。

### 5. 先给看得见的东西，再开工

- 六个候选 → 六张缩略图 → 挑三版做真稿
- Junior Designer 工作流：先写 assumptions + placeholders + reasoning，尽早 show，哪怕只是灰块
- 三方向门：摆出来就停，用户选完才做完整版

**对我们的启发**：

- 新题材/封面可以先出 **3 张样片页**，再全量；不要 64 页每页都三方向。
- agent 写台词/分镜时，先落 5 行 assumptions + 页表骨架占位，再写全文，
  治“读完文档不写文件、空转十几分钟”。

### 6. Gate 文件：检查点物化成文件

它有 `brand-spec.md`、`direction-approved.md`、`导演稿.md`；
“文件不在 = 环节没做”。

**对我们的启发**：我们的 `docs/审批.json` 已经是同一个思路；
可以补上“展示了哪几版、用户原话、截图路径”，而不只是 verdict。

### 7. 品牌资产协议：资产 > 规范

五步：问 → 搜官方渠道 → 下载 → 核验 → 固化成 `brand-spec.md`。
“绝不从记忆猜品牌色；从资产里 grep 色值。”

**对我们的启发**：角色卡/风格包已经是“量出来的色板”，这条我们做得对；
以后加新角色/新风格继续用“先拿定妆图/参考图，再量色，不凭记忆写色值”。

### 8. 参考板：动手前先亲眼看

`scripts/ref_board.py` 把参考作品截成一张板，先看再拆。
**对我们的启发**：新题材可以先收集 3–6 张参考帧/插画，做一张参考板，
再写生图提示词；比凭记忆写“暖色纸本”更稳。

## 不建议直接搬的

| 东西 | 原因 |
|---|---|
| 84 种 HTML 风格库 | 媒介不同；我们的视频风格已锁定 `warm-emotion` |
| PPTX / 网页原型 / motion 引擎 | 不解决长片分页、配音、字幕、角色一致性 |
| 三方向门做成每页强制 | 64 页 × 3 版，成本爆炸 |
| 它的设计评分替代我们的 5 条验收 | 我们的验收判据更贴片子，不要换掉 |

## 一句话结论

**它的价值在方法论，不在代码。**
最值得先借的三条：**经验分层、外观账本+撞车检测、能力探测不崩**。
其次：**新题材先出 3 张样片页**、**agent 先写 assumptions/placeholder**。

当前状态：**仅存档，不接入生产**。
