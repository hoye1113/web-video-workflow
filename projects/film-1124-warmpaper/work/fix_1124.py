import json
from pathlib import Path

import opencc

src = Path(r"E:\video-factory\1124\work\1124.json")
dst = Path(r"E:\video-factory\1124\work\1124-fixed.json")
cc = opencc.OpenCC("t2s")
data = json.loads(src.read_text(encoding="utf-8"))

repl = {
    "迴避": "回避",
    "致死不渝": "至死不渝",
    "世世体贴": "事事体贴",
    "补弃": "补足",
    "理想办理": "理想伴侣",
    "竟然让焦虑": "进而让焦虑",
    "浴室习惯": "于是习惯",
    "偏偏剧不配合": "偏偏拒不配合",
    "异心缩进自己的独处事件": "一心缩进自己的独处世界",
    "爱意所取": "爱意索取",
    "被感压抑": "倍感压抑",
    "一般认清": "一旦认清",
    "型一脸": "型依恋",
    "一妹躲避": "一味躲避",
    "丝毫不与回应": "丝毫不予回应",
    "刨根问题": "刨根问底",
    "所要态度答案": "索要态度答案",
    "堵定": "笃定",
    "依恋格": "依恋人格",
    "嫉妒渴望": "极度渴望",
    "常年诉求": "常年需求",
    "隔禾": "隔阂",
    "封闭的时间": "封闭的世界",
    "去功课": "去攻克",
    "多么坚持": "多么煎熬",
}

for seg in data["segments"]:
    t = cc.convert(seg.get("text", ""))
    for a, b in repl.items():
        t = t.replace(a, b)
    seg["text"] = t

dst.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
text = "".join(s["text"] for s in data["segments"])
Path(r"E:\video-factory\1124\work\1124-fixed.txt").write_text(text, encoding="utf-8")
print("segments", len(data["segments"]), "chars", len(text))
for bad in ["迴避", "致死不渝", "世世", "补弃", "办理", "浴室", "剧不", "异心", "所取", "被感", "一脸", "一妹", "与回应", "刨根问题", "堵定", "依恋格", "嫉妒", "隔禾", "功课"]:
    if bad in text:
        print("STILL", bad)
