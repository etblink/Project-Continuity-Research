# CCP-1 Project-Agnostic Portability Attack 0.1.0

Date: 2026-09-20  
Status: **PREREGISTERED — NOT YET ADJUDICATED**

## Question

CCP was derived largely from HiVenues, FCP, NFC, and Project Observatory
incidents.

That creates an overfitting risk:

> Are the emerging semantics actually project-agnostic, or do they merely look
> generic because the implementation uses generic class names around
> assumptions inherited from the source projects?

## Hypothesis under attack

The same unchanged semantic engine should be configurable for materially
different project vocabularies without adding domain-specific branches to CCP
core logic.

The first bounded portability test will instantiate profiles for:

1. software/product release;
2. scientific/research adjudication;
3. creative/editorial publication;
4. an opaque synthetic domain using intentionally meaningless identifiers.

## Portable profile surface

A profile may supply domain vocabulary for:

```text
PURPOSE
PHASE SUBJECT
FROM STATE
TO STATE
TRANSITION NAME
REQUIRED ACTION
AUTHORITY SCOPE
HELD ROUTE
HOLD BASIS
```

The core engine must continue to provide the same semantics for:

- authority/action/scope;
- policy identity;
- guarded state transition;
- held negative knowledge;
- operation-scoped orientation contract;
- kernel freshness and sufficiency.

Domain vocabulary belongs in profile data, not core conditionals.

## Injected failures

The attack will deliberately attempt:

1. a profile missing a required semantic field;
2. an unauthorized actor transition in each domain;
3. an orientation profile omitting the domain's held route;
4. cross-profile state leakage;
5. a profile whose opaque identifiers have no human semantic cues.

The opaque profile is important: success must not depend on recognizing words
such as `release`, `review`, `publish`, `evidence`, or `deployment`.

## Positive controls

The prototype must demonstrate that:

1. all four profiles use the same engine code;
2. each profile can establish authority, active policy, phase state, held route,
   and sufficient operation kernel;
3. authorized transitions work without modifying core implementation;
4. unauthorized transitions fail in every profile;
5. profile identity/digest is deterministic;
6. the opaque profile works despite semantically meaningless identifiers;
7. one profile's identifiers/state never appear in another profile's
   projection.

## Preregistered dispositions

### A — FAIL

At least one domain requires domain-specific core branching or the opaque
profile cannot operate.

### B — PARTIAL

Multiple domains work but orientation/authority/negative-knowledge semantics
still depend on source-project vocabulary.

### C — PASS WITH BOUNDED SCOPE

The unchanged generic engine executes all four profiles, including the opaque
control, with isolated state and identical semantic rules.

## Important limitation

Outcome C would not establish universal domain portability.

It would show only that the current semantics are not trivially tied to the
source-project vocabulary.

Further evidence still requires:

- independent projects not designed by this research program;
- unfamiliar users;
- domain-specific adapters;
- blind successor trials;
- projects whose authority/evidence models differ materially from Git-centric
  software/research workflows.

## Boundary

```text
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
UNIVERSAL_PORTABILITY_CLAIM = NOT_AUTHORIZED
```
