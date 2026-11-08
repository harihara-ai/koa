#!/usr/bin/env python3
"""purpose: every REQ ID in the change's spec appears in at least one test file (traceability, G3 check 6).

Input: {"spec_dirs": [change folder], "type": work type}. Requirement IDs come from spec.md and specs/*.md only
(never the fetched ticket). Test files are code or .feature files matching the fixed test globs (kitconst), so
an ID in production code, docs or a text file does not count. REQ-AREA-001, REQ_AREA_001, testReq_Area_001 match.
One code PR per slice (S04): with "metrics" (the PR's metrics.csv from slicer actual --metrics), a requirement whose
slices.md row (approved plan) names only slices without a metrics row is pending (a warning); the rest need a test.
"""
import os
import re
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
from gateio import UsageError, finding, run  # noqa: E402
from kitconst import NO_REQUIREMENT_TYPES, SKIP_DIRS, TEST_EXT, is_test_file  # noqa: E402

SPEC_ID = re.compile(r"REQ-[A-Z0-9]+-[0-9]+")
TEST_ID = re.compile(r"(?<![0-9])REQ[-_]([A-Za-z0-9]+?)[-_]([0-9]+)(?![0-9])", re.I)


def norm(area, num):
    return "REQ-%s-%03d" % (area.upper(), int(num))


def spec_ids(dirs):
    found = set()
    for d in dirs:
        specs = [os.path.join(d, "spec.md")]
        specs += [os.path.join(r, n) for r, _d, fs in os.walk(os.path.join(d, "specs")) for n in fs if n.endswith(".md")]
        for path in specs:
            if os.path.isfile(path):
                with open(path, encoding="utf-8", errors="ignore") as fh:
                    found |= {norm(*i.split("-")[1:]) for i in SPEC_ID.findall(fh.read())}
    return found


def test_ids():
    found, n = set(), 0
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            rel = os.path.relpath(os.path.join(root, name), ".").replace(os.sep, "/")
            if not is_test_file(rel) or not rel.lower().endswith(TEST_EXT):
                continue
            n += 1
            with open(rel, encoding="utf-8", errors="ignore") as fh:
                found |= {norm(a, b) for a, b in TEST_ID.findall(fh.read())}
    return found, n


def check(p):
    ids = spec_ids([d for d in p.get("spec_dirs", []) if os.path.isdir(d)])
    if not ids:
        if p.get("type") in NO_REQUIREMENT_TYPES:
            return [finding("nothing_to_check", "no requirements in a %s change" % p["type"], "", "warn")], {}
        return [finding("no_ids", "no REQ IDs found in %s" % p.get("spec_dirs"))], {}
    tested, n = test_ids()
    if not n:
        return [finding("no_test_files", "no test files found (see kitconst.TEST_GLOBS)")], {}
    later = pending(p.get("spec_dirs", []), p.get("metrics"))
    f = [finding("untested", "%s has no test" % i, i) for i in sorted(ids - tested - later)]
    f += [finding("pending", "%s belongs to a slice not built yet" % i, i, "warn") for i in sorted((ids & later) - tested)]
    return f, {"requirements": sorted(ids)}


def pending(dirs, metrics):
    """Requirements whose slices.md rows name only slices with no metrics.csv row yet."""
    later, built = set(), set()
    if not (metrics and os.path.isfile(metrics)):
        return later
    with open(metrics, encoding="utf-8", errors="ignore") as fh:
        done = {line.split(",")[0].strip() for line in fh.readlines()[1:]}
    for d in dirs:
        rows = os.path.join(d, "slices.md")
        if not os.path.isfile(rows):
            continue
        with open(rows, encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                cells = line.strip().strip("|").split("|")
                if line.startswith("|") and len(cells) > 1:
                    reqs = {norm(*i.split("-")[1:]) for i in SPEC_ID.findall(line)}
                    (built if cells[0].strip() in done else later).update(reqs)
    return later - built


if __name__ == "__main__":
    sys.exit(run("trace_check", check))
