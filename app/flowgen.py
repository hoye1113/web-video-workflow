"""驱动 Flow 生图。

手工跑通过一次（第 23 镜那只手），这里把它封成能批量跑的东西。

踩过的坑，都写在代码里了：
  ① Flow 的输入框是 React contenteditable，bsk 的 `fill` 会报 "target changed" ——
     必须用 `evaluate` + `execCommand('insertText')`，而且提示词要用 base64 传（避开引号转义）。
  ② 同一项目的图都堆在一个网格里，所以用「生成前后 URL 的差集」来认哪几张是新出的。
  ③ 图床 flow-content.google 命令行连不上（浏览器走代理、命令行不走），
     只能在页面里 `fetch` 成 base64 再落盘。
  ④ 首页可能弹更新日志（"Nano Banana x.x"），要点掉。
"""
import base64
import json
import os
import re
import shutil
import subprocess
import time
from pathlib import Path

import store                          # 项目落盘（store 不反过来 import 本模块，安全）

ROOT = Path(__file__).resolve().parent.parent
BSK = str(Path.home() / ".local" / "bin" / "bsk.exe")


def _env():
    e = os.environ.copy()
    e["BSK_AUTO_START"] = "0"          # daemon 由外部保证在跑；这里不自动拉起
    e["PYTHONUTF8"] = "1"
    return e


def _bsk(*args, timeout=120, json_out=False):
    cmd = [BSK] + [str(a) for a in args]
    if json_out:
        cmd.append("--json")
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=_env(), timeout=timeout)
    return r.stdout or "", r.stderr or "", r.returncode


def daemon_ok():
    try:
        out, _, _ = _bsk("status", json_out=True, timeout=30)
        return '"daemon_version"' in out
    except Exception:                                          # noqa: BLE001
        return False


# 认生成的图：**按域名白名单**，且**不要求已经加载完**。
# 踩过四次：
#   ① 只按尺寸（naturalWidth>=800）会把界面上的广告图一起收走 —— 收回来一摞毛毡垫。
#   ② 要求"一次至少出 2 张"会误判 —— Flow 有时只出 1 张。
#   ③ 要求 naturalWidth>400 会漏 —— 项目里的图多了以后，新图在网格里
#      可能在视野外，浏览器懒加载不触发，naturalWidth 一直是 0，于是"等不到新图"。
#   ④ **域名会变**：早先是 flow-content.google，2026-10-16 实测变成了
#      `flow.google.com/asb/...`（内容 image/webp）。所以白名单要放宽成"两个都认"，
#      不然会静默地"没等到新图"。
_IMG_HOSTS = ("flow-content.google", "flow.google.com/asb", "/asb/")
_GET_IMGS = (
    "(()=>{const H=" + json.dumps(list(_IMG_HOSTS)) + ";const s=new Set();"
    "for(const i of document.querySelectorAll('img')){"
    "if(H.some(h=>i.src.includes(h)))s.add(i.src);}"
    "return [...s];})()"
)

# 出问题时把现场打出来（页面文字 + 图列表），别让人对着"没等到新图"猜
_DUMP = (
    "(()=>{const imgs=[...document.querySelectorAll('img')].filter(i=>i.src.includes('flow-content.google'));"
    "const txt=(document.body.innerText||'').replace(/\\n+/g,' | ').slice(0,300);"
    "return {count:imgs.length,"
    " sizes:imgs.map(i=>i.naturalWidth+'x'+i.naturalHeight).slice(-8),"
    " txt:txt};})()"
)


