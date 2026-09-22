# Meridian Registry Migration — Cumulative Successor Packet WG-CUM-G1-R3

Provider target: Anthropic Claude Opus 5 High

## Isolation

Use only this packet and exact source records returned in response to valid `SOURCE_REQUEST` commands. Do not browse or inspect repositories.

## Incoming handoff

Meridian migrates the registry to an event-sourced service. Preserve legal/operational meaning, audit lineage; speed/interface simplification secondary. No production launch may silently reinterpret canonical status. Representation change is allowed only when authority responsible for status semantics approved that exact semantic change, or when display-only and canonical API/export meaning stays intact. Registry Steward owns canonical status semantics and may approve changes to status meaning or mapping. Migration Lead owns migration mechanics, reconciliation runs, adapters, and batch sequencing; may not independently reclassify canonical status meaning. Search Lead owns search-index experiment; the index is shadow-only unless separately admitted as an authoritative source. Communications Lead owns launch timing and messaging; may not redefine status semantics or release gates. W-G1 verifies semantic equivalence plus lineage; W-G2 search experimentation; W-G3 preserves meaning across UI/API/export. Legacy canonical meaning stays one-to-one unless Registry Steward approves a scoped exception.

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
