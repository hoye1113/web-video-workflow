"""像人一样在实习工作台上操作（bsk 真实点击），直到出片。

    python tools/intern_web.py --new "主题…" --minutes 3      # 打开页面、填表、点「开始做视频」
    python tools/intern_web.py --click-map                    # 等到分镜出来 → 点确认
    python tools/intern_web.py --click-img                    # 等到图出来 → 点「都可以，去出片」
    python tools/intern_web.py --click-film                   # 等到成片 → 点「可以，就这样」
    python tools/intern_web.py --watch                        # 一次盯到底，出现哪个确认就点哪个

会话死了（bsk 空闲 10 分钟会自动回收）会自动重建，并回到上次那条片子的页面。
"""
import argparse
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen                                              # noqa: E402

BASE = "http://127.0.0.1:8900"
STATE = ROOT / "experiments" / "uitest" / "intern-web-session.json"


def load_state():
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except Exception:                                      # noqa: BLE001
            pass
    return {}


def save_state(**kw):
    st = load_state()
    st.update(kw)
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(st, ensure_ascii=False), encoding="utf-8")


def alive(f):
    return f._run("1") == 1


def new_session():
    out, _, _ = flowgen._bsk("session", "start", json_out=True, timeout=180)
    sid = json.loads(out).get("session_id")
    if not sid:
        raise RuntimeError("开 bsk 会话失败")
    save_state(sid=sid)
    return sid


def open_page(film=None):
    """保证有一个活着的会话，并把页面开到片子（或首页）。"""
    f = flowgen.Flow(log=print)
    f.sid = load_state().get("sid") or new_session()
    flowgen._bsk("window", "resize", "--session", f.sid, "--width", "1600", "--height", "900", timeout=60)
    if not alive(f):
        print("  会话已过期，重开一个…", flush=True)
        f.sid = new_session()
        flowgen._bsk("window", "resize", "--session", f.sid, "--width", "1600", "--height", "900", timeout=60)
    url = BASE + ("/#/f/" + film if film else "/#/")
    flowgen._bsk("navigate", url, "--session", f.sid, timeout=120)
    time.sleep(4)
    return f


def js(f, code):
    return f._run(code)


def wait_text(f, needle, timeout=120):
    t0 = time.time()
    while time.time() - t0 < timeout:
        if js(f, f"document.body.innerText.includes({json.dumps(needle)})") is True:
            return True
        time.sleep(2)
    return False


def click_by_text(f, text, tag="button"):
    """在页面上找文字匹配的按钮，打标后用 bsk 真实点击；点完验证页面确实变了。"""
    hit = js(f, (
        "(()=>{const b=[...document.querySelectorAll(" + json.dumps(tag) + ")]"
        ".find(x=>((x.textContent||'').trim()).includes(" + json.dumps(text) + ")&&!x.disabled);"
        "if(!b)return 'not found';b.setAttribute('data-vf-click','1');"
        "return (b.textContent||'').trim().slice(0,30);})()"
    ))
    if hit == "not found":
        return False
    flowgen._bsk("click", "--session", f.sid, "--selector", "[data-vf-click='1']", timeout=120)
    return True


def shot(f, name):
    p = ROOT / "experiments" / "uitest" / name
    flowgen._bsk("screenshot", "--session", f.sid, "--out", str(p), timeout=120)
    print("    截图：", p.relative_to(ROOT), flush=True)


