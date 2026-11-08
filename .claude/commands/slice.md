---
description: Break an approved spec into slices: impact scan, granularity score, split, slice plan for human approval.
argument-hint: <change-name>
---

purpose: Break an approved spec into slices: impact scan, granularity score, split, slice plan for human approval.

Follow `kit/core/rules.md`. Arguments: `$ARGUMENTS`.

0. Refine (DoR): run `python3 kit/scripts/refine.py <dir>/spec.md`. Ask the owner each question as one tap question with its options (the owner ticks each input edge). Write the answers into the spec (a scenario, a REQ id in `## Inputs`, or `out`) and run it again until it exits 0. Do not slice before.
1. List requirements and scenarios from `spec.md`.
2. Impact scan each requirement with capability.codenav `impact`. Write `impact.md` and `inputs/diff_scope.json`.
3. Measure each candidate slice (codenav `impact` gives symbols and files; mark guesses `"estimate": true`) and write `inputs/granularity.json` with `"requirements": ["REQ-..."]` (the REQ IDs the slice builds; trace_check reads them) and `"seeds": {"symbols": [...], "values": [...]}` per slice (values: what the change alters, e.g. a bug's wrong result; write a value as a test writes it, e.g. `'Content-Length', 'hey'`, not a common word, and check its pins against the bug spike). Run `python3 kit/scripts/slicer.py scan --change <dir>`: it writes `inputs/impact.json`, raises files and symbols, and adds callers and tests that pin the values to the scan. Never lower its numbers. A characterization slice has `"kind": "characterization"`.
4. Split any slice the gate marks split (`scan` prints `"split"` from the gate's own score: rescan until it is empty), preferring: by scenario, thin vertical slice, by contract, by data variant, by risk (spike). Never by technical layer alone.
5. Order by dependency. Add Slice 0 (characterization only) for untested code in scope.
6. Write `slices.md`, run `gate_check.py ready`, then open the plan PR. A human merging it is the approval.
