# Architecture Competition Result 0.1.0

Date: 2026-09-20  
Status: COMPETITION COMPLETE — COMPOSITE E SELECTED FOR PROTOTYPE TESTING

## Decision

None of the four pure architectures satisfies the frozen critical requirement
set.

The failures are complementary:

- document-centric architecture preserves intent but cannot reliably enforce
  freshness or transitions;
- event sourcing preserves historical truth but cannot by itself decide what
  may happen next;
- state/policy control enforces transitions but needs a trustworthy epistemic
  substrate;
- provenance graphs preserve authority and scoped supersession but do not
  naturally intercept action.

A composite is therefore justified by the evidence rather than by aesthetic
preference.

The selected prototype candidate is:

> **Composite E — Event-Sourced Provenance Control Plane**

working name:

> **Continuity Control Plane (CCP)**

## Why this is not a premature final architecture

Selection means only:

```text
BEST CURRENT CANDIDATE FOR PROTOTYPE TESTING
```

It does **not** mean:

```text
PUBLIC STANDARD
FINAL FILE FORMAT
FINAL TERMINOLOGY
PROVEN SCALABILITY
PROVEN USABILITY
PROJECT OBSERVATORY MIGRATION AUTHORIZED
```

The architecture must still survive implementation and cold-start testing.

## Most important architectural conclusion

The Project Kernel is demoted from "the memory system" to a more precise role:

> **Project Kernel = compact auditable orientation projection over deeper
> durable continuity state.**

That is now the leading hypothesis.

## Logos / Agape / authority-action interpretation

Composite E naturally separates three questions that the incident corpus kept
mixing when no architecture was present:

```text
LOGOS-LIKE:
What is true / justified?
→ evidence + provenance + current-state derivation

AGAPE-LIKE:
What does this serve?
→ human intent + North Star + agency boundaries

UNNAMED AUTHORITY/ACTION DIMENSION:
Given the first two, what transition is permitted now?
→ policy guards + authority + hold/reopen semantics
```

The third dimension remains unnamed. Architecture selection does not settle its
philosophical interpretation.

## Next operation

Build a **minimal semantic prototype**, not a production system.

The prototype should replay at least AR-02, AR-03, AR-04, AR-05, AR-06, AR-07,
AR-08, and AR-10 and demonstrate that:

- stale/current state is distinguishable;
- partial supersession works;
- invalid promotions are blocked;
- legitimate waiting is preserved;
- negative knowledge can reopen only under its predicate;
- a kernel can be regenerated from durable state;
- a worker return cannot directly become canonical state;
- an overlong safeguard has an explicit exit condition.

Only after those tests pass should the architecture be trialed on one live
project.
