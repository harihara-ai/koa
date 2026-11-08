purpose: RED then GREEN per scenario for KOA-7 (written by /implement).

## S1 REQ-REQ-003, REQ-REQ-005 (request.ips IPv4 port, request.ip)
RED: `node --test __tests__/request/ips.test.js __tests__/request/ip.test.js` -> pass 13, fail 2 (ips of
`'23.243.1.1:38242, 10.0.0.1'`: expected `['23.243.1.1', '10.0.0.1']`, got the port kept; ip: expected
`'23.243.1.1'`, got `'23.243.1.1:38242'`). `guard`: invalid entries unchanged (REQ-REQ-003 edge) and no header gives
the socket address (REQ-REQ-005 edge) already hold on master (the owner's edge answers pin them).
GREEN: `stripPort` in `lib/request.js` (IPv4 with a numeric port only), mapped over `ips` -> pass 15, fail 0; full
suite pass 475, fail 0; `npx standard` clean; lines 99.9%, branches 99.14%.
Root cause: `ips` split the header on `,` and trimmed, never parsing an entry's port.
