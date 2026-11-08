purpose: RED then GREEN per scenario for KOA-4 (written by /implement).

## S1 REQ-RES-002 (response.problem, problem+json)
RED: `node --test __tests__/response/problem.test.js` -> pass 0, fail 3 (`ctx.response.problem is not a function`;
the two api cases got 500 from the same error).
GREEN: after `problem (status, detail)` in `lib/response.js` -> pass 3, fail 0. `npx standard` clean.

## S2 REQ-RES-003 (text fallback)
RED: `node --test __tests__/response/problem.test.js` -> pass 4, fail 1 (Accept text/plain: expected
`text/plain; charset=utf-8`, got `application/problem+json`). The Accept image/png case passed already (S1 always
sends problem+json); it pins that fallback.
GREEN: after the `request.accepts` branch in `problem` -> pass 5, fail 0. `npx standard` clean.

## Out of scope noticed
- A 4xx/5xx code with no `statuses` message (e.g. 499) gets no `title` (JSON.stringify drops undefined). Not in the
  spec; left as is.
