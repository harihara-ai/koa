purpose: slice plan for KOA-4 (G1: a human merging the plan PR approves it).

Impact scan (`slicer.py scan`, kit 1.0.7, seeds per slice in `inputs/granularity.json`): `problem` is a new symbol,
so no code calls it and no test holds its values (`application/problem+json`, `Not Found: `,
`response.problem() needs`): `inputs/impact.json` lists no callers, tests or pins. The files below are the plan's
own (`inputs/diff_scope.json`). `response.js` gains `problem` next to `json`; it reads `this.request.accepts`
(already wired by `application.js`), so `request.js` does not change. `context.js` adds `.method('problem')` to the
response delegate list. All touched modules are tested (lines 99.9% at bootstrap), so no Slice 0. Contracts: none
(no OpenAPI or schema files; the new method is public API, reviewed by a human).

| Slice | Requirement | Scenarios | Files | Est. lines | Depends on |
| --- | --- | --- | --- | --- | --- |
| S1 | REQ-RES-002 | 3 | `lib/response.js`, `__tests__/response/problem.test.js` | 45 (estimate) | - |
| S2 | REQ-RES-003 | 2 | `lib/response.js`, `__tests__/response/problem.test.js` | 30 (estimate) | S1 |
| S3 | REQ-CTX-002 | 2 | `lib/context.js`, `__tests__/context/problem.test.js`, `docs/api/response.md`, `docs/api/context.md` | 40 (estimate) | S2 |

One code PR per slice, in order; each runs `slicer.py actual --slice <id> --metrics` against its merge base.