class Flow:
    """一个 bsk 会话 + 一个 Flow 项目。用完记得 close()。"""

    def __init__(self, log=print):
        self.log = log
        self.sid = None
        self.known = set()

    # ---------- 会话 ----------

    def open(self):
        out, err, _ = _bsk("session", "start", json_out=True, timeout=180)
        try:
            self.sid = json.loads(out).get("session_id")
        except Exception:                                      # noqa: BLE001
            raise RuntimeError(f"开 bsk 会话失败：{out[:200]} {err[:200]}")
        if not self.sid:
            raise RuntimeError(f"开 bsk 会话没拿到 id：{out[:200]}")
        self.log(f"bsk 会话 {self.sid}")

        # **窗口放到最大**：Flow 是响应式的，窗口一小就折叠掉一排按钮 ——
        # 实测 1600×900 时 "Characters"/"Scenes"/"Agent" 这些才会出现，
        # 折叠状态下连 observe 都看不到它们（用户提的，一试就灵）。
        try:
            _bsk("window", "resize", "--session", self.sid, "--width", "1600", "--height", "900", timeout=60)
        except Exception:                                      # noqa: BLE001
            pass                                               # 放不大也不致命

        out, _, _ = _bsk("navigate", "https://flow.google.com", "--session", self.sid, timeout=180)
        m = re.search(r"url=(\S+)", out or "")
        url = m.group(1) if m else "?"
        if "unsupported-country" in url:
            raise RuntimeError("Flow 在这个地区不可用（/unsupported-country）")
        self.log(f"Flow 已打开：{url}")
        time.sleep(4)
        self._dismiss_changelog()
        self._enter_project()
        self.known = self._image_urls()
        self.log(f"项目里已有的图：{len(self.known)} 张（用来区分新图）")

    def _has_input(self):
        v = self._run("(()=>document.querySelectorAll('[contenteditable=true]').length)()")
        return isinstance(v, int) and v > 0

    def _enter_project(self):
        """光打开 flow.google.com 是项目列表页，没有输入框，得先新建或打开一个项目。"""
        if self._has_input():
            return
        r = self._run(
            "(()=>{const bs=[...document.querySelectorAll('button,a')];"
            "const n=bs.find(x=>/new project|新建项目/i.test(x.textContent||''));"
            "if(n){n.click();return 'new';}"
            "const o=bs.find(x=>/open project|打开项目/i.test(x.textContent||''));"
            "if(o){o.click();return 'open';}return 'none';})()"
        )
        self.log(f"进项目：{r}")
        time.sleep(6)
        self._dismiss_changelog()
        time.sleep(2)
        if not self._has_input():
            raise RuntimeError("进了项目还是没有输入框 —— Flow 的界面可能变了")

    def close(self):
        if self.sid:
            try:
                _bsk("session", "stop", self.sid, timeout=120)
            except Exception:                                  # noqa: BLE001
                pass
            self.sid = None

    # ---------- 内部 ----------

    def _dismiss_changelog(self):
        """挡路的弹窗：更新日志、条款/隐私的 Agree/No thanks。点掉。找不到就算了。"""
        self._run(
            "(()=>{const bs=[...document.querySelectorAll('button')];"
            "const g=bs.find(x=>/get started|开始|知道了|got it/i.test(x.textContent||''));"
            "if(g){g.click();return 'changelog';}"
            # 条款/隐私弹窗：用户在用 Flow、也让我用，这里点 Agree 放行（会在日志里说一声）
            "const a=bs.find(x=>/^agree$/i.test((x.textContent||'').trim()));"
            "if(a){a.click();return 'agree';}"
            "return 'none';})()"
        )
        time.sleep(2)

    def _run(self, js):
        out, err, code = _bsk("evaluate", js, "--session", self.sid, json_out=True, timeout=180)
        try:
            return json.loads(out).get("value")
        except Exception:                                      # noqa: BLE001
            return {"_raw": (out or err)[:300], "_code": code}

    def _image_urls(self):
        v = self._run(_GET_IMGS)
        return set(v) if isinstance(v, list) else set()

    def _type_prompt(self, text):
        """往 Flow 的输入框里打字。用 execCommand —— bsk 的 fill 在这个 React contenteditable 上会失败。"""
        b64 = base64.b64encode(text.encode("utf-8")).decode()
        js = (
            "(()=>{const t=new TextDecoder().decode(Uint8Array.from(atob('" + b64 + "'),"
            "c=>c.charCodeAt(0)));"
            "const els=[...document.querySelectorAll('[contenteditable=true]')];"
            "const el=els[els.length-1];if(!el)return {ok:false,reason:'no input'};"
            "el.focus();document.execCommand('insertText',false,t);"
            "return {ok:true,len:el.textContent.length};})()"
        )
        return self._run(js)

    def _click_generate(self):
        """点生成。

        **必须用 bsk 的真实点击，不能用 JS 的 .click()** —— 实测 JS 点击返回成功、
        按钮也不 disabled，但页面毫无反应（React 那边的处理没被触发）。
        手工跑通那次用的就是 `bsk click @eNN`，这里照做：
        先 observe 拿到按钮的 ref，再 click。
        """
        out, err, _ = _bsk("observe", "--session", self.sid,
                           "--max-tokens", "6000", timeout=180)
        m = re.search(r'@(e\d+)\s+button\s+"(Start generation|开始生成)"', out or "")
        if not m:
            m = re.search(r'@(e\d+)\s+button\s+"[^"]*generation[^"]*"', out or "", re.I)
        if not m:
            btns = re.findall(r'@e\d+\s+button\s+"[^"]{0,40}"', out or "")[:20]
            return {"ok": False, "reason": "observe 里找不到生成按钮", "buttons": btns}
        ref = "@" + m.group(1)
        o2, e2, c2 = _bsk("click", ref, "--session", self.sid, timeout=180)
        ok = "click ok" in (o2 or "") or c2 == 0
        return {"ok": ok, "ref": ref, "out": (o2 or e2 or "")[:120]}

    # ---------- 参考图（ingredients）----------

    def attach(self, path):
        """把一张参考图挂到提示框（Flow 的 Add ingredients）。

        实测出来的三个细节（都踩过）：
          ① 那个按钮带 `[has-submenu]`：点完菜单开在**新图层**里，必须**重新 observe** 才拿得到菜单项的 ref；
             直接对它做 `upload --mode input` 会失败（"did not activate a file input"）。
          ② 菜单项叫 **"Upload media"**；点它才会走文件选择器，这时 bsk 的 upload 才接得住。
          ③ bsk 不肯猜目标：给它 CSS 选择器会报 "could not be safely resolved"，必须用 observe 给的 `@eN`。
        """
        p = Path(path)
        if not p.exists():
            raise RuntimeError(f"参考图不存在：{p}")
        out, _, _ = _bsk("observe", "--session", self.sid, "--max-tokens", "12000", timeout=300)
        m = re.search(r'@(e\d+)\s+button\s+"Add ingredients', out or "")
        if not m:
            raise RuntimeError("找不到 Add ingredients 按钮（Flow 界面可能变了）")
        _bsk("click", "@" + m.group(1), "--session", self.sid, timeout=120)
        time.sleep(2)
        out2, _, _ = _bsk("observe", "--session", self.sid, "--max-tokens", "12000", timeout=300)
        m2 = re.search(r'@(e\d+)\s+button\s+"Upload media"', out2 or "")
        if not m2:
            raise RuntimeError("点了 Add ingredients 却没看到 Upload media 菜单项（Flow 界面可能变了）")
        o, e, c = _bsk("upload", "--file", str(p), "--session", self.sid,
                       "--ref", "@" + m2.group(1), "--mode", "input", "--timeout", "120s", timeout=300)
        txt = ((o or "") + (e or ""))
        if c != 0 or "error" in txt.lower():
            raise RuntimeError(f"挂参考图失败：{txt.strip()[:240]}")
        self.log(f"  挂上参考图：{p.name}")
        time.sleep(4)                       # 等它把缩略图渲染出来
        return True

    # ---------- 对外 ----------

    def generate(self, prompt, timeout=240, settle=6):
        """生成一次，返回新出的图的字节流（通常是 2 张）。"""
        before = self.known
        t = self._type_prompt(prompt)
        if not isinstance(t, dict) or not t.get("ok"):
            raise RuntimeError(f"提示词没输进去：{t}")
        time.sleep(2)
        c = self._click_generate()
        if not isinstance(c, dict) or not c.get("ok"):
            raise RuntimeError(f"点不到生成按钮：{c}")

        deadline = time.time() + timeout
        last = 0
        while time.time() < deadline:
            time.sleep(6)
            cur = self._image_urls()
            n = len(cur - before)
            if n != last:
                self.log(f"  出图 {n} 张")
                last = n
            if n >= 1:
                time.sleep(settle)         # 还有第二张的话，多等一会儿
                if len(self._image_urls() - before) != n:
                    time.sleep(6)
                break
        new = list(self._image_urls() - before)
        if not new:
            # 别只说"没等到"——把现场打出来，好知道是卡住了、被拒了、还是界面变了
            d = self._run(_DUMP)
            self.log(f"  超时现场：{json.dumps(d, ensure_ascii=False)[:600]}")
            raise RuntimeError(f"{timeout} 秒内没等到新图（现场已打在日志里）")
        self.known = self._image_urls()
        return self._fetch(new[:2])        # 一次只收前两张，多的不要

    def _fetch(self, urls):
        """在页面里 fetch 成 base64 再拿回来（命令行连不上 flow-content.google）。

        顺便在浏览器里判尺寸：网格里的缩略图会混进来，宽度小于 900 的直接丢掉。
        """
        arr = ",".join("'" + u.replace("'", "\\'") + "'" for u in urls)
        js = (
            "(async()=>{const urls=[" + arr + "];const res=[];for(const u of urls){"
            "const r=await fetch(u);const b=await r.blob();"
            "let w=0,h=0;try{const bm=await createImageBitmap(b);w=bm.width;h=bm.height;bm.close();}catch(e){}"
            "if(w&&w<900)continue;"
            "const buf=await b.arrayBuffer();const u8=new Uint8Array(buf);"
            "let s='';const CH=0x8000;for(let i=0;i<u8.length;i+=CH)"
            "{s+=String.fromCharCode.apply(null,u8.subarray(i,i+CH));}"
            "res.push({w:w,h:h,size:u8.length,b64:btoa(s)});}return res;})()"
        )
        out, err, code = _bsk("evaluate", js, "--session", self.sid, json_out=True, timeout=600)
        try:
            o = json.loads(out)
        except Exception:                                      # noqa: BLE001
            raise RuntimeError(f"取图失败：{(out or err)[:300]}") from None
        if not o.get("ok"):
            raise RuntimeError(f"取图失败：{json.dumps(o)[:300]}")
        got = o["value"] or []
        if not got:
            raise RuntimeError(f"新图都是缩略图尺寸，没收到大图（{len(urls)} 个候选）")
        self.log("  收到 " + "、".join(f'{x.get("w")}x{x.get("h")}' for x in got))
        return [base64.b64decode(x["b64"]) for x in got]


