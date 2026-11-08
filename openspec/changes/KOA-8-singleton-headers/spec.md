# Change: KOA-8-singleton-headers
Ticket: KOA-8
Type: bug

## Problem
`ctx.set('Content-Type', ['a','b'])` throws AssertionError "Assign multiple Content-Type for response header is not allowed" (from upstream #1899), but only in the string form and only for Content-Type. `ctx.set({ 'Content-Type': ['a','b'] })` does not throw and the header becomes `['a','b']`. `ctx.set('Content-Length', ['1','2'])`, `ctx.set('Location', ['/a','/b'])` and `ctx.set('ETag', ['"a"','"b"'])` do not throw; the header holds the array. `ctx.append('Location','/a')` then `ctx.append('Location','/b')` gives `['/a','/b']` (upstream #1973).

## Outcome
For the five headers koa's own setters write (Content-Type, Content-Length, Location, ETag, Last-Modified),
`ctx.set` with any array value (two values, one value or `[]`), in the string form or the object form and with the
name in any case, throws an AssertionError "Assign multiple <Header> for response header is not allowed" and the
header keeps its earlier value, as Content-Type does today. `ctx.append` of a second value to one of them throws
the same way. Strings and numbers are set as today; list headers such as Link still take arrays.

## Requirements

### REQ-RES-001: response.set refuses an array for a singleton header
Errors: AssertionError when the value of a singleton header is an array
Scenario: happy - a single string value is set
  Given a response with no Location header
  When ctx.set('Location', '/a') is called
  Then ctx.response.get('Location') is '/a'
  Level: unit
Scenario: error - an array of two values throws
  Given a response with Location '/old'
  When ctx.set('Location', ['/a', '/b']) is called
  Then it throws an AssertionError and ctx.response.get('Location') is '/old'
  Level: unit
Scenario: edge - a short array throws
  Given a response with no ETag or Content-Length header
  When ctx.set('ETag', []) is called, then ctx.set('Content-Length', ['5'])
  Then each throws an AssertionError and both headers are undefined
  Level: unit
Scenario: edge - a header name in another case throws
  Given a response with no Last-Modified header
  When ctx.set('LAST-MODIFIED', ['a', 'b']) is called
  Then it throws an AssertionError
  Level: unit
Scenario: edge - other values are set as today
  Given a response with no Content-Length, ETag or Link header
  When ctx.set('Content-Length', 5), ctx.set('ETag', '') and ctx.set('Link', ['<a>', '<b>']) are called
  Then the headers are 5, '' and ['<a>', '<b>']
  Level: unit

### REQ-RES-002: response.set with an object refuses an array for a singleton header
Errors: AssertionError when a value for a singleton header in the object is an array
Scenario: happy - a single string value is set
  Given a response with no Content-Type header
  When ctx.set({ 'Content-Type': 'text/plain' }) is called
  Then ctx.response.get('Content-Type') is 'text/plain'
  Level: unit
Scenario: error - an array of two values throws
  Given a response with no ETag header
  When ctx.set({ ETag: ['"a"', '"b"'] }) is called
  Then it throws an AssertionError and ctx.response.get('ETag') is undefined
  Level: unit

### REQ-RES-003: response.append refuses a second value for a singleton header
Errors: AssertionError when a singleton header already has a value
Scenario: happy - the first append sets the value
  Given a response with no Location header
  When ctx.append('Location', '/a') is called
  Then ctx.response.get('Location') is '/a'
  Level: unit
Scenario: error - a second append throws
  Given a response with Location '/a'
  When ctx.append('Location', '/b') is called
  Then it throws an AssertionError and ctx.response.get('Location') is '/a'
  Level: unit

## Inputs
- value of a singleton header: absent out; empty REQ-RES-001; boundary REQ-RES-001; invalid REQ-RES-001

## Non-functional
none

## Out of scope
Request headers; header value syntax; Set-Cookie and other list headers; headers beyond the five (owner
2026-11-08); `undefined` removes the header as today (owner: unchanged).

## Assumptions
none

## Open questions
none
