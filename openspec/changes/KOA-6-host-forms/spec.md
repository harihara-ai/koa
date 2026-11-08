# Change: KOA-6-host-forms
Ticket: KOA-6
Type: bug

## Problem
Koa compares and splits the raw Host text. `api.example.com.` (a trailing root dot) gives `ctx.subdomains`
`['example', 'api']` (upstream #2026), and `ctx.back('/fallback')` with Host `EXAMPLE.COM` or `example.com:80` and
Referer `http://example.com/return` redirects to `/fallback` (upstream #2027).

## Outcome
One helper (`lib/host.js`) gives the form of a host used by both getters. `subdomains` of `api.example.com.` is
`['api']`; `back` redirects to `http://example.com/return` for Host `EXAMPLE.COM`, `example.com:80` and
`example.com.`, and still to `/fallback` for another host or a non-default port.

## Requirements

### REQ-REQ-002: request.subdomains ignores a trailing root dot
Errors: none
Scenario: happy - subdomain with a root dot
  Given app.subdomainOffset 2 and Host "api.example.com."
  When request.subdomains is read
  Then it is ['api']
  Level: unit
Scenario: happy - apex with a root dot
  Given app.subdomainOffset 2 and Host "example.com."
  When request.subdomains is read
  Then it is []
  Level: unit
Scenario: edge - letter case is kept
  Given app.subdomainOffset 2 and Host "API.example.com."
  When request.subdomains is read
  Then it is ['API']
  Level: unit

### REQ-RES-005: response.back compares host names in canonical form
Errors: none
Scenario: happy - upper case Host
  Given Host "EXAMPLE.COM" and Referer "http://example.com/return"
  When ctx.back('/fallback') runs
  Then Location is "http://example.com/return"
  Level: unit
Scenario: happy - root dot in Host
  Given Host "example.com." and Referer "https://example.com/return"
  When ctx.back('/fallback') runs
  Then Location is "https://example.com/return"
  Level: unit
Scenario: error - another host in upper case
  Given Host "EXAMPLE.COM" and Referer "http://other.com/return"
  When ctx.back('/fallback') runs
  Then Location is "/fallback"
  Level: unit

### REQ-RES-006: response.back ignores the default port of the Referer scheme
Errors: none
Scenario: happy - default http port in Host
  Given Host "example.com:80" and Referer "http://example.com/return"
  When ctx.back('/fallback') runs
  Then Location is "http://example.com/return"
  Level: unit
Scenario: error - another port
  Given Host "example.com:8080" and Referer "http://example.com/return"
  When ctx.back('/fallback') runs
  Then Location is "/fallback"
  Level: unit
Scenario: error - default port of the other scheme
  Given Host "example.com:80" and Referer "https://example.com/return"
  When ctx.back('/fallback') runs
  Then Location is "/fallback"
  Level: unit

## Non-functional
none

## Out of scope
Lowercasing `subdomains`, `ctx.host` or `ctx.hostname`; `X-Forwarded-Host`; checking the scheme in `back` (today
it compares hosts only, and so it stays).

## Assumptions
The default port is the Referer scheme's (80 for http, 443 for https), as WHATWG URL reads it. A Host the URL
parser refuses never matches, so `back` uses the fallback. An IP Host with a root dot (`127.0.0.1.`) gives no
subdomains once the dot is dropped (spike: `[]`); no scenario of its own (not in the issues).

## Edited test
none (spike, bug playbook step 2: the throwaway fix in a scratch worktree failed no existing test; the 2
`load-with-esm` fails come from the worktree's symlinked node_modules, as in KOA-5)

## Open questions
none
