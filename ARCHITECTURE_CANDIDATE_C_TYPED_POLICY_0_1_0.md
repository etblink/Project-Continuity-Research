# Candidate C — Typed State Machine / Policy Gate 0.1.0

Status: PURE CANDIDATE

## Core idea

Project continuity is modeled as typed states and explicit guarded transitions.
Actions are commands that must satisfy evidence, authority, phase, and safety
predicates before a state change is accepted.

Illustrative transition:

```text
FROM: FUNCTIONAL_REMEDIATION_ACCEPTED
ACTION: START_ASTRA_REGRESSION
REQUIRES:
  VISUAL_GATE == PASS
  EXACT_HEAD_PROVENANCE == VERIFIED
  AUTHORITY includes PROJECT_LEAD
TO: ASTRA_REGRESSION_AUTHORIZED
```

A legitimate hold can be first-class:

```text
STATE: WAITING_FOR_EVIDENCE
REOPEN_IF: MATERIAL_NEW_EVIDENCE_TRIGGER
```

## Native strengths

This paradigm directly addresses Transition Drift.

It is excellent at representing:

- legal next states;
- forbidden transitions;
- hold/wait states;
- preconditions;
- authorization;
- environmental safety checks;
- exit conditions;
- separation of selected/preregistered/executed/adjudicated.

It also makes negative knowledge operational rather than passive:

```text
ROUTE_CLOSED
until
REOPEN_PREDICATE == TRUE
```

## Native weaknesses

Pure state machines tend to flatten rich epistemic meaning into state labels and
guards. They are not naturally good at:

- why a claim is believed;
- evidence lineage;
- historical artifact provenance;
- partial supersession across many claims;
- competing interpretations;
- reconstructing nuanced scientific justification;
- representing a large evolving knowledge graph.

The machine can know that a transition is blocked because `GATE_X == FAIL`
without retaining the full provenance that makes `GATE_X` credible.

It also needs an external history mechanism if prior states and decisions must
remain independently auditable.

## Historical replay expectation

Candidate C naturally catches:

- functional success without visual authorization;
- selection without preregistration;
- occupied deployment target;
- evidence-triggered hold;
- succession safeguards without exit criteria, if those criteria are encoded.

It is weaker on:

- wrong repository evidence;
- partial claim supersession;
- historical/current provenance recovery;
- evidence-to-disposition misclassification unless the disposition rules are
  formalized in advance.

## Critical architectural risk

A beautifully enforced state machine can enforce the wrong model of reality.

Control correctness depends on epistemic correctness of the state and guards.

## Best role if not selected as the core

A typed transition/policy layer is a strong candidate for the **action-control
plane** of a composite system.
