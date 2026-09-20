# CCP-1 Orientation-Contract Quality Attack 0.1.0

Date: 2026-09-20  
Status: **PREREGISTERED — NOT YET ADJUDICATED**

## Question

The kernel-omission attack established:

```text
FRESH KERNEL != SUFFICIENT KERNEL
```

and introduced operation-scoped orientation contracts.

But that creates a higher-order risk:

> What prevents an under-specified orientation contract from certifying its own
> incomplete view?

A contract cannot be considered trustworthy merely because the generated kernel
satisfies every requirement the contract happened to declare.

## Hypothesis under attack

Orientation-contract admission should be tested against an **external review
policy**, not against a regression list chosen by the candidate contract itself.

The review policy should be:

- operation-scoped;
- versioned;
- provenance-bound;
- immutable under the same identity;
- able to encode known historical omission regressions and bounded anti-bloat
  checks.

## Bounded review model

The first review policy will test a release-oriented contract against known
decision-critical categories derived from the empirical program:

- current phase/state;
- governing policy identity;
- required authority;
- held external-effect / negative-knowledge route.

It will also include a bounded anti-bloat regression for a deliberately known
irrelevant requirement.

The review suite is intentionally small; this is a semantics test, not a claim
that the suite is complete.

## Injected failures

The attack will deliberately submit:

1. a contract missing required authority;
2. a contract missing held-route / negative knowledge;
3. a contract containing a known irrelevant requirement that the bounded review
   policy explicitly forbids;
4. a changed contract under the same ID/version;
5. a changed review policy under the same ID/version.

All must fail.

## Positive controls

The prototype must demonstrate that:

1. a contract covering the external review cases may be admitted;
2. the candidate contract cannot reduce the required review suite by declaring
   fewer regressions;
3. a genuinely new contract version may change requirements explicitly and is
   reviewed independently;
4. contract-review results are deterministic and bind:
   - contract digest;
   - review-policy digest;
   - per-case result;
5. the admitted contract remains usable by the operation-kernel generator.

## Preregistered dispositions

### A — FAIL

The candidate contract can effectively choose its own test suite, or a known
critical omission passes admission.

### B — PARTIAL

Known omissions are caught, but review-policy identity/provenance is mutable or
results are not reproducibly bound.

### C — PASS WITH BOUNDED SCOPE

The prototype:

- externally defines the review suite;
- rejects known under-broad and deliberately over-broad candidates;
- prevents silent contract/review-policy identity changes;
- admits the bounded good contract;
- produces deterministic review identity;
- preserves all earlier tests.

## Important limitation

Outcome C would not prove that the external review policy is complete.

The architecture would have moved the epistemic burden one level upward:

```text
WHO REVIEWS THE REVIEW POLICY?
```

That is intentional and must remain visible.

Blind successor trials, new incident discovery, and periodic adversarial review
must remain capable of adding regression cases.

The correct claim is only:

```text
ORIENTATION CONTRACT DOES NOT SELF-CERTIFY
```

not:

```text
ORIENTATION CONTRACT COMPLETENESS IS SOLVED
```

## Boundary

```text
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
BLIND_SUCCESSOR_VALIDATION = STILL_REQUIRED
```
