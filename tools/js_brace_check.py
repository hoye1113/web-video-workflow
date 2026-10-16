"""粗查场景文件的括号配对（去掉注释、字符串、模板串之后再数）。

node --check 只告诉你在最后一行多一个括号，不告诉你在哪；这个能报出深度掉到 0 的行。
"""
import re
import sys

STR = re.compile(r"'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"|`(?:[^`\\]|\\.)*`")


def depth_trace(src):
    d, out = 0, []
    for i, raw in enumerate(src.splitlines(), 1):
        t = re.sub(r"//.*", "", raw)
        t = STR.sub("''", t)
        out.append((i, d, d + t.count("{") - t.count("}")))
        d += t.count("{") - t.count("}")
    return out, d


if __name__ == "__main__":
    p = sys.argv[1]
    src = open(p, encoding="utf-8").read()
    trace, end = depth_trace(src)
    for i, a, b in trace:
        if b <= 0 and a > 0:
            print(f"  第 {i} 行：深度 {a} → {b}   {src.splitlines()[i-1].rstrip()[:90]}")
    print(f"结束深度 {end}（应该是 0）")