# ---------- 生图体检：量构图，不合格的重画 ----------
#
# 评审反复挑"主体太小""偏在一侧"，这两条**量得出来**（app/measure.py）。
# 关键结论：构图歪是**裁不回来**的（主体在 0.86 想挪到中间要放大 3.6 倍，画质废），
# 所以只能在生图这一步修正 —— 但也不能"全部重画"（慢、还可能有画得好的被换掉）。
# 做法：逐页量，只对不合格的页带着修正要求重画，再量一遍确认。

BAD_CENTER = 0.20          # 主体中心离画面中心超过这么多 → 不合格（横向）
BAD_CENTER_Y = 0.28        # 纵向宽松一点：屏上字一般压在下方，主体略偏上是对的
BAD_SIZE = 0.25            # 主体长边小于画面这么多 → 不合格

CORRECT = ("\n\n【重画要求：把主体放在**画面中部偏上**、占画面一半左右；"
           "**最下面 18%（画面下缘那一条）必须留空** —— 成片要在那里烧字幕，"
           "主体或任何东西都不要进那一条带，否则会被字幕压住；"
           "不要贴边、不要缩在角落；画面里只出现这一件主体 —— "
           "不要孩子、不要人脸、不要任何文字。】")


def audit_one(r):
    """量出来的结果 → (是否合格, 一句人话的原因)。"""
    cx, cy = r["box"][0] + r["box"][2] / 2, r["box"][1] + r["box"][3] / 2
    size = max(r["box"][2], r["box"][3])
    why = []
    if abs(cx - 0.5) > BAD_CENTER:
        why.append(f"主体横向偏在 {cx:.2f}")
    if abs(cy - 0.5) > BAD_CENTER_Y:
        why.append(f"主体纵向偏在 {cy:.2f}")
    if size < BAD_SIZE:
        why.append(f"主体只占 {size:.0%}")
    return (not why), "、".join(why)


