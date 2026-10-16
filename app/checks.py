"""确定性检查 —— 不看图、不调模型，秒级出结果。

两条腿里的「量数」那条。为什么必须有：
模型看图能挑出语义问题，但**每轮都在挑同样的几类规则性违反**，而且改不动。
这些规则性违反根本不用看图 —— 静态读代码、或量一下渲出来的像素就知道。

分两层：
  scene_lint  读代码。查色相字面量、渐变、Math.random、显式线宽档数、有没有填底。
  frame_audit 量像素。查色相越界、构图（内容框/重心）、帧差。

边界（别指望它们）：
  抓得到——规则性违反：新色相、随机数、构图太小、该停没停。
  抓不到——语义判断：「主体太细读不出」「像随手画的」「形状越界」。
  所以它们不能替代模型看图，只能让模型**少看一半**。
"""
import re
from collections import Counter

import numpy as np
from PIL import Image

import store
import subtitle                       # 字幕带的位置由它定义，两处必须一致

# ---------------- 静态检查 ----------------

COLOR = re.compile(r"#[0-9A-Fa-f]{6}\b")
LINEW = re.compile(r"lineWidth\s*=\s*([\d.]+)")
GRAD = re.compile(r"create(Linear|Radial)Gradient")
SOFT = re.compile(r"shadowBlur|shadowColor|filter\s*=")
RAND = re.compile(r"Math\.random")
ALPHA = re.compile(r"globalAlpha\s*=\s*([\d.]+)")
BG = re.compile(r"fillRect\(\s*0\s*,\s*0\s*,\s*W\s*,\s*H")


def hue_sat(px):
    """px: (N,3) 0-255 → (hue 度, saturation 0-1)。"""
    mx, mn = px.max(axis=1), px.min(axis=1)
    d = mx - mn
    s = np.where(mx > 0, d / np.maximum(mx, 1.0), 0.0)
    h = np.zeros_like(mx)
    nz = d > 0
    r, g, b = px[:, 0], px[:, 1], px[:, 2]
    m = (mx == r) & nz
    h[m] = (60 * ((g[m] - b[m]) / d[m])) % 360
    m = (mx == g) & nz
    h[m] = 60 * ((b[m] - r[m]) / d[m]) + 120
    m = (mx == b) & nz
    h[m] = 60 * ((r[m] - g[m]) / d[m]) + 240
    return h, s


def _palette(project):
    return [c.upper() for c in ((store.load(project) or {}).get("style") or {}).get("palette") or []]


def scene_lint(project, shot, src=None):
    """静态读代码。返回 {problems, warnings, ...}。"""
    pal = _palette(project)
    src = store.read_scene(project, shot) if src is None else src
    out = {"problems": [], "warnings": [], "palette": pal, "chars": len(src)}
    if not src.strip():
        out["problems"].append("这一页还没有代码")
        return out

    # 色值字面量（注意：色相越界要靠 frame_audit 量像素，这里只查字面量不一致）
    used = Counter(c.upper() for c in COLOR.findall(src))
    outside = {c: n for c, n in used.items() if pal and c not in pal}
    if outside:
        out["warnings"].append(
            "色值不在色板里（可能是明暗层次，也可能是硬编码了别的色）："
            + "、".join(f"{c}×{n}" for c, n in list(outside.items())[:5]))

    g = GRAD.findall(src)
    if g:
        out["problems"].append(
            f"用了 {len(g)} 处渐变。画风锁要平涂，模型每次都在这里栽，直接删掉，用两档平涂代替")

    if RAND.findall(src):
        out["problems"].append("用了 Math.random。要用 U.rng(种子)，否则同一时刻渲两次结果不一致")

    if SOFT.findall(src):
        out["warnings"].append("用了 shadowBlur / filter。扁平线稿通常不需要，容易读成「发光的色块」")

    lw = sorted({float(x) for x in LINEW.findall(src)})
    out["lineWidths"] = lw
    if len(lw) > 3:
        out["warnings"].append(
            f"显式线宽用了 {len(lw)} 档（{', '.join(f'{x:g}' for x in lw)}）。"
            f"扁平线稿建议 ≤3 档，否则读成两套笔触。**注意：计算出来的线宽查不到**")

    a = [float(x) for x in ALPHA.findall(src)]
    if len(a) > 6:
        out["warnings"].append(f"globalAlpha 用了 {len(a)} 处。叠太多半透明会失去平涂的干净感")

    if not BG.search(src):
        out["problems"].append("没找到整屏填底 fillRect(0,0,W,H)。引擎每帧会清空画布，不填底就是一片透明")

    out["text_below"] = _text_in_subtitle_band(src)
    if out["text_below"]:
        out["problems"].append(
            f"屏上字画进了字幕带（y = {'、'.join(str(x) for x in out['text_below'])}）。"
            f"成片最下面 18%（y 从 {int(1080 * (1 - subtitle.SUB_BAND))} 起）要烧字幕，"
            f"屏上字的 y 必须 <= {subtitle.safe_bottom()}（稳妥值 <= 820）。"
            f"把字挪到左上方：x 140，y 210 起，每条 +76")

    # 做法检查：这一页该走生图，代码就必须真的用那张图。
    # 踩过：模型（`opencode run` 是个有文件工具的 agent）自己"重画"了整页 ——
    # 页 02 该是「铺图 + 慢推」，它却手画了一道纸裂缝，6660 字，图完全没用上。
    shot = next((s for s in (store.load(project) or {}).get("shots", []) if s.get("id") == shot), None)
    mode = (shot or {}).get("mode") or "code"
    if mode in ("image", "mixed"):
        if "MD.cover(" not in src and "drawImage(" not in src:
            out["problems"].append(
                f"这一页是贴图页（mode={mode}），但代码里没有铺图（找不到 MD.cover / drawImage）——"
                f"画面全是自己画的。图已经生成好了，直接铺上去："
                f"`MD.cover(c, IMG[P], {{ z, fx, fy }})`")
        elif "IMG[" not in src:
            out["problems"].append("这一页是贴图页，但代码里没引用 IMG[...]，图没铺上")
    return out


