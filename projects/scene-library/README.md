# 处境图库 · warm-emotion

> 情感类口播解说用的**处境图**：一张图说清"谁、在哪、在做什么、光从哪来"。
> 生成方式：Flow（`video-factory` 工程）+ 挂角色 `小芽` / `小树` + `🍌 Nano Banana 2.1`（生图，不花积分）。

## 规格

| 项 | 值 |
|---|---|
| 尺寸 | **1376×768**（16:9，与旧管线一致）|
| 风格 | 暖色纸本插画：平涂 + 细铅笔线、一支笔笔触、不描粗边不发光 |
| 角色 | `小芽`（女）/ `小树`（男）—— **衣服、发型、头顶嫩芽都不许变** |
| 构图 | 米白纸底留白多；**画面下方 20% 完全留空**（字幕带）|
| 禁忌 | 无文字 / 无图表 / 无箭头 / 无圆圈 / 无边框 |

**生成要点**：角色**不写进提示词**，而是用 `Add ingredients → Characters → 选角色 → Add to prompt`
挂成**素材 chip**；实测出来的图衣服、发型、头顶嫩芽都对得上。

---

## 一、通用处境库（16 张 = 8 处境 × 男/女）

每个处境**男女各一张**，同一句提示词（性别中立），只换挂的角色。

| # | 处境 | 语义 | 男 | 女 |
|---|---|---|---|---|
| 01 | `paper-fold` | 隐忍 / 遮掩 | `male-01-paper-fold.png` | `female-01-paper-fold.png` |
| 02 | `phone-glow` | 秘密 / 暴露 | `male-02-phone-glow.png` | `female-02-phone-glow.png` |
| 03 | `long-table` | 距离 / 冷战 | `male-03-long-table.png` | `female-03-long-table.png` |
| 04 | `empty-chair` | 缺席 | `male-04-empty-chair.png` | `female-04-empty-chair.png` |
| 05 | `door-crack` | 隔阂 | `male-05-door-crack.png` | `female-05-door-crack.png` |
| 06 | `bed-edge` | 失眠 / 消耗 | `male-06-bed-edge.png` | `female-06-bed-edge.png` |
| 07 | `hand-on-door` | 犹豫 | `male-07-hand-on-door.png` | `female-07-hand-on-door.png` |
| 08 | `empty-living` | 冷清 | `male-08-empty-living.png` | `female-08-empty-living.png` |

## 二、P2-d 专用（3 张，对应 05/15/18 三页）

| 文件 | 页 | 处境 |
|---|---|---|
| `p05-kneel.png` | 05 · 案例一·周先生 | 小树跪着、双手撑地、头低下去；面前地上摊着一页白纸（离婚协议）|
| `p15-night-door.png` | 15 · 案例三·李先生 | 夜里，小树背影站在亮着灯的家门口，手正把外套挂上衣架 |
| `p18-two-doors.png` | 18 · 真相拆解 | 小树站在走廊：左边门内暖黄的家里的光、右边门缝冷青的手机屏光 |

---

## 怎么用

```js
P.scene('assets/06-bed-edge.png', {
  reveal: { from: 0.25, to: 1, at: 0.3, dur: 1.6 },
  cam: [{ t: 0, z: 1 }, { t: 3.4, z: 1 }, { t: 4, z: 1.06 }, { t: 9, z: 1.06 }],   // 停-推-停
});
```

- **夜间页复用浅底图**：`ground: 'plate'`（白底变夜色底、主体保留）
- **情绪低谷**：`grade: { brightness: 0.86, saturate: 0.82 }` + 一盏灯
- 图里已经有"处境"了，**代码只做三件事**：摆位、让它动、上面加字（GRAMMAR 的规矩）

## 批次记录

| 批次 | 张数 | 时间 | 结果 |
|---|---|---|---|
| A（P2-d 三页） | 3 | 2026-10-18 | 零失败 |
| B（通用处境库） | 16 | 2026-10-18 21:59–22:23 | **零失败**，约 24 分钟（每张 ~100 秒）|
