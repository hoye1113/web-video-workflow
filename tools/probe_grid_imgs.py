"""探针：项目网格里的 img 到底是什么 URL 结构（缩略图 vs 原图）。

要回答三件事：
  ① 网格里有没有 >=900 宽的原图 URL（还是全是缩略图）
  ② 原图 URL 长什么样（能不能靠 URL 认出来）
  ③ img 上有没有 srcset / currentSrc 线索

只读，不点生成、不下载。
"""
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

PROJECT = "https://flow.google.com/project/2423a8a2-2219-4dd5-83ea-563fd00a79fb"

JS = r"""
(()=>{const out=[];
for(const i of document.querySelectorAll('img')){
  const s=i.src||'';
  if(!/flow-content\.google|\/asb\//.test(s))continue;
  const r=i.getBoundingClientRect();
  out.push({
    n:i.naturalWidth+'x'+i.naturalHeight,
    src:s.slice(-100),
    srcset:(i.srcset||'').replace(/\s+/g,' ').slice(-140),
    cur:(i.currentSrc||'').slice(-100),
    top:Math.round(r.top), w:Math.round(r.width),
  });
}
return {total:out.length, imgs:out};})()
"""

f = flowgen.Flow(log=lambda *a: None)
try:
    out, _, _ = flowgen._bsk("session", "start", json_out=True, timeout=180)
    f.sid = json.loads(out).get("session_id")
    flowgen._bsk("window", "resize", "--session", f.sid, "--width", "1600", "--height", "900", timeout=60)
    flowgen._bsk("navigate", PROJECT, "--session", f.sid, timeout=180)
    time.sleep(9)
    print("会话:", f.sid)

    print("=== 滚一遍网格（懒加载） ===")
    for i in range(8):
        f._run(f"window.scrollTo(0, {i * 800})")
        time.sleep(1.0)
    f._run("window.scrollTo(0, 0)")
    time.sleep(1.5)

    d = f._run(JS)
    imgs = d.get("imgs", []) if isinstance(d, dict) else []
    print(f"\n=== 共 {len(imgs)} 张图 ===")
    for k, x in enumerate(imgs, 1):
        print(f"[{k:2d}] {x['n']:>11}  w={x['w']:<4} top={x['top']:<6} {x['src']}")
        if x.get("srcset"):
            print(f"      srcset: {x['srcset']}")
        if x.get("cur") and x["cur"] != x["src"]:
            print(f"      cur   : {x['cur']}")

    big = [x for x in imgs if int(x["n"].split("x")[0] or 0) >= 900]
    print(f"\n>=900 宽的（原图）：{len(big)} 张")
    for x in big[:8]:
        print("   ", x["n"], x["src"])
finally:
    print("\n会话保留：", f.sid, "（想看可以接着用）")
