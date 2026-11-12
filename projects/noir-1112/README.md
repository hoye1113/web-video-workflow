# 裂痕之后（noir-1112）· 婚姻信任重建

> 项目名：**《裂痕之后》** · 内部 slug：`noir-1112` · 源音频：`1112.mp4`
> 后面引用这部片，直接说「裂痕之后」或「noir-1112」即可。

用 `noir-editorial` 风格包，把用户提供的 `E:\音频素材\1112.mp4` 音频做成 6 分 17 秒的横屏成片。

| 项 | 值 |
|---|---|
| 音频源 | `E:\音频素材\1112.mp4`（只取音频，377.5s） |
| 成片（带字幕） | `out/noir-1112-有字幕.mp4`（1920×1080 / 30fps / 6:17） |
| 成片（无字幕母版） | `out/noir-1112-无字幕.mp4` |
| 720p 压缩测试 | `out/noir-1112-720p.mp4` |
| 结构 | 7 章 / 39 页 / 235 条 cue |
| 配音 | 用户原音频；`voice.js` 由原音频逐条切开，未重录、未合成 |
| 字幕 | `out/字幕.srt`；成片字幕由引擎从同一批 cue 烧入 |

## 重新生成

```powershell
python projects/noir-1112/make.py
python tools/voice_from_map.py noir-1112 "E:\音频素材\1112.mp4"
cd projects/noir-1112
node engine/tools/render.mjs --fps 30 --workers 6 --name noir-1112
```

## 说明

- `make.py` 里是 39 页的章节/页型/文案表；`from` / `to` 是转写 segment 的下标。改页型或改标题只改这里，再重跑。
- `cue-audio-map.json` 记录每条 cue 在原音频里的起点；`voice_from_map.py` 按“本条起点 → 下一条起点”切音频，所以整条片的音轨就是原音频的时间轴，不插静音。
- 转写来源：`experiments/transcribe/1112.json`（faster-whisper small）。`make.py` 里修了明显的同音错字（如“堵定→笃定”“谦恶→煎熬”“九汉逢甘陵→久旱逢甘霖”）。
- 这版**没有加 BGM / 音效**，保留用户原声；BGM 是下一步可选项。
- 字体仍用系统 `SimSun` 做 proof；交付商用前建议换有授权的宋体。
