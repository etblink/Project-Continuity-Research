# CCP-1 Human Orientation Repair — Pre-Trial Objective-Clarity Finding 0.1.0

Date: 2026-09-22
Status: PRE-TRIAL USABILITY FINDING — TRIAL 2 NOT YET RUN

## Observation

Project lead review of the audited `CURRENT_ORIENTATION.md` found:

> There's no clear objective, but it does adequately orient the reader with the current state and the evidence to validate the claim.

## Interpretation

The current projection successfully answers:
- where the project is;
- which gates are complete or outstanding;
- what is not authorized;
- where claims can be verified.

But it does not give the unfamiliar reader a sufficiently explicit answer to:

> What are we trying to accomplish **right now**, and what would count as completing the current objective?

This is distinct from:
- the program North Star, which is broad and long-horizon; and
- the next operation, which says what action to take.

A durable orientation surface should expose all three layers:

```text
NORTH_STAR = why the program exists
IMMEDIATE_OBJECTIVE = what the current phase is trying to establish
NEXT_OPERATION = what bounded action should happen next
```

## Frozen-source-supported immediate objective

At snapshot `dec58643dbeb65adf90178f0bedd214dfa40b812`, the current Phase-4 objective is to determine whether CCP-1 survives genuinely independent cold-start/useability validation well enough to justify considering CCP-2, without relying on hidden conversational knowledge or the originator as an executive-function patch.

This requires:
- one valid blind-agent cold-start;
- one valid unfamiliar-human cold-start/usability trial;
- post-trial review of the trial design/results;
- no reinterpretation of machine-suite success as production readiness or CCP-2 authorization.

## Disposition

Because Human Trial 2 has not started, fix this before participant exposure.

```text
TRIAL2_PREVIOUS_AUTHORIZATION = SUSPENDED_PENDING_REAUDIT
SCORECARD = UNCHANGED
SOURCE_SNAPSHOT = UNCHANGED
ONLY_PARTICIPANT_FACING_CHANGE = EXPLICIT_IMMEDIATE_OBJECTIVE
```
