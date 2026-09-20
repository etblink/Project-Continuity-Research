# CCP-1 Accepted-Event Correction Result 0.1.0

Date: 2026-09-20  
Status: **COMPLETE — SECONDARY CLAIM-CORRECTION SLICE SURVIVES INITIAL BOUNDED ATTACK**

## Frozen implementation under adjudication

```text
IMPLEMENTATION_COMMIT =
1700855dcc701c53aa2e3ae276288cca0a694a79

prototype/ccp1/correction.py
blob c1c1af53e3385da01e7b538361ec0fee43ea2ff1

prototype/ccp1/tests/test_correction.py
blob a278a86ddccc07d2bde34babc58c73aa4fb7aa75
```

## Preregistered disposition

```text
C — PASS WITH BOUNDED SCOPE
```

## Core result

The prototype now distinguishes:

```text
HISTORICALLY_ACCEPTED
```

from:

```text
CURRENTLY_EFFECTIVE / CURRENTLY_SETTLED
```

for accepted claim events.

The original event remains in the append-only ledger.

Later correction events may mark it:

```text
ACCEPTED
DISPUTED
INVALIDATED
```

without rewriting or deleting the original record.

## Injected failures detected

The bounded correction layer rejects:

1. mutation through the public immutable event view;
2. invalidation by an unauthorized actor;
3. invalidation without verified correction evidence;
4. invalidation of an unknown event;
5. repeat invalidation of the same event.

A disputed latest claim is no longer presented as settled.

An invalidated latest claim is excluded from the public effective claim
projection.

## Positive controls

The prototype demonstrates that:

1. disputing a claim preserves the original event in history;
2. the effective claim becomes explicitly unresolved while disputed;
3. invalidating the claim still preserves the original event;
4. after invalidation, the effective projection falls back to the most recent
   prior non-invalidated claim;
5. a newer independent valid claim remains current when an older claim is later
   invalidated;
6. correction records bind:
   - target event sequence;
   - correction reason;
   - correcting authority;
   - verified correction evidence digests.

## CI verification

GitHub Actions run:

```text
RUN_ID = 35537239554
HEAD = 1700855dcc701c53aa2e3ae276288cca0a694a79
JOB = 106148356074
CONCLUSION = success
```

Exact CI result:

```text
CCP0_REGRESSION_SUITE = 27 / 27 PASS
CCP1_ADVERSARIAL_SUITE = 60 / 60 PASS

TOTAL = 87 / 87 PASS
FAIL = 0
ERROR = 0
```

The accepted-event correction slice contributes 9 tests beyond the prior
51-test CCP-1 checkpoint.

## What this establishes

Within the claim-event boundary:

> **Auditability does not require a known falsehood to remain authoritative.**

A project can preserve the historically true statement:

```text
"this claim was accepted at event N"
```

while also preserving the later truth:

```text
"event N is disputed / invalid and no longer governs the effective claim"
```

This is preferable to both destructive history rewriting and permanent
institutionalization of a known error.

## What this does not establish

This slice does not solve arbitrary causal rollback.

If downstream actions explicitly depended on an invalidated event, safe repair
may require:

- dependency tracking;
- descendant quarantine;
- compensating transitions;
- human adjudication;
- domain-specific rollback semantics.

Therefore:

```text
CLAIM_LEVEL_APPEND_ONLY_CORRECTION = DEMONSTRATED
GENERAL_EVENT_ROLLBACK = NOT DEMONSTRATED
```

## Disposition

```text
SECONDARY_ACCEPTED_EVENT_CORRECTION = C__PASS_WITH_BOUNDED_SCOPE
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED

NEXT_SECONDARY_ATTACK =
AUTHORITY_DURABILITY_AND_IDENTITY_BOUNDARY
```
