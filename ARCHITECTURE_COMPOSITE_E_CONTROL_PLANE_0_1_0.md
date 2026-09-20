# Composite E — Event-Sourced Provenance Control Plane 0.1.0

Status: DERIVED CANDIDATE — SELECTED FOR PROTOTYPE TESTING, NOT YET IMPLEMENTED

Working name only: **Continuity Control Plane (CCP)**.

The name is provisional and does not replace the broader public-project naming
research.

## 1. Derivation

The pure competition shows that no single paradigm covers the critical
requirements.

Composite E therefore combines only the mechanisms whose absence caused a
specific pure-candidate failure:

```text
A gives human-readable intent/orientation
B gives immutable event history + reproducible projections
C gives guarded transitions + hold/exit semantics
D gives provenance/authority/scoped supersession
```

The combination is not "put everything everywhere." Each layer has one primary
job.

## 2. Layer model

### Layer 0 — Human Intent / Doctrine

Human-readable, relatively stable statements of:

- project identity;
- North Star;
- human/community purpose;
- non-negotiable doctrine;
- human-agency boundaries.

This is the strongest home for the current Agape hypothesis.

### Layer 1 — Append-Only Event Ledger

Records accepted project-changing events.

Examples:

```text
PHASE_OPENED
CLAIM_PROPOSED
EVIDENCE_BOUND
CLAIM_QUALIFIED
ROUTE_HELD
SUBCLAIM_SUPERSEDED
TRANSITION_AUTHORIZED
TRANSITION_REJECTED
PHASE_CLOSED
```

Corrections append; they do not rewrite history.

### Layer 2 — Provenance / Authority Graph

Maintains typed relations among:

- claims;
- evidence;
- artifacts;
- events;
- agents;
- authorities;
- phases;
- routes;
- uncertainties;
- purposes.

Key edges include:

```text
SUPPORTED_BY
GENERATED_BY
AUTHORIZED_BY
GOVERNS
SUPERSEDES(scope)
CURRENT_INTERPRETATION_OF
BLOCKS
REOPENED_BY
SERVES_PURPOSE
```

This layer answers **why** a current state is justified and what exactly a later
artifact supersedes.

### Layer 3 — Typed State / Transition Policy

Defines legal transitions and their guards.

Illustrative policy object:

```text
transition: START_ASTRA_REGRESSION
from: FUNCTIONAL_ACCEPTED
requires:
  - VISUAL_GATE == PASS
  - EXACT_HEAD == VERIFIED
  - authority(PROJECT_LEAD)
produces: ASTRA_REGRESSION_AUTHORIZED
otherwise: HOLD
```

Negative knowledge is active here:

```text
route: FCP27
state: HELD
basis: no qualifying evidence trigger
reopen_if: named material evidence event + fresh preregistration
```

### Layer 4 — Current-State Projection

Deterministically/materially derives the current view from accepted events,
authority relations, and policy state.

It records its freshness identity:

```text
projection_event_seq
projection_graph_revision
policy_version
intent_version
computed_at
```

### Layer 5 — Project Kernel / Orientation Projection

The Kernel becomes a compact human-readable and machine-readable view, not the
source of truth.

It should answer:

```text
What is this project for?
Where are we?
What is authoritative now?
What evidence establishes that?
What is uncertain?
What is held or forbidden?
What would reopen it?
What is the next authorized operation—or why should we wait?
What must not be lost during the next operation?
```

A stale kernel can be detected because its projection revision no longer
matches the underlying state.

### Layer 6 — Execution Contract

A tactical worker receives only the bounded context needed for the current
operation, including:

- macro anchor;
- current authorized transition;
- scope;
- negative constraints;
- evidence required for completion;
- exit condition.

### Layer 7 — Return / Verification Capsule

Workers do not directly rewrite canonical state merely because they report
success.

A return capsule contains candidate observations/results plus evidence refs.
The control plane then decides which events/transitions are justified.

This preserves:

```text
WORKER CLAIM
!=
CANONICAL PROJECT STATE
```

## 3. Reorientation surfaces

Composite E introduces deliberate control points where the active frame is
reconstructed from durable state.

Candidate surfaces:

### Successor bootstrap
Before work begins.

### Pre-transition gate
Before any material promotion, external effect, or phase change.

### Post-result adjudication
Before worker output becomes canonical state.

### Phase-exit review
Before next-phase activation.

### Staleness / contradiction trigger
Whenever current projection conflicts with authoritative evidence.

### Safeguard exit check
Whenever reconstruction, quarantine, cleanup, or review risks becoming its own
open-ended process.

## 4. Negative knowledge object

A first-class negative-knowledge record should minimally contain:

```text
id
subject / route
state = HELD | REJECTED | EXHAUSTED | FORBIDDEN
basis
scope
authority
closed_at_event
reopen_predicate
reopen_evidence_types
expiry = optional
```

This makes "do not reopen" operational rather than mnemonic.

## 5. Scoped supersession object

A supersession relation should minimally contain:

```text
prior_claim_or_artifact
superseding_claim_or_artifact
scope
unaffected_prior_content
reason
effective_event
authority
```

Whole-object replacement is one allowed scope, not the default assumption.

## 6. Reflection / correction rule

Reflection does not write durable state directly.

A durable correction should normally require one or more of:

- new external evidence;
- deterministic replay;
- independent review;
- counterexample;
- violated invariant;
- changed result under a controlled intervention.

The exact burden can vary by project risk.

## 7. Human agency rule

The control plane may automate bounded transitions only where authority has
been explicitly delegated.

It must preserve a distinction between:

```text
SYSTEM MAY RECOMMEND
SYSTEM MAY EXECUTE
HUMAN APPROVAL REQUIRED
```

A public implementation should make this visible rather than burying it in
prompt text.

## 8. Profiles for public usability

The underlying model can support graduated complexity.

### Lite profile

For one human + a few AI sessions:

- intent/doctrine document;
- append-only decision/event log;
- generated kernel;
- negative-knowledge register;
- simple transition checklist.

### Project profile

Adds:

- typed claims/evidence;
- policy gates;
- scoped supersession;
- multiple workers;
- verification capsules.

### Observatory profile

Adds:

- cross-project dependency graph;
- multiple authority domains;
- portfolio routing;
- external triggers;
- project-level isolation/quarantine.

These profiles are hypotheses for later usability testing.

## 9. Main risk

Composite E is the strongest architectural candidate and the easiest to make
unusable.

Its dominant failure risk is **governance overcomplexity**.

Therefore the next prototype should not implement the entire architecture. It
should test the minimum mechanism set that distinguishes Composite E from the
failed pure candidates.

## 10. Prototype boundary

A first prototype should implement only:

```text
1. append-only event ledger
2. typed claim/state records
3. scoped supersession
4. negative-knowledge records with reopen predicates
5. guarded transitions
6. generated Project Kernel with freshness identity
7. return capsule → adjudication → accepted-event loop
```

It should **not** yet implement a generalized graph database, workflow engine,
web UI, agent framework, or multi-project deployment.

A simple file-backed reference model is sufficient for testing the semantics.
