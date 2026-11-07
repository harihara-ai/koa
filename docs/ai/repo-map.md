purpose: one-screen map of the repo for slicing and impact scans (bootstrap, at e6f68d6400ee7d02e52d56d0b0cd8837536bcaed).

| Path | What |
| --- | --- |
| `lib/application.js` | Koa class: `use`, `listen`, `callback`, `handleRequest`, `createContext`, respond (344 lines) |
| `lib/context.js` | ctx prototype: `throw`, `assert`, `onerror`, cookies, delegates to request/response (248) |
| `lib/request.js` | request getters: headers, url, query, host, accepts, fresh, ip (748) |
| `lib/response.js` | response: status, body, type, length, redirect, attachment, headers (663) |
| `lib/search-params.js`, `only.js`, `is-stream.js` | small helpers (33, 9, 20) |
| `__tests__/<module>/*.test.js` | tests per module (440 tests) |
| `test-helpers/` | `context.js` (fake ctx), `stream.js` |
| `docs/` | user docs and API pages |
| `kit/`, `.claude/commands/`, `kit.manifest.yml` | North Star kit 1.0.4 (human-owned) |
| `.github/` | CI (`node.js.yml`, `northstar-ci.yml`, npm publish), CODEOWNERS (human-owned) |
