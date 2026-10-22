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
import io
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
# 踩过五次：
#   ① 只按尺寸（naturalWidth>=800）会把界面上的广告图一起收走 —— 收回来一摞毛毡垫。
#   ② 要求"一次至少出 2 张"会误判 —— Flow 有时只出 1 张。
#   ③ 要求 naturalWidth>400 会漏 —— 项目里的图多了以后，新图在网格里
#      可能在视野外，浏览器懒加载不触发，naturalWidth 一直是 0，于是"等不到新图"。
#   ④ **域名会变**：早先是 flow-content.google，2026-10-16 实测变成了
#      `flow.google.com/asb/...`（内容 image/webp）。所以白名单要放宽成"两个都认"，
#      不然会静默地"没等到新图"。
#   ⑤ **尺寸写在 URL 后缀里**（2026-10-19 探明）：同一张图在网格里可能先是
#      `…=s512-rw`（缩略图）过一会儿才换成 `…=s1600-rw`（原图 1376×768）。
#      → 所以：**按 base 去重**（把 `=sN-rw` 掐掉），**取图时自己拼 `=s1600-rw`**。
#      这样既不会把同一张图数两遍，也不会"只拿到缩略图"。
_IMG_HOSTS = ("flow-content.google", "flow.google.com/asb", "/asb/")
_STRIP_SIZE = "u.replace(/=s\\d+(-rw)?$/, '')"
_GET_IMGS = (
    "(()=>{const H=" + json.dumps(list(_IMG_HOSTS)) + ";const s=new Set();"
    "for(const i of document.querySelectorAll('img')){"
    "const u=i.src||'';if(!H.some(h=>u.includes(h)))continue;s.add(" + _STRIP_SIZE + ");}"
    "return [...s];})()"
)

_FETCH_IMGS = (
    "(async()=>{const bases=%s;const minW=%d;const siz=%d;const res=[];"
    "for(const b of bases){let best=null;"
    "for(const u of [b+'=s'+siz+'-rw',b]){"
    "try{const r=await fetch(u);const blob=await r.blob();"
    "let w=0,h=0;try{const bm=await createImageBitmap(blob);w=bm.width;h=bm.height;bm.close();}catch(e){}"
    "if(!best||w>best.w)best={w:w,h:h,blob:blob};if(w>=minW)break;}catch(e){}}"
    "if(!best||best.w<minW)continue;"
    "const buf=await best.blob.arrayBuffer();const u8=new Uint8Array(buf);"
    "let s='';const CH=0x8000;for(let i=0;i<u8.length;i+=CH){s+=String.fromCharCode.apply(null,u8.subarray(i,i+CH));}"
    "res.push({b:b,w:best.w,h:best.h,size:u8.length,b64:btoa(s)});}return res;})()"
)


# ---- 感知哈希：识破"把项目里的老图当成新图"（网格是虚拟滚动，老图会后加载）----
# 用 16×16 灰度图比"平均绝对差"：同一张图（都是同一份原始文件）差 ≈0，
# 不同轮次生成的两张风格相似的图，差会明显大于阈值 —— 阈值取 6 很安全。
def _sig(data: bytes, n=16):
    from PIL import Image
    im = Image.open(io.BytesIO(data)).convert("L").resize((n, n))
    return list(im.getdata())


