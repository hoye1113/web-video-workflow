"""把一组图拼成联络表（几列几行），用来一眼看整体风格。

用法：python tools/contact_sheet.py <输出图> <列数> <输入图...>
"""
import subprocess
import sys
from pathlib import Path

FFMPEG = "ffmpeg"


def sheet(out, files, cols=4, cell=620):
    files = [str(f) for f in files]
    n = len(files)
    rows = (n + cols - 1) // cols
    parts = [f"[{i}:v]scale={cell}:-1[v{i}]" for i in range(n)]
    tags = []
    for r in range(rows):
        idx = list(range(r * cols, min(n, (r + 1) * cols)))
        if len(idx) == 1:
            parts.append(f"[v{idx[0]}]null[rt{r}]")
        else:
            parts.append("".join(f"[v{i}]" for i in idx) + f"hstack=inputs={len(idx)}[rh{r}]")
        if len(idx) < cols:
            # 最后一行不满：补黑边到整行宽，否则 vstack 会因为宽度不一致报错
            parts.append(f"[rh{r}]pad=width={cols * cell}:height=ih:x=0:y=0:color=0x111111[rt{r}]")
        else:
            parts.append(f"[rh{r}]null[rt{r}]")
        tags.append(f"[rt{r}]")
    parts.append(f"[rt0]null[out]" if rows == 1
                 else "".join(tags) + f"vstack=inputs={rows}[out]")
    args = [FFMPEG, "-y", "-v", "error"]
    for f in files:
        args += ["-i", f]
    args += ["-filter_complex", ";".join(parts), "-map", "[out]", "-frames:v", "1", str(out)]
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(r.stderr[-800:])
    return out


if __name__ == "__main__":
    out = sys.argv[1]
    cols = int(sys.argv[2])
    files = sys.argv[3:]
    print("拼了", len(files), "张 →", sheet(out, files, cols))
