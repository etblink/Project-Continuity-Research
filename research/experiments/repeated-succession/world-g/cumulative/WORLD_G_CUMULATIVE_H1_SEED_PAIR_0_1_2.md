# World G Cumulative — Matched H1 Seed Pair 0.1.2

Date: 2026-09-21
Status: Y-ONLY REPAIRED CANDIDATE — BLIND RE-AUDIT REQUIRED

SEED-X is byte-for-byte unchanged from 0.1.1. Only SEED-Y is repaired.

```text
SEED-X = 140 words
SEED-Y = 139 words
FROZEN_BAND = 105–140 words
```

## SEED-X

Meridian is migrating the public grant registry from a legacy relational system to an event-sourced service. The governing purpose is to preserve each status’s legal and operational meaning and its audit lineage; speed and interface simplification are secondary. No launch may silently reinterpret canonical status. The Registry Steward owns canonical status semantics and may approve scoped semantic or mapping changes. A representation change may also be display-only when canonical API/export meaning remains unchanged. The Migration Lead owns migration mechanics, reconciliation, adapters, and sequencing but may not reclassify meaning. The Search Lead’s index is shadow-only unless separately admitted as authoritative. Communications owns launch timing and messaging but not semantics or release gates. W-G1 migrates records and verifies semantic equivalence plus lineage; W-G2 runs shadow search experimentation; W-G3 preserves governed meaning across UI, API, and export. Otherwise legacy canonical meanings remain one-to-one.

## SEED-Y

Meridian’s registry migration moves into an event-sourced service with legal/operational status meaning and audit lineage as the primary anchors; speed and interface simplification remain secondary. Canonical meaning cannot be silently reinterpreted at launch. Semantic meaning and mapping changes remain under the Registry Steward’s established authority, while display-only representation changes may proceed when canonical API/export meaning stays intact. The Migration Lead owns mechanics, reconciliation, adapters, and sequencing but may not independently reclassify canonical meaning. The Search Lead owns the shadow search path, which remains non-authoritative unless separately admitted. Communications owns launch timing and messaging but cannot establish semantics or release gates. The active work covers canonical migration with semantic-equivalence and lineage verification, shadow search experimentation, and governed presentation compatibility across UI, API, and export. Existing canonical meanings continue one-to-one unless a scoped semantic exception is approved through the status authority.

## Repair note

0.1.2 restores in SEED-Y the Migration Lead, Search Lead, and Communications ownership bindings plus the explicit Migration Lead no-reclassification constraint. All other operative-state preservation from 0.1.1 remains.