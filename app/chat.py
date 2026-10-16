"""聊天接口：按 Vercel AI SDK 的 UI message stream 协议输出，给 assistant-ui 直接用。

为什么走这个协议：`@assistant-ui/react-data-stream` 的 `useDataStreamRuntime` 认它，
前端一行 `useDataStreamRuntime({ api: "/api/chat", onData })` 就能得到
聊天线程 + 流式 + 自定义数据部件（`data-*`），不用自己写运行时胶水。

协议长这样（SSE，每行 `data: <json>`）：

    data: {"type":"start"}
    data: {"type":"text-delta","id":"t0","delta":"你好"}
    data: {"type":"data-page","data":{"shot":"02","status":"rendering"}}   ← 驱动界面的自定义部件
    data: {"type":"finish"}
    data: [DONE]

响应头必须是 `x-vercel-ai-ui-message-stream: v1`，它据此识别协议。

为什么不让前端直连 opencode：
  ① 桌面版 opencode 的服务要鉴权，而 SDK 生成的 client 不带鉴权头（OpenAPI 里 securitySchemes 是空的）
  ② SDK 的 createOpencodeServer 等的服务横幅是 `opencode server listening`，
     桌面版 CLI 打的是 `server listening`，对不上
  ③ 我们的 Python 后端已经会用 CLI 跟 opencode 通信（这条是通的），
     让后端当中转，前端永远不用碰鉴权和 CORS
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UV = shutil.which("uv") or str(Path.home() / ".local" / "bin" / "uv.exe")


def _cli():
    import llm
    return llm.cli_path()


def sse(obj):
    """一帧 SSE。obj 是字符串时原样发（比如 [DONE]）。"""
    body = obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False)
    return f"data: {body}\n\n".encode("utf-8")


def stream(project, message, write, model=None):
    """把一次对话按 UI message stream 协议吐出去。

    write(chunk: bytes) 由调用方提供（写进 HTTP 响应）。
    """
    import prompts as P
    import store
    if model is None:
        import llm
        model = llm.MODEL

    m = store.load(project) or {}
    shots = m.get("shots", [])
    def _line(s):
        mode = s.get("mode") or "code"
        if mode in ("image", "mixed"):
            mode += "·有图" if s.get("images") else "·缺图"
        return f'  {s["id"]}  {mode}  {s.get("dur")}s  {s.get("title","")}'
    state = "\n".join(_line(s) for s in shots[:40]) or "  （还没有页面）"
    style = m.get("style") or {}

    prompt = f"""你是这条片子的导演助手。用户会让你改动画面、渲染、或者问进展。

## 现在的状态
项目：{project}（{m.get('title','')}）
画风：{style.get('name') or '未选'}　{style.get('look') or ''}
骨架：{'  →  '.join(m.get('skeleton') or []) or '（还没定）'}
页面（{len(shots)} 页）：
{state}

## 用户说
{message}

## 怎么回
先用一两句话说你打算做什么，然后**只输出一个 JSON**（不要代码块围栏）：

{{"say": "你的回话（口语，别学术）", "actions": [{{"op": "操作名", "shot": "页号"}}]}}

可用的操作：
  list_pages                     列页面和状态
  write_scene   shot             给这一页写场景代码
  render_shot   shot             渲这一页
  review_shot   shot             抽帧并评审
  gen_images    shot 或 shots    按 imagePrompt 去生图（不传页号就是把缺的图都生出来）
  write_scenes  shot 或 shots    写场景代码（不传页号就是把还没写的页都写了）
  image_audit                    生图体检：量主体位置大小，构图不合格的带着修正要求重画
  render_film                    全部渲完并拼接（整片出片）

说话要短。不确定就先问，actions 留空数组。"""

    write(sse({"type": "start"}))
    write(sse({"type": "data-status", "data": {"text": "模型在想…"}}))

    cmd = [_cli(), "run", "--standalone", "--model", model, "--format", "json", prompt]
    text = ""
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             text=True, encoding="utf-8", errors="replace", bufsize=1)
        for line in p.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
            except Exception:                                  # noqa: BLE001
                continue
            if o.get("type") == "error":
                write(sse({"type": "data-status", "data": {"text": "模型报错：" + str(o.get("error"))[:200]}}))
            if o.get("type") == "text" and o.get("part", {}).get("text"):
                text += o["part"]["text"]
        p.wait()
    except Exception as e:                                     # noqa: BLE001
        write(sse({"type": "text-delta", "id": "t0", "delta": f"\n\n出错了：{e}"}))
        write(sse({"type": "finish"}))
        write(sse("[DONE]"))
        return

    # 模型给的是 "先说一句 + 一个 JSON"，拆开发
    say, actions = _split(text)
    if say:
        write(sse({"type": "text-delta", "id": "t0", "delta": say}))
    if actions:
        # 自定义数据部件：前端 onData 收到就会去刷新对应面板
        write(sse({"type": "data-actions", "data": {"actions": actions}}))
    write(sse({"type": "finish"}))
    write(sse("[DONE]"))


def _split(text):
    """把模型的输出拆成 (要说的话, 操作列表)。JSON 抠不出来就整段当话说。"""
    import text as T
    t = (text or "").strip()
    i = t.find("{")
    j = t.rfind("}")
    if i >= 0 and j > i:
        try:
            o = json.loads(t[i:j + 1])
        except Exception:                                      # noqa: BLE001
            try:
                o = json.loads(T.repair_json(t[i:j + 1]))
            except Exception:                                  # noqa: BLE001
                return t, []
        say = (o.get("say") or "").strip()
        acts = o.get("actions") or []
        if not say and not acts:
            return t, []
        return say or t[:i].strip(), acts
    return t, []
