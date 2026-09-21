# Difficulty-Escalation Run Ledger 0.1.10

Date: 2026-09-21
Status: ACTIVE — TWENTY-TWO RAW RETURNS / ADJUDICATIONS FROZEN
Governing docket: Issue #16
Supersedes: `DIFFICULTY_ESCALATION_RUN_LEDGER_0_1_9.md`

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
| D-B-ANTHROPIC-01 | Claude Opus 5 High | D | B | YES | PASS | NEGATIVE | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| E-A-OPENAI-01 | OpenAI GPT-5.6 Sol High | E | A | YES | PASS | NEGATIVE | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |

```text
PLANNED_RUNS = 24
RAW_RESPONSES_FROZEN = 22
VALID_ADJUDICATED_RUNS = 22
COMPLETED_RUNS = 22
E1_PASS = 22
E1_FAIL = 0
E2_POSITIVE = 0
E3_ASSIGNMENTS = 5
```

Formal E3 assignments:
- F / Anthropic = `BASELINE_CEILING`.
- D / OpenAI = `BASELINE_CEILING`.
- F / OpenAI = `BASELINE_CEILING`.
- D / Anthropic = `BASELINE_CEILING`.
- E / OpenAI = `BASELINE_CEILING`.

## Final seeded runs

OpenAI seeded order final run: `E-D` using `difficulty-runs/RUN_E_D_0_1_1.md`, Git blob `a067b7c9a4aa7d15517b5cd6f4fc038d650f0ca1`.

Anthropic seeded order final run: `E-A` using `difficulty-runs/RUN_E_A_0_1_1.md`, Git blob `2a9c1ec50da17a9d2485e26f1e5f3a9efa138c3a`.

Each must use a separate genuinely fresh context and only its provider-specific packet. No headline interpretation until both final raw responses are frozen and adjudicated.
