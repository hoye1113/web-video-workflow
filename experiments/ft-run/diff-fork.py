"""比对"原始 zip"和"我们改过的树"，列出我们到底动了哪些文件。

为什么要：FRAMETELL 是 zip 解出来的，不是 git 仓库；我们改了十几处地方没有记录。
上游更新时要能一眼看出"哪些是我们的、哪些是它的"。
"""
import hashlib
import io
import pathlib
import shutil
import sys
import zipfile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SRC = pathlib.Path(r"D:\WorkSpace\video-factory\experiments\frametell-src")
ZIP = SRC / "ft-main.zip"
OURS = SRC / "frametell-main"
PRISTINE = SRC / "_pristine"
SKIP = ("node_modules", "dist", "out", "chunks", "subs", ".git", ".render.lock")


def digest(p: pathlib.Path) -> str:
    return hashlib.sha1(p.read_bytes()).hexdigest()


def rel_files(root: pathlib.Path):
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        parts = set(p.relative_to(root).parts)
        if parts & set(SKIP):
            continue
        if p.name.endswith((".log", ".lock")):
            continue
        yield p.relative_to(root).as_posix()


def main():
    if PRISTINE.exists():
        shutil.rmtree(PRISTINE)
    print("解压原始 zip …")
    with zipfile.ZipFile(ZIP) as z:
        z.extractall(PRISTINE)
    base = PRISTINE / "frametell-main"
    if not base.exists():
        # 压缩包里可能直接是文件
        base = PRISTINE

    ours = {f: digest(OURS / f) for f in rel_files(OURS)}
    theirs = {f: digest(base / f) for f in rel_files(base)}

    added = sorted(set(ours) - set(theirs))
    removed = sorted(set(theirs) - set(ours))
    changed = sorted(f for f in set(ours) & set(theirs) if ours[f] != theirs[f])

    print(f"\n新增 {len(added)} 个：")
    for f in added:
        print("   +", f)
    print(f"\n改动 {len(changed)} 个：")
    for f in changed:
        print("   ~", f)
    print(f"\n删除 {len(removed)} 个：")
    for f in removed:
        print("   -", f)

    # 给 OURS.md 用
    out = pathlib.Path(r"D:\WorkSpace\video-factory\experiments\ft-run\our-changes.txt")
    out.write_text("\n".join([f"+ {f}" for f in added] + [f"~ {f}" for f in changed] + [f"- {f}" for f in removed]),
                   encoding="utf-8")
    print(f"\n清单写到：{out}")


if __name__ == "__main__":
    main()
