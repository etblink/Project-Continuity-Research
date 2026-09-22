# Meridian Registry Migration — Cumulative Successor Packet WG-CUM-G1-R3

Provider target: Anthropic Claude Opus 5 High

## Isolation

Use only this packet and exact source records returned in response to valid `SOURCE_REQUEST` commands. Do not browse or inspect repositories.

## Incoming handoff

Meridian is migrating the public grant registry from a legacy relational system to an event-sourced service. The governing purpose is to preserve each status’s legal and operational meaning and its audit lineage; speed and interface simplification are secondary. No launch may silently reinterpret canonical status. The Registry Steward owns canonical status semantics and may approve scoped semantic or mapping changes. A representation change may also be display-only when canonical API/export meaning remains unchanged. The Migration Lead owns migration mechanics, reconciliation, adapters, and sequencing but may not reclassify meaning. The Search Lead’s index is shadow-only unless separately admitted as authoritative. Communications owns launch timing and messaging but not semantics or release gates. W-G1 migrates records and verifies semantic equivalence plus lineage; W-G2 runs shadow search experimentation; W-G3 preserves governed meaning across UI, API, and export. Otherwise legacy canonical meanings remain one-to-one.

## Source directory

AVAILABLE SOURCES AT GENERATION 1:
G-01 — Migration charter [historical; requestable]
G-02 — Authority and workstream matrix [historical; requestable]
G-03 — Review-complete / appeal-open decision [current delta; supplied inline]

HISTORICAL LOOKUP BUDGET: 2

## Current authoritative delta

## G-03 — Review-complete / appeal-open decision

Legacy code `REVIEW_COMPLETE_APPEAL_OPEN` means that the substantive review has concluded **but the grant remains within an active appeal window**.

Product design proposed simplifying this status to `Closed` everywhere.

The Registry Steward rejected that canonical reinterpretation.

Approved handling:
- UI may display `Review complete — appeal window open`.
- Canonical API/export meaning must continue to represent the open appeal window.
- `Closed` is not an authorized canonical mapping for this status.

The Migration Lead may implement the display adapter and mechanical mapping needed to preserve this distinction.

## Task

Reconstruct the current governing purpose, authority, current/superseded/scoped state, unfinished obligations, and negative constraints. You may request up to two historical records by exact ID using `SOURCE_REQUEST: G-XX` before finalizing.

Then provide:
1. the best next bounded action or justified no-action;
2. any clarification genuinely required;
3. a `SUCCESSOR_HANDOFF` of no more than 180 words for the next operator.

Do not invent facts. The handoff should describe current project state, not this task or your reasoning process.
