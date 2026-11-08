purpose: slice plan for KOA-6 (G1: a human merging the plan PR approves it).

Impact scan (`slicer.py scan`, kit 1.0.13, seeds per slice in `inputs/granularity.json`): `stripRootDot` and
`canonicalHost` are new. Code: `lib/request.js` (S1), `lib/response.js` (S2, S3), and `lib/context.js` for all (it
delegates `subdomains` and `back`; no change). Tests: `__tests__/request/subdomains.test.js`,
`__tests__/response/back.test.js`. Pins: S3's seed `'example.com:8080'` matched
`__tests__/request/host.test.js:114` (a userinfo test of `request.host`, which this change does not touch; it passed
with the spike fix): a false pin, kept in `diff_scope.json`, S3 files raised 3 -> 4, never lowered. Both modules
are tested (lines 99.9% at bootstrap), so no Slice 0. Contracts: none.

| Slice | Requirement | Scenarios | Files | Est. lines | Depends on |
| --- | --- | --- | --- | --- | --- |
| S1 | REQ-REQ-002 | 3 | `lib/host.js` (new), `lib/request.js`, `__tests__/request/subdomains.test.js` | 30 (estimate) | - |
| S2 | REQ-RES-005 | 3 | `lib/host.js`, `lib/response.js`, `__tests__/response/back.test.js` | 30 (estimate) | S1 |
| S3 | REQ-RES-006 | 3 | `lib/host.js`, `lib/response.js`, `__tests__/response/back.test.js` | 25 (estimate) | S2 |

First `ready` run: granularity split (S1 4 scenarios, S2 5, each over 2 modules); re-sliced by scenario into
3 slices (S2 case and root dot, S3 default port). 5 files.

One code PR per slice, in order, each with `slice_pr.py start` and `finish` (body generated, used as is).
