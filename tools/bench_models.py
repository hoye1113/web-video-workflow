"""同一份「改代码」任务，换几个模型各跑一次，比输出速度和产出大小。

用法：python tools/bench_models.py
"""
import json
import sys
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import prompts                      # noqa: E402
import store                        # noqa: E402
from llm import LLM                 # noqa: E402

PROJ, SHOT = "marriage", "22"

# 一份真实的评审结果（实测拿到的），让各模型改同一处
REV = {
    "score": 8, "ok": False,
    "problems": [
        "玻璃内部那道白色弧形高光不在 5 色色板内，且压到了玻璃轮廓线上，不符合扁平线稿的画风。",
        "立柱两侧、玻璃外的地面上散落着沙点，读起来像沙子漏到了沙漏外面。",
        "沙漏只占画幅宽度约 1/4，左右各约 700px 纯背景空白。",
        "底座的地面阴影是正下方左右对称的椭圆，但玻璃高光在左上，阴影方向与光源不一致。",
    ],
    "fixes": [
        "把高光改成 #E9B872 的暖黄，或直接删掉，并确保它完全落在玻璃轮廓内侧。",
        "把地面上的散沙点全部删掉。",
        "把沙漏整体放大到占画幅宽度约 45%（把 HW 从 188 提到 300 左右）。",
        "把地面阴影改成偏右下（比如中心右移 60px），和左上的光源方向一致。",
    ],
}

MODELS = [
    "opencode-go/deepseek-v4.1-flash",
    "opencode-go/qwen3.8-flash",
    "opencode-go/glm-5.3-flash",
    "opencode-go/cat-jam-free",
]

results = {}


def go(mname):
    src = store.read_scene(PROJ, SHOT)
    prompt = prompts.REVISE.format(
        issues="\n".join(f"- {x}" for x in REV["problems"]),
        fixes="\n".join(f"- {x}" for x in REV["fixes"]),
        source=src,
    )
    t0 = time.time()
    try:
        out = LLM(model=mname)._one_shot_cli(prompt, timeout=900)
        dt = time.time() - t0
        results[mname] = {"sec": round(dt, 1), "chars": len(out), "empty": not out.strip()}
    except Exception as e:                                     # noqa: BLE001
        results[mname] = {"sec": round(time.time() - t0, 1), "err": str(e)[:160]}


def main():
    print(f"输入代码 {len(store.read_scene(PROJ, SHOT))} 字\n", flush=True)
    ths = [threading.Thread(target=go, args=(m,)) for m in MODELS]
    t0 = time.time()
    for t in ths:
        t.start()
    for t in ths:
        t.join()
    print(f"\n全部跑完，墙钟 {round(time.time()-t0)}s（并行跑的）\n")
    print(f"{'模型':<34}{'耗时':>8}{'字数':>8}   速度")
    for m in MODELS:
        r = results.get(m, {})
        if "err" in r:
            print(f"{m:<34}{r['sec']:>7}s{'—':>8}   失败: {r['err'][:60]}")
        else:
            cps = round(r["chars"] / r["sec"], 1) if r["sec"] else 0
            print(f"{m:<34}{r['sec']:>7}s{r['chars']:>8}   {cps} 字/秒")
    (ROOT / "experiments" / "bench_models.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
