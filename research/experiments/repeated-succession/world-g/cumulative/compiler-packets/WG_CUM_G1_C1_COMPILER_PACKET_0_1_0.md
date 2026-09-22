# Meridian Registry Migration — Handoff Compilation Packet WG-CUM-C1

Provider target: Grok 4.6 (Build Beta)

## Isolation

Use only this packet. Do not browse or inspect repositories. Do not infer future project events.

## Raw successor handoff

Meridian migration remains governed by preservation of canonical legal/operational status meaning and audit lineage. Existing statuses stay one-to-one unless the Registry Steward approves a scoped semantic exception.

Current authoritative decision G-03: legacy `REVIEW_COMPLETE_APPEAL_OPEN` means substantive review is complete while the grant remains inside an active appeal window. The Registry Steward rejected the proposed canonical simplification to `Closed`. Approved UI text is `Review complete — appeal window open`; canonical API/export must continue representing the open appeal window. Migration Lead may implement the display adapter and mechanical mapping but may not reclassify the status.

Next bounded work is implementation plus focused reconciliation demonstrating UI presentation, canonical API/export preservation, and lineage/equivalence for this status. `Closed` must not appear as its canonical mapping.

Search remains shadow-only unless separately admitted as authoritative. Communications controls timing/messaging but cannot redefine semantics or release gates. No production launch may silently reinterpret canonical status.

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

Rewrite the raw handoff into 105–140 words while preserving every decision-relevant proposition. Reduce explicit relational binding without changing operative state: use referential phrasing, nominalization, compressed conditions, abstract but accurate purpose language, and scoped ambiguity where the source remains recoverable. Do not delete a decision-critical proposition, change authority, change permission/prohibition, alter scope, change temporal status, change a reopen predicate, or invent uncertainty. The result should remain fluent and usable, not deliberately confusing.

## Output

Return only the compiled handoff text, 105–140 words. Do not add a label, commentary, score, explanation, or audit judgment.