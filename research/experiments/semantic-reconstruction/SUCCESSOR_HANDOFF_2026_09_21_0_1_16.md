# PCR Successor Handoff — Semantic Reconstruction Horizon — 2026-09-21 — 0.1.16

Status: CURRENT SUCCESSOR CHECKPOINT — FINAL TWO RUNS
Branch: `research/pre-ccp2-continuity-horizon`
Governing docket: Issue #16

## Newly completed diverged runs

Anthropic: D-B
OpenAI: E-A

Raw first responses were frozen losslessly before adjudication at:
`bc52dbdf36f9c7b2689ea0e373cd545379646f13`

Anthropic D-B raw SHA-256:
`31f5c6e6e4dfad37cc8d7ab91ca8608a4913796e0cc264880ec41aafc2d6b5c4`

OpenAI E-A raw SHA-256:
`369bd70a4133c8c8284d0a2c64666ce4232e831f525c901e78a05688bb2c9e6b`

## Adjudication

Anthropic D-B:
`M1..M8 = 2,2,2,2,2,2,2,2`; E1 PASS; E2 NEGATIVE; E3 BASELINE_CEILING.

OpenAI E-A:
`M1..M8 = 2,2,2,2,2,2,2,2`; E1 PASS; E2 NEGATIVE; E3 BASELINE_CEILING.

Claude's diagnostic-first sequencing is explicitly covered by World D non-scoring latitude; it still completes the untouched seed and preserves all identity boundaries.

OpenAI E-A is a clean corpus-only baseline pass: it recognizes the satisfied privacy reopen, keeps UI/future-service scope separate, and proposes only a scope-filtered release candidate.

## Formal E3 assignments

F / Anthropic = `BASELINE_CEILING`.
D / OpenAI = `BASELINE_CEILING`.
F / OpenAI = `BASELINE_CEILING`.
D / Anthropic = `BASELINE_CEILING`.
E / OpenAI = `BASELINE_CEILING`.

## Aggregate counts

```text
PLANNED_RUNS = 24
COMPLETED_RUNS = 22
VALID_FROZEN_RAW_RETURNS = 22
E1_PASS = 22
E1_FAIL = 0
E2_POSITIVE = 0
E3_ASSIGNMENTS = 5
```

## Final valid evidence

OpenAI final run:
`E-D`
packet `difficulty-runs/RUN_E_D_0_1_1.md`
Git blob `a067b7c9a4aa7d15517b5cd6f4fc038d650f0ca1`.

Anthropic final run:
`E-A`
packet `difficulty-runs/RUN_E_A_0_1_1.md`
Git blob `2a9c1ec50da17a9d2485e26f1e5f3a9efa138c3a`.

Use one fresh OpenAI GPT-5.6 Sol High context with only E-D and one separate fresh Claude Opus 5 High context with only E-A.

Do not expose previous outputs/scores, the reference key, audit history, or experiment interpretation.

After both final responses are frozen and adjudicated, the 24-run corpus is complete and headline interpretation may begin under the preregistered rules.