# 找屏上字的 y：只扫"画字"那几行，取里面的数字。
# 为什么够用：模型写文字位置都是**字面量**（`fillText(s, 150, 880 + i * 74)` 这种），
# 实测 26 页里每页都是这个形状；算出来的 y 查不到，所以这是提示不是铁律。
TEXT_LINE = re.compile(r"fillText\(|word\(|LINES\.forEach|TXT\[i\]")
NUM = re.compile(r"\b(\d{3,4})\b")


def _text_in_subtitle_band(src):
    """画字的那几行里，出现了落在字幕带（> safe_bottom）的数字 → 返回它们。"""
    limit = subtitle.safe_bottom()
    hits = set()
    for line in (src or "").splitlines():
        if line.lstrip().startswith("//"):
            continue                                  # 注释里的数字不算
        if not TEXT_LINE.search(line):
            continue
        for m in NUM.finditer(line):
            v = int(m.group(1))
            # 886 往下是字幕带；再往上留一点，字有高度
            if limit < v <= 1080:
                hits.add(v)
    return sorted(hits)


# ---------------- 像素检查 ----------------

HUE_TOL = 35        # 色相离所有色板色都超过这么多度 = 新色相
SAT_MIN = 0.25      # 饱和度低于它算中性色，不参与色相判断
BRIGHT_MIN = 40     # 亮度低于它的像素色相没意义（近黑处抗锯齿会误判）
BAD_CELL = 0.001    # 单格新色相超过 0.1% 就报（全分辨率下约 20×20 像素，人看得见）
MIN_BOX = 0.42      # 内容框短边低于它就报「空」
EMPTY_CELL = 0.25   # 细节密度低于中位数的这个倍数算空白格
EDGE = 12.0         # 梯度幅值超过它算「有细节」


def _hue_gap(h, pal_hues):
    if not pal_hues:
        return np.zeros_like(h)
    diff = np.abs(h[:, None] - np.array(pal_hues)[None, :])
    return np.minimum(diff, 360 - diff).min(axis=1)


