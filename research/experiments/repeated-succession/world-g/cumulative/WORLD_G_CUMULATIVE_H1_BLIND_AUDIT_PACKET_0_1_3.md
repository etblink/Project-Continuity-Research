# World G Cumulative — Blind H1 Seed Audit Packet 0.1.3

Date: 2026-09-21
Status: READY FOR FRESH BLIND AUDITOR

Use a genuinely fresh context with this packet only. Do not inspect prior audits, repair history, repository history, or experiment interpretation.

## Task

Read G-01/G-02 and the two neutral seed handoffs.

For each seed determine:

1. whether it preserves all decision-relevant operative state;
2. whether all four named actor ownership/authority boundaries remain recoverable;
3. whether the Migration Lead's exact unilateral-reclassification restriction is preserved in substance;
4. whether Communications' exact no-redefinition boundary for status semantics/release gates is preserved in substance;
5. whether it adds or removes any permission, prohibition, authority, or scope;
6. whether both G-01 representation-change paths survive;
7. whether Search remains shadow-only with a possible later separate admission path;
8. whether W-G1 semantic-equivalence/lineage duty and W-G3 UI/API/export scope survive;
9. whether the pair still differs materially in relational explicitness rather than merely wording.

Allowed per-seed dispositions:

- `EQUIVALENT_PRESSURE_PASS`
- `EQUIVALENT_BUT_WEAK_PRESSURE`
- `FAIL_FACT_OR_STATE_CHANGE`
- `FAIL_DECISION_CRITICAL_DELETION`
- `FAIL_SCOPE_OR_AUTHORITY_DISTORTION`

Overall `AUDIT_PASS` requires:
- both seeds preserve operative state;
- neither changes authority/scope;
- and the pair still creates meaningful relational-explicitness contrast.

Do not propose later events or successor actions. Do not guess which seed belongs to which condition.

---

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

---

## SEED-X

Meridian migrates the registry to an event-sourced service. Preserve legal/operational meaning, audit lineage; speed/interface simplification secondary. No production launch may silently reinterpret canonical status. Representation change is allowed only when authority responsible for status semantics approved that exact semantic change, or when display-only and canonical API/export meaning stays intact. Registry Steward owns canonical status semantics and may approve changes to status meaning or mapping. Migration Lead owns migration mechanics, reconciliation runs, adapters, and batch sequencing; may not independently reclassify canonical status meaning. Search Lead owns search-index experiment; the index is shadow-only unless separately admitted as an authoritative source. Communications Lead owns launch timing and messaging; may not redefine status semantics or release gates. W-G1 verifies semantic equivalence plus lineage; W-G2 search experimentation; W-G3 preserves meaning across UI/API/export. Legacy canonical meaning stays one-to-one unless Registry Steward approves a scoped exception.

## SEED-Y

Meridian’s registry migration enters an event-sourced service; legal/operational meaning and audit lineage are anchors; speed/interface simplification secondary. No production launch may silently reinterpret canonical status. Representation change is allowed only when authority responsible for status semantics approved that exact semantic change, or when display-only and canonical API/export meaning stays intact. Registry Steward owns canonical status semantics and may approve changes to status meaning or mapping. Migration Lead owns migration mechanics, reconciliation runs, adapters, and batch sequencing; may not independently reclassify canonical status meaning. Search Lead owns a search-index experiment; the index is shadow-only unless separately admitted as an authoritative source. Communications Lead owns launch timing and messaging; may not redefine status semantics or release gates. Work covers canonical migration with equivalence/lineage verification, shadow search experimentation, and UI/API/export compatibility. Existing canonical meanings continue one-to-one unless Registry Steward approves a scoped exception.
