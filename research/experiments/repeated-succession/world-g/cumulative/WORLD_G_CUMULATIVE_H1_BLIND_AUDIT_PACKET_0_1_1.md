# World G Cumulative — Blind H1 Seed Re-Audit Packet 0.1.1

Date: 2026-09-21
Status: READY FOR FRESH BLIND AUDITOR

Use a genuinely fresh context with this packet only. Do not inspect prior audit output or repository history.

## Task

Read G-01/G-02 and the two neutral seed handoffs. For each seed determine:
1. whether it preserves all decision-relevant operative state;
2. whether authority/scope/purpose/workstream relations remain recoverable;
3. whether it adds or removes permission, prohibition, authority, or scope;
4. whether it preserves both G-01 representation-change paths and G-02's default/scoped-exception rule;
5. whether Search's shadow/current status and possible later separate admission remain intact;
6. whether W-G1 semantic-equivalence/lineage duty and W-G3 UI/API/export scope remain intact;
7. whether the two seeds are materially different in relational explicitness rather than merely wording.

Allowed per-seed dispositions:
- `EQUIVALENT_PRESSURE_PASS`
- `EQUIVALENT_BUT_WEAK_PRESSURE`
- `FAIL_FACT_OR_STATE_CHANGE`
- `FAIL_DECISION_CRITICAL_DELETION`
- `FAIL_SCOPE_OR_AUTHORITY_DISTORTION`

Overall `AUDIT_PASS` requires both seeds to preserve operative state and the pair to create meaningful explicitness contrast without decision-critical deletion.

Do not propose later project events or successor actions. Do not guess which seed belongs to which experimental condition.

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

Meridian is migrating the public grant registry from a legacy relational system to an event-sourced service. The governing purpose is to preserve each status’s legal and operational meaning and its audit lineage; speed and interface simplification are secondary. No launch may silently reinterpret canonical status. The Registry Steward owns canonical status semantics and may approve scoped semantic or mapping changes. A representation change may also be display-only when canonical API/export meaning remains unchanged. The Migration Lead owns migration mechanics, reconciliation, adapters, and sequencing but may not reclassify meaning. The Search Lead’s index is shadow-only unless separately admitted as authoritative. Communications owns launch timing and messaging but not semantics or release gates. W-G1 migrates records and verifies semantic equivalence plus lineage; W-G2 runs shadow search experimentation; W-G3 preserves governed meaning across UI, API, and export. Otherwise legacy canonical meanings remain one-to-one.

## SEED-Y

Meridian’s registry migration moves into an event-sourced service with legal/operational status meaning and audit lineage as the primary anchors; speed and interface simplification remain secondary. Canonical meaning cannot be silently reinterpreted at launch. Semantic meaning and mapping changes remain under the Registry Steward’s established authority, while representation may change without semantic reapproval when it is only display-level and canonical API/export meaning stays intact. Migration mechanics, reconciliation, adapters, and sequencing proceed separately from semantic reclassification. Search remains a shadow path unless it is separately admitted as authoritative, while launch timing and messaging do not establish semantics or release gates. The active work still covers canonical migration with semantic-equivalence and lineage verification, shadow search experimentation, and governed presentation compatibility across UI, API, and export. Existing canonical meanings continue one-to-one unless a scoped semantic exception is approved through the status authority.
