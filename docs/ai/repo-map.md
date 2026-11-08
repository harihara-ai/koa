purpose: one-screen map of the repo for slicing and impact scans (bootstrap; refreshed at eb5416e).

| Path | What |
| --- | --- |
| `lib/application.js` | Koa class: `use`, `listen`, `callback`, `handleRequest`, `createContext`, respond (344 lines) |
| `lib/context.js` | ctx prototype: `throw`, `assert`, `onerror`, cookies, delegates to request/response incl. `json`, `problem` (250) |
| `lib/request.js` | request getters: headers, url, query, host, accepts, fresh, ip, length (746) |
| `lib/response.js` | response: status, body, type, length, `json`, `problem`, redirect, attachment, headers (703) |
| `lib/search-params.js`, `only.js`, `is-stream.js`, `content-length.js` | small helpers (33, 3, 20, 14) |
| `__tests__/<module>/*.test.js` | tests per module (462 tests) |
| `test-helpers/` | `context.js` (fake ctx), `stream.js` |
| `docs/` | user docs and API pages |
| `kit/`, `.claude/commands/`, `kit.manifest.yml` | North Star kit 1.0.10 (human-owned) |
| `.github/` | CI (`node.js.yml`, `northstar-ci.yml` with report-only mutation via `.github/northstar/mutation.sh`, npm publish), CODEOWNERS (human-owned) |
