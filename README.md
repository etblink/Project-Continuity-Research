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
