"""往 `projects/<片>/events.jsonl` 追加一条事件（面板读它渲染"过程"）。

用法：
    python tools/emit.py <片名> <事件.json>

事件.json 是一个 UTF-8 文件，内容是 pipeline.emit 的关键字参数，例如：
    {"kind": "stage", "stage": "分镜", "status": "done", "detail": "26 页"}

为什么要单独一个工具：**中文不要进命令行**（Windows 的壳会把中文弄乱），
所以正文一律走 UTF-8 文件。
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import pipeline                                            # noqa: E402


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    proj = sys.argv[1]
    payload = json.loads(pathlib.Path(sys.argv[2]).read_text(encoding="utf-8"))
    kind = payload.pop("kind", "log")
    rec = pipeline.emit(proj, kind, **payload)
    print(json.dumps(rec, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
