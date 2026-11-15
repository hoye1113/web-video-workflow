# 夜读 · 五步重建信任（night-trust-1115）

用 `E:\音频素材\1115.mp4` 的原音频做的 **4:3 横屏**深色心理图解。

## 规格

| 项 | 值 |
|---|---|
| 画幅 | **4:3 / 1920×1440（1440p） / 30fps** |
| 时长 | 03:46.1（29 页） |
| 音频 | 用户原声，未改语速、未补静音；约 -16.1 LUFS |
| 风格 | `night-insight` 4:3 变体 |
| 成片 | `out/night-1115-43-无字幕.mp4` |
| 交付 | `E:\video-factory\night-1115\` |

## 结构

1. 钩子：出轨之后，还能继续吗？
2. 第一步：重建信任
3. 第二步：允许情绪被看见
4. 第三步：把不安说出口
5. 第四步：建立新的安全感规则
6. 第五步：给时间
7. 收尾：从废墟里重新长出来

## 文件

| 文件 | 用途 |
|---|---|
| `script-source.json` | 音频切页后的 cue 源数据 |
| `script.js` / `voice.js` | 时间轴和原音频切片 |
| `night-spec.js` | 29 页内容 + 版式 |
| `build_spec.py` | 从内容表生成 `night-spec.js` |
| `covers/a.html` / `b.html` | 两张 3:4 封面源文件 |
| `covers/render.mjs` | 渲染两张封面 |
| `out/` | 成片、字幕、封面 |

## 重建

```powershell
python projects/night-1115/build_spec.py
cd projects/night-1115
$env:VF_STAGE="1920x1440"
node engine/tools/render.mjs --skip-subs --fps 30 --workers 4 --name night-1115-43
```

4:3 布局在 `night-insight` 套版的 `render43` 里：页面按 1440×1080 排，输出按 1920×1440 等比放大，文字保持矢量清晰。
