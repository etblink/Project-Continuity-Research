# Difficulty-Escalation Run Ledger 0.1.7

Date: 2026-09-21
Status: ACTIVE — SIXTEEN RAW RETURNS / ADJUDICATIONS FROZEN
Governing docket: Issue #16
Supersedes: `DIFFICULTY_ESCALATION_RUN_LEDGER_0_1_6.md`

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

```text
PLANNED_RUNS = 24
RAW_RESPONSES_FROZEN = 16
VALID_ADJUDICATED_RUNS = 16
COMPLETED_RUNS = 16
E1_PASS = 16
E1_FAIL = 0
E2_POSITIVE = 0
E3_ASSIGNMENTS = 1
```

Formal E3 assignments remain:
- F / Anthropic = `BASELINE_CEILING`.

OpenAI F now has A/B/C passing; F-D remains before formal E3 assignment.

OpenAI D now has A/C/D passing; D-B is next and will complete that quartet.

## Next frozen runs by provider

OpenAI seeded order next: `D-B` using `difficulty-runs/RUN_D_B_0_1_1.md`, Git blob `281b81d64745c65830335439d83396140e8b5eb6`.

Anthropic seeded order next: `E-C` using `difficulty-runs/RUN_E_C_0_1_1.md`, Git blob `a5e8d40c5ecd1fa683b28f65f2e213b955c1b854`.

Each must use a separate genuinely fresh context and only its provider-specific next packet.
