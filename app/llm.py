"""LLM 层：走本机已有的 opencode，复用 OpenCode Go 的凭证。产品代码里不出现任何 key。

三条调用路径：
  generate(prompt)             一次性生成文本 —— 文案切镜头、写场景代码
  generate(prompt, files=[..]) 带图生成 —— 导演回路：让模型看渲出来的帧
  models()                     列出可用模型

实现上常驻一个私有 opencode server（起一次约 7 秒，之后每次调用只等模型），
起不来就退回 `opencode run --standalone`，慢一点但一定能跑。
"""
import json
import os
import subprocess
import threading
import time
from pathlib import Path

APPDATA = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
PORT = 47801

# 模型**写死**：这套东西绑定的是 OpenCode Go 的套餐，通过本机 opencode CLI 走。
# 不给界面切 provider / 切模型 —— 用户不需要知道有这回事，也没有别的凭证可用。
# 要换只改这一行。
MODEL = "opencode-go/deepseek-v4.1-flash"


def cli_path():
    """opencode CLI 在桌面版目录下，版本号会变，按版本挑最新的。"""
    base = APPDATA / "ai.opencode.desktop" / "cli"
    cands = sorted(base.glob("*/opencode-cli.exe")) if base.exists() else []
    if not cands:
        raise RuntimeError("找不到 opencode-cli.exe，请确认桌面版 OpenCode 已安装")
    return str(cands[-1])


class LLM:
    """调用 opencode 的封装。

    两个必须守住的点（都踩过）：
      - 私有 server 会跟着桌面版服务的重启一起死掉，所以**每次调用前**都要探活，不能只探一次。
      - 任何一次调用都要有总超时，否则会静默挂住整个请求（实测挂满 25 分钟）。
    """

    # 超时按输出长度分档：短输出（评审、切页）240 秒够；长输出（写/改场景代码，
    # 5000-9000 字）实测要 120-440 秒，给 600 秒。再超就是真出问题了。
    TIMEOUT = 240
    TIMEOUT_LONG = 600

    def __init__(self, model=MODEL):
        self.model = model
        self.proc = None
        self.password = None
        self.lock = threading.Lock()

    # ---------- 私有服务 ----------

    def _server_alive(self):
        if not (self.proc and self.proc.poll() is None and self.password):
            return False
        try:
            r = subprocess.run(
                [cli_path(), "api", "get", "/api/info", "--server", f"http://127.0.0.1:{PORT}"],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                env={**os.environ, "OPENCODE_PASSWORD": self.password}, timeout=15,
            )
        except subprocess.TimeoutExpired:
            return False
        return '"version"' in (r.stdout or "")

    def _start_server(self):
        self.password = None
        self.proc = subprocess.Popen(
            [cli_path(), "serve", "--hostname", "127.0.0.1", "--port", str(PORT)],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", bufsize=1,
        )
        deadline = time.time() + 60
        for line in self.proc.stdout:
            if "server password" in line:
                self.password = line.split()[-1].strip()
                break
            if time.time() > deadline:
                raise RuntimeError("opencode server 启动超时")

    def _ensure(self):
        """每次调用前都走一遍：活着就用，死了就重起。"""
        with self.lock:
            if self._server_alive():
                return
            self._start_server()
            for _ in range(40):
                if self._server_alive():
                    return
                time.sleep(0.5)
            raise RuntimeError("opencode 私有服务起不来（桌面版 OpenCode 可能正在重启，稍后再试）")

    # ---------- 调用 ----------

    def models(self):
        self._ensure()
        r = subprocess.run(
            [cli_path(), "api", "get", "/api/model", "--server", f"http://127.0.0.1:{PORT}"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            env={**os.environ, "OPENCODE_PASSWORD": self.password}, timeout=60,
        )
        try:
            return json.loads(r.stdout)
        except Exception:                          # noqa: BLE001
            return {"raw": (r.stdout or "")[:2000], "err": (r.stderr or "")[:500]}

    def _one_shot_cli(self, prompt, files=None, timeout=None):
        """退回方案：每次起一个私有 server 跑一次。"""
        cmd = [cli_path(), "run", "--standalone", "--model", self.model, "--format", "json"]
        for f in files or []:
            cmd += ["--file", str(f)]
        cmd.append(prompt)
        try:
            r = subprocess.run(cmd, capture_output=True, text=True,
                               encoding="utf-8", errors="replace",
                               timeout=timeout or self.TIMEOUT)
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"模型超过 {timeout or self.TIMEOUT} 秒没有返回，已中断") from None
        text = ""
        for line in (r.stdout or "").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
            except Exception:                      # noqa: BLE001
                continue
            if o.get("type") == "error":
                raise RuntimeError(str(o.get("error") or o)[:400])
            if o.get("type") == "text" and o.get("part", {}).get("text"):
                text += o["part"]["text"]
        if not text.strip():
            raise RuntimeError((r.stderr or r.stdout or "模型没有返回文本")[:800])
        return text

    def generate(self, prompt, files=None, model=None, timeout=None):
        """带文件时走 CLI 的 --file（generate 端点不收附件）；纯文本走常驻服务，最快。"""
        timeout = timeout or self.TIMEOUT
        if files:
            return self._one_shot_cli(prompt, files=files, timeout=timeout)
        try:
            self._ensure()
            body = {"prompt": prompt}
            if model or self.model:
                pid, _, mid = (model or self.model).partition("/")
                body["model"] = {"providerID": pid, "id": mid}
            try:
                r = subprocess.run(
                    [cli_path(), "api", "post", "/api/experimental/generate",
                     "--server", f"http://127.0.0.1:{PORT}", "-d", json.dumps(body)],
                    capture_output=True, text=True, encoding="utf-8", errors="replace",
                    env={**os.environ, "OPENCODE_PASSWORD": self.password}, timeout=timeout,
                )
            except subprocess.TimeoutExpired:
                raise RuntimeError(f"模型超过 {timeout} 秒没有返回，已中断") from None
            o = json.loads(r.stdout)
            if "data" in o and "text" in o["data"]:
                return o["data"]["text"]
            raise RuntimeError(str(o)[:600])
        except Exception as e:                     # noqa: BLE001
            print(f"[llm] 常驻服务这次不行（{e}），退回 CLI 再试一次", flush=True)
            return self._one_shot_cli(prompt, timeout=timeout)

    def stop(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
