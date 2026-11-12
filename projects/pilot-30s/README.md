# 30 秒风格样片：深色心理图解

这是“对标-心理图解”路线的第一条 30 秒样片，用来确认画风、版式和节奏。
不是正式交付片，音频还没接。

## 看效果

- 视频：`out/preview-30s.mp4`（1920×1080 / 30fps / 30 秒 / 静音）
- 七页对照表：`out/contact-sheet.jpg`
- 可交互预览：用 Chrome 打开 `preview.html`，点击画面暂停/继续

## 文件

| 文件 | 用途 |
|---|---|
| `script-source.json` | 30 秒文案 + 分页 + 屏上字 + 画面描述 |
| `storyboard.md` | 逐页分镜、时间码、视觉规范 |
| `preview.html` | 7 页动效的独立预览（不依赖引擎） |
| `render_preview.mjs` | 用 Playwright 逐帧截图 → ffmpeg 合成 mp4 |
| `make_sheet.py` | 7 张关键帧拼成 3×3 对照表 |
| `out/` | 生成物（被 .gitignore 忽略） |

## 重新生成

```powershell
# 只出 7 张关键帧
node projects/pilot-30s/render_preview.mjs --no-video

# 出 30 秒静音 mp4
node projects/pilot-30s/render_preview.mjs

# 拼对照表
python projects/pilot-30s/make_sheet.py
```

## 接音频后怎么改

1. 用 `tools/transcribe.py` 转写音频，拿每段起止时间；
2. 按句号/问号重排 7 页，不切在句子中间；
3. 每页首句/末句对到画面首帧/尾帧，误差 <0.2 秒；
4. 重新跑 `render_preview.mjs` 或接入 `night-insight` 引擎风格包。

## 现在的限制

- 还没有 BGM 和转场音效；
- 还没有接入正式引擎，只是独立预览；
- 文案是样片，正式生产前要按选题库重写并做事实核查。
