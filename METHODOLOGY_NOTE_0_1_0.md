# Methodology Note 0.1.0 — Event Evidence vs Initiative Evidence

Date: 2026-09-20

## Trigger

The first corroboration/counterexample pass exposed a measurement problem.

A repository artifact can prove that a correction happened, but it often
cannot prove **who noticed the problem first**.

For example:

- a commit can prove that a fail-closed deployment gate was added;
- an issue can prove that functional readiness and visual readiness were
  separated;
- a method file can prove that a governance invariant was revised.

None of those facts, by themselves, prove that the AI independently noticed
the problem before a human prompted the correction.

## Rule

For positive controls and self-correction claims, track two evidence fields:

```text
EVENT_EVIDENCE
INITIATIVE_EVIDENCE
```

### EVENT_EVIDENCE

Uses the existing R0–R4 ladder and answers:

> How strongly can we establish that the correction, refusal, or safety action
> actually occurred?

### INITIATIVE_EVIDENCE

Uses the same ladder but answers:

> How strongly can we establish that the AI/process initiated the corrective
> move without the human first supplying the specific correction?

## Why this matters

Without this split, a successful outcome can be falsely interpreted as agent
metacognition when it was actually human rescue.

Conversely, failing to track initiative can hide genuine examples where a
well-designed governance scaffold caused the AI/process to catch its own drift.

## Provisional consequence

The research should distinguish at least three positive-control types:

1. `HUMAN_RESCUE` — human detects the specific failure first.
2. `SCAFFOLDED_SELF_CORRECTION` — a designed review/gate/process causes the
   AI/process to detect or block the failure.
3. `UNSCAFFOLDED_SELF_CORRECTION` — the AI independently reframes or catches the
   issue without an obvious external gate.

The third category should be claimed conservatively.

No architectural preference is frozen by this note.
