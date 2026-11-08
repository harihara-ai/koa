purpose: RED then GREEN per scenario for KOA-5 (written by /implement).

## S1 REQ-REQ-001 (request.length)
RED: `node --test __tests__/request/length.test.js` -> pass 8, fail 2 (`10.5` and `10abc`: expected undefined,
got 10). The happy case passed already (digits were read right). The old test "should handle floating-point-like
strings (truncate decimal)" pinned the bug (spike, spec "Edited test"); it became the `10.5` error case.
GREEN: `lib/content-length.js` (digits only, after trim) used by `request.length` -> pass 10, fail 0; full suite
pass 461, fail 0; `npx standard` clean. Branches 99.12% (a null guard in the parser was dead code: removed).
Root cause: `Number.parseInt` stops at the first non-digit, so any prefix of digits was accepted.
