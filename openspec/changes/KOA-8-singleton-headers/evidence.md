purpose: RED then GREEN per scenario for KOA-8 (written by /implement).

## S1 REQ-RES-003 (response.append on a singleton header)
RED: `node --test __tests__/response/append.test.js` -> pass 5, fail 1 (second `append('Location', '/b')`: expected
an AssertionError, got `['/a', '/b']`). `guard`: the first append sets `'/a'` already on master.
GREEN: `SINGLETON_HEADERS` (Content-Type, Content-Length, Location, ETag, Last-Modified, by lower-case name) in
`lib/response.js`; `append` asserts when the header is in the list and already has a value -> pass 6, fail 0;
full suite pass 480, fail 0; `npx standard` clean; lines 99.9%, branches 99.14%.
Root cause: `append` always concatenated; only `set` checked Content-Type, and only for an array value.
