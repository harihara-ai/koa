# KOA-8: response.set and append accept several values for headers that allow one

Type: bug

## Why
Upstream koajs/koa open issue #1973 (read 2026-11-08), real backlog, scale step S2 item 5:
"follow-up to https://github.com/koajs/koa/pull/1899 — if an HTTP header is a singleton, we should have stricter validations and disallow setting multiple fields."

## What done looks like
- Setting or appending a second value for a singleton header throws, as Content-Type already does for `ctx.set('Content-Type', [...])`.

## Not included
Request headers; validating header value syntax.
