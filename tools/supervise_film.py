"""监督器：把一条片按流程推到底（操作员版）。

它不是"又一个流程" —— 它只做四件事：
    等 → 检查 → 点头（调面板的 /api/gate）→ 修（失败重排/重试）

关键节点会打印出来，人可以随时接管（打回/改词）。用法：
    python tools/supervise_film.py infidelity-1021
"""
import json
import pathlib
import re
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "http://127.0.0.1:8900"
PUNCT = re.compile(r"[，。！？；：、,.!?;:]")


def api(path, body=None):
    req = urllib.request.Request(BASE + path,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json"} if body is not None else {})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())


def state(f):
    return api("/api/state?film=" + urllib.parse.quote(f))


def say(msg):
    print(time.strftime("[%H:%M:%S] ") + msg, flush=True)


def wait(label, cond, timeout, step=10):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            if cond():
                say(f"✓ {label}（等了 {int(time.time() - t0)} 秒）")
                return True
        except Exception as e:                                # noqa: BLE001
            say(f"  （检查时出错，继续等：{e}）")
        time.sleep(step)
    say(f"✗ {label} 超时（{timeout} 秒）")
    return False


def script_files(f):
    d = ROOT / "projects" / f
    src = json.loads((d / "script-source.json").read_text(encoding="utf-8")) \
        if (d / "script-source.json").exists() else {}
    md = d / "docs" / "页-处境映射.md"
    rows = [l for l in md.read_text(encoding="utf-8").splitlines() if l.strip().startswith("|")] if md.exists() else []
    spec = json.loads((d / "page-spec.json").read_text(encoding="utf-8")) \
        if (d / "page-spec.json").exists() else []
    return src.get("pages", []), rows, spec


def audit_pages(pages):
    """审台词：每条 cue ≤12 字、且第 12 字前有标点（否则字幕会切开词）。"""
    hard = []
    for p in pages:
        for c in p.get("cues", []):
            if len(c) <= 12:
                continue
            if not PUNCT.search(c[:12]):
                hard.append((p.get("id"), c))
    return hard


def main():
    f = sys.argv[1] if len(sys.argv) > 1 else "infidelity-1021"
    say(f"监督：{f}")
    d = ROOT / "projects" / f

    # ---------- ① 等台词 / 映射表 / 页表 ----------
    def ready():
        pages, rows, spec = script_files(f)
        return len(pages) >= 5 and len(rows) >= len(pages) and len(spec) >= len(pages)
    if not wait("第一阶段（台词 + 映射表 + 页表）", ready, 1800):
        pages, rows, spec = script_files(f)
        say(f"  现状：台词 {len(pages)} 页 · 映射表 {len(rows)} 行 · 页表 {len(spec)} 页")
        say("  提示：可以在页面上点「再写一次」，或告诉我哪里要改")
        return 2

    pages, rows, spec = script_files(f)
    say(f"  台词 {len(pages)} 页 / {sum(len(p.get('cues', [])) for p in pages)} 条 cue")
    say(f"  映射表 {len(rows)} 行 · 页表 {len(spec)} 页")
    hard = audit_pages(pages)
    if hard:
        say(f"  ⚠ 有 {len(hard)} 条 cue 会被 12 字硬切（前 3 条）：")
        for pid, c in hard[:3]:
            say(f"     {pid}：{c}")
    else:
        say("  ✓ 台词没有 12 字硬切")

    # 打印映射表前几行，供人看
    say("  映射表（前 5 行）：")
    for r in rows[1:6]:
        say("    " + " | ".join(x.strip() for x in r.strip().strip("|").split("|")[:4])[:110])

    # ---------- ② 点头：分镜 ----------
    say("点头①：分镜通过 → 开始画图")
    api("/api/gate", {"film": f, "gate": "map", "verdict": "ok", "note": ""})

    # ---------- ③ 等图 ----------
    def imgs():
        st = state(f)
        return st.get("images", [])
    def all_done():
        im = imgs()
        return len(im) >= len(pages) and all(i["status"] in ("review", "saved", "approved") for i in im)
    if not wait("画图（全部出完）", all_done, 5400, step=20):
        im = imgs()
        failed = [i for i in im if i["status"] == "failed"]
        queued = [i for i in im if i["status"] in ("queued", "retry")]
        say(f"  现状：{len(im)} 条 · 完成 {len([i for i in im if i['file']])} · 失败 {len(failed)} · 排队 {len(queued)}")
        if failed:
            for i in failed:
                api("/api/queue/retry", {"film": f, "id": i["page"] + "-1", "page": i["page"]})
            say("  已把失败的重排，再给一轮时间")
            if not wait("画图（重排后）", all_done, 3600, step=20):
                say("  ✗ 仍有图没出来，先停在这里（看 logs/gen-*.log）")
                return 3

    im = imgs()
    bad = [i for i in im if (i.get("metrics") or {}).get("sprout_px", 1) == 0
           or (i.get("metrics") or {}).get("band_std", 0) > 15]
    say(f"  ✓ 图全部出完：{len(im)} 张；一致性可疑 {len(bad)} 张")
    for i in bad[:5]:
        say(f"     {i['page']} 芽{i['metrics'].get('sprout_px')} 带{i['metrics'].get('band_std')}")

    # ---------- ④ 点头：图 ----------
    say("点头②：图通过 → 出片（素材/排页/配音/字幕/渲染）")
    api("/api/gate", {"film": f, "gate": "img", "verdict": "ok", "note": ""})

    # ---------- ⑤ 等成片 ----------
    def film_ok():
        fs = [x for x in (d / "out").glob("*.mp4")] if (d / "out").exists() else []
        return bool(fs) and all(x.stat().st_size > 1_000_000 for x in fs)
    if not wait("出片（mp4）", film_ok, 5400, step=20):
        say("  ✗ 成片没出来；看 logs/gen-*.log 与面板的日志")
        return 4

    fs = sorted((d / "out").glob("*.mp4"))
    say("  ✓ 成片：")
    for x in fs:
        say(f"     {x.name}  {x.stat().st_size / 1024 / 1024:.1f} MB")
    srt = d / "out" / "字幕.srt"
    if srt.exists():
        say(f"     字幕.srt  {len(srt.read_text(encoding='utf-8').splitlines())} 行")
    say("完成。页面上点「可以，就这样」再下载（或直接取 out/ 里的文件）。")
    return 0


if __name__ == "__main__":
    import urllib.parse                                       # noqa: PLC0415
    sys.exit(main())
