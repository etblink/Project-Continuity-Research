# CCP-1 Stale / Concurrent Transition Attack 0.1.0

Date: 2026-09-20  
Status: **PREREGISTERED — NOT YET ADJUDICATED**

## Question

CCP-1 now has explicit authority and explicit policy admission.

A remaining failure mode is temporal:

> What happens when two individually valid actors act from the same earlier
> state, or when authority/policy changes after an actor forms its plan but
> before the transition is accepted?

A state check performed only at planning time is insufficient.

## Hypothesis under attack

A material transition should be accepted only if the decision-critical state
the actor relied on still matches the canonical control plane at acceptance.

The first bounded concurrency model will test a transition snapshot containing:

```text
SUBJECT REVISION
ACTIVE POLICY DIGEST
AUTHORITY DIGEST
```

and a unique command identity.

## Injected failures

The attack will deliberately attempt to:

1. let two commands act from the same subject revision;
2. let two conflicting transitions from the same state both become canonical;
3. replay the same accepted command and create duplicate state-change events;
4. reuse a command ID for different semantics;
5. act from an authority snapshot after the relevant grant was revoked;
6. act with a mismatched/stale policy digest.

## Positive controls

The system must also demonstrate that:

1. the first valid command from a fresh snapshot succeeds;
2. exact retry of the same accepted command is idempotent rather than duplicated;
3. after refreshing state, a still-authorized operation may proceed if its
   current transition predicates remain satisfied;
4. a transition on an unrelated subject is not rejected merely because another
   subject changed.

The last control is important: a global event-sequence compare-and-swap would be
safe but unnecessarily paralyzing. CCP-1 should protect the state that matters
without making unrelated project progress invalidate every in-flight operation.

## Canonicalization rule under test

For a material transition:

```text
EXPECTED SUBJECT REVISION
+ EXPECTED POLICY DIGEST
+ EXPECTED AUTHORITY DIGEST
+ UNIQUE COMMAND ID
+ CURRENT TRANSITION GUARDS
+ CURRENT AUTHORITY
→ at most one accepted transition
```

If two conflicting requests share the same earlier subject revision, acceptance
of one must make the other stale.

This prototype does not attempt distributed consensus. It tests whether a
single canonical event ledger can prevent ambiguous acceptance under sequential
interleavings that represent concurrent actors.

## Preregistered dispositions

### A — FAIL

Two conflicting requests can both become canonical, or duplicate command replay
creates duplicate accepted transitions.

### B — PARTIAL

Subject staleness is detected, but authority/policy races or idempotent command
identity remain ambiguous.

### C — PASS WITH BOUNDED SCOPE

The prototype:

- rejects stale subject revisions;
- permits at most one conflicting transition from a shared prior revision;
- provides idempotent exact command replay;
- rejects command-ID semantic reuse;
- detects authority-snapshot invalidation after revocation;
- detects policy-digest mismatch;
- does not falsely stale unrelated subjects;
- preserves all earlier CCP-0/CCP-1 tests.

## Important limitation

Even outcome C would not establish a distributed consensus protocol.

The attack is limited to deterministic sequential interleavings over one
canonical semantic control plane. Network partitions, durable database
transactions, process crashes, multi-writer storage, and Byzantine actors remain
outside this slice.

## Boundary

```text
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
REAL_PROJECT_CONCURRENCY_CONTROL = NOT_AUTHORIZED
```
