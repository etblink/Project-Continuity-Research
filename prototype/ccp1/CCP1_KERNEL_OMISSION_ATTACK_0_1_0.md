# CCP-1 Kernel-Omission Attack 0.1.0

Date: 2026-09-20  
Status: **PREREGISTERED — NOT YET ADJUDICATED**

## Question

CCP-0 made the Project Kernel a derived orientation projection with a freshness
identity.

Freshness solves one failure:

> Is this kernel stale relative to the control plane?

It does not automatically solve another:

> Does this fresh kernel contain the decision-critical information required for
> the operation a successor is about to perform?

A perfectly fresh projection may still omit the one fact that matters.

## Hypothesis under attack

Kernel validity must separate:

```text
FRESHNESS
```

from:

```text
ORIENTATION SUFFICIENCY FOR A NAMED OPERATION
```

The bounded attack will introduce an explicit operation-scoped orientation
contract.

A contract names only the semantic facts needed to orient a particular
operation. It is not a demand to put the whole project into the kernel.

## Candidate requirement kinds

The first prototype may require bounded items such as:

- project purpose;
- phase/current state for a named subject;
- active policy identity;
- authority needed for a named action/scope;
- a held/closed route and reopen condition;
- a named claim;
- an external-source freshness status.

## Injected failures

The attack will deliberately create kernels that are fresh but omit:

1. a decision-critical authority constraint;
2. a held route / negative-knowledge constraint;
3. active policy identity.

Each omitted kernel must remain fresh relative to the same underlying state, so
the test cannot pass merely by reusing the existing staleness detector.

## Positive controls

The prototype must also demonstrate that:

1. a bounded kernel satisfying the operation contract passes;
2. irrelevant project facts need not be rendered merely to achieve
   sufficiency;
3. changing the orientation contract invalidates the earlier sufficiency claim;
4. changing underlying project state invalidates freshness even if the old
   contract coverage was complete.

## Preregistered dispositions

### A — FAIL

A fresh kernel that omits a named decision-critical requirement is still treated
as sufficient.

### B — PARTIAL

Omission can be detected, but only by requiring an effectively complete project
dump or by coupling the contract to one historical incident.

### C — PASS WITH BOUNDED SCOPE

The prototype:

- represents operation-scoped orientation requirements generically;
- can produce a fresh-but-insufficient kernel deliberately;
- identifies the missing requirement;
- produces a bounded fresh-and-sufficient kernel when the requirement is
  included;
- does not require unrelated facts;
- distinguishes contract revision from project-state freshness;
- preserves all earlier tests.

## Important limitation

Outcome C would not prove that humans or agents choose the *right*
orientation contract.

A bad contract can omit something important and then certify its own incomplete
view.

Therefore the result can establish:

```text
KERNEL SATISFIES DECLARED ORIENTATION CONTRACT
```

but not:

```text
DECLARED ORIENTATION CONTRACT IS COMPLETE IN REALITY
```

The latter remains a metacognitive/governance problem and is an explicit attack
target for later blind cold-start evaluation.

## Boundary

```text
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
KERNEL_AS_SOLE_SOURCE_OF_TRUTH = FORBIDDEN
```
