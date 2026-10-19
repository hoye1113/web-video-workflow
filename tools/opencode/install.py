"""把仓库里的 OpenCode 配置装到本机（agent / skill）。

为什么放仓库里：**配置也是代码** —— 版本化、可复核、换机器一条命令装回去。

装的东西：
    tools/opencode/agents/material.md   → ~/.config/opencode/agents/material.md
    tools/opencode/skills/new-film/     → ~/.config/opencode/skills/new-film/

用法：
    python tools/opencode/install.py            # 装/更新（已存在就覆盖，会先备份 .bak）
    python tools/opencode/install.py --check    # 只看会不会装、装到哪
"""
import argparse
import filecmp
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "tools" / "opencode"
DST = pathlib.Path.home() / ".config" / "opencode"


def copy_file(src: pathlib.Path, dst: pathlib.Path, check: bool):
    same = dst.exists() and filecmp.cmp(src, dst, shallow=False)
    print(f'  {"=" if same else "→"} {dst}')
    if check or same:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        shutil.copy2(dst, dst.with_suffix(dst.suffix + ".bak"))
    shutil.copy2(src, dst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    print(f"装到：{DST}")
    copy_file(SRC / "agents" / "material.md", DST / "agents" / "material.md", a.check)
    for f in (SRC / "skills" / "new-film").glob("**/*"):
        if f.is_file():
            copy_file(f, DST / "skills" / "new-film" / f.relative_to(SRC / "skills" / "new-film"),
                      a.check)
    print("\n装完自检（用 OpenCode 自己的接口看它认不认）：")
    cli = pathlib.Path.home() / "AppData" / "Local" / "Programs" / "@opencodedesktop" / "resources" / "opencode-cli.exe"
    if not cli.exists():
        print(f"  ! 没找到 {cli}（桌面版没装？）—— 手动跑：opencode api get /api/agent")
        return 0
    import json
    import subprocess
    for path, name in (("/api/agent", "agent"), ("/api/skill", "skill")):
        r = subprocess.run([str(cli), "api", "get", path], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        txt = (r.stdout or "")[:2000]
        hit = "material" in txt if name == "agent" else "new-film" in txt
        print(f'  {"✓" if hit else "✗"} {path} 里{"有" if hit else "没看到"} {name}'
              f'{"（可能要重启 OpenCode 才刷新）" if not hit else ""}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
