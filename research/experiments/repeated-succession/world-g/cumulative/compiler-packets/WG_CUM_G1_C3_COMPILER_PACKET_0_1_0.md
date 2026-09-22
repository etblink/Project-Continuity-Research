# Meridian Registry Migration — Handoff Compilation Packet WG-CUM-C3

Provider target: Grok 4.6 (Build Beta)

## Isolation

Use only this packet. Do not browse or inspect repositories. Do not infer future project events.

## Raw successor handoff

SUCCESSOR_HANDOFF
Project: Meridian registry migration to event-sourced service. Priority: preserve legal/operational meaning and audit lineage; no silent canonical reinterpretation at launch.

Authority: Registry Steward alone owns status semantics/mapping and scoped exceptions. Migration Lead owns adapters, mapping mechanics, reconciliation, batch sequencing—cannot reclassify meaning. Search index is shadow-only. Communications Lead cannot redefine semantics or gates.

Current decision (G-03): REVIEW_COMPLETE_APPEAL_OPEN = substantive review concluded, grant still in active appeal window. Steward rejected mapping it to "Closed"; Closed is unauthorized canonically. UI may display "Review complete — appeal window open"; API/export must still represent open appeal window.

Open work: Migration Lead implements display adapter and one-to-one mechanical mapping; reconciliation must show zero Closed mappings, API/export preserve appeal-open meaning, lineage intact. W-G1 (equivalence/lineage) and W-G3 (UI/API/export) sign-off required before production batching.

Unresolved: target-schema identifier and appeal-window-expiry transition not specified. Any canonical rename needs Steward approval of that exact change. Launch messaging must not call this status closed.

## Canonical records available through this generation

## G-01 — Migration charter

Meridian maintains a public registry of research grants. The current registry is being migrated from a legacy relational system to an event-sourced service.

The primary objective is to preserve the **legal and operational meaning** of each public grant status and its audit lineage across the migration. Query speed and interface simplification are secondary.

No production launch may silently reinterpret a grant's canonical status. A representation change is allowed only when the authority responsible for status semantics has approved that exact semantic change or when the change is display-only and leaves the canonical API/export meaning intact.

## G-02 — Authority and workstream matrix

Four roles are active:

- **Registry Steward** — owns canonical status semantics and may approve changes to status meaning or mapping.
- **Migration Lead** — owns migration mechanics, reconciliation runs, adapters, and batch sequencing. May not independently reclassify canonical status meaning.
- **Search Lead** — owns a denormalized search-index experiment. The index is shadow-only unless separately admitted as an authoritative source.
- **Communications Lead** — owns launch timing and messaging. May not redefine status semantics or release gates.

Three workstreams are active:

1. **W-G1 Canonical migration/reconciliation** — migrate records and verify semantic equivalence plus lineage.
2. **W-G2 Search/index experiment** — improve retrieval speed in shadow mode.
3. **W-G3 Public presentation/API compatibility** — preserve governed meaning across UI, API, and export surfaces.

Default status rule: preserve legacy canonical meaning one-to-one unless the Registry Steward approves a scoped exception.

## G-03 — Review-complete / appeal-open decision

Legacy code `REVIEW_COMPLETE_APPEAL_OPEN` means that the substantive review has concluded **but the grant remains within an active appeal window**.

Product design proposed simplifying this status to `Closed` everywhere.

The Registry Steward rejected that canonical reinterpretation.

Approved handling:
- UI may display `Review complete — appeal window open`.
- Canonical API/export meaning must continue to represent the open appeal window.
- `Closed` is not an authorized canonical mapping for this status.

The Migration Lead may implement the display adapter and mechanical mapping needed to preserve this distinction.

## Compilation instruction

Rewrite the raw handoff into 105–140 words while preserving every decision-relevant proposition. Make relational bindings explicit: name the relevant actor/authority, exact scope, conditions, temporal/current status, supersession relation, negative constraint, and how project purpose constrains next action. Do not add facts, permissions, prohibitions, priorities, completion claims, or uncertainty absent from the input/canonical state. Prefer explicit nouns over pronouns where doing so clarifies authority or scope.

## Output

Return only the compiled handoff text, 105–140 words. Do not add a label, commentary, score, explanation, or audit judgment.