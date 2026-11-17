# 12布布 · 当前状态（2026-11-17）

## 已建立

- `README.md`：角色、风格、情绪、文字、场景、道具规则
- `cast.json`：一二 / 布布的角色卡、风格 preset、文字策略、成片流程
- `prompts/base.md`：基础提示词、负向词、场景/情绪矩阵、检查清单
- `tests/scene-prompts.json`：6 个测试场景
- `tests/make_refs.py`：把测试场景拼成 Flow 队列
- `tests/refs-queue.json`：6 张参考图的完整队列
- `refs/`：**6 张参考图已生成**

## Flow 项目

- 项目名：**12布布**
- 项目 URL：`https://flow.google.com/project/eb48e574-1a2f-4ceb-b499-2433b432afdd`
- 账号：`nishinon857@gmail.com` / nanase nishino（PRO）
- 生成方式：no-chip，提示词直接描述角色；项目里没有挂旧 1bubu/2bubu

## 参考图

| 文件 | 内容 | 状态 |
|---|---|---|
| `refs/pair-hero.png` | 深夜客厅，布布递杯子，一二抱臂后撤 | 已生成 |
| `refs/yier-hero.png` | 一二单人全身，抱臂、耳朵下垂、眼角看左 | 已生成（重画过：去黑色手脚） |
| `refs/bubu-hero.png` | 布布单人全身，前倾伸手、耳朵竖起、尾巴微翘 | 已生成 |
| `refs/scene-note.png` | 餐桌，布布举便签「别走」，一二抱臂 | 已生成（重画过：文字改横排、便签举到胸口） |
| `refs/scene-outdoor.png` | 夜晚公交站，站牌纯色空白 | 已生成 |
| `refs/scene-silence.png` | 空房间，一二抱膝，布布伸手，道具极少 | 已生成 |

## 当前小偏差

- 部分图的台灯/灯柱靠近右侧边缘，右下角空地面不够干净
- `cast.json` / `prompts/base.md` 已加强规则：**所有灯具、桌椅、道具放左侧或中部，右下角 15% 必须空地面**
- 正式片按新规则生成；这 6 张作为方向参考，不重画

## 之后

用户给音频后：

1. 转写 → 修正错字 → 按语义分页
2. 每页写处境 + 情绪（布布够 / 一二挡）
3. 按 `prompts/base.md` 拼 16:9 提示词
4. Flow 生图
5. 预检 → 渲染 `--skip-subs` → 后检
6. 只交付无字幕 mp4：`E:\video-factory\<片号>\out\<片名>-无字幕.mp4`
