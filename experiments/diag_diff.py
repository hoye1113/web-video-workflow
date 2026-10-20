"""用 flowgen 自己的那套函数（_GET_IMGS / _image_bases / known）复现一次检测。

用法：python experiments/diag_diff.py
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
SCENE = ("一个女孩背对镜头坐在窗边的椅子上，一部亮着的手机屏幕朝上放在旁边的桌角，"
         "她没有看它；窗口的冷白光照在地板上，屋里很暗，主体占画面中部")


def main():
    f = flowgen.Flow(log=lambda *a: print("   ", *a, flush=True))
    try:
        f.enter(PROJECT)
        print("known(enter):", len(f.known))
        f.attach_character("小芽")
        print("known(after attach):", len(f.known))
        before = set(f.known)
        f._type_prompt(full_prompt(SCENE))
        f.baseline_sigs()
        c = f._click_generate()
        print("click:", c)
        t0 = time.time()
        while time.time() - t0 < 150:
            time.sleep(6)
            raw = f._run(flowgen._GET_IMGS)
            cur = f._image_bases()
            fresh = sorted(set(cur) - before)
            print(f"  {int(time.time()-t0):>3}s raw_type={type(raw).__name__} "
                  f"raw_len={len(raw) if isinstance(raw, list) else 'NA'} "
                  f"cur={len(cur)} fresh={len(fresh)}")
            if fresh:
                print("   fresh base[:60]:", fresh[0][:60])
                print("   raw[0][:120]:", (raw[0][:120] if raw else ""))
                break
    finally:
        f.close()


if __name__ == "__main__":
    main()
