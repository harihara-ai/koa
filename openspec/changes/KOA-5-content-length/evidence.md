purpose: RED then GREEN per scenario for KOA-5 (written by /implement).

## S1 REQ-REQ-001 (request.length)
RED: `node --test __tests__/request/length.test.js` -> pass 8, fail 2 (`10.5` and `10abc`: expected undefined,
got 10). The happy case passed already (digits were read right). The old test "should handle floating-point-like
strings (truncate decimal)" pinned the bug (spike, spec "Edited test"); it became the `10.5` error case.
GREEN: `lib/content-length.js` (digits only, after trim) used by `request.length` -> pass 10, fail 0; full suite
pass 461, fail 0; `npx standard` clean. Branches 99.12% (a null guard in the parser was dead code: removed).
Root cause: `Number.parseInt` stops at the first non-digit, so any prefix of digits was accepted.

## S2 REQ-RES-004 (response.length)
RED: `node --test __tests__/response/length.test.js` -> pass 7, fail 2 (`hey`: expected undefined, got 0; `10abc`:
expected undefined, got 10). The happy case passed already. The old test "but not number / should return 0" pinned
the bug (spike, spec "Edited test"); it became the `hey` error case.
GREEN: `response.length` uses `parseContentLength` when the header is set -> pass 9, fail 0; full suite pass 462,
fail 0; `npx standard` clean; branches 99.12%, response.js 100%. The two false pins of the `'hey'` seed
(`request/fresh.test.js`, `response/body.test.js`) pass unchanged.
Root cause: `parseInt(...) || 0` turned NaN into 0 and accepted any digit prefix.
