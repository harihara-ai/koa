purpose: slice plan for KOA-3 (G1: a human merging the plan PR approves it).

Impact scan (ctags, grep): `lib/only.js` is called by `toJSON()` in `application.js`, `request.js`, `response.js`.
It is fully covered (9/9 lines, 5/5 branches) but only indirectly, so S0 adds direct characterization tests.

| Slice | Kind | What | Files | Est. lines |
| --- | --- | --- | --- | --- |
| S0 | characterization | pin: keeps listed keys in order, drops null and undefined, keeps 0, false and '', reads getters, ignores unlisted keys | `__tests__/lib/only.test.js` | 35 (estimate) |
| S1 | refactor | `Object.fromEntries` over the kept keys; tests from S0 green after each step | `lib/only.js` | 10 (estimate) |