def do_image_audit(project, only=None, job=None, regen=True):
    """给生图页做体检；不合格的带着修正要求重画。

    返回 {checked, bad, fixed, still_bad}。**重画过的页，场景代码就过期了**，
    调用方要顺手把那些页的代码重写一遍。
    """
    import measure
    import llm
    say = job.say if job else print
    m = store.load(project) or {}
    todo = [s for s in m.get("shots", [])
            if s.get("images")
            and (not only or s["id"] in only)]
    if not todo:
        raise ValueError("没有有图的页")

    ai = llm.LLM()
    say(f"体检 {len(todo)} 页：{' '.join(s['id'] for s in todo)}")
    bad, fixed, still = [], [], []

    # 先把所有页量一遍（量过的复用，不重复花钱）
    for s in todo:
        got = measure.of(project, s["id"], ai=ai, say=say)
        if not got:
            say(f"  页 {s['id']}：没量出来，跳过")
            continue
        ok, why = audit_one(got)
        s["_why"] = why
        if ok:
            say(f"  页 {s['id']}：合格")
        else:
            bad.append(s)
            say(f"  页 {s['id']}：不合格 —— {why}")

    if not bad or not regen:
        say(f"体检结束：{len(todo)} 页里 {len(bad)} 页构图不合格" + ("（这轮不改）" if bad else ""))
        return {"checked": [s["id"] for s in todo], "bad": [s["id"] for s in bad],
                "fixed": [], "still_bad": []}

    if not daemon_ok():
        raise RuntimeError("bsk daemon 不在，没法重画")
    f = Flow(log=say)
    try:
        f.open()
        for i, s in enumerate(bad, 1):
            if job:
                job.step(i - 1, len(bad), f"重画页 {s['id']}")
            say(f"[{i}/{len(bad)}] 重画页 {s['id']}（{s['_why']}）")
            prompt = (s.get("imagePrompt") or "").strip() + CORRECT
            try:
                blobs = None
                for attempt, wait_s in ((1, 240), (2, 420)):
                    try:
                        blobs = f.generate(prompt, timeout=wait_s)
                        break
                    except Exception as e:                      # noqa: BLE001
                        say(f"    第 {attempt} 次没成：{e}")
                        if attempt == 1:
                            time.sleep(5)
                if not blobs:
                    still.append({"shot": s["id"], "why": "重画两次都没出来"})
                    continue
                names = save_images(project, s["id"], blobs)
                store.patch_shot(project, s["id"], images=names,
                                 subject=None, subjectBox=None)   # 清了重画
                got = measure.of(project, s["id"], ai=ai, say=say, force=True)
                if got is None:
                    still.append({"shot": s["id"], "why": "重画了但量不出来"})
                    continue
                ok, why = audit_one(got)
                if ok:
                    fixed.append(s["id"])
                    say(f"    ✓ 页 {s['id']} 修好了")
                else:
                    still.append({"shot": s["id"], "why": why})
                    say(f"    ✗ 页 {s['id']} 还是不合格：{why}")
            except Exception as e:                              # noqa: BLE001
                say(f"    ✗ 页 {s['id']} 出错：{e}")
                still.append({"shot": s["id"], "why": str(e)[:120]})
            if job:
                job.step(i, len(bad), f"重画页 {s['id']}")
    finally:
        f.close()

    say(f"═══ 体检结束：{len(todo)} 页里 {len(bad)} 页不合格，修好 {len(fixed)} 页"
        f"{'，还差 ' + ' '.join(x['shot'] for x in still) if still else ''}")
    return {"checked": [s["id"] for s in todo], "bad": [s["id"] for s in bad],
            "fixed": fixed, "still_bad": still}


