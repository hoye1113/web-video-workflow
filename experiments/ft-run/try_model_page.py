"""验证：把 FRAMETELL 的提示词原文喂给 OpenCode Go 的 deepseek-v4.1-flash，
让它写一页 pages/p09.js —— 然后拿它自己的检查器验。

这一步回答的是："模型是不是瓶颈"。如果它能写出过检查的页面，
那这套架构就成立：模型只做决策，引擎保证下限。
"""
import io
import json
import sqlite3
import sys
import urllib.request
import urllib.error
from pathlib import Path
from os.path import expanduser

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

FT = Path(r"D:\WorkSpace\video-factory\experiments\frametell-src\frametell-main")
OUT = Path(r"D:\WorkSpace\video-factory\experiments\ft-run\实验-情感\pages\p09.js")

key = json.loads(sqlite3.connect(
    "file:" + expanduser("~/.local/share/opencode/opencode.db") + "?mode=ro",
    uri=True).execute("select value from credential limit 1").fetchone()[0])["key"]

PAGE = (FT / "packages/agent/prompts/PAGE.md").read_text(encoding="utf-8")
API = (FT / "packages/agent/prompts/API.md").read_text(encoding="utf-8")
GRAMMAR = (FT / "packages/engine/styles/warm-story/GRAMMAR.md").read_text(encoding="utf-8")
LIB = (FT / "packages/agent/prompts/LIB.md").read_text(encoding="utf-8")

SYSTEM = f"""# Frametell · Page agent (one page at a time)

{PAGE}

---

{API}

---

## This film's style: warm-story

{GRAMMAR}

---

{LIB}

---

## 这一部片子的组件（已经拷进项目，直接用，不用再 use-extra）

`extras/warm.js`：`ground` 地面 / `snowball` 雪球 / `jar` 罐子 / `coin` 硬币 / `tree` 树 /
`trail` 山路 / `hand` 手（无脸）/ `calendar` 台历 / `tag` 数字标签（可数到某个词）

页文件写在 `pages/<id>.js`，第一行是 `ENGINE.visual('<id>', (P) => {{ ... }});`
只输出这一个文件的完整代码，不要 Markdown 围栏，不要解释。
"""

USER = """这一页：

- id：`p09`
- 段落：案例之前 · 无波无澜
- 页标题：婚姻在出事之前，早就进入了无波无澜的状态
- 旁白（cue 0 起）：
  0. 很多人以为婚姻的危机是从出轨那天开始的，
  1. 但真正出问题的时间要早得多，
  2. 早到两个人自己都没察觉 ——
  3. 日子照过，只是没什么话可说了。
- 这一页要说清的一件事：**出事之前，婚姻早就进入了"无波无澜"**

分镜（每一拍：什么东西 / 做什么动作 / 镜头 / 屏上什么字）：
- c0：一条水平的水面（物体：一条平的水面线）—— 一点波动都没有 —— 固定 —— 无
- c1：两个人的位置（物体：两个小圆点）—— 从中间慢慢往两边分开，距离越拉越远 —— 固定 —— 无
- c2：两个人之间（物体：那条被拉开的空隙）—— 中间落下一行字，说明这不是吵架，是没话说 —— 推近 —— 「没话可说」

这一页画的是抽象状态（不是具体场景），用几何和水面来做。
时间一律用 `P.c(i)` / `P.ce(i)` / `P.endT`，不要写死秒数。
现在写 `pages/p09.js`。"""

body = {
    "model": "deepseek-v4.1-flash",
    "max_tokens": 32000,
    "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": USER}],
}
req = urllib.request.Request(
    "https://opencode.ai/inference/go/openai/v1/chat/completions",
    data=json.dumps(body).encode(),
    headers={"Authorization": "Bearer " + key, "Content-Type": "application/json",
             "User-Agent": "video-factory/0.1", "x-opencode-session": "vf-page-test"},
)
print("问模型要一页代码（提示词约 %d 字）…" % (len(SYSTEM) + len(USER)))
try:
    with urllib.request.urlopen(req, timeout=600) as f:
        r = json.loads(f.read().decode())
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:400]); sys.exit(1)

msg = r["choices"][0]["message"]
text = (msg.get("content") or "").strip()
if text.startswith("```"):
    text = "\n".join(text.splitlines()[1:])
    text = text.rsplit("```", 1)[0]
usage = r.get("usage") or {}
print("用量：", json.dumps(usage, ensure_ascii=False))
print("输出 %d 字 / %d 行" % (len(text), len(text.splitlines())))
OUT.write_text(text + "\n", encoding="utf-8")
print("写到", OUT)
print("--- 前 8 行 ---")
print("\n".join(text.splitlines()[:8]))
