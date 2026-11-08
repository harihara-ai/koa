purpose: slice plan for KOA-8 (G1: a human merging the plan PR approves it).

DoR before slicing (DIRECTION 10 row 6): `refine.py` (kit 1.0.16) on the draft spec asked 8 questions (4 open
questions, 4 input edges of a singleton header value); the owner answered all by tap. Second run: exit 0.

Impact scan (`slicer.py scan`, kit 1.0.16, seeds per slice in `inputs/granularity.json`): `SINGLETON_HEADERS` is
new. Code: `lib/response.js` (`append`, `set`). Tests: `__tests__/response/append.test.js`,
`__tests__/response/set.test.js`; pin `__tests__/application/response.test.js:105` (Content-Type array throws:
kept, must stay green). The scan also lists `lib/context.js` (delegates `append`, `set`; no change),
`lib/search-params.js` and `__tests__/response/vary.test.js` (same word `append`; no change). First scan with the
symbol seed `set` gave 35 files and split S2, S3 (finding S13, broad seed); seeds narrowed to the new list and the
existing Content-Type message. `lib/response.js` is tested, so no Slice 0. Contracts: none.

| Slice | Requirement | Scenarios | Files | Est. lines | Depends on |
| --- | --- | --- | --- | --- | --- |
| S1 | REQ-RES-003 | 2 | `lib/response.js`, `__tests__/response/append.test.js` | 30 (estimate) | - |
| S2 | REQ-RES-001 | 5 | `lib/response.js`, `__tests__/response/set.test.js` | 50 (estimate) | S1 |
| S3 | REQ-RES-002 | 2 | `lib/response.js`, `__tests__/response/set.test.js` | 20 (estimate) | S2 |

Order: `append` builds an array and calls `set`, so once `set` refuses arrays the append error test could not be
red; S1 (append) goes first and adds the singleton list. S2 extends the string form of `set` from Content-Type to
the list; S3 the object form.

One code PR per slice, in order, each with `slice_pr.py start` and `finish` (body generated, used as is).
