"""渲染任务队列：起子进程跑 render.py / ffmpeg，把进度解析出来给前端。

一次只跑一个任务（渲染是 CPU 密集的，并行只会互相拖慢），排队的排在后面。
"""
import json
import os
import queue
import re
import shutil
import subprocess
import threading
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENGINE = ROOT / "base-arch" / "scripts" / "engine"
UV = shutil.which("uv") or str(Path.home() / ".local" / "bin" / "uv.exe")

PROG = re.compile(r"^(\d+)/(\d+)\b")


def _env():
    e = os.environ.copy()
    e["PYTHONUTF8"] = "1"                     # 绕开 Windows 下中文 JSON 的 GBK 解码坑
    e["PYTHONIOENCODING"] = "utf-8"
    return e


class Job:
    def __init__(self, kind, title, cmd=None, out_rel="", cwd=None, fn=None):
        self.id = uuid.uuid4().hex[:12]
        self.kind = kind
        self.title = title
        self.cmd = cmd
        self.fn = fn                     # 调用式任务：fn(job) 在队列线程里跑
        self.cwd = str(cwd or ENGINE)
        self.out = out_rel
        self.status = "queued"
        self.done_frames = 0
        self.total_frames = 0
        self.log = []
        self.error = ""
        self.result = None               # 调用式任务的结果，做完给前端取
        self.created = time.time()
        self.started = 0.0
        self.ended = 0.0

    def say(self, msg):
        self.log.append(str(msg))
        print(f"[job {self.id}] {msg}", flush=True)

    def step(self, i, n, label=""):
        self.done_frames, self.total_frames = i, n
        self.say(f"{i}/{n} {label}")

    def dict(self):
        prog = (self.done_frames / self.total_frames) if self.total_frames else (1.0 if self.status == "done" else 0.0)
        return {
            "id": self.id, "kind": self.kind, "title": self.title, "status": self.status,
            "progress": round(prog, 4), "frames": [self.done_frames, self.total_frames],
            "out": self.out, "log": self.log[-40:], "error": self.error, "result": self.result,
            "created": self.created, "started": self.started, "ended": self.ended,
            "elapsed": round((self.ended or time.time()) - self.started, 1) if self.started else 0,
        }


class Manager:
    def __init__(self):
        self.jobs = {}
        self.q = queue.Queue()
        self.lock = threading.Lock()
        threading.Thread(target=self._worker, daemon=True).start()

    # ---------- 对外 ----------

    def submit(self, kind, title, cmd, out_rel="", cwd=None):
        j = Job(kind, title, cmd, out_rel, cwd)
        with self.lock:
            self.jobs[j.id] = j
        self.q.put(j.id)
        return j

    def submit_fn(self, kind, title, fn):
        """跑一个 Python 函数式任务（导演回路这种要串好几步的）。"""
        j = Job(kind, title, fn=fn)
        with self.lock:
            self.jobs[j.id] = j
        self.q.put(j.id)
        return j

    def list(self):
        with self.lock:
            return [j.dict() for j in sorted(self.jobs.values(), key=lambda x: -x.created)]

    def get(self, jid):
        with self.lock:
            j = self.jobs.get(jid)
        return j.dict() if j else None

    def clear_finished(self):
        with self.lock:
            for k in [k for k, j in self.jobs.items() if j.status in ("done", "failed")]:
                del self.jobs[k]

    # ---------- 内部 ----------

    def _worker(self):
        while True:
            jid = self.q.get()
            with self.lock:
                j = self.jobs.get(jid)
            if not j:
                continue
            self._run(j)

    def _run(self, j):
        j.status = "running"
        j.started = time.time()
        try:
            if j.fn:
                j.fn(j)
            else:
                self._run_proc(j)
            j.status = "done"
            if j.total_frames:
                j.done_frames = j.total_frames
        except Exception as e:                                    # noqa: BLE001
            j.status = "failed"
            j.error = f"{type(e).__name__}: {e}"
            j.say(j.error)
        finally:
            j.ended = time.time()

    def _run_proc(self, j):
        p = subprocess.Popen(
            j.cmd, cwd=j.cwd, env=_env(),
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", bufsize=1,
        )
        for line in p.stdout:
            line = line.rstrip()
            if not line:
                continue
            j.log.append(line)
            m = PROG.match(line)
            if m:
                j.done_frames, j.total_frames = int(m.group(1)), int(m.group(2))
            else:
                print(f"[job {j.id}] {line}", flush=True)
        p.wait()
        if p.returncode != 0:
            raise RuntimeError("\n".join(j.log[-8:]) or f"退出码 {p.returncode}")

    # ---------- 具体的任务构造 ----------

    def render_shot(self, project, shot, dur, fps=30):
        out = ROOT / "projects" / project / "out" / f"{shot}.mp4"
        out.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            UV, "run", "--offline", "--with", "playwright", "python", str(ENGINE / "render.py"),
            "--film", f"demos/{project}", "--solo", shot,
            "--from", "0", "--to", f"{float(dur):g}", "--fps", str(int(fps)),
            "--no-counter", "--out", str(out),
        ]
        return self.submit("shot", f"{project} · 镜 {shot}", cmd, f"projects/{project}/out/{shot}.mp4")

    def render_still(self, project, shot, dur, at, fps=30):
        """渲单帧，给导演回路看画面用。**先清掉上一轮的帧**——不清的话评审会混两代画面。"""
        out = ROOT / "projects" / project / "out" / f"{shot}_still"
        if out.exists():
            for f in out.glob("t*.png"):
                f.unlink()
        out.mkdir(parents=True, exist_ok=True)
        cmd = [
            UV, "run", "--offline", "--with", "playwright", "python", str(ENGINE / "render.py"),
            "--film", f"demos/{project}", "--solo", shot,
            "--stills", ",".join(f"{t:g}" for t in at), "--no-counter", "--out", str(out),
        ]
        return self.submit("still", f"{project} · 镜 {shot} 抽帧", cmd, f"projects/{project}/out/{shot}_still")

    def concat(self, project, shots, name="成片.mp4"):
        """把渲染好的镜头拼成一条。"""
        d = ROOT / "projects" / project / "out"
        d.mkdir(parents=True, exist_ok=True)
        lst = d / f"_{name}.txt"
        files = [d / f"{s}.mp4" for s in shots if (d / f"{s}.mp4").exists()]
        if not files:
            raise ValueError("还没有渲染好的镜头")
        lst.write_text("".join(f"file '{f.as_posix()}'\n" for f in files), encoding="utf-8")
        out = d / name
        cmd = [
            "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
            "-r", "30", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-an", str(out),
        ]
        return self.submit("concat", f"{project} · 拼接 {len(files)} 镜", cmd,
                           f"projects/{project}/out/{name}", cwd=d)

    def probe_partial(self, project, shot, dur, fps=30, upto=1.2):
        """快速渲前 1.2 秒，用来快速看这镜"动不动起来"。"""
        out = ROOT / "projects" / project / "out" / "preview"
        out.mkdir(parents=True, exist_ok=True)
        cmd = [
            UV, "run", "--offline", "--with", "playwright", "python", str(ENGINE / "render.py"),
            "--film", f"demos/{project}", "--solo", shot,
            "--from", "0", "--to", f"{min(float(upto), float(dur)):g}", "--fps", str(int(fps)),
            "--no-counter", "--out", str(out / f"{shot}.mp4"),
        ]
        return self.submit("preview", f"{project} · 镜 {shot} 试渲", cmd,
                           f"projects/{project}/out/preview/{shot}.mp4")
