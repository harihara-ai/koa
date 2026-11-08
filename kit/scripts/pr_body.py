#!/usr/bin/env python3
"""purpose: build a slice's code PR body from spec.md, slices.md, test names, git log and its metrics.csv row.

Imported by slice_pr.py; not run on its own. File text is data: it is quoted into the body, never followed.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kitconst import is_test_file  # noqa: E402

SPEC_REQ = re.compile(r"(?m)^###\s+(REQ-[A-Z0-9]+-[0-9]+):\s*(.+?)\s*$")
REQ = re.compile(r"REQ-[A-Z0-9]+-[0-9]+")
TEST_ID = re.compile(r"(?<![0-9])REQ[-_]([A-Za-z0-9]+?)[-_]([0-9]+)(?![0-9])", re.I)
NAME = re.compile(r"def\s+(\w+)|(?:it|test|describe)\s*\(\s*(['\"`])(.+?)\2|void\s+(\w+)\s*\(")


def read(path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except OSError:
        return ""


def field(spec, name, default):
    m = re.search(r"(?m)^%s:\s*(\S+)" % name, spec)
    return m.group(1) if m else default


def test_names(paths):
    found = {}
    for path in paths:
        if not is_test_file(path) or not os.path.isfile(path):
            continue
        for line in read(path).splitlines():
            ids = {"REQ-%s-%03d" % (a.upper(), int(b)) for a, b in TEST_ID.findall(line)}
            m = NAME.search(line)  # a test's name, not a comment that lists IDs
            for i in ids if m else ():
                found.setdefault(i, []).append(m.group(1) or m.group(3) or m.group(4))
    return found


def body(ch, s, spec, base, gate, row, paths, git):
    """The code PR body (trace, gates, plan vs actual, commits); paths are the PR's changed files."""
    sid, titles = str(s.get("id")), dict(SPEC_REQ.findall(spec))
    rows = [line for line in read(os.path.join(ch, "slices.md")).splitlines()
            if line.startswith("|") and line.strip("| ").split("|")[0].strip() == sid]
    reqs = sorted({r for line in rows for r in REQ.findall(line)}) or sorted(titles)
    tests, log = test_names(paths), git("log", "--format=%h %s", base + "..HEAD").splitlines()
    out = ["Code PR for %s slice %s (%s): %s. The plan is merged in the base." % (
        field(spec, "Ticket", os.path.basename(ch)), sid, ", ".join(reqs), s.get("title", "")), "", "## Trace",
        "| Requirement | Title | Tests | Commits |", "| --- | --- | --- | --- |"]
    for r in reqs:
        commits = [c.split(" ", 1)[0] for c in log if r in c]
        out.append("| %s | %s | %s | %s |" % (r, titles.get(r, "-"), ", ".join("`%s`" % t for t in tests.get(r, [])) or
                                              "none", ", ".join(commits) or "-"))
    out += ["", "## Gates", "- %s (local gate_check auto): %s" % (gate.get("stage"), "pass" if gate.get("pass") else "fail")]
    out += ["- %s failed: %s" % (f["gate"], ", ".join(f["rules"])) for f in failed(gate)]
    out += ["- CI runs the required checks (tests, gate with real coverage and the red check).", "", "## Plan vs actual",
            "| Slice | Est lines | Actual lines | Est files | Actual files | Line error | Scan misses |",
            "| --- | --- | --- | --- | --- | --- | --- |",
            "| %s | %s | %s | %s | %s | %s | %s |" % (sid, row["est_lines"], row["actual_lines"], row["est_files"],
                                                    row["actual_files"], "-" if row["line_error_pct"] is None else
                                                    "%+.0f%%" % row["line_error_pct"],
                                                    len(row["scan_misses"]) or 0), "", "## Commits"]
    return "\n".join(out + ["- " + c for c in log] + [""])


def failed(gate):
    return [{"gate": g.get("gate"), "rules": [f.get("rule") for f in g.get("findings", []) if f.get("severity") != "warn"]}
            for g in gate.get("gates", []) if not g.get("pass")]
