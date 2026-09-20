# CCP-0 Advancement Decision 0.1.0

Date: 2026-09-20  
Decision type: Prototype-phase gate.

## Decision

```text
CCP0 = ACCEPT_FOR_SEMANTIC_FEASIBILITY

CCP1 = AUTHORIZED_AS_BOUNDED_RESEARCH_PROTOTYPE

LIVE_PROJECT_CONTROL_PLANE_INTEGRATION = NOT_AUTHORIZED

AUTOMATIC_MUTATION_OF_HIVENUES_NFC_FCP_PGH = NOT_AUTHORIZED
```

## Rationale

CCP-0 has earned continuation because:

- all ten historical replay scenarios pass;
- six counterfactual controls demonstrate that the system is not merely
  fail-closed;
- seven self-audits test the integrity of the continuity mechanism itself;
- three external-freshness tests distinguish frozen reconstruction from later
  source movement;
- the Project Observatory shadow trial produced a useful real-world result;
- several mechanisms explain multiple incidents rather than one rule being
  written per incident.

CCP-0 has **not** earned production integration because authority, concurrency,
policy correctness, evidence authenticity, human usability, and blind successor
orientation remain untested.

## CCP-1 objective

Build the smallest durable/read-only control-plane prototype that can operate
over a real project corpus without becoming the project's authority itself.

CCP-1 should add only the mechanisms required to attack CCP-0's highest-risk
assumptions:

1. explicit actor/role/authority grants;
2. durable append/replay;
3. expected-version concurrency guards;
4. policy provenance/versioning;
5. evidence verification adapters;
6. kernel-omission adversarial testing;
7. flexible reopen-predicate testing;
8. blind agent cold-start trial.

## CCP-1 hard boundary

CCP-1 remains:

```text
READ_ONLY_OR_SHADOW_MODE
```

with respect to the real projects unless a later gate separately authorizes
mutation.

No migration should occur merely because the prototype can model a project's
state.

## Stop condition

CCP-1 should stop and return to architecture research if any of the following
occur:

- authority cannot be represented without domain-specific hard-coding;
- correct replay requires hidden conversational knowledge;
- scoped supersession becomes un-auditable at realistic scale;
- kernel projection repeatedly omits decision-critical state;
- reopen semantics either allow obvious dead-end repetition or prevent obvious
  legitimate reopening;
- concurrency creates ambiguous canonical state that cannot be resolved without
  an ad hoc human rule.

## Current research posture

This is neither:

```text
"Composite E is proven"
```

nor:

```text
"we should keep theorizing indefinitely"
```

The warranted state is:

```text
PROMISING_ENOUGH_TO_ATTACK_AT_HIGHER_REALISM
```
