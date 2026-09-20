# CCP-1 Bad-Policy Enforcement Result 0.1.0

Date: 2026-09-20  
Status: **COMPLETE — P1 BAD-POLICY SLICE SURVIVES INITIAL BOUNDED ATTACK**

## Preregistered question

Can CCP-1 distinguish:

```text
A POLICY THAT IS CONSISTENTLY ENFORCED
```

from:

```text
A POLICY THAT IS JUSTIFIED TO GOVERN
```

and, in particular, prevent a changed or historically contradicted policy from
acquiring mechanical authority merely because it is syntactically valid?

## Frozen implementation under adjudication

```text
IMPLEMENTATION_COMMIT =
e0e1500a38edfb768486a0cdb7dc733d8029bce4

prototype/ccp1/policy.py
blob fd2cac9ba1397c68b418b29e958567ab194ac15c

prototype/ccp1/tests/test_bad_policy.py
blob 30ebd22ffdc8629c3657d1fb43b74a39949aa266
```

The preregistration remains preserved separately in:

```text
prototype/ccp1/CCP1_BAD_POLICY_ATTACK_0_1_0.md
```

and is not rewritten by this result.

## Result

The bounded attack satisfies preregistered disposition:

```text
C — PASS WITH BOUNDED SCOPE
```

The prototype now separates:

```text
POLICY ID
POLICY VERSION
POLICY DIGEST
AUTHORITY SOURCE
REQUIRED REGRESSIONS
ACTIVE POLICY
```

and prevents a policy from silently changing semantics while retaining the same
ID/version identity.

## Injected failures detected

### 1. Silent semantic replacement under the same identity

A second policy using the same:

```text
policy_id
version
```

but a different digest is rejected.

Result: PASS.

### 2. Deliberately bad policy drops a historically required gate

The attack policy removes the `visual_gate = PASS` requirement from the
HiVenues-style `START_ASTRA` transition.

Against the frozen regression:

```text
STATE = FUNCTIONAL_ACCEPTED
visual_gate = FAIL

START_ASTRA must remain blocked
```

the candidate policy fails.

Result: PASS.

### 3. Failed required regression cannot be activated

A candidate with a failed required regression remains inadmissible even when it
has a distinct explicit version.

Result: PASS.

### 4. Unprivileged policy activation

An actor without the required `ACTIVATE_POLICY` grant cannot activate a policy
that otherwise passes its regression.

Result: PASS.

### 5. Missing policy provenance

A policy with no `authority_source` cannot be registered.

Result: PASS.

## Positive controls

### Explicit new versions may change semantics

A genuinely new policy version may carry a different digest and different
semantics without being mistaken for the prior policy.

This does not authorize it; it merely gives the changed policy an honest new
identity.

Result: PASS.

### Passing policy may activate under proper authority

A policy that:

- has a distinct immutable identity;
- has a nonempty authority source;
- passes its required regression; and
- is activated by an appropriately granted actor

can become active.

Result: PASS.

### Valid transition remains possible

Under the admitted policy:

```text
STATE = FUNCTIONAL_ACCEPTED
visual_gate = PASS
```

permits `START_ASTRA`, assuming the authority requirement is also satisfied.

Result: PASS.

### Governing policy identity is bound to the transition

The accepted operation records the exact:

```text
policy_id
version
digest
authority_source
```

that governed the transition.

Result: PASS.

### Policy activation invalidates prior kernel freshness

A Project Kernel generated before policy activation is stale afterward because
the governing policy identity is part of the projection state/freshness
identity.

Result: PASS.

## Important hardening performed during the attack

The first implementation shape would have allowed a caller to record an
externally supplied boolean saying that a regression had passed.

That was rejected as too weak.

The hardened implementation instead evaluates the registered
`PolicyRegressionCase` against the candidate policy and records the result
itself.

Therefore:

```text
CALLER_SAYS_REGRESSION_PASS
!=
REGRESSION_PASS
```

The admission result is derived from the bounded regression evaluator.

## Verification result

The final bounded local verification associated with the implementation before
this result was frozen was:

```text
CCP0_REGRESSION_SUITE = 27 / 27 PASS
CCP1_AUTHORITY_SUITE  =  7 /  7 PASS
CCP1_BAD_POLICY_SUITE =  9 /  9 PASS

TOTAL                 = 43 / 43 PASS
FAIL                   = 0
ERROR                  = 0
```

## What this establishes

Within the CCP-1 semantic prototype boundary:

> **Policy identity is not policy correctness, and deterministic enforcement is
> not sufficient evidence of policy legitimacy.**

A candidate policy now has to be:

1. explicitly identified;
2. content-bound by digest;
3. provenance-bound;
4. tested against named required regressions;
5. activated by an authorized actor.

This directly addresses the CCP-0 limitation that a typed transition system
could faithfully enforce the wrong model of reality.

## What this does not establish

Outcome C does **not** mean:

```text
POLICY_CORRECTNESS = SOLVED
```

Open limitations remain:

- a regression suite can itself be incomplete or wrong;
- regression selection is still a higher-order governance decision;
- policy provenance is recorded, not cryptographically authenticated;
- one historical regression is intentionally insufficient evidence of broad
  correctness;
- this prototype does not yet model concurrent policy activation;
- policy migration and replacement semantics are intentionally deferred;
- the policy engine has not been tested at realistic rule-graph scale;
- a malicious in-process caller remains outside this semantic threat model.

The result establishes disciplined **admission**, not infallibility.

## Disposition

```text
P1_BAD_POLICY_ENFORCEMENT = INITIAL_BOUNDED_PASS
PREREGISTERED_DISPOSITION = C__PASS_WITH_BOUNDED_SCOPE

CCP0_REGRESSION = PASS
AUTHORITY_SPOOFING_SLICE = PASS_WITH_NARROW_SCOPE

LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
REAL_PROJECT_POLICY_REPLACEMENT = NOT_AUTHORIZED

NEXT_P1_ATTACK = STALE_AND_CONCURRENT_TRANSITIONS
```
