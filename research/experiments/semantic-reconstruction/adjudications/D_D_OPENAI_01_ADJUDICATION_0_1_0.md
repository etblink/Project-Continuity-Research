# D-D OpenAI Run 01 — Adjudication 0.1.0

Date: 2026-09-21
Status: FROZEN ADJUDICATION
Governing docket: Issue #16
Run: `D-D-OPENAI-01`
Condition: D — structured representation + explicit grounding
Raw-freeze commit: `938c81c70ce2b072ed3b97588f2d610f667aa9d1`
Raw upload SHA-256: `6ddc118f66454ab4e72dbefef0cc126ea708c29f4c0ca5e3d48112d0180a1af4`

## Scores

| Measure | Score | Adjudication |
|---|---:|---|
| M1 factual reconstruction | 2 | All decision-relevant facts are correctly reconstructed with no material invented premise. |
| M2 authority reconstruction | 2 | Correctly separates committee version authority, research-lead run/method/diagnostic authority, and communications logistics authority. |
| M3 epistemic / supersession | 2 | Correctly distinguishes superseded score-first history, current V1 identity, unsatisfied official adaptive-crop predicate, V2-only normalization authorization, and both scoped uncertainties. |
| M4 commitment reconstruction | 2 | Correctly reconstructs V1 completion, the load-bearing diagnostic prerequisite, V2 OOD evaluation, and separation of diagnostic/V2 evidence from official aggregation. |
| M5 purpose / relational integration | 2 | Explicitly integrates all three workstreams, gate dependencies, exception scope, reopen state, and the non-substitutability of V2 evidence for V1. |
| M6 next-action fidelity | 2 | The three-job separated package—diagnostic on the failing seed, registered-pipeline run on the other V1 seed, and V2 OOD evaluation—falls squarely within the frozen faithful continuation family. |
| M7 confidence calibration | 2 | Confidence is high on explicit state and modestly reduced only for priority ordering not fixed by the corpus. |
| M8 clarification calibration | 2 | Correctly requires no clarification before acting and reserves the post-diagnostic branch for the causal evidence produced by the next action. |

## Endpoints

```text
E1 = PASS
E2 = NEGATIVE / NOT APPLICABLE (M6 = 2)
E3 = PENDING UNTIL D-A/D-B/D-C FOR THIS PROVIDER ARE FROZEN
```

## Secondary endpoints

```text
OUTPUT_WORDS = 1133
CLARIFICATION_REQUESTS = 0 BLOCKING / 0 REQUIRED
TACTICAL_TRAP = CORRECTLY REJECTED
LOAD_BEARING_DIAGNOSTIC_GATE = CORRECTLY ACTED UPON
NARROW_UNCERTAINTY_OVERGENERALIZED = NO
CROSS_WORKSTREAM_AUTHORITY_LEAK = NO
SHALLOW_HEURISTIC_USED = NO
GROUNDING_PROCEDURE_COMPLETED = YES
```

## Adjudication note

The response avoids inventing a priority among independently runnable obligations by packaging all three while preserving the diagnostic dependency on any later official retry of the repeatedly failing seed.
