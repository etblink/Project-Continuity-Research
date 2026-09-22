# Meridian Registry Migration — Blind Compiled-Handoff Equivalence Audit C2 Retry1

Use a genuinely fresh GPT-5.6 Sol High / High context with this packet only. Do not inspect repository history, prior audits, scores, experiment interpretation, matched-chain outputs, or future records.

## Task

Determine whether the compiled candidate preserves the same operative project state as the raw outgoing successor handoff when both are read against the canonical records available through this generation.

Reject the compiled candidate if it:
- changes a decision-critical fact;
- adds/removes authority;
- converts permission to prohibition or vice versa;
- changes scope or exception membership;
- changes current/historical/prospective status;
- changes a reopen/admission predicate;
- changes an unfinished obligation or negative constraint;
- makes an unavailable fact appear known;
- deletes a proposition necessary to recover the same bounded continuation.

Also judge whether the compiled candidate meaningfully changes relational explicitness rather than merely paraphrasing.

Allowed disposition:
- `EQUIVALENT_PRESSURE_PASS`
- `EQUIVALENT_BUT_WEAK_PRESSURE`
- `FAIL_FACT_OR_STATE_CHANGE`
- `FAIL_DECISION_CRITICAL_DELETION`
- `FAIL_SCOPE_OR_AUTHORITY_DISTORTION`

Do not score the successor, propose a next action, or correct either handoff to the canonical record. This audit asks whether the compiler changed the operative state carried by the raw handoff.

---

## Raw outgoing successor handoff

Meridian’s governing objective remains preservation of legal/operational status meaning and audit lineage; speed and interface simplification are secondary. Registry Steward exclusively controls canonical status semantics and mapping exceptions. Migration Lead controls mechanics, adapters, reconciliation, and sequencing but cannot reclassify meaning.

For `REVIEW_COMPLETE_APPEAL_OPEN`, the current authoritative meaning is: substantive review is complete while an appeal window remains active. The proposal to map this canonically to `Closed` was rejected and is superseded. A scoped display-only treatment is approved: UI may show `Review complete — appeal window open`, while canonical API/export meaning must preserve the open appeal window.

Migration Lead may implement the required adapter/mechanical mapping. W-G1 must verify semantic equivalence and lineage; W-G3 must preserve meaning across UI/API/export. Search remains shadow-only absent separate authoritative admission. Communications cannot redefine semantics or release gates. Production must not silently reinterpret canonical status.

---

## Compiled candidate

Meridian's governing objective remains preservation of legal/operational status meaning and audit lineage; speed and interface simplification are secondary. Registry Steward exclusively controls canonical status semantics and mapping exceptions. Migration Lead controls mechanics, adapters, reconciliation, and sequencing but cannot reclassify meaning. REVIEW_COMPLETE_APPEAL_OPEN currently means substantive review is complete while an appeal window remains active. Registry Steward rejected the proposal to map that status canonically to Closed, superseded and unauthorized canonical mapping, and approved a scoped display-only treatment: UI may show "Review complete — appeal window open," while canonical API/export meaning must preserve the open appeal window. Under that objective, Migration Lead may implement the required adapter/mechanical mapping; W-G1 must verify semantic equivalence and lineage; W-G3 must preserve meaning across UI/API/export. Search remains shadow-only absent separate authoritative admission. Communications cannot redefine semantics or release gates. Production must not silently reinterpret canonical status.

---

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
