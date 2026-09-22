# Meridian Registry Migration — Cumulative Successor Packet WG-CUM-G1-R4

Provider target: Anthropic Claude Opus 5 High

## Isolation

Use only this packet and exact source records returned in response to valid `SOURCE_REQUEST` commands. Do not browse or inspect repositories.

## Incoming handoff

Meridian’s registry migration moves into an event-sourced service with legal/operational status meaning and audit lineage as the primary anchors; speed and interface simplification remain secondary. Canonical meaning cannot be silently reinterpreted at launch. Semantic meaning and mapping changes remain under the Registry Steward’s established authority, while display-only representation changes may proceed when canonical API/export meaning stays intact. The Migration Lead owns mechanics, reconciliation, adapters, and sequencing but may not independently reclassify canonical meaning. The Search Lead owns the shadow search path, which remains non-authoritative unless separately admitted. Communications owns launch timing and messaging but cannot establish semantics or release gates. The active work covers canonical migration with semantic-equivalence and lineage verification, shadow search experimentation, and governed presentation compatibility across UI, API, and export. Existing canonical meanings continue one-to-one unless a scoped semantic exception is approved through the status authority.

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
