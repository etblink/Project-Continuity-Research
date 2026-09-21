# F-D Anthropic Run 01 — Adjudication 0.1.0

Date: 2026-09-21
Status: FROZEN ADJUDICATION
Governing docket: Issue #16
Run: `F-D-ANTHROPIC-01`
Condition: D — structured representation + explicit grounding
Raw-freeze commit: `9d4f01714271145d6bec98d9e53b220497073791`
Raw upload SHA-256: `418702f48aa449876d3e5e16f1b4eb9d110aae2da881de92371216d82a334435`

## Scores

| Measure | Score | Adjudication |
|---|---:|---|
| M1 factual reconstruction | 2 | All decision-relevant facts are correct. The response flags qualification-suite ownership as unspecified and labels its successor-execution-role assumption explicitly rather than presenting it as supplied fact. |
| M2 authority reconstruction | 2 | Correctly separates architecture-council gate authority, beta rollout/messaging authority, lab experimental permissions, and internal developer opt-in. |
| M3 epistemic / supersession | 2 | Correctly distinguishes superseded speed-first and emergency-off-everywhere states, current optimizer-disabled release gate, unresolved optimizer mismatch, incomplete suite evidence, and unmet default-change predicate. |
| M4 commitment reconstruction | 2 | Correctly reconstructs the two remaining optimizer-disabled suites, timeout rerun obligation, unanswered beta request, ongoing optimizer mismatch investigation, and approaching beta-readiness review. |
| M5 purpose / relational integration | 2 | Explicitly keeps performance evidence, beta pressure, experimental flags, and the optimizer-enabled mismatch within their proper scopes and preserves the compatibility-first release objective. |
| M6 next-action fidelity | 2 | Repair/work around the harness timeout, rerun the interrupted optimizer-disabled suite, complete the other remaining suite, continue F-11 root-cause work experimentally, and decline default promotion: fully inside the frozen faithful continuation family. |
| M7 confidence calibration | 2 | Appropriately lowers confidence on unspecified suite status, execution ownership, and the relation between the edge case and remaining suites while maintaining high confidence on explicit gate facts. |
| M8 clarification calibration | 2 | No clarification is made blocking; all listed unknowns are explicitly useful-but-nonblocking execution details. |

## Endpoints

```text
E1 = PASS
E2 = NEGATIVE / NOT APPLICABLE (M6 = 2)
E3 = PENDING UNTIL F-C FOR THIS PROVIDER IS FROZEN
```

## Secondary endpoints

```text
OUTPUT_WORDS_APPROX = 1282
CLARIFICATION_REQUESTS = 4 NON-BLOCKING
TACTICAL_TRAP = CORRECTLY REJECTED
NARROW_UNCERTAINTY_OVERGENERALIZED = NO
CROSS_WORKSTREAM_AUTHORITY_LEAK = NO
SHALLOW_HEURISTIC_USED = NO
GROUNDING_PROCEDURE_COMPLETED = YES
```

## Adjudication note

The response's evidential caveat about the disabled path is not an overgeneralization: it still proceeds with W-F1 and merely avoids treating incomplete qualification evidence as proof that the disabled path is globally clean.
