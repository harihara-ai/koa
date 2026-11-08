---
description: Implement one approved slice with red-green-refactor, evidence, and a 3-attempt cap.
argument-hint: <change-name> [slice]
---

purpose: Implement one approved slice with red-green-refactor, evidence, and a 3-attempt cap.

Follow `kit/core/rules.md`. Arguments: `$ARGUMENTS`.

0. Check: the plan PR is merged. Branch from the target: `python3 kit/scripts/slice_pr.py start --change <dir> --slice <id> --target <branch>`. `gate_check.py done` fails while the plan is not merged, and if you edit the plan.
1. For each task (one scenario): write the test with the REQ ID in its name. Run it. RED for the right reason. Append command and short output to `evidence.md`. A scenario that guards behaviour that already holds (often a bug's error case) passes at once: mark it `guard` there; the slice still needs one RED test.
2. Minimum code to pass. Run it. GREEN. Append to `evidence.md`.
3. Refactor only what you just wrote, tests green. Commit `REQ-<AREA>-<NNN>: <what>`.
4. Run `python3 kit/scripts/slice_pr.py finish --change <dir> --slice <id> --target <branch> -- <gate flags>`: it stops on files outside the plan, runs `slicer.py actual --metrics`, updates `status.md`, runs the local gate, commits only in-scope paths and prints the PR title and body. Say any miss in `evidence.md`. Use that body as is; never hand-write it.
5. After 3 failed attempts on a task: stop and report with evidence. Out-of-scope ideas go under "Out of scope noticed" in `evidence.md`.
Never edit a test to make it pass. Never touch files outside the merged `inputs/diff_scope.json`.
