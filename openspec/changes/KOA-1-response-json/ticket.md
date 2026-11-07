# KOA-1: ctx.json() and response.json()

Type: story

## Why
A handler that wants a JSON body has to know Koa's rules: an object body becomes JSON, but a string body is sent
as text/plain, so `ctx.body = 'ok'` is not JSON. Pilot owner asked for one call that always sends JSON.

## What done looks like
- `ctx.json({ a: 1 })` sends `{"a":1}` with `Content-Type: application/json; charset=utf-8`.
- `ctx.json('ok')` sends `"ok"` (JSON-encoded), still `application/json`.

## Not included
- Pretty printing, JSONP, streaming JSON.
