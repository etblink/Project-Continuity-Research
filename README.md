# Project Observatory — Kernel Research Seed 0.1.0

Frozen: 2026-09-20

## Purpose

This packet preserves the initial design conversation that led to the idea of a
Project Kernel for Project Observatory and the projects it oversees.

It is intentionally a **research seed**, not yet a repository architecture,
governance standard, or implementation specification.

## Central research question

> What is the minimum durable information architecture necessary for a
> succession of intelligent but context-limited agents to preserve purpose,
> truth, state, and direction across arbitrarily long projects?

## Immediate design posture

Do not jump directly to implementing `PROJECT_KERNEL.md` files.

Preferred sequence:

1. Observe real long-horizon AI project failures.
2. Build a failure-mode taxonomy.
3. Derive requirements from those failures.
4. Study analogous solutions in adjacent fields.
5. Design competing architectures.
6. Adversarially test them.
7. Prototype on one project.
8. Run cold-start succession tests.
9. Propagate only after the architecture survives testing.

## Important limitation

This packet is not a guaranteed verbatim export of every ChatGPT turn.
`RESEARCH_SEED.md` is a canonical reconstruction of the ideas and decisions
reached in the conversation. The supplied Gemini conversation is preserved
unchanged in `sources/`.

For archival-grade preservation, a raw chat export can later be added as a
separate immutable source artifact.


## 0.1.1 update

Added `PRE_TAXONOMY_RESEARCH_CHARTER.md`, freezing the research objective and
the candidate Logos / Agape hypotheses before empirical incident mining begins.

## Incident corpus phase

The empirical incident phase began on 2026-09-20.

Current research artifacts:

- `INCIDENT_SCHEMA.md`
- `INCIDENT_CORPUS_0_1_0.md`
- `PROVISIONAL_FAILURE_DIMENSIONS_0_1_0.md`

The corpus is deliberately provisional. Early entries reconstructed from cross-chat history remain queued for transcript/artifact corroboration before any final taxonomy is frozen.


## Corroboration / positive-control pass

The first evidence-strengthening pass is now recorded in:

- `CORROBORATION_PASS_0_1_0.md`
- `COUNTEREXAMPLE_CORPUS_0_1_0.md`
- `METHODOLOGY_NOTE_0_1_0.md`

This pass promotes selected incident cores to artifact-corroborated `R2` while
keeping initiative attribution conservative until raw transcripts are archived.
It also introduces the distinction between **event evidence** and **initiative
evidence** for claims of AI/process self-correction.


## Edge-case pass

The next empirical pass is recorded in:

- `FAILED_SELF_CORRECTION_CORPUS_0_1_0.md`
- `SILENT_SUCCESS_CORPUS_0_1_0.md`
- `EDGE_CASE_SYNTHESIS_NOTE_0_1_0.md`

The pass distinguishes failures of metacognition from ordinary blindness and
examines bounded stretches where scaffolding appears to have prevented drift.
The emerging `reorientation surface` and `frame-preserving correction` concepts
remain research hypotheses, not frozen architecture.

## First empirical taxonomy

The targeted transition/authority/negative-knowledge pass and first provisional
taxonomy are now recorded in:

- `TARGETED_TRANSITION_AUTHORITY_NEGATIVE_KNOWLEDGE_PASS_0_1_0.md`
- `PROVISIONAL_EMPIRICAL_FAILURE_TAXONOMY_0_1_0.md`
- `TAXONOMY_READINESS_ASSESSMENT_0_1_0.md`

The current six provisional failure classes are Orientation Drift,
Epistemic-State Drift, Authority Drift, Transition Drift, Negative-Knowledge
Loss, and Metacognitive Drift. These are research classifications, not yet an
architecture or Project Kernel specification.


## Cross-discipline comparison

The first external comparison pass is recorded in:

- `EXTERNAL_SOURCE_REGISTER_0_1_0.md`
- `ADJACENT_FIELDS_COMPARATIVE_REVIEW_0_1_0.md`
- `CROSS_DISCIPLINE_TRANSFER_MATRIX_0_1_0.md`
- `POST_LITERATURE_REQUIREMENTS_0_1_0.md`
- `CROSS_DISCIPLINE_SYNTHESIS_0_1_0.md`

The review compares the empirical taxonomy with hierarchical planning, event
sourcing, provenance, distributed systems, safety/control engineering,
organizational memory, cognitive science, mission intent, and current LLM agent
memory/planning/reflection research.

The most important refinement is that a future Project Kernel is now treated as
a candidate **auditable orientation projection**, not the sole source of truth.


## Architecture competition

The first controlled architecture competition is recorded in:

- `ARCHITECTURE_COMPETITION_CHARTER_0_1_0.md`
- `ARCHITECTURE_CANDIDATE_A_DOCUMENT_KERNEL_0_1_0.md`
- `ARCHITECTURE_CANDIDATE_B_EVENT_SOURCED_0_1_0.md`
- `ARCHITECTURE_CANDIDATE_C_TYPED_POLICY_0_1_0.md`
- `ARCHITECTURE_CANDIDATE_D_PROVENANCE_GRAPH_0_1_0.md`
- `ARCHITECTURE_REQUIREMENTS_SCORECARD_0_1_0.md`
- `ARCHITECTURE_ADVERSARIAL_REPLAY_MATRIX_0_1_0.md`
- `ARCHITECTURE_COMPOSITE_E_CONTROL_PLANE_0_1_0.md`
- `ARCHITECTURE_COMPETITION_RESULT_0_1_0.md`

No pure architecture covers the critical requirement set. The current prototype
candidate is Composite E, an event-sourced provenance control plane with guarded
transitions and a generated Project Kernel as an orientation projection rather
than the sole source of truth.


## CCP-0 semantic prototype

The first executable Composite-E prototype is in `prototype/ccp0/`.

It replays ten historical failure scenarios, includes counterfactual and
self-audit controls, tracks external-source freshness, and has completed a
read-only Project Observatory shadow trial.

The frozen decision is:

```text
CCP0_SEMANTIC_FEASIBILITY = PASS
CCP1_BOUNDED_RESEARCH_PROTOTYPE = AUTHORIZED
LIVE_PROJECT_CONTROL_PLANE_INTEGRATION = NOT_AUTHORIZED
```

See the prototype experiment report, limitation/attack register, and advancement
decision in that directory.

## License

Unless otherwise noted, this repository is licensed under the Apache License,
Version 2.0. See `LICENSE`.
