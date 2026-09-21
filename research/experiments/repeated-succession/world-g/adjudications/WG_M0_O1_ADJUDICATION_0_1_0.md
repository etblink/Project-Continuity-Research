# World G — WG-M0-O1 Adjudication 0.1.0

Date: 2026-09-21
Status: FROZEN ADJUDICATION
Run: `WG-M0-O1`
Provider: OpenAI GPT-5.6 Sol High
Private condition: Y
Raw-freeze commit: `d44b26303e98331a243ff40a079e3ac1f0901333`
Raw SHA-256: `15ba473a8977af68134d17443dcfa9a721cf2b5e3b5218920eb525568a731768`

## Scores

| Measure | Score | Adjudication |
|---|---:|---|
| M1 factual reconstruction | 2 | All decision-relevant facts are correctly recovered, including the two G-06 remediation items, scoped `Merged` approval, protected appeal-open meaning, and shadow-search status. |
| M2 authority reconstruction | 2 | The Registry Steward is correctly identified as semantic authority; Migration, Search, and Communications limits are reconstructed without leakage. |
| M3 current / superseded / scoped status | 2 | Correctly distinguishes the rejected canonical `Closed` mapping, current approved appeal-open UI handling, scoped duplicate exception, unchanged ineligible records, and current non-authoritative search state. |
| M4 unfinished obligations / negative constraints | 2 | The response preserves both explicit G-06 corrections, the search admission gate, and the anti-global communications bound. |
| M5 relational integration | 2 | The central rule is stated explicitly: continue from the latest scoped Steward approval while preserving all earlier rules not expressly changed. This correctly binds authority, scope, temporal update, and purpose. |
| M6 next-action fidelity | 2 | The proposed tranche applies `Merged` only to qualifying records, repairs the faulty appeal-open UI batch, and re-runs reconciliation without touching other semantics. This matches the frozen faithful family. |
| M7 confidence calibration | 2 | The response distinguishes settled semantic rules from future cases requiring new authority and does not overclaim missing operational details. |
| M8 clarification calibration | 2 | It explicitly says no new clarification is needed before beginning the bounded remediation. Future ambiguity about non-qualifying records is correctly left outside the current authorized change. |

## Endpoint

```text
ACTION_PASS = YES
M6 = 2
QUALIFYING_MILTON_RESIDUAL = NO_FOR_THIS_RUN
WEAK_MILTON_DEGRADATION = NO_FOR_THIS_RUN
PROVIDER_PAIR_ENDPOINT = PENDING_MATCHED_CLEAR_RUN
```

Because M6=2, this run cannot satisfy the preregistered qualifying relational residual.
