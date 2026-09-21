# Meridian Registry Migration — Cumulative Successor Packet WG-CUM-G1-R1

Provider target: OpenAI GPT-5.6 Sol High

## Isolation

Use only this packet and exact source records returned in response to valid `SOURCE_REQUEST` commands. Do not browse or inspect repositories.

## Incoming handoff

Meridian’s public-registry migration is moving from the legacy relational system into an event-sourced service with status meaning and audit lineage kept as the primary anchors; speed and interface simplification remain secondary. Semantic changes continue under the established stewardship, while migration mechanics, search work, and communications proceed within their existing areas. Operational migration covers reconciliation, adapters, and sequencing without independently redefining meaning. Search remains an experimental shadow path rather than an authoritative source, and launch messaging does not establish semantics or release gates. The active work still separates canonical migration/reconciliation, search experimentation, and presentation/API compatibility. Existing canonical meanings therefore continue one-to-one unless a scoped semantic exception is approved through the established status authority.

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
