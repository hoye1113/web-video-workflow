"""2.5D 视差样片：一张图 → 3 秒慢推 + 近远层位移 + 可选字幕/原声。

这不是 AI 视频，只是把一张图按“深度”做轻微位移：
底部/人物近，墙/窗远；近处动得多，远处动得少。
深度是启发式（底部近、顶部远、人物椭圆更近），只用于演示，不是精确深度图。

用法：
    python tools/parallax_shot.py <图片> <输出.mp4>
        [--seconds 3] [--fps 60] [--audio out/voice.wav] [--text "字幕"]
"""
import argparse
import math
import pathlib
import shutil
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H = 1920, 1080


def cover(im, w=W, h=H):
    ih, iw = im.shape[:2]
    k = max(w / iw, h / ih)
    nw, nh = int(round(iw * k)), int(round(ih * k))
    im = cv2.resize(im, (nw, nh), interpolation=cv2.INTER_CUBIC)
    x = (nw - w) // 2
    y = (nh - h) // 2
    return im[y:y + h, x:x + w]


def depth_map(im):
    h, w = im.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    # 顶部远、底部近：桌面/前景离镜头最近
    depth = 0.84 - 0.64 * np.power(yy / h, 1.15)
    # 人物椭圆：比桌子再近一档
    cx, cy = w * 0.46, h * 0.43
    ax, ay = w * 0.19, h * 0.34
    person = (((xx - cx) / ax) ** 2 + ((yy - cy) / ay) ** 2) < 1.0
    depth = np.where(person, 0.08, depth)
    # 平滑，避免硬边
    depth = cv2.GaussianBlur(depth, (0, 0), 28)
    return np.clip(depth, 0, 1)


def subtitle_layer(text, w=W, h=H):
    if not text:
        return None
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = None
    for p in (r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf",
              r"C:\Windows\Fonts\msyhbd.ttc"):
        if pathlib.Path(p).exists():
            try:
                font = ImageFont.truetype(p, 46)
                break
            except Exception:
                pass
    if font is None:
        font = ImageFont.load_default()
    box = d.textbbox((0, 0), text, font=font)
    tw, th = box[2] - box[0], box[3] - box[1]
    pad_x, pad_y = 34, 14
    bw, bh = tw + pad_x * 2, th + pad_y * 2
    x, y = (w - bw) // 2, h - 58 - bh
    d.rounded_rectangle([x, y, x + bw, y + bh], radius=18,
                        fill=(253, 249, 241, 238), outline=(170, 135, 100, 60), width=2)
    d.text((x + pad_x - box[0], y + pad_y - box[1]), text, font=font, fill=(43, 37, 32, 255))
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2BGRA)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("out")
    ap.add_argument("--seconds", type=float, default=3.0)
    ap.add_argument("--fps", type=int, default=60)
    ap.add_argument("--audio", default="")
    ap.add_argument("--text", default="")
    a = ap.parse_args(argv)

    src = cv2.imread(str(pathlib.Path(a.image)))
    if src is None:
        sys.exit(f"读不到图：{a.image}")
    im = cover(src)
    depth = depth_map(im)
    sub = subtitle_layer(a.text)
    h, w = im.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w * 0.5, h * 0.48
    n = max(2, int(round(a.seconds * a.fps)))

    ffmpeg = shutil.which("ffmpeg") or "ffmpeg"
    cmd = [ffmpeg, "-y", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}", "-r", str(a.fps), "-i", "-"]
    if a.audio and pathlib.Path(a.audio).exists():
        cmd += ["-i", a.audio, "-t", f"{a.seconds:.3f}", "-map", "0:v", "-map", "1:a",
                "-af", f"afade=t=out:st={max(0, a.seconds - 0.3):.3f}:d=0.3"]
    else:
        cmd += ["-t", f"{a.seconds:.3f}"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", a.out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL,
                         stderr=subprocess.PIPE)
    try:
        for i in range(n):
            t = i / (n - 1)
            e = t * t * (3 - 2 * t)                 # smoothstep
            scale = 1.0 + 0.045 * e                 # 慢推
            rel = 26.0 * math.sin(math.pi * t)      # 近远相对位移，峰值约 20px
            rel_y = 6.0 * math.sin(math.pi * t)
            cam_x = 12.0 * (e - 0.5)                # 整体轻微横移
            cam_y = 3.0 * (e - 0.5)
            map_x = (xx - cx) / scale + cx + (depth - 0.5) * rel + cam_x
            map_y = (yy - cy) / scale + cy + (depth - 0.5) * rel_y + cam_y
            frame = cv2.remap(im, map_x, map_y, cv2.INTER_CUBIC,
                              borderMode=cv2.BORDER_REFLECT)
            # 窗光轻微呼吸（只在右上更亮一点）
            if t > 0.1:
                glow = np.clip((xx - w * 0.55) / (w * 0.5), 0, 1) * np.clip((yy - h * 0.05) / (h * 0.6), 0, 1)
                frame = np.clip(frame.astype(np.float32) + glow[..., None] * (2.0 * math.sin(math.pi * t)), 0, 255).astype(np.uint8)
            if sub is not None:
                al = sub[..., 3:4].astype(np.float32) / 255.0
                frame = (frame.astype(np.float32) * (1 - al) + sub[..., :3].astype(np.float32) * al).astype(np.uint8)
            p.stdin.write(frame.tobytes())
    finally:
        p.stdin.close()
        err = p.stderr.read().decode("utf-8", "replace")
        code = p.wait()
    if code != 0:
        sys.exit(f"ffmpeg 失败：{err[-800:]}")
    print(f"✓ {a.out}  {a.seconds}s / {a.fps}fps / {w}x{h}")


if __name__ == "__main__":
    main(sys.argv[1:])
