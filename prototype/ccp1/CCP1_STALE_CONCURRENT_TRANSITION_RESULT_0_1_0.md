# CCP-1 Stale / Concurrent Transition Result 0.1.0

Date: 2026-09-20  
Status: **COMPLETE — P1 CONCURRENCY SLICE SURVIVES INITIAL BOUNDED ATTACK**

## Frozen implementation under adjudication

```text
IMPLEMENTATION_COMMIT =
59dc31b57654c99b0153d44912568736121bebef

prototype/ccp1/concurrency.py
blob 329064c45f5b75a6fa96c8b0de91c2ea1599ceb5

prototype/ccp1/tests/test_concurrency.py
blob b86d9fae5382c68f7a5d9987308482f2e4afbf01
```

## Preregistered disposition

The slice satisfies:

```text
C — PASS WITH BOUNDED SCOPE
```

for the semantic single-ledger concurrency model.

## Mechanism

A material transition request is now bound to a decision snapshot:

```text
SUBJECT REVISION
ACTIVE POLICY DIGEST
AUTHORITY DIGEST
UNIQUE COMMAND ID
```

The current canonical state is rechecked at acceptance time.

## Injected failures detected

1. Two actors planning from the same subject revision cannot both commit.
2. Two conflicting valid transitions cannot both become canonical.
3. Exact accepted-command retry does not create a duplicate transition.
4. Reusing a command ID for different semantics is rejected.
5. Authority revocation after planning invalidates the earlier snapshot.
6. A mismatched policy digest invalidates the earlier snapshot.
7. An ABA cycle (CANDIDATE -> HELD -> CANDIDATE) is still detected as stale
   because revision identity is stronger than state-label equality.

## Positive controls

1. The first valid fresh command succeeds.
2. Either conflicting transition may win depending on canonical acceptance
   order; the loser becomes stale rather than silently merging.
3. Exact retry of the winner is idempotent.
4. An unrelated subject may still advance using its own unchanged snapshot.

That final control prevents an over-broad global compare-and-swap model from
turning unrelated project activity into artificial serialization.

## Verification

Bounded local verification against the exact committed blobs:

```text
CCP0_REGRESSION_SUITE     = 27 / 27 PASS
CCP1_EXISTING_SUITES      = 16 / 16 PASS
CCP1_CONCURRENCY_SUITE    =  9 /  9 PASS

TOTAL                     = 52 / 52 PASS
FAIL                      = 0
ERROR                     = 0
```

## What this establishes

Within one canonical semantic ledger:

> A transition planned from valid earlier state does not retain an unconditional
> right to execute after decision-critical state changes.

The control plane now distinguishes planning validity from acceptance-time
validity.

It also establishes a bounded idempotency rule:

```text
SAME COMMAND ID + SAME SEMANTICS
→ return the already accepted transition

SAME COMMAND ID + DIFFERENT SEMANTICS
→ reject
```

## What this does not establish

This is not distributed consensus.

Still open:

- database transaction isolation;
- multi-process atomicity;
- network partitions;
- crash recovery between state event and policy-binding event;
- Byzantine writers;
- durable command-record storage;
- cross-ledger transactions;
- concurrent policy replacement;
- cryptographically authenticated authority changes.

The current test models sequential interleavings that stand in for concurrent
actors sharing one canonical acceptance point.

## Disposition

```text
P1_STALE_CONCURRENT_TRANSITIONS = C__PASS_WITH_BOUNDED_SCOPE
CCP0_REGRESSION = PASS
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED

NEXT_P1_ATTACK = KERNEL_OMISSION
```
