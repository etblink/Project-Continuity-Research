# Candidate B — Event-Sourced State + Materialized Kernel 0.1.0

Status: PURE CANDIDATE

## Core idea

Durable project truth is represented as an append-only sequence of typed events.
Current state and the Project Kernel are derived projections.

Illustrative event sequence:

```text
PROJECT_CREATED
DOCTRINE_FROZEN
PHASE_OPENED
CLAIM_PROPOSED
EVIDENCE_BOUND
CLAIM_QUALIFIED
ROUTE_HELD
SUBCLAIM_SUPERSEDED
PHASE_CLOSED
NEXT_OPERATION_AUTHORIZED
```

The current kernel is regenerated from the event log plus projection rules.

## Native strengths

This architecture cleanly separates:

```text
WHAT HAPPENED
from
WHAT IS CURRENTLY TRUE / ACTIVE
```

It naturally preserves history without rewriting it, supports replay and
reconstruction, provides sequence identity, and can mark snapshots with the
exact event position from which they were generated.

Scoped supersession can be represented as an event targeting a specific claim
or subclaim rather than deleting an older artifact. Negative-knowledge states
can likewise be recorded as events such as:

```text
ROUTE_HELD(route_id, basis, reopen_predicate)
ROUTE_REOPENED(route_id, evidence_ref)
```

A stale kernel is detectable because the projection records its source event
sequence or revision.

## Native weaknesses

Event sourcing tells us **what occurred**, not automatically **what ought to be
allowed**.

A malformed but validly appended event such as:

```text
FIRST_CUSTOMER_AUTHORIZED
```

can still exist unless a separate command/policy layer rejects it.

Likewise, event sourcing does not by itself supply:

- a normative authority model;
- a rich evidence/provenance graph;
- project purpose;
- strategic/tactical separation;
- a rule for whether a reflective conclusion deserves promotion.

These semantics can be encoded in event schemas and projection logic, but pure
event sourcing has no intrinsic gatekeeper.

## Historical replay expectation

Candidate B is excellent for:

- historical/current separation;
- partial supersession;
- provenance of state changes;
- stale snapshot detection;
- negative-knowledge chronology.

It is only conditional for:

- phase authorization;
- unsafe mutation;
- evidence-to-disposition closure;
- human-agency limits.

## Critical architectural risk

The append-only log can become perfectly auditable while faithfully recording
bad transitions.

History integrity is not transition correctness.

## Best role if not selected as the core

A durable event ledger is a strong candidate for the historical spine of a
composite architecture, with current kernels generated as materialized views.
