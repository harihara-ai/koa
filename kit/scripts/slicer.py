#!/usr/bin/env python3
"""purpose: measure a slice's impact from git (scan) and compare a finished change with its plan (actual).

Usage: slicer.py scan   --change openspec/changes/<name> [--repo DIR]
       slicer.py actual --change openspec/changes/<name> --base REF [--slice ID] [--metrics] [--repo DIR]
scan: each slice in inputs/granularity.json names "seeds": {"symbols": [...], "values": [...]} (from codenav and the
spec). git grep finds code and tests that use a symbol, and tests that hold a value (tests that pin current
behaviour, P04). Writes inputs/impact.json, raises "files" and "symbols" (never lowers them) and adds the files to
inputs/diff_scope.json impact_scan. actual: changed lines and files outside the change folder vs the estimate; a
miss is more than 50% over; scan_misses are changed files the scan did not list. --metrics appends a metrics.csv row.
Report only: exit 0, or 2 on bad input. Seeds are data: matched literally, never as options or patterns.
"""
import argparse
import csv
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kitconst import DOCS, is_test_file, matches  # noqa: E402

SKIP = ["openspec/*", "kit/*", "docs/*", ".claude/*", ".github/*"]
MISS_PCT = 50
FIELDS = ["slice", "est_lines", "actual_lines", "est_files", "actual_files", "line_error_pct", "miss", "scan_misses"]


def git(*args):
    p = subprocess.run(["git", *args], capture_output=True, text=True)
    if p.returncode not in (0, 1):  # git grep exits 1 when nothing matches
        raise ValueError("git %s: %s" % (args[0], p.stderr.strip()))
    return p.stdout


def grep(text, words):
    flags = ["-w"] if words else []
    out = git("grep", "-n", "-I", "-F", *flags, "-e", text, "--")
    return [line.split(":", 2)[:2] for line in out.splitlines()]


def kept(path):
    return not matches(path, SKIP) and not matches(path, DOCS)


def load(path, default=None):
    if not os.path.isfile(path):
        if default is not None:
            return default
        raise ValueError("missing " + path)
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=1)
        fh.write("\n")


def scan(ch):
    gpath, dpath = os.path.join(ch, "inputs", "granularity.json"), os.path.join(ch, "inputs", "diff_scope.json")
    plan, scope = load(gpath), load(dpath, {})
    if not any(isinstance(s.get("seeds"), dict) for s in plan.get("slices", [])):
        raise ValueError("no slice has seeds: add \"seeds\": {\"symbols\": [...], \"values\": [...]} per slice")
    impact, raised, found = {}, [], set()
    for s in plan["slices"]:
        seeds = s.get("seeds")
        if not isinstance(seeds, dict):
            continue
        syms = [str(x) for x in seeds.get("symbols", [])]
        code, tests, pins = set(), set(), set()
        for sym in syms:
            for path, _ in grep(sym, True):
                if kept(path):
                    (tests if is_test_file(path) else code).add(path)
        for val in (str(x) for x in seeds.get("values", [])):
            pins.update("%s:%s" % (p, n) for p, n in grep(val, False) if kept(p) and is_test_file(p))
        files = code | tests | {p.split(":")[0] for p in pins}
        impact[str(s.get("id"))] = {"code": sorted(code), "tests": sorted(tests), "pins": sorted(pins)}
        for key, measured in (("files", len(files)), ("symbols", len(syms))):
            if not isinstance(s.get(key), (int, float)) or s[key] < measured:
                raised.append("%s %s: %s -> %d" % (s.get("id"), key, s.get(key), measured))
                s[key] = measured
        found |= files
    save(os.path.join(ch, "inputs", "impact.json"), {"slices": impact})
    save(gpath, plan)
    scope["impact_scan"] = list(scope.get("impact_scan", [])) + sorted(found - set(scope.get("impact_scan", [])))
    save(dpath, scope)
    return {"impact": impact, "raised": raised}


def changed(base, ch):
    lines = {}
    for row in git("diff", "--numstat", "--no-renames", base, "--").splitlines():
        add, dele, path = row.split("\t", 2)
        lines[path] = (0 if add == "-" else int(add)) + (0 if dele == "-" else int(dele))
    for path in git("ls-files", "--others", "--exclude-standard").splitlines():
        with open(path, "rb") as fh:
            lines[path] = fh.read().count(b"\n")
    return {p: n for p, n in lines.items() if not p.startswith(ch + "/")}


def actual(ch, base, slice_id, metrics):
    slices = load(os.path.join(ch, "inputs", "granularity.json")).get("slices", [])
    pick = [s for s in slices if slice_id in (None, str(s.get("id")))]
    if len(pick) != 1:
        raise ValueError("name one slice with --slice: %s" % [s.get("id") for s in slices])
    s, diff = pick[0], changed(base, ch)
    scanned = load(os.path.join(ch, "inputs", "impact.json"), {"slices": {}})["slices"].get(str(s.get("id")), {})
    listed = set(scanned.get("code", []) + scanned.get("tests", []) + [p.split(":")[0] for p in scanned.get("pins", [])])
    est_l, est_f = s.get("lines") or 0, s.get("files") or 0
    got_l, got_f = sum(diff.values()), len(diff)
    err = round(100.0 * (got_l - est_l) / est_l, 1) if est_l else None
    row = {"slice": str(s.get("id")), "est_lines": est_l, "actual_lines": got_l, "est_files": est_f,
           "actual_files": got_f, "line_error_pct": err,
           "miss": got_l > est_l * (1 + MISS_PCT / 100.0) or got_f > est_f * (1 + MISS_PCT / 100.0),
           "scan_misses": sorted(p for p in diff if scanned and p not in listed)}
    if metrics:
        path = os.path.join(ch, "metrics.csv")
        new = not os.path.isfile(path) or not os.path.getsize(path)
        with open(path, "a", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, FIELDS)
            if new:
                w.writeheader()
            w.writerow(dict(row, scan_misses=" ".join(row["scan_misses"])))
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["scan", "actual"])
    ap.add_argument("--change", required=True)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--base")
    ap.add_argument("--slice")
    ap.add_argument("--metrics", action="store_true")
    a = ap.parse_args()
    ch = a.change.rstrip("/")
    if not ch.startswith("openspec/changes/") or ".." in ch:
        ap.error("--change must be openspec/changes/<name>")
    try:
        os.chdir(a.repo)
        if a.mode == "scan":
            out = scan(ch)
        elif not a.base:
            raise ValueError("actual needs --base")
        else:
            out = actual(ch, a.base, a.slice, a.metrics)
    except (OSError, ValueError, KeyError, TypeError) as e:
        print(json.dumps({"error": str(e)}))
        return 2
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