def frame_audit(project, shot, width=320):
    """量渲染出来的帧。返回 {problems, warnings, frames, ...}。"""
    pal_hex = _palette(project)
    if not pal_hex:
        return {"error": "项目没选画风（没有色板），先选一个预设"}
    pal = np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in pal_hex], dtype=np.float32)
    ph, ps = hue_sat(pal)
    pal_hues = [round(float(x), 1) for x, s in zip(ph, ps) if s >= SAT_MIN]
    pal_hues = [h for h in pal_hues if 0 <= h < 360]

    d = store.pdir(project) / "out" / f"{shot}_still"
    files = sorted(d.glob("t*.png")) if d.exists() else []
    if not files:
        return {"error": "没有帧，先抽帧"}

    out = {"problems": [], "warnings": [], "frames": [], "palette": pal_hex, "palette_hues": pal_hues}
    prev = None
    for f in files:
        im = Image.open(f).convert("RGB")
        h0 = round(im.height * width / im.width)
        im = im.resize((width, h0))
        a = np.asarray(im).astype(np.float32)
        px = a.reshape(-1, 3)

        hh, ss = hue_sat(px)
        chroma = (ss >= SAT_MIN) & (px.max(axis=1) >= BRIGHT_MIN)
        gap = np.zeros(len(px))
        if pal_hues and chroma.any():
            gap[chroma] = _hue_gap(hh[chroma], pal_hues)
        newhue = (chroma & (gap > HUE_TOL)).reshape(h0, width)
        gy, gx = np.array_split(np.arange(h0), 3), np.array_split(np.arange(width), 3)
        worst_cell = max(float(newhue[np.ix_(r, c)].mean()) for r in gy for c in gx)
        worst = []
        if newhue.any():
            q = (a[newhue] // 12).astype(np.int32)
            k = q[:, 0] * 4096 + q[:, 1] * 64 + q[:, 2]
            for kk, n in Counter(k.tolist()).most_common(3):
                col = (kk // 4096 * 12 + 6, (kk // 64 % 64) * 12 + 6, (kk % 64) * 12 + 6)
                worst.append("#%02X%02X%02X" % col)

        g = np.asarray(im.convert("L")).astype(np.float32)
        mag = np.maximum(np.abs(np.diff(g, axis=1, prepend=g[:, :1])),
                         np.abs(np.diff(g, axis=0, prepend=g[:1, :])))
        det = mag > EDGE
        tot = float(mag.sum())
        if tot > 0:
            yy, xx = np.mgrid[0:h0, 0:width]
            cmx = float((mag * xx).sum() / tot) / width
            cmy = float((mag * yy).sum() / tot) / h0
        else:
            cmx = cmy = 0.5
        if det.any():
            ys, xs = np.where(det)
            bw = (xs.max() - xs.min()) / width
            bh = (ys.max() - ys.min()) / h0
        else:
            bw = bh = 0.0
        dens = sorted(float(det[np.ix_(r, c)].mean()) for r in gy for c in gx)
        med = dens[len(dens) // 2] or 1e-6
        empty = sum(1 for x in dens if x < med * EMPTY_CELL)

        row = {"frame": f.name, "newhue_cell": round(worst_cell, 4),
               "max_gap": round(float(gap[chroma].max()), 1) if chroma.any() else 0,
               "box": [round(bw, 3), round(bh, 3)], "centroid": [round(cmx, 3), round(cmy, 3)],
               "empty_cells": empty, "worst": worst}
        if prev is not None:
            row["diff"] = round(float(np.abs(a - prev).mean()), 2)
        out["frames"].append(row)
        prev = a

    for r in out["frames"]:
        t = f"[{r['frame']}]"
        if r["newhue_cell"] > BAD_CELL:
            out["problems"].append(
                f"{t} 出现色板里没有的色相（占该区域 {r['newhue_cell']*100:.1f}%，"
                f"离最近色板色相差 {r['max_gap']:.0f}°）：{'、'.join(r['worst'][:2])}。"
                f"规则允许加减明暗和透明度，但不许引入新色相")
        if r["box"][0] < MIN_BOX or r["box"][1] < MIN_BOX:
            out["problems"].append(
                f"{t} 内容框只占画面 {r['box'][0]:.0%}×{r['box'][1]:.0%}。四周大片空白，主体要放大")
        cx, cy = r["centroid"]
        if abs(cx - 0.5) > 0.12 or abs(cy - 0.5) > 0.14:
            out["problems"].append(
                f"{t} 内容重心偏在 ({cx:.2f}, {cy:.2f})，构图不居中。要往中间收")
        elif r["empty_cells"] >= 4:
            out["warnings"].append(f"{t} 有 {r['empty_cells']} 格几乎没有细节，画面偏空")

    diffs = [r["diff"] for r in out["frames"] if "diff" in r]
    out["max_diff"] = max(diffs) if diffs else None
    cam = next((s.get("camera") for s in (store.load(project) or {}).get("shots", []) if s["id"] == shot), None)
    out["camera"] = cam
    if diffs:
        if cam == "停" and max(diffs) > 6:
            out["warnings"].append(
                f"标的是「停」但帧间差异最大 {max(diffs)}；画面自己在动是好的，"
                f"但主体位置或大小在变就是「该停的没停」")
        if max(diffs) < 1.0:
            out["problems"].append(f"帧间差异只有 {max(diffs)}，画面几乎是死的")
    return out
