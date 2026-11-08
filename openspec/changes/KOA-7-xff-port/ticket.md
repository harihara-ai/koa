# KOA-7: request.ip and request.ips keep the port from X-Forwarded-For

Type: bug

## Why
Upstream koajs/koa open issue #827 (read 2026-11-08), real backlog, scale step S2 item 4:
some proxies (Azure) send the client port in X-Forwarded-For, e.g. `'x-forwarded-for': '23.243.1.1:38242'`;
`request.ip` returns `23.243.1.1:38242`, not `23.243.1.1`.

## What done looks like
- With `app.proxy` true, `request.ips` and `request.ip` give addresses without a port.

## Not included
`Forwarded` (RFC 7239) header parsing; trusted-proxy lists (upstream #281).
