"""看网格里每一张图的 URL 长什么样（为什么新图没被认出来）。

用法：python experiments/diag_urls.py
"""
import json
import pathlib
import re
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECT = "https://flow.google.com/project/2423a8a2-2219-4dd5-83ea-563fd00a79fb"


def bsk(*args, timeout=180, json_out=False):
    cmd = ["bsk", *[str(a) for a in args]]
    if json_out:
        cmd.append("--json")
    p = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    return p.stdout or "", p.stderr or "", p.returncode


JS = r"""(()=>{
  const rows=[];
  const seen=new Set();
  for(const el of document.querySelectorAll('*')){
    let u=el.src||'';
    if(!u && el.style && el.style.backgroundImage){
      const m=/url\(["']?([^"')]+)/.exec(el.style.backgroundImage);
      if(m) u=m[1];
    }
    if(!u) continue;
    if(seen.has(u)) continue; seen.add(u);
    rows.push({tag:el.tagName, w:el.naturalWidth||0, h:el.naturalHeight||0,
               u:u.slice(0,160), host:(u.match(/^https?:\/\/[^/]+/)||[''])[0]});
  }
  return JSON.stringify(rows);
})()"""


def main():
    out, err, _ = bsk("session", "start", json_out=True)
    sid = re.search(r'"session_id"\s*:\s*"([^"]+)"', out).group(1)
    try:
        bsk("window", "resize", "--session", sid, "--width", "1600", "--height", "900")
        bsk("navigate", PROJECT, "--session", sid)
        time.sleep(15)
        for _ in range(3):
            bsk("scroll-to", "--selector", "body", "--session", sid)
            bsk("wheel", "0", "1200", "--session", sid)
            time.sleep(2)
        out, err, _ = bsk("evaluate", JS, "--session", sid, json_out=True, timeout=300)
        try:
            val = json.loads(out).get("value")
            if isinstance(val, str):
                val = json.loads(val)
        except Exception as e:                                      # noqa: BLE001
            print("parse fail", out[:300], err[:300])
            return 1
        hosts = {}
        for r in val:
            hosts[r["host"]] = hosts.get(r["host"], 0) + 1
        print("hosts:", json.dumps(hosts, ensure_ascii=False, indent=1))
        print("total:", len(val))
        for r in val[:60]:
            print(f'  {r["tag"]:<6} {r["w"]}x{r["h"]:<5} {r["u"][:120]}')
    finally:
        bsk("session", "stop", sid)
    return 0


if __name__ == "__main__":
    sys.exit(main())
