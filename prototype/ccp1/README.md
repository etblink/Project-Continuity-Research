# CCP-1 — Adversarial Hardening Prototype

CCP-1 attacks the assumptions that survived CCP-0.

It remains read-only / shadow mode with respect to real projects.

## P1 attack sequence

1. authority spoofing — **complete: survived initial bounded attack**
2. bad-policy enforcement
3. stale / concurrent transitions
4. kernel omission
5. reopen-predicate brittleness

The CCP-0 prototype and its frozen 27-test suite remain unchanged under
`prototype/ccp0/` and serve as the regression baseline.
