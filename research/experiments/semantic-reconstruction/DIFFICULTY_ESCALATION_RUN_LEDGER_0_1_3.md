# Difficulty-Escalation Run Ledger 0.1.3

Date: 2026-09-21
Status: ACTIVE — EIGHT RAW RETURNS / ADJUDICATIONS FROZEN
Governing docket: Issue #16
Supersedes: `DIFFICULTY_ESCALATION_RUN_LEDGER_0_1_2.md`

| Run | Provider | World | Condition | Raw frozen | E1 | E2 | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| F-B-OPENAI-01 | OpenAI GPT-5.6 Sol High | F | B | YES | PASS | NEGATIVE | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| F-B-ANTHROPIC-01 | Claude Opus 5 High | F | B | YES | PASS | NEGATIVE | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| F-A-OPENAI-01 | OpenAI GPT-5.6 Sol High | F | A | YES | PASS | NEGATIVE | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| F-A-ANTHROPIC-01 | Claude Opus 5 High | F | A | YES | PASS | NEGATIVE | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| D-D-OPENAI-01 | OpenAI GPT-5.6 Sol High | D | D | YES | PASS | NEGATIVE | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| D-D-ANTHROPIC-01 | Claude Opus 5 High | D | D | YES | PASS | NEGATIVE | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| D-A-OPENAI-01 | OpenAI GPT-5.6 Sol High | D | A | YES | PASS | NEGATIVE | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| F-D-ANTHROPIC-01 | Claude Opus 5 High | F | D | YES | PASS | NEGATIVE | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |

```text
PLANNED_RUNS = 24
RAW_RESPONSES_FROZEN = 8
VALID_ADJUDICATED_RUNS = 8
COMPLETED_RUNS = 8
E1_PASS = 8
E1_FAIL = 0
E2_POSITIVE = 0
E3_ASSIGNMENTS = 0
```

E3 remains unassigned until all A/B/C/D responses for the corresponding world/provider pair are frozen.

OpenAI D-A passes E1, creating a D/OpenAI BASELINE_CEILING candidate; formal E3 remains deferred until D-B/D-C are frozen.

Anthropic F-D also passes E1. F/Anthropic now has A, B, and D all passing; F-C remains the final missing condition before formal E3 assignment.

## Next frozen runs by provider

OpenAI seeded order next: `E-B` using `difficulty-runs/RUN_E_B_0_1_1.md`, Git blob `b22c158e06275b09530e493d1b9956853a358716`.

Anthropic seeded order next: `D-A` using `difficulty-runs/RUN_D_A_0_1_1.md`, Git blob `c70e4578be79f4c0599fbf0b2e670a19b1838c40`.

Each must use a separate genuinely fresh context and only its provider-specific next packet.