def _sig_dist(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / max(len(a), 1)

# 出问题时把现场打出来（页面文字 + 图列表），别让人对着"没等到新图"猜
_DUMP = (
    "(()=>{const H=" + json.dumps(list(_IMG_HOSTS)) + ";"
    "const imgs=[...document.querySelectorAll('img')].filter(i=>H.some(h=>(i.src||'').includes(h)));"
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
        self._sigs = None          # 基线指纹（懒算）
        self._rejected = set()     # 这一轮里判过"是项目里的老图"的 base，别再试

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
        self.known = self._image_bases()
        self.log(f"项目里已有的图：{len(self.known)} 张（用来区分新图）")

    def _wait_composer(self, timeout=45):
        """等 Flow 的输入区出现（图多了以后页面加载慢，8 秒有时不够）。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self._has_input():
                return True
            time.sleep(2)
        return False

    def enter(self, url):
        """开一个会话并**直接进指定的项目**（不经过首页，免得误点"新建项目"）。

        用法：角色挂载、批量生图都走这里。项目地址是这个：
        https://flow.google.com/project/2423a8a2-2219-4dd5-83ea-563fd00a79fb（video-factory）
        """
        out, err, _ = _bsk("session", "start", json_out=True, timeout=180)
        try:
            self.sid = json.loads(out).get("session_id")
        except Exception:                                      # noqa: BLE001
            raise RuntimeError(f"开 bsk 会话失败：{out[:200]} {err[:200]}") from None
        if not self.sid:
            raise RuntimeError(f"开 bsk 会话没拿到 id：{out[:200]}")
        self.log(f"bsk 会话 {self.sid}")
        try:
            _bsk("window", "resize", "--session", self.sid, "--width", "1600", "--height", "900", timeout=60)
        except Exception:                                      # noqa: BLE001
            pass
        o, e, _ = _bsk("navigate", url, "--session", self.sid, timeout=180)
        m = re.search(r"url=(\S+)", o or "")
        if "unsupported-country" in (m.group(1) if m else ""):
            raise RuntimeError("Flow 在这个地区不可用（/unsupported-country）—— 换个代理节点")
        time.sleep(8)
        self._dismiss_changelog()
        if not self._wait_composer():
            raise RuntimeError("项目页打开了但输入区一直没出现（Flow 可能卡住/没登录）")
        # **滚一遍取并集**：网格虚拟滚动，读一次取不全 → 后面会"把老图当新图"
        self.known = self._full_bases()
        self._sigs = None
        self.log(f"已进项目，里面已有的图：{len(self.known)} 张（滚全了）")
        return self.sid

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

    def _image_bases(self):
        """网格里所有图的 base URL（尺寸后缀已掐掉）。"""
        v = self._run(_GET_IMGS)
        return set(v) if isinstance(v, list) else set()

    def _type_prompt(self, text, tries=10, gap=6):
        """往 Flow 的输入框里打字。用 execCommand —— bsk 的 `fill` 在这个 React contenteditable 上会失败。

        2026-10-19 加的两条（都是实测踩出来的）：
          ① **先清空**（`selectAll` + `delete`）。生成完 Flow 有时留着上一句，
             直接 insert 会**把新提示词接在旧提示词后面**，出来的是两张图揉在一起的东西。
          ② **要等输入框回来**：一张生成完之后，Flow 会把提示框收掉一小会儿
             （也许是"正在出图"那个状态），这时候 `[contenteditable]` 一个都没有 ——
             直接写就是 `{ok:false, reason:'no input'}`。所以要**轮询等它回来**。
        """
        b64 = base64.b64encode(text.encode("utf-8")).decode()
        js = (
            "(()=>{const t=new TextDecoder().decode(Uint8Array.from(atob('" + b64 + "'),"
            "c=>c.charCodeAt(0)));"
            "const els=[...document.querySelectorAll('[contenteditable=true]')];"
            "const el=els[els.length-1];if(!el)return {ok:false,reason:'no input'};"
            "el.focus();"
            "document.execCommand('selectAll',false,null);"
            "document.execCommand('delete',false,null);"
            "document.execCommand('insertText',false,t);"
            "return {ok:true,len:el.textContent.length,text:(el.textContent||'')};})()"
        )
        last = None
        for i in range(max(1, tries)):
            last = self._run(js)
            if isinstance(last, dict) and last.get("ok") and last.get("len"):
                if i:
                    self.log(f"    输入框回来了（等了 {(i + 1) * gap} 秒）")
                return last
            if i < tries - 1:
                self.log(f"    还没看到输入框（{last}），等 {gap} 秒再试")
                time.sleep(gap)
        return last

    def _click_generate(self):
        """点生成。

        **必须用 bsk 的真实点击，不能用 JS 的 .click()** —— 实测 JS 点击返回成功、
        按钮也不 disabled，但页面毫无反应（React 那边的处理没被触发）。

        2026-10-21 界面更新：生成按钮是输入框右侧的箭头，`aria-label="Start generation"`，
        **不带文字** —— 所以先按 aria-label 用 DOM 找，找不到再退回 observe（兼容旧界面）。
        """
        hit = self._run(
            "(()=>{const b=[...document.querySelectorAll('button,[role=button]')].find(x=>"
            "/start generation|开始生成/i.test(x.getAttribute('aria-label')||''));"
            "if(!b)return 'not found';b.setAttribute('data-vf-gen','1');"
            "return {ok:true,label:b.getAttribute('aria-label')};})()"
        )
        if isinstance(hit, dict) and hit.get("ok"):
            o2, e2, c2 = _bsk("click", "--session", self.sid, "--selector", "[data-vf-gen='1']", timeout=180)
            ok = "click ok" in (o2 or "") or c2 == 0
            return {"ok": ok, "ref": "aria:" + str(hit.get("label")), "out": (o2 or e2 or "")[:120]}

        out, err, _ = _bsk("observe", "--session", self.sid,
                           "--max-tokens", "6000", timeout=180)
        m = re.search(r'@(e\d+)\s+(?:\[)?button(?:\])?\s+"(Start generation|开始生成)"', out or "")
        if not m:
            m = re.search(r'@(e\d+)\s+(?:\[)?button(?:\])?\s+"[^"]*generation[^"]*"', out or "", re.I)
        if not m:
            btns = re.findall(r'@e\d+\s+(?:\[)?button(?:\])?\s+"[^"]{0,40}"', out or "")[:12]
            return {"ok": False, "reason": "找不到生成按钮", "buttons": btns}
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
        out, _, _ = _bsk("observe", "--session", self.sid, "--max-tokens", "16000", timeout=300)
        m = re.search(r'@(e\d+)\s+button\s+"Add ingredients', out or "")
        if not m:
            # 输入区是瞬时的：窗口小了会折叠、刚加载时会晚出现。放回 1600×900 + 等输入框 + 再试两次。
            for attempt in range(3):
                try:
                    _bsk("window", "resize", "--session", self.sid,
                         "--width", "1600", "--height", "900", timeout=60)
                except Exception:                              # noqa: BLE001
                    pass
                self._wait_composer(20)
                self._run("document.body.click()")
                time.sleep(2)
                out, _, _ = _bsk("observe", "--session", self.sid, "--max-tokens", "16000", timeout=300)
                m = re.search(r'@(e\d+)\s+button\s+"Add ingredients', out or "")
                if m:
                    self.log(f"  第 {attempt + 1} 次重试找到了 Add ingredients")
                    break
        if not m:
            raise RuntimeError("找不到 Add ingredients 按钮（Flow 界面可能变了，或输入区没展开）")
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

    # ---------- 角色（Flow 内置 Characters）----------

    def attach_character(self, name):
        """把 Flow 项目里**已建好的角色**挂成提示词的素材 chip。

        2026-10-21 Flow 换了界面（右侧 Agent 面板）：入口仍是提示框左下那个 `+`
        （aria-label = "Add ingredients to the prompt box"），点开是**素材选择器**：
        左筛选（All/Images/Voices/**Characters**…）、中列表、右预览 + **Add to prompt**。
        所以这里全按 DOM 找，**不依赖 observe 的文本格式**（它会变）：
            + → 列表里文本以角色名开头的 `[role=option]` → Add to prompt
        **角色名不要写进提示词** —— 写进去等于让模型自己编，挂 chip 才锁得住形象。
        """
        try:
            _bsk("window", "resize", "--session", self.sid,
                 "--width", "1600", "--height", "900", timeout=60)
        except Exception:                                      # noqa: BLE001
            pass
        self._wait_composer(30)
        hit = self._run(
            "(()=>{const b=[...document.querySelectorAll('button,[role=button]')].find(x=>"
            "(x.getAttribute('aria-label')||'').includes('Add ingredients'));"
            "if(!b)return 'no + button';b.setAttribute('data-vf-plus','1');"
            "return b.getAttribute('aria-label');})()"
        )
        if not isinstance(hit, str) or hit.startswith("no "):
            raise RuntimeError(f"找不到提示框的 + 按钮（Flow 界面又变了？）：{hit}")
        _bsk("click", "--session", self.sid, "--selector", "[data-vf-plus='1']", timeout=120)

        ok = False
        for _ in range(10):
            time.sleep(2)
            n = self._run("document.querySelectorAll('[role=option]').length")
            if isinstance(n, int) and n > 0:
                ok = True
                break
        if not ok:
            self._run("document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}))")
            raise RuntimeError("点了 + 但素材选择器没出现")

        pick = self._run(
            "(()=>{const opts=[...document.querySelectorAll('[role=option]')];"
            "const hit=opts.find(e=>(e.textContent||'').replace(/\\s+/g,'').includes(" + json.dumps(name) + "));"
            "if(!hit)return 'not found';hit.setAttribute('data-vf-pick','1');"
            "return (hit.textContent||'').replace(/\\s+/g,' ').trim().slice(0,30);})()"
        )
        if pick == "not found":
            # 选择器是个大面板，左栏有分类：All / Images / Videos / Voices / **Characters** / Avatars。
            # 以前按"文本正好等于 Characters"找 —— 按钮里带图标名（accessibility_newCharacters），永远匹配不上，
            # 于是角色被埋在几千张图里（2026-10-22：小芽明明在 Characters 里，选择器却"搜不到"）。
            # 现在：① 在搜索框所在面板里点"含 Characters 的按钮" ② 用原生 setter 往搜索框里填名字。
            self._run(
                "(()=>{const i=[...document.querySelectorAll('input')].find(x=>"
                "(x.placeholder||'').includes('Search'));let p=i;for(let k=0;k<6&&p;k++)p=p.parentElement;"
                "const root=p||document;"
                "const b=[...root.querySelectorAll('button,[role=tab],[role=button]')].find(x=>"
                "/Characters/.test(x.textContent||''));"
                "if(!b)return 'no tab';b.setAttribute('data-vf-chars','1');return 'ok';})()"
            )
            _bsk("click", "--session", self.sid, "--selector", "[data-vf-chars='1']", timeout=120)
            time.sleep(2)
            self._run(
                "(()=>{const i=[...document.querySelectorAll('input')].find(x=>"
                "(x.placeholder||'').includes('Search'));if(!i)return 'no';(i.focus());"
                "const s=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;"
                "s.call(i," + json.dumps(name) + ");"
                "i.dispatchEvent(new Event('input',{bubbles:true}));return 'ok';})()"
            )
            time.sleep(2)
            pick = self._run(
                "(()=>{const opts=[...document.querySelectorAll('[role=option]')];"
                "const hit=opts.find(e=>(e.textContent||'').replace(/\\s+/g,'').includes(" + json.dumps(name) + "));"
                "if(!hit)return 'not found';hit.setAttribute('data-vf-pick','1');"
                "return (hit.textContent||'').replace(/\\s+/g,' ').trim().slice(0,30);})()"
            )
        if pick == "not found":
            self._run(
                "(()=>{const o=document.querySelector('[role=option]');"
                "const lb=o?o.closest('[role=listbox]')||o.parentElement:null;"
                "if(lb)lb.scrollTop=lb.scrollHeight;return lb?'ok':'no list';})()"
            )
            time.sleep(2)
            pick = self._run(
                "(()=>{const opts=[...document.querySelectorAll('[role=option]')];"
                "const hit=opts.find(e=>(e.textContent||'').replace(/\\s+/g,'').includes(" + json.dumps(name) + "));"
                "if(!hit)return 'not found';hit.setAttribute('data-vf-pick','1');"
                "return (hit.textContent||'').replace(/\\s+/g,' ').trim().slice(0,30);})()"
            )
        if pick == "not found":
            self._run("document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}))")
            raise RuntimeError(f"选择器里没有角色「{name}」（Flow 里的角色名改过？）")
        before = len(self.prompt_chips())
        _bsk("click", "--session", self.sid, "--selector", "[data-vf-pick='1']", timeout=120)
        time.sleep(3)

        # 2026-10-22 的界面上，点角色条目**直接就挂上了**（选择器自动关），不再有 "Add to prompt"。
        # 所以先看 chip 有没有变多；没变多再去点 Add to prompt（老界面）。
        chips = self.prompt_chips()
        if len(chips) <= before:
            add = self._run(
                "(()=>{const b=[...document.querySelectorAll('button')].find(x=>/add to prompt/i.test(x.textContent||''));"
                "if(!b)return 'not found';if(b.disabled)return 'disabled';b.setAttribute('data-vf-add','1');return 'ok';})()"
            )
            if add == "ok":
                _bsk("click", "--session", self.sid, "--selector", "[data-vf-add='1']", timeout=120)
                time.sleep(4)
                chips = self.prompt_chips()
            elif not chips:
                raise RuntimeError(f"点了「{name}」但既没挂上 chip，也没有 Add to prompt：{add}")

        # chip 挂上之后要**刷新一次已知集合** —— chip 本身也是个 img，
        # 不刷新的话它会被当成"新图"，取图那一步会白等。
        self.known |= self._image_bases()
        chips = self.prompt_chips()
        self.log(f"  挂上角色：{name}（提示框里的 chip {len(chips)} 个）")
        if not chips:
            raise RuntimeError(f"挂了「{name}」但提示框里没有 chip —— 挂载没生效")
        return chips

    def prompt_chips(self):
        """提示框容器里的 chip（参考图/角色都会以 img 出现在这）。"""
        v = self._run(
            "(()=>{const els=[...document.querySelectorAll('[contenteditable=true]')];"
            "const el=els[els.length-1];if(!el)return [];"
            "let p=el;for(let i=0;i<3&&p;i++)p=p.parentElement;"
            "if(!p)return [];"
            "return [...p.querySelectorAll('img')].map(i=>({src:i.src||'',w:i.naturalWidth,h:i.naturalHeight}));})()"
        )
        return v if isinstance(v, list) else []

    def prompt_area(self):
        """读回提示框附近的一段文字（chip 名、提示词都会出现在这里）——用来确认挂对了。"""
        return self._run(
            "(()=>{const els=[...document.querySelectorAll('[contenteditable=true]')];"
            "const el=els[els.length-1];if(!el)return '(找不到输入框)';"
            "let p=el;for(let i=0;i<3&&p;i++)p=p.parentElement;"
            "const t=((p||el).innerText||'').replace(/\\n+/g,' | ');"
            "return t.slice(-260);})()"
        )

    # ---------- 对外 ----------

    def generate(self, prompt, timeout=240, settle=6, keep=1):
        """生成一次，返回新出的图（字节流）。默认只收**前 1 张**。

        Flow 一次通常出 2 张，但解说片每页只用一张 —— 收多了是浪费（落盘、量、比对都要挑）。
        要两版比自己改 keep=2。

        取图三步（2026-10-19 定稿，每步都是踩出来的）：
          ① 等 base 变新 —— 尺寸写在 URL 后缀里（`=s512-rw` / `=s1600-rw`），所以按 base 去重，
             并且**取图时自己拼 `=s1600-rw`** 拿原图；
          ② **跟基线指纹比** —— 网格是虚拟滚动，老图会在生成后"补加载"而看起来像新图
             （这个坑吃掉了批次 C 的两张：长桌、门前，都是项目里早先就有的图）；
             比中基线的（同一张图，16×16 灰度平均绝对差 ≈ 0）直接扔掉继续等；
          ③ 收不到就再等一轮 —— 别急着报错（出图要排队）。
        """
        before = self.known
        t = self._type_prompt(prompt)
        if not isinstance(t, dict) or not t.get("ok"):
            raise RuntimeError(f"提示词没输进去：{t}")
        # 读回核对：输入框里有旧提示词没清掉的话，这里会露馅
        back = "".join((t.get("text") or "").split())
        want = "".join(prompt.split())
        if want and want not in back:
            raise RuntimeError(f"提示词读回不一致（要 {len(want)} 字，框里 {len(back)} 字）：{back[:60]}…")
        time.sleep(2)
        self.baseline_sigs()               # 先把指纹算好（生成之后项目里就多一张图了）
        c = self._click_generate()
        if not isinstance(c, dict) or not c.get("ok"):
            raise RuntimeError(f"点不到生成按钮：{c}")

        deadline = time.time() + timeout
        new, got = [], []
        while time.time() < deadline:
            time.sleep(6)
            cur = self._image_bases()
            fresh = [b for b in sorted(cur - before) if b not in self._rejected]
            if len(fresh) != len(new):
                new = fresh
                self.log(f"  新图 {len(new)} 张（等生成）")
            if new:
                time.sleep(settle)
                try:
                    cand = self._fetch_raw(new[:6], min_w=900)
                except Exception as e:                  # noqa: BLE001
                    self.log(f"    取图没成（可能还在生成）：{e}")
                    cand = []
                fresh2 = []
                for x in cand:
                    blob = base64.b64decode(x["b64"])
                    old, why = self._is_old(blob)
                    if old:
                        self.log(f'    扔掉 {x.get("b") and x["b"][-14:]}: 跟老图一模一样（差 {why[0]}）')
                        if x.get("b"):
                            self._rejected.add(x["b"])   # 记住，别再反复试它
                        continue
                    fresh2.append((x, blob))
                if fresh2:
                    got = [b for _, b in fresh2[:max(keep, 1)]]
                    self.log("  收到 " + "、".join(f'{x.get("w")}x{x.get("h")}' for x, _ in fresh2))
                    break
        if not new:
            # 别只说"没等到"——把现场打出来，好知道是卡住了、被拒了、还是界面变了
            d = self._run(_DUMP)
            self.log(f"  超时现场：{json.dumps(d, ensure_ascii=False)[:600]}")
            raise RuntimeError(f"{timeout} 秒内没等到新图（现场已打在日志里）")
        if not got:
            raise RuntimeError(f"新图出来了（{len(new)} 张）但都不是新的（全是老图或尺寸不达标）")
        self.known |= self._image_bases()
        if self._sigs is not None:
            for b in got:                       # 记上刚生成的，免得下一轮当成老图
                try:
                    self._sigs.append((_sig(b), "(刚生成)"))
                except Exception:               # noqa: BLE001
                    self._sigs = None
                    break
        return got

    def _fetch_raw(self, bases, min_w=900, size=1600):
        """在页面里 fetch 成 base64 再拿回来（命令行连不上图床）。

        每个 base 先试 `=s<size>-rw`（原图 / 指定尺寸），失败再退回原始 URL；
        宽度不到 `min_w` 的一律不要（网格里有素材缩略图 512×512）。
        返回 `[{b, w, h, size, b64}, …]`（`b` 是 base，用来对号入座）。

        **必须分批**：项目里的图会越攒越多（200+ 张时一次拼进去，命令行超过
        Windows 的 32K 上限 → WinError 206，整批生图全挂）。2026-10-22 踩过。
        """
        bases = list(bases)
        if not bases:
            return []
        got = []
        for i in range(0, len(bases), 20):
            chunk = bases[i:i + 20]
            js = _FETCH_IMGS % (json.dumps(chunk), min_w, size)
            out, err, code = _bsk("evaluate", js, "--session", self.sid, json_out=True, timeout=600)
            try:
                o = json.loads(out)
            except Exception:                                      # noqa: BLE001
                raise RuntimeError(f"取图失败：{(out or err)[:300]}") from None
            if not o.get("ok"):
                raise RuntimeError(f"取图失败：{json.dumps(o)[:300]}")
            got.extend(o.get("value") or [])
        return got

    def _fetch(self, bases, min_w=900):
        """只要字节流（老接口，保持兼容）。"""
        got = self._fetch_raw(bases, min_w=min_w)
        if not got:
            raise RuntimeError(f"没收到大图（{len(list(bases))} 个候选，宽度都不到 {min_w}）")
        self.log("  收到 " + "、".join(f'{x.get("w")}x{x.get("h")}' for x in got))
        return [base64.b64decode(x["b64"]) for x in got]

    # ---------- 指纹（挡"老图当新图"）----------

    def baseline_sigs(self, refresh=False):
        """已知图片的指纹（16×16 灰度）——"新图"里混进老图时，靠它认出来扔掉。

        用 `=s128-rw` 拉小图（省流量、快）。一次会话算一次就够。
        """
        if self._sigs is not None and not refresh:
            return self._sigs
        got = self._fetch_raw(sorted(self.known), min_w=0, size=128)
        self._sigs = [(_sig(base64.b64decode(x["b64"])), x.get("b") or "")
                      for x in got if x.get("b64")]
        self.log(f"  基线指纹：{len(self._sigs)} 张")
        return self._sigs

    def _full_bases(self, passes=10):
        """把网格滚一遍取**并集**。

        网格是虚拟滚动：离屏的图会被卸载，所以"读一次"永远取不全已知集合；
        取不全的后果就是**把老图当新图**（这个坑踩过两次了）。
        """
        seen = set()
        for i in range(passes):
            seen |= self._image_bases()
            self._run(f"window.scrollTo(0, {i * 700})")
            time.sleep(0.9)
        seen |= self._image_bases()
        self._run("window.scrollTo(0, 0)")
        time.sleep(0.8)
        seen |= self._image_bases()
        return seen

    def _is_old(self, png, thresh=2.5):
        """这张图是不是项目里已有的那张（跟基线指纹比）。

        阈值 2.5 是实测定的：**同一份文件**（同图不同尺寸再缩放）差 ≈ 0–1.5；
        两次**不同**的生成（哪怕提示词一样、构图很像）差 ≥ 4 —— 所以 2.5 能分开，
        而早先写的 6.0 会把"重新画过但很像"的图误判成老图（实测踩到，还死循环）。
        """
        sigs = self.baseline_sigs()
        if not sigs:
            return False, None
        s = _sig(png)
        best = None
        for other, base in sigs:
            d = _sig_dist(s, other)
            if best is None or d < best[0]:
                best = (d, base)
            if d <= thresh:
                return True, (round(d, 2), base[-24:])
        return False, (round(best[0], 2), best[1][-24:]) if best else None


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
