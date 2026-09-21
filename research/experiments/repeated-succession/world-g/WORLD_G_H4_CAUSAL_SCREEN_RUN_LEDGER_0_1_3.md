# World G — H4 Causal Screen Run Ledger 0.1.3

Date: 2026-09-21
Status: FINAL — 4 / 4 RUNS ADJUDICATED

| Order | Run | Provider | Condition | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 | Action |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | WG-M0-A1 | Anthropic Claude Opus 5 High | Y | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | PASS |
| 2 | WG-M0-O1 | OpenAI GPT-5.6 Sol High | Y | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | PASS |
| 3 | WG-M0-O2 | OpenAI GPT-5.6 Sol High | X | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | PASS |
| 4 | WG-M0-A2 | Anthropic Claude Opus 5 High | X | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | PASS |

```text
PLANNED_RUNS = 4
RAW_RESPONSES_FROZEN = 4
ADJUDICATED_RUNS = 4
ACTION_PASS = 4
M6_FAILURE = 0
QUALIFYING_MILTON_RESIDUAL_RUNS = 0
WEAK_MILTON_DEGRADATION_RUNS = 0
PROVIDER_PAIR_ENDPOINTS_COMPLETE = 2
OPENAI_PAIR = NO_M6_DEGRADATION
ANTHROPIC_PAIR = NO_M6_DEGRADATION
H4_CAUSAL_SCREEN = BASELINE_CEILING
```

Descriptive non-primary observation: Anthropic Y had M8=1 while Anthropic X had M8=2. This is not a preregistered action-fidelity endpoint and did not replicate in OpenAI.