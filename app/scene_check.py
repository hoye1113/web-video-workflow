"""场景代码的语法检查（确定性，秒级）。

**为什么必须有这一道**：实测模型会写出 `}})();` 这种多一个大括号的代码。
不检查的话，这个错要等到**渲染抽帧**才暴露 —— 抽帧要起 Playwright、等十几秒，
报回来的还是一句 "Unexpected token '}'"，得人肉回去数括号。
用 node --check 解析一遍只要 50 毫秒，在存盘**之前**就能拦下来。

node 不在也不影响：返回空字符串放行（不假装检查过）。
"""
import subprocess
import tempfile
from pathlib import Path

NODE = None
for p in (Path("C:/Program Files/nodejs/node.exe"), Path("C:/Program Files (x86)/nodejs/node.exe")):
    if p.exists():
        NODE = str(p)
        break


def syntax_errors(src):
    """返回一句人话的语法错（没毛病返回 ""）。"""
    if not NODE:
        return ""
    if not (src or "").strip():
        return "文件是空的"
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False,
                                     encoding="utf-8", newline="\n") as f:
        f.write(src)
        tmp = f.name
    try:
        r = subprocess.run([NODE, "--check", tmp], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=30)
        if r.returncode == 0:
            return ""
        # node 的报错长这样：
        #   <文件>:<行>
        #   <那一行>
        #    ^
        #   SyntaxError: Unexpected token '}'
        msg = (r.stderr or r.stdout or "").strip().splitlines()
        err = next((x for x in reversed(msg) if "Error" in x), msg[-1] if msg else "未知")
        line = next((x.strip() for x in msg if x.strip().endswith(":") is False and
                     x.strip().isdigit()), "")
        return f"{err.strip()}（第 {line} 行附近）" if line else err.strip()
    except Exception as e:                                     # noqa: BLE001
        return f"检查没跑起来：{e}"
    finally:
        try:
            Path(tmp).unlink()
        except OSError:
            pass


def braces_balanced(src):
    """数括号（去掉注释和字符串）——node 报"在多出来的那个"不报位置，这个能报位置。"""
    import re
    STR = re.compile(r"'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\"|`(?:[^`\\]|\\.)*`")
    d, bad = 0, []
    for i, raw in enumerate((src or "").splitlines(), 1):
        t = STR.sub("''", re.sub(r"//.*", "", raw))
        prev = d
        d += t.count("{") - t.count("}")
        if d < prev and d < 0:
            bad.append(i)
    return (d == 0 and not bad), d


def fix_syntax(ai, src, sid, say=print, tries=1):
    """存盘前解析一遍；有错就让模型**只修那一处**（别的一概不许动）。

    服务端和导演回路都走这一个函数，别各写一套。
    """
    import prompts
    import text as T
    err = syntax_errors(src)
    if not err:
        return src
    for _ in range(tries):
        say(f"代码有语法错（{err}），让模型修一遍…")
        out = T.strip_fence(ai.generate(
            prompts.FIX_SYNTAX.format(error=err, src=src, shot=sid), timeout=420))
        out, _renamed = T.fix_scene_id(out, sid)
        err2 = syntax_errors(out)
        if not err2:
            say("修好了")
            return out
        say(f"还是错：{err2}")
        src, err = out, err2
    raise ValueError(f"模型修了 {tries} 遍还是有语法错：{err}")


if __name__ == "__main__":
    import sys
    s = Path(sys.argv[1]).read_text(encoding="utf-8")
    print("node:", syntax_errors(s) or "没问题")
    ok, d = braces_balanced(s)
    print(f"括号差 {d}", "配对" if ok else "不配对")
