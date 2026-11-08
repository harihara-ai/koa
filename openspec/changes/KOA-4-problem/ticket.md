# KOA-4: ctx.problem() sends an RFC 9457 problem reply

Type: story

## Why
Handlers that fail build their own error JSON (`ctx.status = 404; ctx.body = { error: ... }`), each in its own
shape. RFC 9457 (problem details) is the standard shape for HTTP API errors. Pilot owner chose this for scale step S2.

## What done looks like
- `ctx.problem(404, 'No user 7')` sends status 404, `Content-Type: application/problem+json`, body
  `{"type":"about:blank","title":"Not Found","status":404,"detail":"No user 7"}`.
- A client that accepts only `text/plain` gets `Not Found: No user 7` as text.

## Not included
Custom `type` URIs, extension members, changing Koa's default error handler (`ctx.onerror`).
