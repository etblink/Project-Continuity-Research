# CCP-1 Accepted-Event Correction Attack 0.1.0

Date: 2026-09-20  
Status: **PREREGISTERED — NOT YET ADJUDICATED**

## Question

CCP-0 treats accepted events as durable history.

That is desirable for auditability, but creates a difficult case:

> What happens when an already accepted event is later shown to be wrong?

Deleting or rewriting the event destroys provenance.

Leaving it fully authoritative preserves a known falsehood.

## Hypothesis under attack

A continuity architecture needs a distinction between:

```text
HISTORICALLY_ACCEPTED
```

and:

```text
CURRENTLY_EFFECTIVE / CURRENTLY_TRUSTED
```

without mutating the original ledger entry.

The first bounded correction model focuses on accepted claim events.

## Correction states under test

For an accepted claim event:

```text
ACCEPTED
DISPUTED
INVALIDATED
```

Semantics:

- `ACCEPTED`: eligible for effective current claim projection.
- `DISPUTED`: preserved and visible, but not safe to treat as settled.
- `INVALIDATED`: preserved in history but excluded from effective claim
  projection.

Invalidation must be an append-only correction event, not deletion.

## Injected failures

The attack will deliberately attempt to:

1. silently delete an accepted event;
2. invalidate an event without correction authority;
3. invalidate an event with no verified correction evidence;
4. invalidate an unknown event;
5. invalidate the same event twice;
6. continue treating a disputed latest claim as settled;
7. continue treating an invalidated latest claim as the effective current claim.

All must fail or produce the safe state.

## Positive controls

The prototype must demonstrate that:

1. disputing an accepted claim preserves the original event;
2. the current effective claim is marked unresolved while the dispute remains;
3. invalidating the disputed claim preserves it in history;
4. after invalidation, effective projection falls back to the most recent prior
   non-invalidated claim where one exists;
5. an independently accepted newer valid claim remains effective even if an
   older claim is later invalidated;
6. the correction event records:
   - target event sequence;
   - reason;
   - correcting authority;
   - verified correction evidence identities.

## Scope boundary

This first slice does **not** attempt universal retroactive dependency repair for
every event type.

It targets claim events because they allow the correction semantics to be tested
without pretending that arbitrary past transitions can always be "unapplied."

A later architecture may need dependency-aware quarantine for downstream events
that explicitly relied on an invalidated event.

## Preregistered dispositions

### A — FAIL

The system must either rewrite history or continue treating a known-invalid
claim as current.

### B — PARTIAL

History is preserved, but disputed/invalidated state does not reliably change
the effective current projection or correction evidence is not bound.

### C — PASS WITH BOUNDED SCOPE

The prototype:

- keeps the original accepted event immutable;
- records dispute/invalidation append-only;
- requires correction authority;
- requires verified correction evidence for invalidation;
- distinguishes disputed from invalidated;
- excludes invalidated claims from effective projection;
- falls back deterministically to a prior valid claim;
- preserves newer independent valid claims;
- preserves all earlier tests.

## Important limitation

Outcome C would **not** solve arbitrary causal rollback.

If later events depended on an invalidated event, they may need explicit
dependency tracking and quarantine rather than silent automatic reversal.

The safe conclusion of this slice can only be:

```text
CLAIM-LEVEL APPEND-ONLY CORRECTION SEMANTICS WORK
```

not:

```text
GENERAL EVENT ROLLBACK IS SOLVED
```

## Boundary

```text
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
LEDGER_EVENT_DELETION = FORBIDDEN
GENERAL_CAUSAL_ROLLBACK = OUT_OF_SCOPE
```
