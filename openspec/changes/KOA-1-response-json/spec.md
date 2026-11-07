# Change: KOA-1-response-json
Ticket: KOA-1
Type: story

## Problem
`ctx.body = 'ok'` is sent as `text/plain; charset=utf-8` with body `ok`, so a handler cannot send a JSON string
without setting the type and encoding it by hand.

## Outcome
`response.json(value)` and `ctx.json(value)` set the body to `JSON.stringify(value)` and the type to
`application/json; charset=utf-8`, for objects, arrays, strings, numbers, booleans and null.

## Requirements

### REQ-RES-001: response.json sends the value as JSON
Scenario: happy - object value
  Given an app whose handler calls ctx.response.json({ a: 1 })
  When GET / is requested
  Then the status is 200, Content-Type is "application/json; charset=utf-8" and the body text is {"a":1}
  Level: api
Scenario: happy - string value is JSON-encoded
  Given an app whose handler calls ctx.response.json('ok')
  When GET / is requested
  Then Content-Type is "application/json; charset=utf-8" and the body text is "ok" with the quotes
  Level: api
Scenario: error - undefined value rejected
  Given a response object
  When response.json(undefined) is called
  Then a TypeError is thrown with the message "response.json() needs a JSON value" and the body is unchanged
  Level: unit

### REQ-CTX-001: ctx.json delegates to response.json
Scenario: happy - ctx.json sends JSON
  Given an app whose handler calls ctx.json([1, 2])
  When GET / is requested
  Then Content-Type is "application/json; charset=utf-8" and the body text is [1,2]
  Level: api
Scenario: error - ctx.json(undefined) throws
  Given a context object
  When ctx.json(undefined) is called
  Then a TypeError is thrown with the message "response.json() needs a JSON value"
  Level: unit

## Non-functional
none

## Out of scope
Pretty printing, JSONP, streaming JSON, a configurable JSON replacer, docs pages under `docs/api/`.

## Assumptions
Values that `JSON.stringify` cannot encode (BigInt, cycles) throw its own TypeError unchanged.

## Open questions
none
