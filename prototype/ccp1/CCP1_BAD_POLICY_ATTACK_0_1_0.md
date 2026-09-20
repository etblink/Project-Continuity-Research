# CCP-1 Bad-Policy Enforcement Attack 0.1.0

Date: 2026-09-20  
Status: **PREREGISTERED — NOT YET ADJUDICATED**

## Question

CCP-0/CCP-1 can enforce transition guards consistently.

That creates a deeper risk:

> What if the policy itself is wrong?

A control plane that perfectly enforces a bad policy can become more dangerous
than an informal process because it gives the wrong rule mechanical authority.

## Hypothesis under attack

A policy must not be treated as correct merely because:

- it is syntactically valid;
- it has a familiar version label;
- its transition rules execute deterministically;
- its guards are internally consistent.

CCP-1 should distinguish:

```text
POLICY IDENTITY
POLICY VERSION
POLICY DIGEST
POLICY SOURCE / PROVENANCE
REGRESSION EVIDENCE
ACTIVE POLICY
```

and should prevent a policy from silently changing under an existing identity.

## Injected failures

The bounded attack will deliberately attempt to:

1. change policy semantics while keeping the same policy ID/version;
2. introduce a policy that drops a historically required gate
   (HiVenues-style functional acceptance -> visual hold);
3. activate a policy whose required historical regression fails;
4. activate a policy using an actor without policy-management authority;
5. register a policy with no authority/provenance source.

## Positive controls

The attack must also demonstrate that:

1. a genuinely new policy version may change semantics explicitly;
2. a policy that passes its required regression may activate;
3. an authorized policy manager may activate it;
4. a transition executed under an active policy records the exact policy
   ID/version/digest/source that governed it;
5. a policy change invalidates the freshness identity of a kernel generated
   before activation.

## Historical regression used in this slice

The first regression case is intentionally small and comes from the existing
corpus:

```text
STATE = FUNCTIONAL_ACCEPTED
visual_gate = FAIL

START_ASTRA must remain blocked.
```

A candidate policy that permits that transition fails the regression.

The paired positive case is:

```text
STATE = FUNCTIONAL_ACCEPTED
visual_gate = PASS

START_ASTRA may proceed, assuming authority requirements are also satisfied.
```

## Preregistered dispositions

### A — FAIL

The system cannot distinguish a changed policy under the same identity, or a
failed regression does not prevent activation.

### B — PARTIAL

Policy identity is immutable, but activation is not meaningfully tied to
regression evidence.

### C — PASS WITH BOUNDED SCOPE

The prototype:

- binds policy semantics to ID/version/digest/source;
- rejects silent semantic replacement;
- detects the deliberately bad policy with the preregistered regression;
- blocks activation after failed required regression;
- permits a passing policy under proper authority;
- records exact policy identity on resulting material transitions.

## Important limitation

Even outcome C would **not** prove policy correctness.

It would establish only:

> a candidate policy is explicit, versioned, provenance-bound, and required to
> survive named regressions before activation.

A bad or incomplete regression suite can still bless a bad policy. That higher
level of metacognitive/policy-review failure remains open.

## Boundary

This is a semantic adversarial prototype only.

```text
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
REAL_PROJECT_POLICY_REPLACEMENT = NOT_AUTHORIZED
```
