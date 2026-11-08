---
description: Break an approved spec into slices: impact scan, granularity score, split, slice plan for human approval.
argument-hint: <change-name>
---

purpose: Break an approved spec into slices: impact scan, granularity score, split, slice plan for human approval.

Follow `kit/core/rules.md`. Arguments: `$ARGUMENTS`.

1. List requirements and scenarios from `spec.md`.
2. Impact scan each requirement with capability.codenav `impact`. Write `impact.md` and `inputs/diff_scope.json`.
3. Measure each candidate slice (codenav `impact` gives symbols and files; mark guesses `"estimate": true`) and write `inputs/granularity.json` with `"seeds": {"symbols": [...], "values": [...]}` per slice (values: what the change alters, e.g. a bug's wrong result). Run `python3 kit/scripts/slicer.py scan --change <dir>`: it writes `inputs/impact.json`, raises files and symbols, and adds callers and tests that pin the values to the scan. Never lower its numbers. A characterization slice has `"kind": "characterization"`.
4. Split any slice the gate marks split, preferring: by scenario, thin vertical slice, by contract, by data variant, by risk (spike). Never by technical layer alone.
5. Order by dependency. Add Slice 0 (characterization only) for untested code in scope.
6. Write `slices.md`, run `gate_check.py ready`, then open the plan PR. A human merging it is the approval.
