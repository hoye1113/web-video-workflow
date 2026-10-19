"""看提示框容器的 HTML：chip 长什么样、能不能靠它认角色。（会话 zpou 上跑）"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

SID = sys.argv[1] if len(sys.argv) > 1 else "zpou"

js = r"""
(()=>{const els=[...document.querySelectorAll('[contenteditable=true]')];
const el=els[els.length-1];if(!el)return 'no input';
let p=el;for(let i=0;i<3&&p;i++)p=p.parentElement;
const imgs=[...p.querySelectorAll('img')].map(i=>({src:(i.src||'').slice(-60),w:i.naturalWidth,h:i.naturalHeight}));
return {html:p.outerHTML.slice(0,900), imgs:imgs};})()
"""
out, err, code = flowgen._bsk("evaluate", js, "--session", SID, json_out=True, timeout=180)
try:
    v = json.loads(out).get("value")
except Exception:                                              # noqa: BLE001
    v = {"error": (out or err)[:400]}
print(json.dumps(v, ensure_ascii=False, indent=1)[:2600])
