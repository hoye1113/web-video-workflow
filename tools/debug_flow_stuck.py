"""调试：生图突然开始一直失败时，看页面上到底在说什么。

生图批量跑到第 9 页之后，每页都"240 秒没等到新图"。打开会话把现场打出来：
页面文字（找配额/报错提示）、图的数量和尺寸、按钮状态。
"""
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

DUMP = (
    "(()=>{const imgs=[...document.querySelectorAll('img')];"
    "const flow=imgs.filter(i=>i.src.includes('flow-content.google'));"
    "const txt=(document.body.innerText||'').replace(/\\n+/g,' | ');"
    "const bs=[...document.querySelectorAll('button')].map(b=>((b.getAttribute('aria-label')||'')+' '+"
    "(b.textContent||'')).trim()).filter(x=>x&&!/^[\\W]*$/.test(x)).slice(0,20);"
    "return {flow:flow.length,sizes:flow.map(i=>i.naturalWidth+'x'+i.naturalHeight).slice(-6),"
    " txt:txt.slice(0,700),buttons:bs};})()"
)

f = flowgen.Flow()
try:
    f.open()
    print("=== 进项目之后的现场 ===")
    print(f._run(DUMP))
    print()

    print("=== 试生成一次（提示词很简单，排除内容问题）===")
    t = f._type_prompt("暖色纸本插画，米白纸底留白多；一条细铅笔线从左到右，无文字无人脸。")
    print("输入：", t)
    time.sleep(2)
    c = f._click_generate()
    print("点生成：", c)
    for i in range(10):
        time.sleep(15)
        d = f._run(DUMP)
        if isinstance(d, dict):
            print(f"[{(i+1)*15:>3}s] flow={d['flow']} sizes={d['sizes']}")
            print("     文字：" + d["txt"][:260])
    print()
    print("=== 最后按钮状态 ===")
    print(f._run(DUMP).get("buttons"))
finally:
    print("（会话留在那儿，人工看一眼）" if "--keep" in sys.argv else "")
    if "--keep" not in sys.argv:
        f.close()
