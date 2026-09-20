# Candidate D — Provenance / Evidence Graph 0.1.0

Status: PURE CANDIDATE

## Core idea

Project continuity is represented as a typed graph of claims, artifacts,
evidence, agents, decisions, phases, authorities, and dependencies.

Illustrative nodes:

```text
Claim
Artifact
Evidence
Decision
Operation
Phase
Authority
HumanIntent
Route
Uncertainty
```

Illustrative edges:

```text
SUPPORTED_BY
CONTRADICTED_BY
GENERATED_BY
AUTHORIZED_BY
GOVERNS
DERIVED_FROM
SUPERSEDES(scope=...)
CURRENT_INTERPRETATION_OF
BLOCKS
REOPENED_BY
SERVES_PURPOSE
DEPENDS_ON
```

A Project Kernel is produced by querying the subgraph relevant to current
orientation.

## Native strengths

This is the strongest pure candidate for Authority Drift.

It naturally represents:

- provenance;
- multiple authority relations;
- partial/scoped supersession;
- historical versus current interpretations;
- evidence dependencies;
- contradictions;
- cross-project relationships;
- negative knowledge and reopen relations;
- exact reasons why a claim is current.

It also avoids forcing every project into one linear hierarchy when the actual
knowledge structure is many-to-many.

## Native weaknesses

A graph answers relational questions better than procedural ones.

Without a separate execution semantics it does not naturally stop an agent from
performing an unauthorized action. One can represent:

```text
ASTRA_REGRESSION BLOCKED_BY VISUAL_GATE
```

but the graph alone does not necessarily intercept the command that starts the
regression.

Likewise, graph consistency can become complex. Multiple edges may support
incompatible current-state queries unless policy determines precedence.

Human usability is also a serious adoption risk. A graph model that requires
specialized tooling can violate the public-generalization goal.

## Historical replay expectation

Candidate D is excellent for:

- wrong repository/source authority;
- partial supersession;
- historical provenance recovery;
- evidence-to-claim traceability;
- negative knowledge.

It is conditional for:

- phase transition gating;
- occupied-target mutation blocking;
- safeguard exit conditions;
- succession reconstruction stopping.

## Critical architectural risk

The system can become an exquisitely accurate map with no traffic laws.

## Best role if not selected as the core

A provenance/evidence graph is a strong candidate for the **epistemic authority
plane** of a composite architecture.
