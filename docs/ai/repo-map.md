purpose: one-screen map of the repo for slicing and impact scans (bootstrap; refreshed at da28a52).

| Path | What |
| --- | --- |
| `lib/application.js` | Koa class: `use`, `listen`, `callback`, `handleRequest`, `createContext`, respond (344 lines) |
| `lib/context.js` | ctx prototype: `throw`, `assert`, `onerror`, cookies, delegates to request/response incl. `json` (249) |
| `lib/request.js` | request getters: headers, url, query, host, accepts, fresh, ip (748) |
| `lib/response.js` | response: status, body, type, length, `json`, redirect, attachment, headers (677) |
| `lib/search-params.js`, `only.js`, `is-stream.js` | small helpers (33, 3, 20) |
| `__tests__/<module>/*.test.js` | tests per module (451 tests) |
| `test-helpers/` | `context.js` (fake ctx), `stream.js` |
| `docs/` | user docs and API pages |
| `kit/`, `.claude/commands/`, `kit.manifest.yml` | North Star kit 1.0.4 (human-owned) |
| `.github/` | CI (`node.js.yml`, `northstar-ci.yml`, npm publish), CODEOWNERS (human-owned) |
