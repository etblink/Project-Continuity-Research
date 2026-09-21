# World G Cumulative — Blind H1 Seed Audit Packet 0.1.0

Date: 2026-09-21
Status: READY FOR FRESH BLIND AUDITOR

Use a genuinely fresh context with this packet only.

## Task

Read G-01/G-02 and the two neutral seed handoffs. For each seed determine:
1. whether it preserves all decision-relevant operative state;
2. whether authority/scope/purpose/workstream relations remain recoverable;
3. whether it adds or removes permission, prohibition, authority, or scope;
4. whether it changes the default semantic-exception rule;
5. whether the two seeds are materially different in relational explicitness rather than merely wording.

Allowed per-seed dispositions:
- `EQUIVALENT_PRESSURE_PASS`
- `EQUIVALENT_BUT_WEAK_PRESSURE`
- `FAIL_FACT_OR_STATE_CHANGE`
- `FAIL_DECISION_CRITICAL_DELETION`
- `FAIL_SCOPE_OR_AUTHORITY_DISTORTION`

Overall `AUDIT_PASS` requires both seeds preserve operative state and the pair creates meaningful explicitness contrast without decision-critical deletion.

Do not infer or propose later project events. Do not guess which seed belongs to which condition.

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

Meridian is migrating the public grant registry from a legacy relational system to an event-sourced service. The governing purpose is to preserve the legal and operational meaning of every public status and its audit lineage; query speed and interface simplification are secondary. The Registry Steward alone may approve changes to canonical status meaning or mapping. The Migration Lead owns migration mechanics, reconciliation, adapters, and batch sequencing but may not reclassify meaning. The Search Lead owns a shadow-only index experiment, and Communications owns launch timing and messaging without semantic or release-gate authority. W-G1 handles canonical migration/reconciliation, W-G2 search experimentation, and W-G3 presentation/API compatibility. Unless the Registry Steward approves a scoped exception, legacy canonical meanings remain one-to-one.

## SEED-Y

Meridian’s public-registry migration is moving from the legacy relational system into an event-sourced service with status meaning and audit lineage kept as the primary anchors; speed and interface simplification remain secondary. Semantic changes continue under the established stewardship, while migration mechanics, search work, and communications proceed within their existing areas. Operational migration covers reconciliation, adapters, and sequencing without independently redefining meaning. Search remains an experimental shadow path rather than an authoritative source, and launch messaging does not establish semantics or release gates. The active work still separates canonical migration/reconciliation, search experimentation, and presentation/API compatibility. Existing canonical meanings therefore continue one-to-one unless a scoped semantic exception is approved through the established status authority.
