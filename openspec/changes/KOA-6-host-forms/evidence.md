purpose: RED then GREEN per scenario for KOA-6 (written by /implement).

## S1 REQ-REQ-002 (request.subdomains)
RED: `node --test __tests__/request/subdomains.test.js` -> pass 3, fail 3 (`api.example.com.`: expected `['api']`,
got `['example', 'api']`; `example.com.`: expected `[]`, got `['example']`; `API.example.com.`: expected `['API']`,
got `['example', 'API']`).
GREEN: `lib/host.js` `stripRootDot`, used by `request.subdomains` -> pass 6, fail 0; full suite pass 465, fail 0;
`npx standard` clean; host.js 100%, branches 99.13% (request.js 101, 113: untouched lines, as before).
Root cause: the getter split the raw host name on `.`, so the root dot made an empty last label and shifted the offset.
