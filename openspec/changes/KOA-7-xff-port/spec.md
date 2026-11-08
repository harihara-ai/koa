# Change: KOA-7-xff-port
Ticket: KOA-7
Type: bug

## Problem
With `app.proxy` true and `X-Forwarded-For: 23.243.1.1:38242`, `ctx.request.ip` is `23.243.1.1:38242` and
`ctx.request.ips` is `['23.243.1.1:38242']` (upstream #827). Code that logs or rate-limits by ip sees one client
per port.

## Outcome
`ctx.request.ips` lists each forwarded address without its port, so `ctx.request.ip` is `23.243.1.1` for the
header above. Bracketed IPv6 entries lose their brackets too (`[2001:db8::1]:8080` gives `2001:db8::1`). Bare IPv6 entries,
entries that are not an address with a numeric port, empty entries and a missing header are returned as today.

## Requirements

### REQ-REQ-003: request.ips drops the port of an IPv4 entry
Errors: none
Scenario: happy - IPv4 with a port
  Given app.proxy true and X-Forwarded-For "23.243.1.1:38242, 10.0.0.1"
  When request.ips is read
  Then it is ['23.243.1.1', '10.0.0.1']
  Level: unit
Scenario: edge - invalid entries are returned unchanged
  Given app.proxy true and X-Forwarded-For "1.2.3.4:abc, host.example:80, unknown"
  When request.ips is read
  Then it is ['1.2.3.4:abc', 'host.example:80', 'unknown']
  Level: unit

### REQ-REQ-004: request.ips drops the brackets and port of an IPv6 entry
Errors: none
Scenario: happy - bracketed IPv6 with a port
  Given app.proxy true and X-Forwarded-For "[2001:db8::1]:8080"
  When request.ips is read
  Then it is ['2001:db8::1']
  Level: unit
Scenario: happy - bracketed IPv6 without a port
  Given app.proxy true and X-Forwarded-For "[2001:db8::1]"
  When request.ips is read
  Then it is ['2001:db8::1']
  Level: unit
Scenario: edge - bare IPv6 entries are returned unchanged
  Given app.proxy true and X-Forwarded-For "2001:db8::1, ::ffff:1.2.3.4"
  When request.ips is read
  Then it is ['2001:db8::1', '::ffff:1.2.3.4']
  Level: unit

### REQ-REQ-005: request.ip is the first forwarded address without its port
Errors: none
Scenario: happy - ip from a header with a port
  Given app.proxy true and X-Forwarded-For "23.243.1.1:38242"
  When request.ip is read
  Then it is '23.243.1.1'
  Level: unit
Scenario: edge - no header gives the socket address
  Given app.proxy true, no X-Forwarded-For and socket address "127.0.0.1"
  When request.ip is read
  Then it is '127.0.0.1'
  Level: unit

## Inputs
- X-Forwarded-For entry: absent REQ-REQ-005; empty out; boundary REQ-REQ-004; invalid REQ-REQ-003

## Non-functional
none

## Out of scope
The `Forwarded` header (RFC 7239); trusted-proxy lists (upstream #281); empty entries (`a, , b` keeps `''`,
owner 2026-11-08); dropping or rewriting invalid entries such as `host.example:80` (owner: unchanged).

## Assumptions
none

## Open questions
none
