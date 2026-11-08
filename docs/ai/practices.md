purpose: how this repo works today, detected by /bootstrap; each line cites its source.

- Commits: conventional-style prefixes (`fix:`, `feat:`, `docs:`) with the upstream PR number in brackets (`git log`).
- Branches: PRs to `master`, the default branch (`.github/workflows/node.js.yml`, `northstar-ci.yml`).
- PR template: none (`.github/` has none).
- Review: code owners for kit, CI and build files (`.github/CODEOWNERS`); master ruleset needs a PR, code-owner
  review and the `tests` and `gate` checks (ruleset read via `rules/branches/master`).
- Tests: `node --test` (Node's built-in runner) over `__tests__/**/*.test.js`, one folder per module
  (`application`, `context`, `request`, `response`, `lib`); assertions with `node:assert`, HTTP with `supertest`;
  helpers in `test-helpers/` (`package.json` scripts, `__tests__/`).
- Coverage: `c8` (`npm run test:coverage`); CI keeps lcov (`northstar-ci.yml`).
- Mutation: Stryker on the lines a PR changed in `lib/`, report only, never a gate (`.github/northstar/mutation.sh`).
- Lint: `standard` (`npm run lint`); 2-space indent, LF, final newline (`.editorconfig`).
- Build: `npm run build` makes `dist/koa.mjs` (ESM wrapper); `__tests__/load-with-esm.test.js` needs it (`package.json`).
- Node: `>= 18` (`package.json` engines); CI matrix 18, 20, 22 (`node.js.yml`).
