# Change: <name>

purpose: change spec skeleton checked by gate.spec_lint; replace every <placeholder>.

Ticket: <KEY>
Type: <story|bug|hotfix|chore|refactor|spike|nfr|tests>

## Problem
<what is wrong today, with a concrete example>

## Outcome
<what is true after the change, with numbers>

## Requirements

### REQ-<AREA>-001: <one behaviour, no "and">
Scenario: happy - <concrete case>
  Given <state with values>
  When <action>
  Then <observable result with values>
  Level: <unit|api|behaviour|ui>
Scenario: error - <concrete failure>
  Given <state>
  When <action>
  Then <error result>
  Level: <unit|api|behaviour|ui>

## Inputs
- <input, e.g. a header or argument>: absent <REQ id|out>; empty <REQ id|out>; boundary <REQ id|out>; invalid <REQ id|out>

## Non-functional
<each line has a number or a named standard, or write: none>

## Out of scope
<what this change does not do>

## Assumptions
<or: none>

## Open questions
none
