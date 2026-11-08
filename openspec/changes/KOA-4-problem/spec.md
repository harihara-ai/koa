# Change: KOA-4-problem
Ticket: KOA-4
Type: story

## Problem
A handler that rejects a request has no standard error reply: `ctx.status = 404; ctx.body = { error: 'No user 7' }`
sends an ad hoc JSON shape with `application/json; charset=utf-8`, so each API invents its own error format.

## Outcome
`response.problem(status, detail)` and `ctx.problem(status, detail)` send an RFC 9457 problem reply: the status,
`Content-Type: application/problem+json` and body `{"type":"about:blank","title":<status message>,"status":<n>}`
plus `"detail"` when given. A client whose Accept header allows `text/plain` but no JSON type gets text instead.

## Requirements

### REQ-RES-002: response.problem sends a problem+json body
Scenario: happy - status and detail
  Given an app whose handler calls ctx.response.problem(404, 'No user 7')
  When GET / is requested with no Accept header
  Then the status is 404, Content-Type is "application/problem+json" and the body text is {"type":"about:blank","title":"Not Found","status":404,"detail":"No user 7"}
  Level: api
Scenario: happy - status only
  Given an app whose handler calls ctx.response.problem(503)
  When GET / is requested with no Accept header
  Then the status is 503 and the body text is {"type":"about:blank","title":"Service Unavailable","status":503}
  Level: api
Scenario: error - status that is not 4xx or 5xx
  Given a response object with body "before"
  When response.problem(302) is called
  Then a TypeError is thrown with the message "response.problem() needs a 4xx or 5xx status" and the body is still "before"
  Level: unit

### REQ-RES-003: response.problem falls back to text for text-only clients
Scenario: happy - client accepts only text/plain
  Given an app whose handler calls ctx.response.problem(404, 'No user 7')
  When GET / is requested with Accept "text/plain"
  Then the status is 404, Content-Type is "text/plain; charset=utf-8" and the body text is "Not Found: No user 7"
  Level: api
Scenario: error - client accepts none of the offered types
  Given an app whose handler calls ctx.response.problem(404)
  When GET / is requested with Accept "image/png"
  Then the status is 404 and Content-Type is "application/problem+json" (the problem body is still sent)
  Level: api

### REQ-CTX-002: ctx.problem delegates to response.problem
Scenario: happy - ctx.problem sends a problem reply
  Given an app whose handler calls ctx.problem(400, 'Bad id')
  When GET / is requested with no Accept header
  Then the status is 400, Content-Type is "application/problem+json" and the body text is {"type":"about:blank","title":"Bad Request","status":400,"detail":"Bad id"}
  Level: api
Scenario: error - ctx.problem(200) throws
  Given a context object
  When ctx.problem(200) is called
  Then a TypeError is thrown with the message "response.problem() needs a 4xx or 5xx status"
  Level: unit

## Non-functional
none

## Out of scope
Custom `type` URIs, extension members, changes to `ctx.onerror` or `ctx.throw`, an HTML fallback.

## Assumptions
`application/problem+json` gets no charset parameter (mime-types gives none; RFC 8259 JSON is UTF-8).
Content negotiation uses `request.accepts` with the offer order problem+json, json, text/plain; no Accept header
picks the first. Docs pages `docs/api/response.md` and `docs/api/context.md` gain one entry each (slice S3).

## Open questions
none