def form(f, topic, minutes):
    js(f, "(()=>{const t=document.getElementById('topic');t.focus();t.value='';return true;})()")
    got = js(f, (
        "(()=>{const t=document.getElementById('topic');"
        "const set=Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set;"
        "set.call(t," + json.dumps(topic) + ");t.dispatchEvent(new Event('input',{bubbles:true}));"
        "const m=document.getElementById('minutes');"
        "const i=[...m.options].findIndex(o=>parseFloat(o.value)===" + str(float(minutes)) + ");"
        "if(i>=0){m.selectedIndex=i;m.dispatchEvent(new Event('change',{bubbles:true}));}"
        "return {topic:t.value.length, minutes:m.value};})()"
    ))
    print("  表单读回：", got, flush=True)
    if not isinstance(got, dict) or float(got.get("minutes") or 0) != float(minutes):
        raise RuntimeError(f"表单没填对：{got}")
    shot(f, "web-01-form.png")
    print("  点「开始做视频」…", flush=True)
    if not click_by_text(f, "开始做视频"):
        raise RuntimeError("找不到「开始做视频」按钮")
    for _ in range(30):
        time.sleep(2)
        h = js(f, "location.hash")
        if isinstance(h, str) and "#/f/" in h:
            film = h.split("#/f/")[-1]
            save_state(film=film)
            print("  已进入进度页：", film, flush=True)
            shot(f, "web-02-started.png")
            return film
    raise RuntimeError("点了开始但没进入进度页")


def do_click(f, film, text, shot_name, timeout):
    """等到按钮出现 → 点 → 验证（分镜：队列出现；图/片：闸门变 ok）。"""
    if not wait_text(f, text, timeout):
        print(f"  ⏰ 等「{text}」超时", flush=True)
        return False
    shot(f, shot_name)
    for attempt in range(3):
        if click_by_text(f, text):
            print(f"  → 点了「{text}」（第 {attempt + 1} 次）", flush=True)
            time.sleep(4)
            return True
        # 按钮可能被上一次点击禁用了：刷新再试
        print("  按钮不可点（可能已点过/被禁用），刷新页面…", flush=True)
        flowgen._bsk("navigate", BASE + "/#/f/" + film, "--session", f.sid, timeout=120)
        time.sleep(4)
    return False


def watch(f, film):
    for i in range(360):
        time.sleep(10)
        if not alive(f):
            print("  会话过期，重开…", flush=True)
            f.sid = new_session()
            flowgen._bsk("navigate", BASE + "/#/f/" + film, "--session", f.sid, timeout=120)
            time.sleep(4)
            continue
        body = js(f, "document.body.innerText") or ""
        if "就这样，开始画图" in body:
            do_click(f, film, "就这样，开始画图", "web-03-map.png", 60)
        elif "都可以，去出片" in body:
            do_click(f, film, "都可以，去出片", "web-04-images.png", 60)
        elif "可以，就这样" in body:
            do_click(f, film, "可以，就这样", "web-05-film.png", 60)
            shot(f, "web-06-done.png")
            print("  ✓ 成片已确认", flush=True)
            return True
        elif "再写一次" in body:
            print("  ⚠ 台词没写出来，页面给了「再写一次」", flush=True)
            do_click(f, film, "再写一次", "web-03b-retry.png", 60)
        elif "继续画图" in body:
            print("  ⚠ 画图停住了，页面给了「继续画图」", flush=True)
            do_click(f, film, "继续画图", "web-03c-resume.png", 60)
        if i % 6 == 0:
            print("  [%3ds] %s" % (i * 10, (body.replace("\n", " | "))[:110]), flush=True)
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--new", default="")
    ap.add_argument("--minutes", type=float, default=3)
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--click-map", action="store_true")
    ap.add_argument("--click-img", action="store_true")
    ap.add_argument("--click-film", action="store_true")
    a = ap.parse_args()
    st = load_state()
    film = st.get("film")
    f = open_page(None if a.new else film)
    try:
        if a.new:
            film = form(f, a.new, a.minutes)
        if a.click_map:
            do_click(f, film, "就这样，开始画图", "web-03-map.png", 300)
        if a.click_img:
            do_click(f, film, "都可以，去出片", "web-04-images.png", 3600)
        if a.click_film:
            do_click(f, film, "可以，就这样", "web-05-film.png", 3600)
        if a.watch:
            watch(f, film)
    finally:
        print("  会话：", f.sid, "· 片子：", film)


if __name__ == "__main__":
    main()
