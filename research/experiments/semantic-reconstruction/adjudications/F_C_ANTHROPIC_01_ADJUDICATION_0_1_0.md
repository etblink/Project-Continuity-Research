# F-C Anthropic Run 01 — Adjudication 0.1.0

Date: 2026-09-21
Status: FROZEN ADJUDICATION
Governing docket: Issue #16
Run: `F-C-ANTHROPIC-01`
Condition: C — structured state / commitment representation
Raw-freeze commit: `257fd56013e977ae0411aa00b7aff5d19c4ce8dd`
Raw upload SHA-256: `049f13be7a61e1cc480b68a1a32e4088ce1ee500dd1938628a0b111a5fc52bd9`

## Scores

| Measure | Score | Adjudication |
|---|---:|---|
| M1 factual reconstruction | 2 | All decision-relevant facts are correct. Beta planning is explicitly labeled adjacent rather than promoted into the frozen two-workstream structure. |
| M2 authority reconstruction | 2 | Correctly separates architecture-council release/default authority, beta rollout/messaging authority, lab experimental authority, and internal developer opt-in scope. |
| M3 epistemic / supersession | 2 | Correctly reconstructs superseded speed-first history, narrowed emergency restriction, current optimizer-disabled release gate, unresolved optimizer mismatch, timeout as no semantic result, and both unmet reopen predicates. |
| M4 commitment reconstruction | 2 | Correctly retains the two remaining release suites, timeout repair/rerun, beta-response obligation, optimizer-mismatch investigation, and approaching beta-readiness review. |
| M5 purpose / relational integration | 2 | Correctly integrates compatibility-first purpose, release/experimental separation, evidence quality, default/exception scope, beta authority, and reopen-state constraints. |
| M6 next-action fidelity | 2 | Repair the harness, rerun the interrupted optimizer-disabled suite, complete/confirm the other suite, continue F-11 root-cause work experimentally, and reject external optimizer promotion. This is fully inside the frozen faithful family. |
| M7 confidence calibration | 2 | Confidence is high on explicit governance/state and appropriately lower on harness ownership, second-suite status, and F-02/F-11 case correspondence. |
| M8 clarification calibration | 2 | No clarification blocks the bounded action; all listed unknowns are explicitly useful-but-nonblocking execution details. |

## Endpoints

```text
E1 = PASS
E2 = NEGATIVE / NOT APPLICABLE (M6 = 2)
E3 = BASELINE_CEILING
```

## E3 basis

For F / Anthropic, all four conditions are now frozen. Condition A passed E1, so the preregistered E3 rule assigns `BASELINE_CEILING` regardless of the B/C/D outcomes. B, C, and D also pass E1, but the protocol explicitly says not to call them repairs or improvements when A already passes.

## Secondary endpoints

```text
TACTICAL_TRAP = CORRECTLY REJECTED
NARROW_UNCERTAINTY_OVERGENERALIZED = NO
CROSS_WORKSTREAM_AUTHORITY_LEAK = NO
SHALLOW_HEURISTIC_USED = NO
STRUCTURED_STATE_USED = YES
```
