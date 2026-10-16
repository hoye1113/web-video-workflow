"""模型输出的文本处理：去围栏、抠 JSON、校准场景注册名。"""
import json
import re

_SCENE_REG = re.compile(r"SCENES\['([^']+)'\]\s*=")


def strip_fence(t):
    t = (t or "").strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n", "", t)
        t = re.sub(r"\n```\s*$", "", t)
    return t.strip() + "\n"


def repair_json(s):
    """模型经常把引号写进字符串里，把 JSON 撑破：

        "problems": ["…违反"不发光、单笔触"的画风锁", "…"]

    这里扫一遍，把「不在 key/值边界上的引号」转义掉。
    边界判断：引号后面第一个非空白字符是 : , } ] 之一 → 它是收尾引号；否则是裸引号。
    """
    out, in_str, i, n = [], False, 0, len(s)
    while i < n:
        ch = s[i]
        if ch == '"':
            if not in_str:
                in_str = True
            else:
                j = i + 1
                while j < n and s[j] in " \t\r\n":
                    j += 1
                nxt = s[j] if j < n else ""
                if nxt in ":,}]" or nxt == "":
                    in_str = False
                else:
                    out.append('\\"')          # 裸引号，转义
                    i += 1
                    continue
        out.append(ch)
        i += 1
    return "".join(out)


def extract_json(text, kind):
    """把第一段合法的 JSON 抠出来；撑破了就先修一遍再试。"""
    t = strip_fence(text)
    span = None
    for cand in (t, text or ""):
        s = cand.find("[" if kind is list else "{")
        e = cand.rfind("]" if kind is list else "}")
        if s >= 0 and e > s:
            span = cand[s:e + 1]
            break
    if span is None:
        raise ValueError("模型没有返回 JSON：" + (text or "")[:300])
    try:
        return json.loads(span)
    except Exception:                                      # noqa: BLE001
        pass
    try:
        return json.loads(repair_json(span))
    except Exception as e:                                 # noqa: BLE001
        raise ValueError(f"模型返回的 JSON 修不好（{e}）：{span[:300]}") from None


def loose_fields(text, keys):
    """最后兜底：JSON 实在修不好时，用正则把几个关键字段抠出来。"""
    out = {}
    for k, pat in (("score", r'"score"\s*:\s*(-?\d+)'),
                   ("ok", r'"ok"\s*:\s*(true|false)')):
        if k in keys:
            m = re.search(pat, text or "")
            if m:
                out[k] = int(m.group(1)) if k == "score" else (m.group(1) == "true")
    for k in ("problems", "fixes"):
        if k not in keys:
            continue
        m = re.search(rf'"{k}"\s*:\s*\[(.*?)\]', text or "", re.S)
        if m:
            items = [x.strip().strip('"').strip() for x in re.split(r'",\s*"', m.group(1))]
            out[k] = [x for x in items if x]
    return out


def parse_review(raw):
    """评审结果的解析：正常 JSON → 修一遍的 JSON → 正则抠字段。三层兜底。"""
    try:
        return extract_json(raw, dict)
    except Exception as e:                                 # noqa: BLE001
        f = loose_fields(raw, ("score", "ok", "problems", "fixes"))
        if f.get("score") is not None or f.get("problems"):
            f["_recovered"] = True
            return f
        raise e


def fix_scene_id(src, sid):
    """场景文件的注册名必须是 SCENES['<页号>']，引擎按它找文件。

    模型经常自己起名字（实测给过 SCENES['p02_window_paper']），引擎就拒绝渲染。
    确定性校验：只有一个注册名但不是目标名，就地改掉；其余情况直接报错。
    """
    ids = _SCENE_REG.findall(src)
    if not ids:
        raise ValueError(f"代码里没有注册 SCENES['{sid}'] —— 引擎要求每个场景文件注册一次")
    if sid in ids:
        return src, False
    if len(set(ids)) == 1:
        return _SCENE_REG.sub(f"SCENES['{sid}'] =", src, count=1), True
    raise ValueError(f"代码里注册了多个名字 {sorted(set(ids))}，不知道用哪个")


def text_field(v, field="这个字段"):
    """把请求里的文本字段取成字符串。

    宽进：PowerShell 的 ConvertTo-Json 会把带扩展属性的长字符串包成
    {"value": "...", "PSPath": "..."}，这种也认。
    严出：真不是文本就明确报错，不要让它一路崩到后面去。
    """
    if isinstance(v, str):
        return v
    if isinstance(v, dict) and isinstance(v.get("value"), str):
        return v["value"]
    if v is None:
        return ""
    raise ValueError(f"{field} 要的是文本，收到 {type(v).__name__}")
