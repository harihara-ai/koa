# KOA-6: same host, different spelling: ctx.subdomains and ctx.back disagree

Type: bug

## Why
Upstream koajs/koa open issues (2026-11-01), real backlog, read for scale step S2 item 3:
- #2026: a trailing root dot in Host adds a subdomain. `api.example.com.` gives `['example', 'api']`, not `['api']`;
  `example.com.` gives `['example']`, not `[]`.
- #2027: `ctx.back('/fallback')` rejects a same-host Referer `http://example.com/return` when Host is `EXAMPLE.COM`
  or `example.com:80`, and redirects to `/fallback`.

## What done looks like
- One helper `lib/host.js` that writes a host one way (no root dot; for comparison also lower case and no default
  port), used by `request.subdomains` and `response.back`.
- `subdomains` ignores a trailing root dot and keeps the letter case (owner, 2026-11-08).
- `back` treats a Referer as same host when only case, a default port or a root dot differ.

## Not included
Lowercasing `subdomains`, `ctx.host` or `ctx.hostname`; `X-Forwarded-Host` handling; scheme checks in `back`.
