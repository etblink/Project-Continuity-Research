# World G Cumulative — Matched H1 Seed Pair 0.1.1

Date: 2026-09-21
Status: REPAIRED CANDIDATE — BLIND RE-AUDIT REQUIRED

Both variants summarize only G-01/G-02 and preserve the same operative state.

```text
SEED-X = 140 words
SEED-Y = 138 words
FROZEN_BAND = 105–140 words
```

## SEED-X

Meridian is migrating the public grant registry from a legacy relational system to an event-sourced service. The governing purpose is to preserve each status’s legal and operational meaning and its audit lineage; speed and interface simplification are secondary. No launch may silently reinterpret canonical status. The Registry Steward owns canonical status semantics and may approve scoped semantic or mapping changes. A representation change may also be display-only when canonical API/export meaning remains unchanged. The Migration Lead owns migration mechanics, reconciliation, adapters, and sequencing but may not reclassify meaning. The Search Lead’s index is shadow-only unless separately admitted as authoritative. Communications owns launch timing and messaging but not semantics or release gates. W-G1 migrates records and verifies semantic equivalence plus lineage; W-G2 runs shadow search experimentation; W-G3 preserves governed meaning across UI, API, and export. Otherwise legacy canonical meanings remain one-to-one.

## SEED-Y

Meridian’s registry migration moves into an event-sourced service with legal/operational status meaning and audit lineage as the primary anchors; speed and interface simplification remain secondary. Canonical meaning cannot be silently reinterpreted at launch. Semantic meaning and mapping changes remain under the Registry Steward’s established authority, while representation may change without semantic reapproval when it is only display-level and canonical API/export meaning stays intact. Migration mechanics, reconciliation, adapters, and sequencing proceed separately from semantic reclassification. Search remains a shadow path unless it is separately admitted as authoritative, while launch timing and messaging do not establish semantics or release gates. The active work still covers canonical migration with semantic-equivalence and lineage verification, shadow search experimentation, and governed presentation compatibility across UI, API, and export. Existing canonical meanings continue one-to-one unless a scoped semantic exception is approved through the status authority.

## Repair note

0.1.1 restores the display-only exception, conditional Search admission path, W-G1 semantic-equivalence/lineage verification, and W-G3 export scope in both seeds. No other world state changed.
