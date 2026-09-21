# Difficulty-Escalation Heterogeneous Execution Order 0.1.1

Date: 2026-09-21
Status: FROZEN BEFORE FIRST SUCCESSOR RESULT
Governing docket: Issue #16
Supersedes: DIFFICULTY_ESCALATION_EXECUTION_ORDER_0_1_0.md before execution

## Randomization method

Canonical run IDs before shuffling:
`D-A, D-B, D-C, D-D, E-A, E-B, E-C, E-D, F-A, F-B, F-C, F-D`

Each provider order was generated independently with Python's `random.Random(seed).shuffle` before any successor result was collected. The listed order is authoritative; the seeds are retained for reproducibility.

## Provider 1

OpenAI — GPT-5.6 Sol — High reasoning.

Seed: `11832696285084917107`

Frozen order:
1. F-B
2. F-A
3. D-D
4. D-A
5. E-B
6. E-C
7. D-C
8. F-C
9. D-B
10. F-D
11. E-A
12. E-D

## Provider 2

Anthropic — Claude Opus 5 — High reasoning.

Seed: `3242582560149794756`

Frozen order:
1. F-B
2. F-A
3. D-D
4. F-D
5. D-A
6. D-C
7. F-C
8. E-B
9. E-C
10. E-D
11. D-B
12. E-A

## Isolation rule

Every entry requires a new fresh context supplied with only its exact frozen packet.

The Claude construction-audit context is ineligible for any successor run.

No successor may see another condition, another successor answer, the reference key, adjudication commentary, or experiment interpretation.
