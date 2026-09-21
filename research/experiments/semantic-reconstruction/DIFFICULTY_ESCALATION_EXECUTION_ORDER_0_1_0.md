# Difficulty-Escalation Heterogeneous Execution Order 0.1.0

Date: 2026-09-21
Status: FROZEN BEFORE FIRST SUCCESSOR RESULT
Governing docket: Issue #16

## Provider 1

OpenAI — GPT-5.6 Sol — High reasoning.

Frozen order:
1. F-D
2. F-A
3. F-C
4. D-C
5. E-A
6. D-D
7. D-A
8. E-B
9. E-D
10. F-B
11. D-B
12. E-C

## Provider 2

Anthropic — Claude Opus 5 — High reasoning.

Frozen order:
1. F-D
2. F-B
3. E-D
4. F-C
5. F-A
6. E-C
7. D-B
8. E-A
9. E-B
10. D-D
11. D-C
12. D-A

## Isolation rule

Every entry requires a new fresh context supplied with only its exact frozen packet.

The Claude construction-audit context is ineligible for any successor run.

No successor may see another condition, another successor answer, the reference key, adjudication commentary, or experiment interpretation.
