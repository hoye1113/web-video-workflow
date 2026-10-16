"""调试：点了生成之后，页面上到底在发生什么。"""
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

DUMP = (
    "(()=>{const imgs=[...document.querySelectorAll('img')];"
    "const flow=imgs.filter(i=>i.src.includes('flow-content.google'));"
    "const big=imgs.filter(i=>i.naturalWidth>400);"
    "const txt=(document.body.innerText||'').replace(/\\n+/g,' | ').slice(0,400);"
    "return {imgs:imgs.length,flow:flow.length,big:big.length,"
    "  flowSizes:flow.map(i=>i.naturalWidth+'x'+i.naturalHeight).slice(0,6),"
    "  txt:txt};})()"
)

f = flowgen.Flow()
try:
    f.open()
    print("=== 点生成之前 ===")
    print(f._run(DUMP))
    print()
    t = f._type_prompt("暖色纸本插画，平涂加细铅笔线，米白纸底留白多；一只手捏着纸的折角，无文字无人脸。")
    print("输入：", t)
    time.sleep(2)
    c = f._click_generate()
    print("点生成：", c)
    print()
    for i in range(12):
        time.sleep(10)
        d = f._run(DUMP)
        if isinstance(d, dict):
            print(f"[{(i+1)*10:>3}s] img={d['imgs']} flow={d['flow']} big={d['big']} sizes={d['flowSizes']}")
            if i in (0, 4, 11):
                print("     页面文字：", d["txt"][:220])
        else:
            print(f"[{(i+1)*10:>3}s] 取样失败：{d}")
finally:
    f.close()
