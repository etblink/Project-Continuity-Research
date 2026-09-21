# Difficulty-Escalation Run Ledger 0.1.2

Date: 2026-09-21
Status: ACTIVE — SIX RAW RETURNS / ADJUDICATIONS FROZEN
Governing docket: Issue #16
Supersedes: `DIFFICULTY_ESCALATION_RUN_LEDGER_0_1_1.md`

| Run | Provider | World | Condition | Raw frozen | E1 | E2 | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| F-B-OPENAI-01 | OpenAI GPT-5.6 Sol High | F | B | YES | PASS | NEGATIVE | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| F-B-ANTHROPIC-01 | Claude Opus 5 High | F | B | YES | PASS | NEGATIVE | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| F-A-OPENAI-01 | OpenAI GPT-5.6 Sol High | F | A | YES | PASS | NEGATIVE | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| F-A-ANTHROPIC-01 | Claude Opus 5 High | F | A | YES | PASS | NEGATIVE | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| D-D-OPENAI-01 | OpenAI GPT-5.6 Sol High | D | D | YES | PASS | NEGATIVE | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| D-D-ANTHROPIC-01 | Claude Opus 5 High | D | D | YES | PASS | NEGATIVE | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |

```text
PLANNED_RUNS = 24
RAW_RESPONSES_FROZEN = 6
VALID_ADJUDICATED_RUNS = 6
COMPLETED_RUNS = 6
E1_PASS = 6
E1_FAIL = 0
E2_POSITIVE = 0
E3_ASSIGNMENTS = 0
```

E3 remains unassigned until all A/B/C/D responses for the corresponding world/provider pair are frozen.

## Next frozen runs by provider

OpenAI seeded order next: `D-A` using `difficulty-runs/RUN_D_A_0_1_1.md`, Git blob `c70e4578be79f4c0599fbf0b2e670a19b1838c40`.

Anthropic seeded order next: `F-D` using `difficulty-runs/RUN_F_D_0_1_1.md`, Git blob `3df5dec6393861ec94723fea2a88a5a89464797a`.

The provider queues now diverge. Each run must use a separate genuinely fresh context and only its provider-specific next packet.
