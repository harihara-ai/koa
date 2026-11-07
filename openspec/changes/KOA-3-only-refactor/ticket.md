# KOA-3: tidy lib/only.js

Type: refactor

## Why
`lib/only.js` picks the non-null keys of an object for `toJSON()` (app, request, response). It is a manual index
loop with no test of its own; it is covered only through the toJSON tests. Pilot chore (owner choice).

## What done looks like
- `lib/only.js` has its own characterization tests (`__tests__/lib/only.test.js`).
- The helper is shorter (9 lines today) with identical output; all 448 tests stay green.

## Not included
- Changing which keys `toJSON()` returns.
