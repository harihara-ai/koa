purpose: RED then GREEN per scenario for KOA-7 (written by /implement).

## S1 REQ-REQ-003, REQ-REQ-005 (request.ips IPv4 port, request.ip)
RED: `node --test __tests__/request/ips.test.js __tests__/request/ip.test.js` -> pass 13, fail 2 (ips of
`'23.243.1.1:38242, 10.0.0.1'`: expected `['23.243.1.1', '10.0.0.1']`, got the port kept; ip: expected
`'23.243.1.1'`, got `'23.243.1.1:38242'`). `guard`: invalid entries unchanged (REQ-REQ-003 edge) and no header gives
the socket address (REQ-REQ-005 edge) already hold on master (the owner's edge answers pin them).
GREEN: `stripPort` in `lib/request.js` (IPv4 with a numeric port only), mapped over `ips` -> pass 15, fail 0; full
suite pass 475, fail 0; `npx standard` clean; lines 99.9%, branches 99.14%.
Root cause: `ips` split the header on `,` and trimmed, never parsing an entry's port.

## S2 REQ-REQ-004 (request.ips IPv6 in brackets)
RED: `node --test __tests__/request/ips.test.js` -> pass 9, fail 2 (`[2001:db8::1]:8080` and `[2001:db8::1]`:
expected `['2001:db8::1']`, got the entry unchanged). `guard`: bare IPv6 entries (`2001:db8::1`, `::ffff:1.2.3.4`)
unchanged already (S1's IPv4 pattern needs exactly 4 dotted parts and a port).
GREEN: `stripPort` also takes `[<v6>]` with an optional numeric port -> pass 18 (ips and ip), fail 0; full suite
pass 478, fail 0; `npx standard` clean; lines 99.9%, branches 99.14%.
S05 check (untested branch found after the plan): none. lcov branches with 0 hits in `lib/request.js`: lines 101 and
113 only (untouched, as before KOA-7); every `stripPort` path (IPv4, bracketed with and without a port, no match)
has a test from the spec's edge list.
