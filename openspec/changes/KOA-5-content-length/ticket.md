# KOA-5: request.length and response.length accept a malformed Content-Length

Type: bug

## Why
Found reading the code for scale step S2 (2026-11-08). RFC 9110 8.6: Content-Length is `1*DIGIT`. Koa parses it
with `parseInt`, so it accepts junk, and the two sides disagree:
- `request.length` is `10` for `Content-Length: 10.5` and for `10abc`.
- `response.length` is `10` for `10abc` and `0` for `hey` (request gives `undefined` for `hey`).
A body parser that trusts `ctx.request.length` reads the wrong size; `0` hides a bad header as an empty body.

## What done looks like
- Both getters return the number for a valid Content-Length (digits only) and `undefined` for anything else.
- One parser in `lib/content-length.js`, used by both.

## Not included
Rejecting the request (a 400) or changing what `response.length=` writes.
