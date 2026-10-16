"""量一张生成图：主体是什么、外接框在哪。

**为什么要量**：评审每轮都在挑"主体太小""重心偏在一侧"，
而这两条**是能量出来的**。量出来之后，场景代码就能用 `MD.cover` 的
`z` / `fx` / `fy` 把主体摆到画面中间、放到该有的尺寸 —— 不用重新生图。

做法：把图丢给模型问四个数（0-1 相对坐标，见下），结果存进项目里，
写场景代码时当成**已知条件**交给它（"主体在 (0.72, 0.60)，外接框 0.22×0.18"），
模型就不用猜了。

判断依据是模型的眼（"画的是什么、哪个是主体"），数值是死板的四个数 ——
量一次存下来，后面每次写代码、每次评审都用同一份，不会飘。
"""
import json
from pathlib import Path

import store

PROMPT = """这是一张给视频用的插画。告诉我画面里**最主要的那个东西**在哪。

只输出一个 JSON，不要别的话：

{"subject": "主体是什么（一句短话，中文）", "box": [x, y, w, h]}

box 是**相对坐标**，四个数都在 0 到 1 之间：
  x = 主体最左边离画面左边多远
  y = 主体最上边离画面上边多远
  w = 主体有多宽　　h = 主体有多高
（整幅画面宽是 1、高是 1。比如主体在正中间、占画面四分之一，就是 [0.375, 0.375, 0.25, 0.25]）

"主体"是**你要让观众一眼看到的那一个东西**（手、人、物件），
不是纸面、不是背景、不是大片的留白。留白不算主体。
如果画面上有几个东西，挑**最重要**的那一个。
"""


def _clamp01(v, d=0.5):
    try:
        return min(1.0, max(0.0, float(v)))
    except (TypeError, ValueError):
        return d


def parse(text):
    """从模型输出里抠出 {subject, box}。抠不出来返回 None。"""
    import text as T
    obj = T.extract_json(text or "", dict)
    if not obj:
        return None
    box = obj.get("box") or []
    if not isinstance(box, list) or len(box) != 4:
        return None
    x, y, w, h = (_clamp01(v) for v in box)
    if w <= 0.02 or h <= 0.02:
        return None
    if x + w > 1.0:
        w = 1.0 - x
    if y + h > 1.0:
        h = 1.0 - y
    return {"subject": str(obj.get("subject") or "").strip()[:60],
            "box": [round(x, 3), round(y, 3), round(w, 3), round(h, 3)]}


def of(project, shot, ai=None, say=print, force=False):
    """拿这一页主图的主体框。**量过就复用**（量一次要调模型，别每次都量）。"""
    m = store.load(project) or {}
    s = next((x for x in m.get("shots", []) if x["id"] == shot), None)
    if not s:
        raise ValueError(f"没有第 {shot} 页")
    if s.get("subjectBox") and not force:
        return {"subject": s.get("subject") or "", "box": s["subjectBox"]}

    imgs = s.get("images") or []
    if not imgs:
        return None
    p = store.pdir(project) / "assets" / imgs[0]
    if not p.exists():
        return None

    if ai is None:
        import llm
        ai = llm.LLM()
    say(f"量一下这张图：主体在哪、多大（{imgs[0]}）…")
    got = parse(ai.generate(PROMPT, files=[str(p)], timeout=300))
    if not got:
        say("没量出来（模型没给出能用的框），后面按默认构图走")
        return None
    store.patch_shot(project, shot, subject=got["subject"], subjectBox=got["box"])
    x, y, w, h = got["box"]
    say(f"主体：{got['subject']}　外接框 {w:.0%}×{h:.0%}　中心 ({x+w/2:.2f}, {y+h/2:.2f})")
    return got


def framing(box, iw=1376, ih=768, frame=(1920, 1080), fill=0.46, zmax=1.35):
    """主体框 → 铺图参数 (z, fx, fy)，外加一句老实话。

    用 `MD.cover(c, IMG[P], {z, fx, fy})` 时：
      - `z`  = 相对"刚好铺满"再放大多少倍；
      - `fx` = **让图上相对位置 fx 的那个点，落在画面同样的相对位置**。
        所以传 fx=0.5 是"以中间为焦点"，不是"把主体摆到中间"。

    要把主体从 c 挪到画面正中，图上得有多余的料可裁：推导下来需要
    `z >= 0.5 / (1 - c)`（c 在右半边）。**c=0.86 时这要求放大 3.57 倍** ——
    1376 宽的图放到 3.57 倍就是糊的。
    所以：**构图歪是裁不回来的，只能在生图时摆正**（见 imagePrompt 的构图要求）。
    这里只做能做的部分：主体够小就推近一点，并在 note 里说明差多少。
    """
    x, y, w, h = box
    W, H = frame
    s0 = max(W / iw, H / ih)
    aw, ah = iw * s0 / W, ih * s0 / H            # 铺满时，图相对画面的尺寸（>=1）
    cx, cy = x + w / 2, y + h / 2

    z_fill = fill / max(w * aw, h * ah)          # 让主体长边占到 fill
    z = min(zmax, max(1.0, z_fill))
    wd, hd = aw * z, ah * z

    def axis(c, d):
        if abs(1 - d) < 1e-6:
            return 0.5
        return min(1.0, max(0.0, (0.5 - c * d) / (1 - d)))

    fx, fy = axis(cx, wd), axis(cy, hd)
    # 把主体挪到正中需要的倍数（大得离谱就说明这张图构图不行，别硬裁）
    need_x = 0.5 / (1 - cx) if cx > 0.5 else (0.5 / cx if cx > 0 else 99)
    need_y = 0.5 / (1 - cy) if cy > 0.5 else (0.5 / cy if cy > 0 else 99)
    note = ""
    if max(need_x, need_y) > zmax * 1.6:
        note = (f"主体偏在 ({cx:.2f}, {cy:.2f})，要挪到正中得放大 {max(need_x, need_y):.1f} 倍"
                f"——裁不回来，这一页的构图问题只能记在生图上")
    return round(z, 3), round(fx, 3), round(fy, 3), note


if __name__ == "__main__":
    import sys
    print(json.dumps(of(sys.argv[1], sys.argv[2], force=True), ensure_ascii=False))
