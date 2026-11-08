purpose: RED then GREEN per scenario for KOA-8 (written by /implement).

## S1 REQ-RES-003 (response.append on a singleton header)
RED: `node --test __tests__/response/append.test.js` -> pass 5, fail 1 (second `append('Location', '/b')`: expected
an AssertionError, got `['/a', '/b']`). `guard`: the first append sets `'/a'` already on master.
GREEN: `SINGLETON_HEADERS` (Content-Type, Content-Length, Location, ETag, Last-Modified, by lower-case name) in
`lib/response.js`; `append` asserts when the header is in the list and already has a value -> pass 6, fail 0;
full suite pass 480, fail 0; `npx standard` clean; lines 99.9%, branches 99.14%.
Root cause: `append` always concatenated; only `set` checked Content-Type, and only for an array value.

## S2 REQ-RES-001 (response.set, string form)
RED: `node --test __tests__/response/set.test.js` -> pass 7, fail 3 (`['/a', '/b']` on Location kept, `[]` on ETag
and `['5']` on Content-Length set, `LAST-MODIFIED` with an array set). `guard`: a string is set; a number, `''` and
a Link array are set as today (the owner's edge answers pin them).
GREEN: the string form of `set` asserts for any array on a `SINGLETON_HEADERS` name (any case), replacing the
Content-Type-only check -> pass 10, fail 0; full suite pass 485, fail 0; `npx standard` clean; lines 99.9%,
branches 99.14%. Pin `__tests__/application/response.test.js:105` (Content-Type array throws) still green.
Root cause: #1899 checked only `content-type` in `set`.
