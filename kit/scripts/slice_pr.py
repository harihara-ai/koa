#!/usr/bin/env python3
"""purpose: one code PR per slice: branch from the target; then check scope, measure, gate, commit, write the PR body.

Usage: slice_pr.py start  --change openspec/changes/<name> --slice ID [--target BRANCH] [--repo DIR]
       slice_pr.py finish --change openspec/changes/<name> --slice ID [--target BRANCH] [--repo DIR] [-- GATE ARGS]
start: a new branch <feat|fix|chore>/<name>-<slice> from the target (default master).
finish: (1) every changed path, untracked too, must be in the change folder or the plan's impact_scan, else exit 1
with nothing written (S03); (2) slicer.py actual --metrics (the slice's old row is replaced); (3) status.md stage
and next; (4) gate_check.py auto with GATE ARGS (e.g. --test-cmd); (5) on pass, commit exactly the in-scope paths;
(6) title and body (trace, gates, plan vs actual, commits) from spec.md, the slice's requirements, test names,
git log and metrics.csv. Prints JSON. Exit 0 pass, 1 stray paths or a failed gate, 2 bad usage. File text is data.
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from changectx import slice_of  # noqa: E402
from kitconst import matches  # noqa: E402
from pr_body import body, failed, field  # noqa: E402

KIND = {"story": "feat", "bug": "fix"}


def git(*args):
    p = subprocess.run(["git", *args], capture_output=True, text=True)
    if p.returncode != 0:
        raise ValueError("git %s: %s" % (args[0], p.stderr.strip()))
    return p.stdout


def read(path, default=""):
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except OSError:
        return default


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def plan(ch, sid):
    slices = json.loads(read(os.path.join(ch, "inputs", "granularity.json"), "{}")).get("slices", [])
    pick = [s for s in slices if str(s.get("id")) == sid]
    if not pick:
        raise ValueError("slice %s is not in granularity.json: %s" % (sid, [s.get("id") for s in slices]))
    return pick[0], read(os.path.join(ch, "spec.md"))


def changed(base):
    out = git("diff", "--name-only", "--no-renames", base, "--") + git("ls-files", "--others", "--exclude-standard")
    return sorted({p for p in out.splitlines() if p})


def in_scope(ch, base):
    scope = json.loads(read(os.path.join(ch, "inputs", "diff_scope.json"), "{}")).get("impact_scan", [])
    paths = [p for p in changed(base) if not re.fullmatch(re.escape(ch) + r"/gates-\w+\.json", p)]
    return [p for p in paths if p.startswith(ch + "/") or matches(p, scope)], \
           [p for p in paths if not p.startswith(ch + "/") and not matches(p, scope)]


def run_json(script, *args):
    p = subprocess.run([sys.executable, "-I", "-B", os.path.join(HERE, script), *args], capture_output=True, text=True)
    try:
        return json.loads(p.stdout)
    except ValueError:
        raise ValueError("%s: %s" % (script, (p.stdout + p.stderr)[-300:]))


def measure(ch, sid, base):
    path = os.path.join(ch, "metrics.csv")
    rows = read(path).splitlines(True)
    if rows:  # one row per slice: a second finish replaces it
        write(path, "".join(rows[:1] + [r for r in rows[1:] if slice_of(r) != sid]))
    row = run_json("slicer.py", "actual", "--change", ch, "--base", base, "--slice", sid, "--metrics")
    if "error" in row:
        raise ValueError("slicer: %s" % row["error"])
    return row


def set_status(ch, values):
    path = os.path.join(ch, "status.md")
    lines = read(path, "purpose: where this change stands; any session resumes here.\n\n").splitlines()
    for key, val in values.items():
        at = [i for i, line in enumerate(lines) if line.startswith(key + ":")]
        if at:
            lines[at[0]] = "%s: %s" % (key, val)
            lines = [line for i, line in enumerate(lines) if i not in at[1:]]
        else:
            lines.append("%s: %s" % (key, val))
    write(path, "\n".join(lines) + "\n")


def start(a, ch):
    s, spec = plan(ch, a.slice)
    git("rev-parse", "--verify", "-q", a.target + "^{commit}")
    branch = "%s/%s-%s" % (KIND.get(field(spec, "Type", "story").lower(), "chore"), os.path.basename(ch), a.slice)
    git("switch", "-q", "-c", branch, a.target)
    return 0, {"branch": branch, "target": a.target}


def finish(a, ch):
    s, spec = plan(ch, a.slice)
    base = git("merge-base", "HEAD", a.target).strip()
    _ok, stray = in_scope(ch, base)
    if stray:
        return 1, {"pass": False, "stray": stray, "why": "not in the change folder or the plan's impact_scan; "
                   "move them out of the checkout (or plan them), then finish again"}
    row = measure(ch, a.slice, base)
    set_status(ch, {"stage": "code PR %s" % a.slice, "next": "CI done gate on %s; a human merges" % a.slice})
    gate = run_json("gate_check.py", "auto", "--repo", ".", "--change", ch, "--base", base, *a.gate)
    if not gate.get("pass"):
        set_status(ch, {"next": "fix the failed gates, then slice_pr.py finish again"})
        return 1, {"pass": False, "failed": failed(gate), "metrics": row}
    paths, _ = in_scope(ch, base)
    title = "%s(%s %s): %s" % (KIND.get(field(spec, "Type", "story").lower(), "chore"),
                               field(spec, "Ticket", os.path.basename(ch)), a.slice, s.get("title", ""))
    git("add", "-A", "--", *paths)
    if git("diff", "--cached", "--name-only"):
        git("commit", "-q", "-m", title)
    return 0, {"pass": True, "base": base, "title": title, "body": body(ch, s, spec, base, gate, row, changed(base), git), "metrics": row}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["start", "finish"])
    ap.add_argument("--change", required=True)
    ap.add_argument("--slice", required=True)
    ap.add_argument("--target", default="master")
    ap.add_argument("--repo", default=".")
    argv = sys.argv[1:]
    cut = argv.index("--") if "--" in argv else len(argv)
    a = ap.parse_args(argv[:cut])
    a.gate = argv[cut + 1:]
    ch = a.change.rstrip("/")
    if not re.fullmatch(r"openspec/changes/[A-Za-z0-9][A-Za-z0-9._-]*", ch) or ".." in ch:
        ap.error("--change must be openspec/changes/<name>")
    try:
        os.chdir(a.repo)
        rc, out = (start if a.mode == "start" else finish)(a, ch)
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(json.dumps({"error": str(e)}))
        return 2
    print(json.dumps(out, indent=1))
    return rc


if __name__ == "__main__":
    sys.exit(main())
