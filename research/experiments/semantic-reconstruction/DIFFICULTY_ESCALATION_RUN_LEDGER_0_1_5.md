# Difficulty-Escalation Run Ledger 0.1.5

Date: 2026-09-21
Status: ACTIVE — TWELVE RAW RETURNS / ADJUDICATIONS FROZEN
Governing docket: Issue #16
Supersedes: `DIFFICULTY_ESCALATION_RUN_LEDGER_0_1_4.md`

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

```text
PLANNED_RUNS = 24
RAW_RESPONSES_FROZEN = 12
VALID_ADJUDICATED_RUNS = 12
COMPLETED_RUNS = 12
E1_PASS = 12
E1_FAIL = 0
E2_POSITIVE = 0
E3_ASSIGNMENTS = 0
HALFWAY_POINT = REACHED
```

E3 remains unassigned until all A/B/C/D responses for the corresponding world/provider pair are frozen.

Anthropic D now has A/C/D all passing; only D-B remains before its formal E3 assignment.

OpenAI E now has B/C passing; E-A/E-D remain.

## Next frozen runs by provider

OpenAI seeded order next: `D-C` using `difficulty-runs/RUN_D_C_0_1_1.md`, Git blob `cb92c2af13036592132b311456e99f9aed636a2c`.

Anthropic seeded order next: `F-C` using `difficulty-runs/RUN_F_C_0_1_1.md`, Git blob `0163d6a80019d34336a0bdd9458b7322362e3157`.

Each must use a separate genuinely fresh context and only its provider-specific next packet.
