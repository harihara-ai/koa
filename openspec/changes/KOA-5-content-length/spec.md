# Change: KOA-5-content-length
Ticket: KOA-5
Type: bug

## Problem
`request.length` and `response.length` parse Content-Length with `parseInt`: `10.5` and `10abc` read as `10`, and
`response.length` reads `hey` as `0` (request reads it as `undefined`). RFC 9110 8.6 allows digits only.

## Outcome
Both getters return the number for a Content-Length of digits only and `undefined` for any other value, through
one parser (`lib/content-length.js`). A response without the header still deduces the length from the body.

## Requirements

### REQ-REQ-001: request.length reads only a valid Content-Length
Errors: none
Scenario: happy - digits only
  Given a request with Content-Length "2147483648"
  When request.length is read
  Then it is 2147483648
  Level: unit
Scenario: error - decimal value
  Given a request with Content-Length "10.5"
  When request.length is read
  Then it is undefined
  Level: unit
Scenario: error - digits then junk
  Given a request with Content-Length "10abc"
  When request.length is read
  Then it is undefined
  Level: unit

### REQ-RES-004: response.length reads only a valid Content-Length
Errors: none
Scenario: happy - digits only
  Given a response with Content-Length "1024"
  When response.length is read
  Then it is 1024
  Level: unit
Scenario: error - not a number
  Given a response with Content-Length "hey"
  When response.length is read
  Then it is undefined
  Level: unit
Scenario: error - digits then junk
  Given a response with Content-Length "10abc"
  When response.length is read
  Then it is undefined
  Level: unit

## Non-functional
none

## Out of scope
A 400 for a bad request header; `response.length=`; `application.js` (HEAD only reads `response.length` when no
Content-Length is set, so it does not see a bad header).

## Assumptions
A header Node holds as a number (`res.setHeader('Content-Length', 5)`) is read as that number. Surrounding spaces
are trimmed (Node already trims request headers).

## Edited test
Spike (bug playbook step 2, throwaway fix in a scratch worktree, full `node --test`): two tests pin the bug and change.
- `__tests__/request/length.test.js` "should handle floating-point-like strings (truncate decimal)": expects `10` for
  `10.5`; becomes `undefined` (S1).
- `__tests__/response/length.test.js` "but not number / should return 0": expects `0` for `hey`; becomes `undefined` (S2).

## Open questions
none
