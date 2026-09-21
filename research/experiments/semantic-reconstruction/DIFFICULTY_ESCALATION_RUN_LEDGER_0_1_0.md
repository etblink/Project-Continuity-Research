# Difficulty-Escalation Run Ledger 0.1.0

Date: 2026-09-21
Status: ACTIVE — RAW RETURNS AND ADJUDICATIONS FROZEN
Governing docket: Issue #16

| Run | Provider | World | Condition | Raw frozen | E1 | E2 | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| F-B-OPENAI-01 | OpenAI GPT-5.6 Sol High | F | B | YES | PASS | NEGATIVE | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| F-B-ANTHROPIC-01 | Claude Opus 5 High | F | B | YES | PASS | NEGATIVE | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |

```text
PLANNED_RUNS = 24
RAW_RESPONSES_FROZEN = 2
VALID_ADJUDICATED_RUNS = 2
COMPLETED_RUNS = 2
E1_PASS = 2
E1_FAIL = 0
E2_POSITIVE = 0
E3_ASSIGNMENTS = 0
```

E3 remains unassigned until all A/B/C/D responses for the corresponding world/provider pair are frozen.

## Next frozen runs

OpenAI order next: `F-A` using `difficulty-runs/RUN_F_A_0_1_1.md`, Git blob `f53983608ec766be789d395d8af8cee9146115d4`.

Anthropic order next: `F-A` using the same packet, Git blob `f53983608ec766be789d395d8af8cee9146115d4`.

Each must use a separate genuinely fresh context.
