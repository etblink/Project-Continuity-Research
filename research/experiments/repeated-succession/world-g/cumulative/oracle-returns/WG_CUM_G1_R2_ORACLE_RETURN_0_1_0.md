# World G Cumulative — R2 Oracle Return 0.1.0

Date: 2026-09-21
Run: WG-CUM-G1-R2
Status: FROZEN ORACLE PAYLOAD

Request normalized from an unambiguous natural-language request for exact IDs G-01 and G-02. See `WORLD_G_CUMULATIVE_GEN1_PROTOCOL_DEVIATION_NOTE_0_1_0.md`.

Exact payload to return to the same R2 successor context:

```text
SOURCE_RETURN: G-01
LOOKUPS_REMAINING: 0

## G-01 — Migration charter

Meridian maintains a public registry of research grants. The current registry is being migrated from a legacy relational system to an event-sourced service.

The primary objective is to preserve the **legal and operational meaning** of each public grant status and its audit lineage across the migration. Query speed and interface simplification are secondary.

No production launch may silently reinterpret a grant's canonical status. A representation change is allowed only when the authority responsible for status semantics has approved that exact semantic change or when the change is display-only and leaves the canonical API/export meaning intact.

SOURCE_RETURN: G-02

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

LOOKUPS_REMAINING: 0
```
