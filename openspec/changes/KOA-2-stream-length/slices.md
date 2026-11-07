purpose: slice plan for KOA-2 (G1: a human merging the plan PR approves it).

Impact scan (ctags): `get length ()` in `lib/response.js`; the HEAD branch of `respond()` in
`lib/application.js` reads it and needs no change. `length.test.js` covers the getter today (no Slice 0).
First code run: `respond.test.js` "should keep Response headers" expects the buggy length 2 (ctags found no
test asserting it); owner widened the scope to that one assertion.

| Slice | Requirement | Scenarios | Files | Est. lines | Depends on |
| --- | --- | --- | --- | --- | --- |
| S1 | REQ-RES-002 | 3 | `lib/response.js`, `__tests__/response/length.test.js`, `__tests__/application/respond.test.js` | 32 (estimate) | - |
