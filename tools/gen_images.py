"""批量生图（命令行版）。跟服务里的 /api/images 走同一个函数。

用法：
  python tools/gen_images.py <项目>            # 自动挑缺图的 image/mixed 页
  python tools/gen_images.py <项目> 01 02 03   # 只生这几页
"""
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402


class Echo:
    """假装是 jobs.Job，好让 do_images 的 say/step 直接打到屏幕。"""

    def __init__(self):
        self.result = None

    def say(self, msg):
        print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

    def step(self, i, n, label=""):
        pass


if __name__ == "__main__":
    proj = sys.argv[1] if len(sys.argv) > 1 else "marriage_full"
    only = sys.argv[2:] or None
    t0 = time.time()
    job = Echo()
    try:
        job.result = flowgen.do_images(proj, only, job)
    finally:
        print(f"总耗时 {time.time() - t0:.0f}s", flush=True)
    r = job.result or {}
    print(f"成功 {len(r.get('done', []))} 页，失败 {len(r.get('failed', []))} 页", flush=True)
    for f in r.get("failed", []):
        print(f"  ✗ 页 {f['shot']}：{f['error'][:120]}", flush=True)
