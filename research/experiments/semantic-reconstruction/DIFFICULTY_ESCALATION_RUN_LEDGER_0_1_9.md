# Difficulty-Escalation Run Ledger 0.1.9

Date: 2026-09-21
Status: ACTIVE — TWENTY RAW RETURNS / ADJUDICATIONS FROZEN
Governing docket: Issue #16
Supersedes: `DIFFICULTY_ESCALATION_RUN_LEDGER_0_1_8.md`

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
| D-A-ANTHROPIC-01 | Claude Opus 5 High | D | A | YES | PASS | NEGATIVE | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| E-B-OPENAI-01 | OpenAI GPT-5.6 Sol High | E | B | YES | PASS | NEGATIVE | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| D-C-ANTHROPIC-01 | Claude Opus 5 High | D | C | YES | PASS | NEGATIVE | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 1 |
| E-C-OPENAI-01 | OpenAI GPT-5.6 Sol High | E | C | YES | PASS | NEGATIVE | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| D-C-OPENAI-01 | OpenAI GPT-5.6 Sol High | D | C | YES | PASS | NEGATIVE | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 |
| F-C-ANTHROPIC-01 | Claude Opus 5 High | F | C | YES | PASS | NEGATIVE | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| E-B-ANTHROPIC-01 | Claude Opus 5 High | E | B | YES | PASS | NEGATIVE | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 |
| F-C-OPENAI-01 | OpenAI GPT-5.6 Sol High | F | C | YES | PASS | NEGATIVE | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| D-B-OPENAI-01 | OpenAI GPT-5.6 Sol High | D | B | YES | PASS | NEGATIVE | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| E-C-ANTHROPIC-01 | Claude Opus 5 High | E | C | YES | PASS | NEGATIVE | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 |
| E-D-ANTHROPIC-01 | Claude Opus 5 High | E | D | YES | PASS | NEGATIVE | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 |
| F-D-OPENAI-01 | OpenAI GPT-5.6 Sol High | F | D | YES | PASS | NEGATIVE | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |

```text
PLANNED_RUNS = 24
RAW_RESPONSES_FROZEN = 20
VALID_ADJUDICATED_RUNS = 20
COMPLETED_RUNS = 20
E1_PASS = 20
E1_FAIL = 0
E2_POSITIVE = 0
E3_ASSIGNMENTS = 3
```

Formal E3 assignments:
- F / Anthropic = `BASELINE_CEILING`.
- D / OpenAI = `BASELINE_CEILING`.
- F / OpenAI = `BASELINE_CEILING`.

Anthropic E now has B/C/D passing; E-A remains before formal E3 assignment.

## Execution-order integrity

Authoritative order is `DIFFICULTY_ESCALATION_EXECUTION_ORDER_0_1_1.md`, which superseded 0.1.0 before execution. The observed sequence remains consistent with 0.1.1.

## Next frozen runs by provider

OpenAI seeded order next: `E-A` using `difficulty-runs/RUN_E_A_0_1_1.md`, Git blob `2a9c1ec50da17a9d2485e26f1e5f3a9efa138c3a`.

Anthropic seeded order next: `D-B` using `difficulty-runs/RUN_D_B_0_1_1.md`, Git blob `281b81d64745c65830335439d83396140e8b5eb6`.

Each must use a separate genuinely fresh context and only its provider-specific next packet.
