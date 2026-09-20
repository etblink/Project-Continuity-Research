# CCP-1 Kernel-Omission Result 0.1.0

Date: 2026-09-20  
Status: **COMPLETE — P1 KERNEL-OMISSION SLICE SURVIVES INITIAL BOUNDED ATTACK**

## Frozen implementation under adjudication

```text
IMPLEMENTATION_COMMIT =
2f846475f32461664167995b5f73073f8dd48afd

prototype/ccp1/kernel_omission.py
blob 6e3f1aafeb8b0facec1e93979f0f5a14a951c04d

prototype/ccp1/tests/test_kernel_omission.py
blob 140d8b5300f0c785d101628401fbb962b2e44a3f
```

## Preregistered disposition

```text
C — PASS WITH BOUNDED SCOPE
```

## Core result

The attack establishes a distinction between:

```text
KERNEL_FRESHNESS
```

and:

```text
KERNEL_SUFFICIENCY_FOR_A_NAMED_OPERATION
```

A kernel may exactly match the current control-plane state while still omitting
decision-critical information.

CCP-1 therefore introduces an explicit `OrientationContract` whose requirements
are operation-scoped rather than project-global.

## Injected omissions detected

Fresh kernels were deliberately generated while omitting:

1. a decision-critical authority constraint;
2. a held route / negative-knowledge constraint;
3. active policy identity.

In all three cases:

```text
FRESH = YES
SUFFICIENT = NO
```

and the missing requirement was identified explicitly.

## Positive controls

The prototype also demonstrates:

1. a bounded kernel satisfying the declared orientation contract passes;
2. irrelevant project facts do not need to be rendered merely to achieve
   sufficiency;
3. changing the orientation contract invalidates the earlier sufficiency claim
   without pretending that project state became stale;
4. changing project state invalidates freshness even when the prior contract
   coverage had been complete.

## Verification

Bounded local verification associated with the committed implementation:

```text
CCP0_REGRESSION_SUITE     = 27 / 27 PASS
CCP1_PREVIOUS_SUITES      = 25 / 25 PASS
CCP1_KERNEL_OMISSION      =  7 /  7 PASS

TOTAL                     = 59 / 59 PASS
FAIL                      = 0
ERROR                     = 0
```

## What this establishes

Within the semantic prototype boundary:

> **Sufficient orientation need not mean exhaustive reconstruction.**

It can instead mean:

```text
THE CURRENT PROJECTION IS FRESH
AND
THE KERNEL COVERS THE DECLARED ORIENTATION CONTRACT FOR THIS OPERATION
```

This directly addresses the historical tension between:

- apparent continuity without epistemic continuity; and
- orientation paralysis caused by endless reconstruction.

## What this does not establish

A contract can certify only the requirements it declares.

Therefore:

```text
KERNEL SATISFIES CONTRACT
!=
CONTRACT IS COMPLETE IN REALITY
```

Open risks include:

- an incorrectly authored orientation contract;
- a contract that omits a requirement nobody realized mattered;
- over-broad contracts that recreate context bloat;
- under-broad contracts that certify a misleadingly sparse view;
- human/agent disagreement over what is decision-critical;
- contracts becoming stale as project structure changes.

This higher-order problem must be attacked through blind cold-start evaluation,
contract provenance/review, and real successor behavior rather than by allowing
the contract to validate itself.

## Disposition

```text
P1_KERNEL_OMISSION = C__PASS_WITH_BOUNDED_SCOPE
CCP0_REGRESSION = PASS
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED

NEXT_P1_ATTACK = REOPEN_PREDICATE_BRITTLENESS
```
