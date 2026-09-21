# Difficulty-Escalation Run Ledger 0.1.1

Date: 2026-09-21
Status: ACTIVE — FOUR RAW RETURNS / ADJUDICATIONS FROZEN
Governing docket: Issue #16
Supersedes: `DIFFICULTY_ESCALATION_RUN_LEDGER_0_1_0.md`

| Run | Provider | World | Condition | Raw frozen | E1 | E2 | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 |
|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| F-B-OPENAI-01 | OpenAI GPT-5.6 Sol High | F | B | YES | PASS | NEGATIVE | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| F-B-ANTHROPIC-01 | Claude Opus 5 High | F | B | YES | PASS | NEGATIVE | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| F-A-OPENAI-01 | OpenAI GPT-5.6 Sol High | F | A | YES | PASS | NEGATIVE | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| F-A-ANTHROPIC-01 | Claude Opus 5 High | F | A | YES | PASS | NEGATIVE | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |

```text
PLANNED_RUNS = 24
RAW_RESPONSES_FROZEN = 4
VALID_ADJUDICATED_RUNS = 4
COMPLETED_RUNS = 4
E1_PASS = 4
E1_FAIL = 0
E2_POSITIVE = 0
E3_ASSIGNMENTS = 0
```

E3 remains unassigned until all A/B/C/D responses for the corresponding world/provider pair are frozen.

Both F-A baselines pass E1. Under the preregistered E3 rule this makes `BASELINE_CEILING` the eventual F/provider repair tier if the remaining F conditions do not invalidate the pair, but the formal E3 assignment remains deferred until F-C and F-D are frozen.

## Next frozen runs

OpenAI seeded order next: `D-D` using `difficulty-runs/RUN_D_D_0_1_1.md`, Git blob `0a4b772b26e9219a973b8b21daf6b3caaffb9fe5`.

Anthropic seeded order next: `D-D` using the same packet and blob.

Each must use a separate genuinely fresh context.
