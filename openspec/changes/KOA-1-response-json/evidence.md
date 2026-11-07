purpose: RED then GREEN per scenario for KOA-1 (written by /implement).

## S1 REQ-RES-001 (response.json)
RED: `node --test __tests__/response/json.test.js` -> pass 0, fail 3 (`ctx.response.json is not a function`;
the two api cases got 500 from the same error).
GREEN: after `json (value)` in `lib/response.js` -> pass 3, fail 0. `npx standard` clean.

## S2 REQ-CTX-001 (ctx.json)
RED: `node --test __tests__/context/json.test.js` -> pass 0, fail 2 (`ctx.json is not a function`).
GREEN: after `.method('json')` in the response delegate list of `lib/context.js` -> pass 2, fail 0. `npx standard` clean.

## Full suite
`npx c8 node --test` -> 445 pass, 0 fail; lines 99.9% (2126/2128), branches 99.1% (441/445).

## Out of scope noticed
- `docs/api/response.md` and `docs/api/context.md` do not list `json()` yet (docs were out of scope in the spec).
