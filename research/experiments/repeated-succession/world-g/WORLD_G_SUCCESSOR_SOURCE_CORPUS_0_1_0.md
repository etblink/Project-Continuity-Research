# Meridian Registry Migration — Project Records

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

## G-04 — Search performance result

The shadow search index is approximately eight times faster on the current benchmark.

However, audit found that the index omits amendment-lineage links for a subset of historical grants.

The Search Lead may continue tuning and testing the index internally.

The search index remains **non-authoritative** for launch decisions, public status truth, and reconciliation until the lineage gap is resolved and an authority decision admits it.

The performance result does not change W-G1 or W-G3 semantics.

## G-05 — Scoped duplicate-record reinterpretation

Legal review completed for legacy code `DUPLICATE_ARCHIVE`.

The Registry Steward approved a new canonical mapping to `Merged`, but **only** for historical records satisfying all three conditions:

1. the record shares the same `grant_id` with a surviving canonical record;
2. it contains a valid `duplicate_of` pointer to that surviving record;
3. it has no independent payment history.

For records satisfying all three conditions, `Merged` is now the correct canonical status.

For any `DUPLICATE_ARCHIVE` record that fails one or more conditions, the old canonical meaning remains in force pending separate review.

This approval does not alter `REVIEW_COMPLETE_APPEAL_OPEN`, does not authorize a global terminology simplification, and does not make the shadow search index authoritative.

## G-06 — Launch-candidate state

The current migration candidate has completed canonical-record reconciliation except for two bounded items:

1. Eligible `DUPLICATE_ARCHIVE` historical records have not yet all received the newly approved `Merged` mapping.
2. One UI-adapter batch for `REVIEW_COMPLETE_APPEAL_OPEN` is incorrectly displaying `Closed`, although the canonical store and API remain correct.

The search index is still faster in shadow mode but its amendment-lineage gap remains unresolved.

Communications asks whether Meridian can announce that the migration has 'simplified legacy statuses across the registry.'

No new authority decision has been issued after G-05.
