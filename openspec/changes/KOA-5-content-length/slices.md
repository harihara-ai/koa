purpose: slice plan for KOA-5 (G1: a human merging the plan PR approves it).

Impact scan (`slicer.py scan`, kit 1.0.9, seeds per slice in `inputs/granularity.json`): `parseContentLength` is new,
so no code or test uses it. Value seeds found the two pinning tests the spike found:
`__tests__/request/length.test.js:39` (S1) and `__tests__/response/length.test.js:19` (S2). The S2 seed `'hey'` also
matched `__tests__/request/fresh.test.js:45` and `__tests__/response/body.test.js:266`: they use `hey` as a body, not
as a Content-Length, and pass with the spike fix (false pins; they stay in `diff_scope.json`, S2 files raised 2 -> 3,
never lowered). `application.js` reads `response.length` only when no Content-Length is set: not touched. Both
modules are tested (lines 99.9% at bootstrap), so no Slice 0. Contracts: none.

| Slice | Requirement | Scenarios | Files | Est. lines | Depends on |
| --- | --- | --- | --- | --- | --- |
| S1 | REQ-REQ-001 | 3 | `lib/content-length.js` (new), `lib/request.js`, `__tests__/request/length.test.js` | 35 (estimate) | - |
| S2 | REQ-RES-004 | 3 | `lib/response.js`, `__tests__/response/length.test.js` | 25 (estimate) | S1 |

Granularity: S1 amber (2 modules: the new parser and `request.js`), S2 green; `gate_check.py auto` -> ready, pass.

One code PR per slice, in order; each runs `slicer.py actual --slice <id> --metrics` against its merge base.
