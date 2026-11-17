# 12布布 · 经验与教训（2026-11-17）

## 1. 新角色 / 新风格必须用新的 Flow 项目

- 旧 `video-factory` 项目里带着 1bubu / 2bubu 的角色与 P3 奶油风格上下文。
- 即使提示词写“16:9 暗蓝极简、白熊猫一二、焦糖小熊布布”，在旧项目里生成出来仍然是旧 P3 的奶油色和旧角色。
- 换成干净项目 **12布布**（`eb48e574-1a2f-4ceb-b499-2433b432afdd`）后，同一批提示词立刻变成暗蓝 + 暖黄、新角色。
- **教训：Flow 的项目上下文会污染/覆盖提示词；换角色、换风格先换项目，不要复用旧项目。**

## 2. Flow 的地区 / 登录 / 调试口

- Flow TV 能看（`labs.google/flow/tv`）不等于 Flow 项目编辑器能用；生图入口是 `flow.google.com/project/...`。
- 代理出口香港（`loc=HK`）时 Flow 跳 `/unsupported-country`；美国（`loc=US`）才正常。
- Chrome 的浏览器账号登录 ≠ Google 网页登录：`Local State` 显示 `nishinon857@gmail.com`，但 Flow 页面仍可能显示“登录”；需要在网页完成 Google 登录。
- 调试口必须用**普通配置**启动：

```powershell
chrome.exe --user-data-dir="$env:LOCALAPPDATA\Google\Chrome\User Data" `
  --profile-directory=Default --remote-debugging-port=9222 `
  --proxy-server=http://127.0.0.1:7890
```

- 如果 Chrome 已经在运行，`--remote-debugging-port` 会被忽略；**先关掉所有 Chrome**。
- `bsk 0.3.3 → 0.5.0`：`bsk update -y` 前设置 `HTTP_PROXY/HTTPS_PROXY`，否则 GitHub 连接会被重置。
- Chrome `157.0.8103.79` 是当前可用最新稳定版；官方安装包/企业 MSI 也是 157；`chrome://settings/help` 显示“已是最新”。版本 API 的 158 还没铺开。

## 3. 角色提示词要写到“不会画错”

- 一二：只说“白色熊猫、黑耳朵黑眼圈”会画出**黑手脚**；必须补“身体和四肢都是白色，不要黑色手脚”。
- 布布：浅焦糖棕、圆耳、杏黄腮红、小圆尾；明确“不要黑手脚、不要胸口图案”。
- 情绪“够 / 挡”有效：
  - 布布：重心前压、伸手/递东西、视线追、耳朵竖、尾巴翘。
  - 一二：后撤/坐实、抱臂抱杯、手护自己、眼角瞟、耳朵垂。
- 不笑、不 w 嘴、不弯眼、不露齿，模型能遵守；不要用问号/汗滴/闪光代替情绪。

## 4. 文字载体

- 便签平放桌上会被画成**竖排/旋转**，而且容易落在画面下部。
- 改成“布布把便签举到胸口高度、横排水平正向、不要旋转”，效果正确。
- 一张图只允许一个文字载体；字号小、不压脸和手；其他平面物体保持纯色空白。

## 5. 右下角空地面

- 模型倾向把台灯/路灯放右边，灯座占右下角。
- 提示词要写死：**所有灯具、桌椅、道具放左侧或中部，右下角 15% 必须空地面。**
- 参考图里仍有少量灯靠右；正式片按加强版提示词生成。

## 6. 旧项目处理

- 旧 1bubu / 2bubu 不删除，标记停用：
  - `projects/character-assets/DEPRECATED.md`
  - `projects/character-assets/bubu-cards.md` 顶部
- 新项目：`projects/12bubu`，Flow 项目名 **12布布**。

## 7. 以后流程

```text
用户音频
→ 转写 / 校对
→ 按语义分页
→ 每页写处境 + 情绪（布布够 / 一二挡）
→ 按 prompts/base.md 拼 16:9 提示词
→ Flow 生图
→ 预检 → 渲染 --skip-subs → 后检
→ 只交无字幕 mp4：E:\video-factory\<片号>\out\<片名>-无字幕.mp4
```

- 16:9；默认 1920×1080，帧率/尺寸按片确认。
- 不挂旧角色 chip；新项目里用提示词描述角色。
