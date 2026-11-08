purpose: RED then GREEN per scenario for KOA-6 (written by /implement).

## S1 REQ-REQ-002 (request.subdomains)
RED: `node --test __tests__/request/subdomains.test.js` -> pass 3, fail 3 (`api.example.com.`: expected `['api']`,
got `['example', 'api']`; `example.com.`: expected `[]`, got `['example']`; `API.example.com.`: expected `['API']`,
got `['example', 'API']`).
GREEN: `lib/host.js` `stripRootDot`, used by `request.subdomains` -> pass 6, fail 0; full suite pass 465, fail 0;
`npx standard` clean; host.js 100%, branches 99.13% (request.js 101, 113: untouched lines, as before).
Root cause: the getter split the raw host name on `.`, so the root dot made an empty last label and shifted the offset.

## S2 REQ-RES-005 (response.back, case and root dot)
RED: `node --test __tests__/response/back.test.js` -> pass 9, fail 2 (Host `EXAMPLE.COM` and `example.com.` with a
same-host Referer: expected the Referer, got `/fallback`). `guard`: another host with an upper case Host already
gives `/fallback`.
GREEN: `lib/host.js` `canonicalHost` (WHATWG URL with `http:`: lower case, no default port, then `stripRootDot`),
used on both sides of the `back` comparison -> pass 11, fail 0; full suite pass 468, fail 0; `npx standard` clean.
Root cause: `back` compared the Referer's parsed host with the raw Host text.
Between S2 and S3 (probe, scratchpad): Host `example.com:80` with an `https:` Referer redirects to the Referer
(same host name; not another host). S3's error scenario turns this back to `/fallback`.
Refactor (before merge, found while building S3): the `try/catch` around `new URL` in `canonicalHost` was dead. A
Host the URL parser refuses (`exa mple.com`, `example.com:99999`) already throws `ERR_INVALID_URL` in `back` at
`new URL(referrer, ctx.href)`, on master too, before the helper runs. Removed; full suite pass 468; host.js lines 100%.
The spec assumption "a Host the URL parser refuses never matches" is wrong: it throws, as before this change
(out of scope; noted, not changed). The non-default port branch is covered by S3's tests.
