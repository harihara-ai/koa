purpose: RED then GREEN for KOA-2 (written by /implement).

## S1 REQ-RES-002
RED: `node --test __tests__/response/length.test.js` -> pass 5, fail 3; actual `2`, `2`, `'2'` (the three new tests).
Root cause: `get length ()` in `lib/response.js` falls through to `Buffer.byteLength(JSON.stringify(body))`;
a ReadableStream or Response encodes as `{}`, so length 2, and `respond()` copies it to Content-Length on HEAD.
Fix: return `undefined` for ReadableStream and Response bodies, as for Node streams.
GREEN: length.test.js pass 8, fail 0. Full suite then: 447 pass, 1 fail, `respond.test.js` "should keep Response
headers" expected `content-length: 2` (it pinned the bug). Owner widened the plan to that assertion; it now checks
that no Content-Length is sent (status 201 and content-type unchanged).
Full suite: `npx c8 node --test` -> 448 pass, 0 fail; lines 99.9% (2126/2128), branches 99.1% (443/447). `npx standard` clean.

## Out of scope noticed
- `Uint8Array` bodies are sent as JSON (`{"0":1,...}`, length 19); not a Buffer. Possible separate ticket.
