# CCP-1 Current Orientation Projection Schema 0.1.0

Status: CANDIDATE REPAIR SCHEMA — HUMAN-ORIENTATION TRIAL

A current-orientation projection is a deliberately small, human-readable starting surface for an unfamiliar successor.

It is not canonical project state and must never become the sole source of truth.

## Required fields

1. Purpose / North Star
2. Current phase
3. Completed major gates
4. Remaining advancement gates
5. Architecture-candidate status
6. Explicit authorization / prohibition boundaries
7. Current bounded next operation
8. Machine-verification checkpoint
9. Open limitations / uncertainty
10. Evidence map linking each summary claim to durable source artifacts
11. Freshness identity:
   - source ref;
   - projection version;
   - source-artifact identities where practical.

## Required semantics

```text
ORIENTATION_PROJECTION != CANONICAL_STATE
SUMMARY != EVIDENCE
MACHINE_PASS != ACCEPTANCE
CURRENT_PHASE != NEXT_PHASE_AUTHORIZATION
CANDIDATE != FINAL_ARCHITECTURE
```

The projection should reduce orientation cost without concealing uncertainty or replacing exact evidence.
