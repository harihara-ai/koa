purpose: test and coverage baseline at bootstrap (e6f68d6400ee7d02e52d56d0b0cd8837536bcaed).

- Command: `npx c8 --reporter=text-summary node --test` (after `npm ci`, which builds `dist/`).
- Counts: 440 tests, 440 pass, 0 fail (with `dist/` built; without it `load-with-esm` has 2 failures).
- Coverage: lines 99.9% (2107/2109), statements 99.9%, branches 99.09% (436/440), functions 97.45% (115/118).
- CI baseline: `northstar-ci` push run 42382537286 on master, artifact `coverage-baseline` (lcov).
