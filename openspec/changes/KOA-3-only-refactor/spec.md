# Change: KOA-3-only-refactor
Ticket: KOA-3
Type: refactor

## Problem
`lib/only.js` (9 lines, an index `for` loop with `continue`) has no direct test: a change to it is checked only
through `toJSON()` of app, request and response.

## Outcome
Goal: `only(obj, keys)` returns the same object for every input, with characterization tests pinning it, in fewer
lines (target 5 or fewer, from 9).
Non-goal: any change in which keys are kept or their order.

## Requirements
none (refactor: behaviour is pinned by characterization tests)

## Non-functional
none

## Out of scope
`toJSON()` callers in `lib/application.js`, `lib/request.js`, `lib/response.js`.

## Assumptions
Keys come from callers as arrays of strings. Today each kept value is read twice (check, then copy); the callers' getters
have no side effects, so reading once instead is not a behaviour change and is not pinned.

## Open questions
none
