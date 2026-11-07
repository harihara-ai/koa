# KOA-2: HEAD sends Content-Length 2 for a ReadableStream or Response body

Type: bug

## Why
Found in the pilot (bug hunt, 2026-11-07). With `ctx.body = new ReadableStream(...)` sending 11 bytes, `GET /`
streams 11 bytes chunked, but `HEAD /` answers `Content-Length: 2`. A client or cache that trusts HEAD gets a
wrong size. Cause: `response.length` falls through to `JSON.stringify(body)`, which is `"{}"` for these objects.

## What done looks like
- `ctx.length` is `undefined` for a ReadableStream body and for a Response body without a Content-Length header.
- `HEAD /` with a ReadableStream body sends no Content-Length header.

## Not included
- Reading the size of a ReadableStream (it is unknown until read).
