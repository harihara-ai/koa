# Change: KOA-2-stream-length
Ticket: KOA-2
Type: bug

## Problem
With `ctx.body = new ReadableStream(...)` that yields 11 bytes, `GET /` sends 11 bytes chunked, but `HEAD /` sends
`Content-Length: 2`, because `response.length` returns `Buffer.byteLength(JSON.stringify(body))` and a
ReadableStream or Response encodes as `{}`.

## Outcome
`response.length` is `undefined` for a ReadableStream body and for a Response body that sets no Content-Length, so
`HEAD` sends no Content-Length for them. Other bodies keep today's lengths.

## Requirements

### REQ-RES-002: no length for web stream bodies
Errors: none
Scenario: happy - ReadableStream body has no length
  Given a context whose body is a ReadableStream yielding "hello world"
  When ctx.length is read
  Then it is undefined
  Level: unit
Scenario: happy - Response body has no length
  Given a context whose body is new Response("hello world") with no Content-Length header
  When ctx.length is read
  Then it is undefined
  Level: unit
Scenario: happy - HEAD sends no Content-Length
  Given an app whose handler sets ctx.body to a ReadableStream yielding "hello world"
  When HEAD / is requested
  Then the status is 200 and the response has no Content-Length header
  Level: api

## Non-functional
none

## Out of scope
Measuring a stream's size; Blob, Buffer, string and JSON bodies (already right: Blob 5 bytes for "hello").

## Assumptions
A Response body that carries its own Content-Length keeps it (the body setter copies the Response headers).

## Edited test
`__tests__/application/respond.test.js` "should keep Response headers" asserts HEAD on `new Response(null, ...)`
sends `content-length: 2`: it pins this bug. Owner decision (2026-11-07): that assertion becomes "no
Content-Length header"; status 201 and the content-type stay. A human reviews the edit (kit rule 10).

## Open questions
none
