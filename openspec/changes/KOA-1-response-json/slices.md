purpose: slice plan for KOA-1 (G1: a human merging the plan PR approves it).

Impact scan (ctags): `response.js` gains `json` next to `body`; `context.js` adds `.method('json')` to the
response delegate list. Both modules are tested (lines 99.9% at bootstrap), so no Slice 0. Contracts: none (Koa
has no OpenAPI or schema files; the new method is public API, reviewed by a human).
First gate run scored one slice amber (5 scenarios, 2 modules): split by requirement.

| Slice | Requirement | Scenarios | Files | Est. lines | Depends on |
| --- | --- | --- | --- | --- | --- |
| S1 | REQ-RES-001 | 3 | `lib/response.js`, `__tests__/response/json.test.js` | 35 (estimate) | - |
| S2 | REQ-CTX-001 | 2 | `lib/context.js`, `__tests__/context/json.test.js` | 20 (estimate) | S1 |