# ---------- 落盘 ----------

def save_images(project, shot, blobs):
    """存到 projects/<项目>/assets/<页号>_<序号>.png，返回文件名列表。"""
    d = ROOT / "projects" / project / "assets"
    d.mkdir(parents=True, exist_ok=True)
    names = []
    for i, b in enumerate(blobs, 1):
        name = f"{shot}_{i}.png"
        (d / name).write_bytes(b)
        names.append(name)
    return names


# ---------- 批量任务 ----------

def do_images(project, only=None, job=None):
    """给需要生图的页批量出图。**一个会话跑完所有页**（每页开关一次太慢）。

    only: 指定页号列表；不传就自动挑 mode 是 image/mixed 且还没图的页。
    失败不连坐：某一页挂了就记下来接着下一页。
    """
    import store
    say = job.say if job else print

    m = store.load(project) or {}
    shots = m.get("shots", [])
    todo = [s for s in shots
            if (not only or s["id"] in only)
            and (s.get("mode") in ("image", "mixed"))
            and (s.get("imagePrompt") or "").strip()]
    if not todo:
        raise ValueError("没有需要生图的页（mode 是 image/mixed 且写了 imagePrompt）")

    say(f"要生图 {len(todo)} 页：{' '.join(s['id'] for s in todo)}")
    if not daemon_ok():
        raise RuntimeError("bsk daemon 不在（先 bsk daemon start --foreground）")

    f = Flow(log=say)
    done, failed = [], []
    try:
        f.open()
        for i, s in enumerate(todo, 1):
            if job:
                job.step(i - 1, len(todo), f"页 {s['id']}")
            say(f"[{i}/{len(todo)}] 页 {s['id']}：{s.get('title','')[:30]}")
            blobs = None
            for attempt, wait_s in ((1, 240), (2, 420)):       # 失败就再来一次，第二次等更久
                try:
                    blobs = f.generate((s.get("imagePrompt") or "").strip(), timeout=wait_s)
                    break
                except Exception as e:                          # noqa: BLE001
                    say(f"    第 {attempt} 次没成：{e}")
                    if attempt == 1:
                        time.sleep(5)
            if blobs:
                names = save_images(project, s["id"], blobs)
                # 立刻写回 project.json，中途挂了前面的也不白跑
                mm = store.load(project)
                for x in mm["shots"]:
                    if x["id"] == s["id"]:
                        x["images"] = names
                store.save(project, mm)
                say(f"    存了 {len(names)} 张：{'、'.join(names)}")
                done.append(s["id"])
            else:
                say(f"    ✗ 两次都没出来，跳过（后面可以单独重跑这一页）")
                failed.append({"shot": s["id"], "error": "两次都没等到新图"})
                time.sleep(3)
            if job:
                job.step(i, len(todo), f"页 {s['id']}")
    finally:
        f.close()

    say(f"═══ 生图结束：成功 {len(done)} 页，失败 {len(failed)} 页")
    return {"done": done, "failed": failed}
