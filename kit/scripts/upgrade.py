#!/usr/bin/env python3
"""purpose: upgrade an installed kit: delete kit/, unzip the install zip, run the gate with the new and the old kit.

Usage: upgrade.py --zip northstar-kit-install.zip [--target BRANCH] [--repo DIR] [-- GATE ARGS]
Refuses (exit 1, nothing changed) a checkout with uncommitted or untracked files; refuses (exit 2, nothing changed)
a zip with no kit/ or with a path outside kit/, .claude/commands/ and kit.manifest.yml. Leaves the result
uncommitted for the human upgrade PR. Prints JSON: changed, deleted, gate_new, gate_old. Exit 0 both gates pass.
"""
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile

ALLOWED = ("kit/", ".claude/commands/")


def git(*args, raw=False):
    p = subprocess.run(["git", *args], capture_output=True, text=not raw)
    if p.returncode != 0:
        raise ValueError("git %s: %s" % (args[0], p.stderr if raw else p.stderr.strip()))
    return p.stdout


def porcelain():
    return [(line[:2], line[3:]) for line in git("status", "--porcelain", "--untracked-files=all").splitlines() if line]


def read_zip(path):
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if not n.endswith("/")]
        bad = [n for n in names if n.startswith("/") or "\\" in n or ".." in n.split("/") or ":" in n
               or not (n.startswith(ALLOWED) or n == "kit.manifest.yml")]
        if bad:
            raise ValueError("refused paths in the zip (only kit/, .claude/commands/, kit.manifest.yml): %s" % bad[:5])
        if not any(n.startswith("kit/") for n in names):
            raise ValueError("no kit/ in the zip")
        return {n: z.read(n) for n in names}


def gate(kit, base, extra):
    p = subprocess.run([sys.executable, "-I", "-B", os.path.join(kit, "scripts", "gate_check.py"), "auto",
                        "--repo", ".", "--change", "auto", "--base", base, *extra], capture_output=True, text=True)
    try:
        out = json.loads(p.stdout)
    except ValueError:
        return {"pass": False, "error": (p.stdout + p.stderr)[-300:]}
    return {"pass": bool(out.get("pass")) and p.returncode == 0, "stage": out.get("stage"), "note": out.get("error"),
            "failed": [g.get("gate") for g in out.get("gates", []) if not g.get("pass")]}


def old_kit(base):
    d = tempfile.mkdtemp(prefix="kit-old-")
    with tarfile.open(fileobj=io.BytesIO(git("archive", "--format=tar", base, "kit", raw=True))) as t:
        t.extractall(d, filter="data")
    return os.path.join(d, "kit")


def upgrade(path, target, extra):
    base = git("merge-base", "HEAD", target).strip()
    dirty = sorted(p for _s, p in porcelain())
    if dirty:
        return 1, {"dirty": dirty, "why": "commit, stash or move these first; an upgrade PR holds only the kit"}
    files = read_zip(path)
    shutil.rmtree("kit", ignore_errors=True)
    for rel, data in files.items():
        os.makedirs(os.path.dirname(rel) or ".", exist_ok=True)
        with open(rel, "wb") as fh:
            fh.write(data)
    status = porcelain()
    out = {"changed": sorted(p for s, p in status if "D" not in s), "deleted": sorted(p for s, p in status if "D" in s),
           "gate_new": gate("kit", base, extra), "gate_old": gate(old_kit(base), base, extra)}
    return (0 if out["gate_new"]["pass"] and out["gate_old"]["pass"] else 1), out


def main():
    argv = sys.argv[1:]
    cut = argv.index("--") if "--" in argv else len(argv)
    opts, extra = argv[:cut], argv[cut + 1:]
    a = {"--zip": None, "--target": "master", "--repo": "."}
    while opts:
        key = opts.pop(0)
        if key not in a or not opts:
            print(__doc__)
            return 2
        a[key] = opts.pop(0)
    if not a["--zip"]:
        print(__doc__)
        return 2
    try:
        zpath = os.path.abspath(a["--zip"])
        os.chdir(a["--repo"])
        rc, out = upgrade(zpath, a["--target"], extra)
    except (OSError, ValueError, zipfile.BadZipFile) as e:
        print(json.dumps({"error": str(e)}))
        return 2
    print(json.dumps(out, indent=1))
    return rc


if __name__ == "__main__":
    sys.exit(main())
