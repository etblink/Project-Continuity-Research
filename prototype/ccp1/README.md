# CCP-1 — Adversarial Hardening Prototype

CCP-1 attacks the assumptions that survived CCP-0.

It remains read-only / shadow mode with respect to real projects.

## P1 attack sequence

1. authority spoofing — **complete: survived initial bounded attack**
2. bad-policy enforcement — **complete: disposition C, bounded pass**
3. stale / concurrent transitions — **complete: disposition C, bounded pass**
4. kernel omission
5. reopen-predicate brittleness

The CCP-0 prototype and its frozen 27-test suite remain unchanged under
`prototype/ccp0/` and serve as the regression baseline.

## Current verified checkpoint

```text
CCP0_REGRESSION_SUITE      = 27 / 27 PASS
CCP1_AUTHORITY_SUITE       =  7 /  7 PASS
CCP1_BAD_POLICY_SUITE      =  9 /  9 PASS
CCP1_CONCURRENCY_SUITE     =  9 /  9 PASS
TOTAL                      = 52 / 52 PASS

NEXT_P1_ATTACK = KERNEL_OMISSION
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
```

Frozen result artifacts:

- `CCP1_AUTHORITY_SPOOFING_RESULT_0_1_0.md`
- `CCP1_BAD_POLICY_RESULT_0_1_0.md`
- `CCP1_STALE_CONCURRENT_TRANSITION_RESULT_0_1_0.md`
