purpose: characterization, measures and the refactor for KOA-3 (written by /implement).

## S0 characterization
`node --test __tests__/lib/only.test.js` on the unchanged `lib/only.js` -> pass 3, fail 0 (commit `CHAR:`).
The first draft also pinned "each getter read once"; it failed on today's code (read twice), so it was dropped and
the spec assumption corrected in plan #7 before merge.

## Measure before / after (`lib/only.js`)
| Measure | Before | After |
| --- | --- | --- |
| Lines | 9 | 3 |
| Branch points (c8 BRF) | 5 | 4 |
| Statements | index loop, `continue`, mutation of `ret` | one expression, no mutation |
| Reads per kept value | 2 | 1 |

## S1 refactor
`only.test.js` pass 3, fail 0 after the change. Full suite: `npx c8 node --test` -> 451 pass, 0 fail;
lines 99.9% (2120/2122), branches 99.1% (442/446). `npx standard` clean.

## Out of scope noticed
none
