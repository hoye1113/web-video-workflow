# 实习工作台（intern studio）

> 面向**只会填表的实习生**：一个表单 → 三次点头 → 下载成片。
> 他们看不到（也不需要知道）：OpenCode、agent、bsk、Flow、frametell、队列、渲染。

## 实习生看到的四屏

| 屏 | 内容 | 他要做的 |
|---|---|---|
| **1. 表单** | 讲什么（一句话）/ 可选资料 / 片长 / 谁的声音 / 用哪个小朋友当主角 | 填完点「开始做视频」 |
| **2. 分镜** | 一张表：第几页 / 讲什么 / 画面 / 主角 | 「就这样，开始画图」或写一句要改的 |
| **3. 图** | 每页一张图（待他看的那张有标记） | 「都可以，去出片」或指出要重画的 |
| **4. 成片** | 播放器 + 下载（带字幕 / 无字幕 / 字幕文件） | 「可以，就这样」 |

进度条只有三个词：**写台词 → 画图 → 出片**。页面自动刷新。

## 背后是谁在干（实习生看不到）

```
表单
 └─ apps/intern/server.py
     ├─ 建工程            → tools/new_film.py
     ├─ 写台词/分镜/页表   → OpenCode 的 material agent（读 docs/新题材开工手册.md）
     ├─ 生图              → bsk 操作 Chrome 在 Flow 里挂角色 chip（tools/gen_worker.py）
     ├─ 点头之后出片        → tools/conductor.py 自动跑：素材→排页→配音→字幕→渲染→验收
     └─ 下载              → frametell 引擎产物（out/*.mp4 + 字幕.srt）
```

三个"点头"落在 `projects/<片>/docs/审批.json`（`gate:map` / `gate:img` / `gate:film`）；
**闸门没过，推进器什么都不做**。

## 跑

```powershell
# 1) 前置：bsk daemon 在跑、Chrome 已登录 Flow、OpenCode 装了 material agent
python tools/opencode/install.py

# 2) 起工作台（实习生用浏览器访问这台机器）
python apps/intern/server.py --port 8900               # 只本机
python apps/intern/server.py --port 8900 --host 0.0.0.0  # 局域网里的实习生可访问（别开公网）

# 3) 实习生打开 http://<这台机器>:8900
```

## 出片机器

出片（渲染）吃 CPU：**用 16G 级以上的机器**；4 核 8G 的老笔记本渲染会把机器拖到硬重启
（`docs/经验与坑.md` 六三/六四）。写词/配音/审片在弱机上没问题。
