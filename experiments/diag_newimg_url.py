"""抓一张新图的 URL 形状：生成前记下网格顶部的图，生成后再记一次，比对差集。

用法：python experiments/diag_newimg_url.py
"""
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
sys.path.insert(0, str(ROOT / "tools"))

import flowgen                                          # noqa: E402
from gen_scenes import full_prompt                      # noqa: E402

PROJECT = "https://flow.google.com/project/2423a8a2-2219-4dd5-83ea-563fd00a79fb"
SCENE = ("一个男孩站在门口，一只手扶着门框，脚没有迈出去；"
         "走廊的光从背后打进来，主体占画面中部")

TOP = r"""(()=>{
  const rows=[];
  for(const el of document.querySelectorAll('img')){
    const u=el.src||'';
    if(!u) continue;
    rows.push({u:u, w:el.naturalWidth, h:el.naturalHeight});
  }
  return JSON.stringify(rows);
})()"""


def main():
    f = flowgen.Flow(log=lambda *a: print("   ", *a, flush=True))
    try:
        f.enter(PROJECT)
        time.sleep(3)
        before = f._run(TOP)
        before = json.loads(before) if isinstance(before, str) else before
        print("before imgs:", len(before))
        for r in before[:4]:
            print("   ", r["w"], "x", r["h"], r["u"][:150])

        f.attach_character("小树")
        t = f._type_prompt(full_prompt(SCENE))
        print("typed ok:", t.get("ok"), t.get("len"))
        c = f._click_generate()
        print("click:", c)
        t0 = time.time()
        seen = None
        while time.time() - t0 < 180:
            time.sleep(8)
            now = f._run(TOP)
            now = json.loads(now) if isinstance(now, str) else now
            tail = (f._run("(()=>document.body.innerText.slice(-160))()") or "")
            print(f"  {int(time.time()-t0):>3}s imgs={len(now)} tail={str(tail)[-90:]!r}")
            if "Thinking" in str(tail) or "stop" in str(tail):
                seen = now
        now = f._run(TOP)
        now = json.loads(now) if isinstance(now, str) else now
        b = {r["u"] for r in before}
        n = {r["u"] for r in now}
        print("=== 新出现的 URL（差集）===")
        for u in sorted(n - b):
            print("   ", u[:200])
        print("=== 消失的 URL ===")
        for u in sorted(b - n)[:5]:
            print("   ", u[:160])
        print("=== 生成后网格前 4 张 ===")
        for r in now[:4]:
            print("   ", r["w"], "x", r["h"], r["u"][:150])
    finally:
        f.close()


if __name__ == "__main__":
    main()
