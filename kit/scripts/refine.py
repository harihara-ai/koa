#!/usr/bin/env python3
"""purpose: DoR before /slice: spec_lint findings and undecided input edges as tap-to-answer questions.

Usage: refine.py SPEC. Prints JSON {"questions": [{id, rule, where, ask, options}], "inputs": {name: {edge: decision}}}.
`## Inputs` lines: `- <input>: absent REQ-X-001; empty out; boundary REQ-X-002; invalid REQ-X-003`.
Exit 0 no questions, 1 questions to ask, 2 bad usage.
"""
import json
import os
import re
import sys
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KIT, "gates"))
sys.path.insert(0, os.path.join(KIT, "scripts"))
import spec_lint  # noqa: E402
from kitconst import NO_REQUIREMENT_TYPES  # noqa: E402

EDGES = ("absent", "empty", "boundary", "invalid")
DECISION = re.compile(r"\b(%s)\s+(REQ-[A-Z0-9]+-\d{3}|out)\b" % "|".join(EDGES))
EDGE_OPTIONS = ["Add a scenario (error or result)", "Same as an existing requirement", "Out of scope"]
OPTIONS = {
    "vague_word": ["Give a number or a standard", "Drop the word"],
    "nfr_threshold": ["Give a number or a standard", "Write: none"],
    "error_case": ["Add an error scenario", "Errors: none"],
    "open_questions": ["Answer it in the spec", "Move it to Out of scope"],
    "inputs": ["List the inputs", "No inputs (pure refactor)"],
}


def inputs(text):
    out = {}
    for line in spec_lint.sections(text.splitlines()).get("Inputs", []):
        t = line[1].strip()
        if t.startswith(("- ", "* ")) and ":" in t:
            name, rest = t[2:].split(":", 1)
            got = dict(DECISION.findall(rest))
            out[name.strip()] = {e: got.get(e) for e in EDGES}
    return out


def questions(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    found, extra = spec_lint.check({"spec": path})
    qs = [(f["rule"], f.get("where", ""), f["message"]) for f in found]
    m = re.search(r"(?m)^Type:\s*(\S+)", text)
    needs_inputs = not (m and m.group(1).lower() in NO_REQUIREMENT_TYPES)
    ins = inputs(text)
    if needs_inputs and not ins:
        qs.append(("inputs", "## Inputs", "Which inputs does this change read (header, argument, setting)?"))
    known = set(extra.get("requirements", []))
    for name, edges in ins.items():
        for edge, decision in edges.items():
            if decision is None:
                qs.append(("edge", "%s: %s" % (name, edge), "%s is %s: what should happen?" % (name, edge)))
            elif decision != "out" and decision not in known:
                qs.append(("edge", "%s: %s" % (name, edge),
                           "%s is %s: %s is not a requirement in the spec. Which one covers it?" % (name, edge, decision)))
    out = [{"id": "Q%d" % i, "rule": r, "where": w, "ask": a,
            "options": EDGE_OPTIONS if r == "edge" else OPTIONS.get(r, ["Fix the spec as asked", "Out of scope"])}
           for i, (r, w, a) in enumerate(qs, 1)]
    return out, ins


def main(argv):
    if len(argv) != 1 or not os.path.isfile(argv[0]):
        print(__doc__)
        return 2
    qs, ins = questions(argv[0])
    print(json.dumps({"questions": qs, "inputs": ins}, indent=1))
    return 1 if qs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
