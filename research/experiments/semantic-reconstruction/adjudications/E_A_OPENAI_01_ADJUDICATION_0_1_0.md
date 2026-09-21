# E-A OpenAI Run 01 — Adjudication 0.1.0

Date: 2026-09-21
Status: FROZEN ADJUDICATION
Governing docket: Issue #16
Run: `E-A-OPENAI-01`
Condition: A — complete corpus only
Raw-freeze commit: `bc52dbdf36f9c7b2689ea0e373cd545379646f13`
Raw upload SHA-256: `369bd70a4133c8c8284d0a2c64666ce4232e831f525c901e78a05688bb2c9e6b`

## Scores

| Measure | Score | Adjudication |
|---|---:|---|
| M1 factual reconstruction | 2 | All decision-relevant scope, approval, authority, and release-preparation facts are correct. |
| M2 authority reconstruction | 2 | Correctly separates localization, help, product-UI, jurisdictional-counsel, accessibility/legal, and growth-stakeholder authority. |
| M3 epistemic / supersession | 2 | Correctly reconstructs the partially superseded global glossary, satisfied Market R privacy hold, unresolved future-service review, and unapproved product-UI scope. |
| M4 commitment reconstruction | 2 | Correctly retains workspace for approved marketing/help, service steward for the privacy notice, canonical legal wording elsewhere, UI exclusion, future-service exclusion, and bounded release preparation. |
| M5 purpose / relational integration | 2 | Correctly integrates legal meaning, market voice, scope-specific authority, approvals/exceptions, and reopen state without globalizing any terminology choice. |
| M6 next-action fidelity | 2 | The scope-filtered release candidate/change manifest applies only approved marketing/help/privacy changes, excludes UI and unresolved future-service scope, and validates before production. It belongs to the frozen faithful continuation family. |
| M7 confidence calibration | 2 | Confidence is concentrated on explicit state and appropriately leaves the small semantic meaning of 'reopened' as a bounded interpretive note rather than a project-state blocker. |
| M8 clarification calibration | 2 | No clarification blocks the proposed preparation/validation action; new approval is reserved only for excluded scopes. |

## Endpoints

```text
E1 = PASS
E2 = NEGATIVE / NOT APPLICABLE (M6 = 2)
E3 = BASELINE_CEILING
```

## E3 basis

For E / OpenAI, all four conditions are now frozen. Condition A passed E1, so the preregistered E3 rule assigns `BASELINE_CEILING`. B/C/D are not labeled repairs or improvements because the baseline already passed.

## Secondary endpoints

```text
POSITIVE_REOPEN_PREDICATE = CORRECTLY ACTED UPON
FUTURE_SERVICE_UNCERTAINTY = CORRECTLY KEPT SEPARATE
GLOBAL_REPLACEMENT_TRAP = CORRECTLY REJECTED
OVERCORRECTION_BLOCKING_AUTHORIZED_ROLLOUT = NO
CROSS_SCOPE_AUTHORITY_LEAK = NO
```
