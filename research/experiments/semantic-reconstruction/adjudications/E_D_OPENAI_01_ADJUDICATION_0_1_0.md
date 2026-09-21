# E-D OpenAI Run 01 — Adjudication 0.1.0

Date: 2026-09-21
Status: FROZEN ADJUDICATION
Governing docket: Issue #16
Run: `E-D-OPENAI-01`
Condition: D — structured representation + explicit grounding
Raw-freeze commit: `1087a6c68bc52c2ce2773690a1ae0dbab43e1cd9`
Raw upload SHA-256: `820a5ecf71476cc621d49ca14cf33c5cf66fbba5219423051ede55ff24becc7e`

## Scores

| Measure | Score | Adjudication |
|---|---:|---|
| M1 factual reconstruction | 2 | All decision-relevant scope, approval, release, and exception facts are correct. |
| M2 authority reconstruction | 2 | Correctly separates localization, help, product-UI, counsel, accessibility/legal, and growth authority. |
| M3 epistemic / supersession | 2 | Correctly treats the global glossary as partially superseded, the privacy reopen predicate as satisfied, the future-service review as narrowly unresolved, and product UI as explicitly unapproved. |
| M4 commitment reconstruction | 2 | Correctly retains all approved marketing/help/privacy terms, excluded UI/future-service scope, canonical legal wording elsewhere, and bounded release-package obligation. |
| M5 purpose / relational integration | 2 | Explicitly integrates purpose, authority, defaults/exceptions, reopen predicates, uncertainty scope, cross-workstream constraints, and a decision rule. |
| M6 next-action fidelity | 2 | The scope-filtered release manifest and non-production validation pass exactly implement the frozen faithful continuation family and reject global propagation. |
| M7 confidence calibration | 2 | Confidence is high on explicit state and implementation-time inventory questions are correctly kept outside policy uncertainty. |
| M8 clarification calibration | 2 | No clarification is required before the bounded action; inventory checks are execution-time verification rather than unresolved policy. |

## Endpoints

```text
E1 = PASS
E2 = NEGATIVE / NOT APPLICABLE (M6 = 2)
E3 = BASELINE_CEILING
```

## E3 basis

For E / OpenAI, E3 had already become `BASELINE_CEILING` when its A condition passed. This D run also passes, completing the quartet with all four E1 passes.

## Secondary endpoints

```text
GROUNDING_PROCEDURE_COMPLETED = YES
POSITIVE_REOPEN_PREDICATE = CORRECTLY_ACTED_UPON
FUTURE_SERVICE_UNCERTAINTY = CORRECTLY_KEPT_SEPARATE
GLOBAL_REPLACEMENT_TRAP = CORRECTLY_REJECTED
CROSS_SCOPE_AUTHORITY_LEAK = NO
```
