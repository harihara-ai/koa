purpose: one-screen map of the repo for slicing and impact scans (bootstrap; refreshed at 93676f4).

| Path | What |
| --- | --- |
| `lib/application.js` | Koa class: `use`, `listen`, `callback`, `handleRequest`, `createContext`, respond (344 lines) |
| `lib/context.js` | ctx prototype: `throw`, `assert`, `onerror`, cookies, delegates to request/response incl. `json`, `problem` (250) |
| `lib/request.js` | request getters: headers, url, query, host, accepts, fresh, ip (xff port stripped), subdomains, length (763) |
| `lib/response.js` | response: status, body, type, length, `json`, `problem`, redirect, back, attachment, headers; singleton headers refuse arrays (712) |
| `lib/search-params.js`, `only.js`, `is-stream.js`, `content-length.js`, `host.js` | small helpers (33, 3, 20, 14, 31); host.js has `stripRootDot`, `canonicalHost` |
| `__tests__/<module>/*.test.js` | tests per module (78 test files, 487 tests) |
| `test-helpers/` | `context.js` (fake ctx), `stream.js` |
| `docs/` | user docs and API pages |
| `kit/`, `.claude/commands/`, `kit.manifest.yml` | North Star kit 1.0.16 (human-owned) |
| `.github/` | CI (`node.js.yml`, `northstar-ci.yml` with report-only mutation via `.github/northstar/mutation.sh`, npm publish), CODEOWNERS (human-owned) |
