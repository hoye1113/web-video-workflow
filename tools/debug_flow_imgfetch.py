"""查清 flow.google.com/asb/... 这种图怎么才能拿下来。"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
import flowgen  # noqa: E402

SID = sys.argv[1] if len(sys.argv) > 1 else "zylj"
f = flowgen.Flow()
f.sid = SID

JS = """(async()=>{
  const img=[...document.querySelectorAll('img')].find(i=>i.naturalWidth>=1000);
  if(!img) return {err:'没有大图'};
  const u=img.src;
  const r=await fetch(u);
  const ct=r.headers.get('content-type')||'';
  const buf=await r.arrayBuffer();
  const head=new Uint8Array(buf.slice(0,24));
  // 也试试 canvas（同源应该能导出）
  let canvas=null;
  try{const c=document.createElement('canvas');c.width=img.naturalWidth;c.height=img.naturalHeight;
    c.getContext('2d').drawImage(img,0,0);canvas=c.toDataURL('image/png').length;}catch(e){canvas='ERR:'+e.name;}
  return {status:r.status, ok:r.ok, ct, size:buf.byteLength,
    magic:[...head].map(b=>b.toString(16).padStart(2,'0')).join(' '),
    asText:(ct.includes('json')||ct.includes('text'))?new TextDecoder().decode(buf).slice(0,200):'',
    canvasPngLen:canvas};
})()"""

out, err, code = flowgen._bsk("evaluate", JS, "--session", SID, json_out=True, timeout=300)
print("evaluate 输出：")
print((out or "")[:1200])
if err:
    print("stderr:", err[:300])
