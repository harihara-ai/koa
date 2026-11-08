purpose: slice plan for KOA-7 (G1: a human merging the plan PR approves it).

DoR before slicing (DIRECTION 10 row 6): `refine.py` (kit 1.0.15, pinned) on the draft spec asked 6 questions
(2 spec_lint `error_case`, 4 input edges of the X-Forwarded-For entry); the owner answered all by tap (plus one
follow-up on brackets without a port). Second run: exit 0, no questions.

Impact scan (`slicer.py scan`, kit 1.0.14, seeds per slice in `inputs/granularity.json`): `stripPort` is new.
Code: `lib/request.js` (`ips`, `ip`), and `lib/context.js` (it delegates `ip` and `ips`; no change). Tests:
`__tests__/request/ips.test.js`, `__tests__/request/ip.test.js`; the scan also lists
`__tests__/request/subdomains.test.js` (same module, no change expected). Files raised S1 3 -> 5, S2 2 -> 4, never
lowered. No pins. `lib/request.js` is tested, so no Slice 0. Contracts: none.

| Slice | Requirement | Scenarios | Files | Est. lines | Depends on |
| --- | --- | --- | --- | --- | --- |
| S1 | REQ-REQ-003, REQ-REQ-005 | 4 | `lib/request.js`, `__tests__/request/ips.test.js`, `__tests__/request/ip.test.js` | 35 (estimate) | - |
| S2 | REQ-REQ-004 | 3 | `lib/request.js`, `__tests__/request/ips.test.js` | 25 (estimate) | S1 |

REQ-REQ-005 (`ip`) is built in S1: `ip` reads `ips[0]`, so after S1 its test would already pass and could not be red
in a later slice.

First local `ready` run (13:06 UTC): fail, granularity split S1 (4 scenarios and 'and' in the title: two ambers;
finding T3-02). The two requirements in S1 are not hidden: the paragraph above says why they go together. Corrective:
titles without 'and'; second run pass (S1 amber: 4 scenarios; S2 green).

One code PR per slice, in order, each with `slice_pr.py start` and `finish` (body generated, used as is).
