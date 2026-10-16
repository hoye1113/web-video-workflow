#!/usr/bin/env python
"""扫描件 PDF → 文字（视觉模型逐页转写）。

**为什么有它**：`packages/core/src/materials.ts` 抽的是 PDF 的**文本层**，注释里写着
"there is no OCR" —— 扫描件会解析出近乎 0 字。它只能报一条警告，救不了。
这个工具就是那条补救路：把每页渲成图，交给**看图模型**逐页读成文字，
写成和它自己的解析结果同样格式的 `<名字>.pdf.md`，导演 agent 照常 `read`。

用法（在项目目录里跑，或把项目目录写在第一个参数）：

    uv run --with pymupdf python engine/tools/ocr-scan.py <项目目录> <文件名.pdf> [--dpi 150] [--model provider/id]

模型与密钥从 `~/.frametell/config.json` 里读（和面板同一份配置：自定义 OpenAI 兼容服务商）。
已经存在的 `<名字>.pdf.md` 会被备份成 `.bak` 再覆盖 —— 别悄悄吃掉别人的稿子。
"""
import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # type: ignore[attr-defined]

PAGE_PROMPT = """这是一份扫描资料的**第 {page} 页**（共 {total} 页）的图片。

把这一页里的**全部文字**转写成 Markdown：
- 照原文，一个字都不要改，不要总结、不要解释、不要补充
- 标题用 `#`/`##`，列表保留列表，表格用 Markdown 表格
- 数字、日期、金额、百分比必须准确（这是要拿去做片子的素材）
- 图片、图表、印章之类无法转成文字的内容，写一行 `[图：一句话描述]`
- 这页如果是空白或者只有图，就只输出那一行 `[图：…]`

只输出转写结果，不要别的话。"""


def load_model():
    """从 ~/.frametell/config.json 找到默认模型与它的服务商（baseUrl + key）。"""
    cfg_path = Path(os.environ.get("FRAMETELL_HOME", Path.home() / ".frametell")) / "config.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    model = (cfg.get("defaults") or {}).get("pageModel") or (cfg.get("defaults") or {}).get("model") or ""
    pid, _, mid = model.partition("/")
    for c in cfg.get("custom") or []:
        if c.get("id") == pid:
            key = (cfg.get("keys") or {}).get(pid) or ""
            base = c["baseUrl"].rstrip("/")
            return mid, base, key, model
    raise SystemExit(f"配置文件里找不到服务商 {pid}（defaults.model={model}）")


def transcribe(img_bytes: bytes, mid: str, base: str, key: str, page: int, total: int) -> str:
    b64 = base64.b64encode(img_bytes).decode()
    body = {
        "model": mid,
        "max_tokens": 8000,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": PAGE_PROMPT.format(page=page, total=total)},
                {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}},
            ],
        }],
    }
    req = urllib.request.Request(
        base + "/chat/completions", data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json",
                 "User-Agent": "frametell-ocr/0.1", "x-opencode-session": "frametell-ocr"})
    last = ""
    for attempt in range(3):                                  # 接口偶发抖动，退避重试
        try:
            with urllib.request.urlopen(req, timeout=300) as f:
                r = json.loads(f.read().decode("utf-8"))
            txt = (r["choices"][0]["message"].get("content") or "").strip()
            if txt:
                return txt
            last = "模型返回空"
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:200]}"
        except Exception as e:                                # noqa: BLE001
            last = f"{type(e).__name__}: {e}"
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(last)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir", help="项目目录（里面有 materials/）")
    ap.add_argument("file", help="materials/ 下的 PDF 文件名")
    ap.add_argument("--dpi", type=int, default=150, help="每页渲染精度（默认 150）")
    ap.add_argument("--model", default=None, help="覆盖模型 provider/id")
    a = ap.parse_args()

    import fitz                                               # pymupdf

    proj = Path(a.dir).resolve()
    src = proj / "materials" / a.file
    if not src.exists():
        raise SystemExit(f"没有这个文件：{src}")
    out = proj / "materials" / f"{a.file}.md"                  # 和 materials.ts 的 parsedTo 同一命名
    if out.exists():
        bak = out.with_suffix(out.suffix + ".bak")
        bak.write_bytes(out.read_bytes())
        print(f"  已存在的解析结果备份成 {bak.name}")

    mid, base, key, full = load_model()
    if a.model:
        mid = a.model.split("/", 1)[-1]
    print(f"  模型 {full}　服务商 {base}")
    print(f"  渲染 {a.file}（{a.dpi} dpi）…")

    doc = fitz.open(src)
    total = doc.page_count
    md = [f'<!-- frametell: parsed from "{a.file}" pages={total} -->', "",
          f"> 由视觉模型逐页转写（扫描件没有文字层）：`node engine/tools/ocr-scan.py`。原文一个字没改，拿不准的地方请对照原 PDF。", ""]
    chars = 0
    t0 = time.time()
    for i in range(total):
        page = doc.load_page(i)
        pix = page.get_pixmap(dpi=a.dpi)
        png = pix.tobytes("png")
        body = transcribe(png, mid, base, key, i + 1, total)
        md += [f"## 第 {i + 1} 页", "", body, ""]
        chars += len(body)
        print(f"  第 {i+1}/{total} 页　{len(body)} 字　（累计 {chars} 字，{time.time()-t0:.0f}s）")
    doc.close()

    out.write_text("\n".join(md), encoding="utf-8")
    print(f"\n写好 {out}")
    print(f"共 {total} 页 / {chars} 字 —— 现在导演 agent 读到的就是这份")


if __name__ == "__main__":
    main()
