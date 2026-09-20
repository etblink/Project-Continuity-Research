# Cross-Discipline Transfer Matrix 0.1.0

Date: 2026-09-20  
Status: Comparative matrix; not final architecture.

Legend:

- `STRONG` — mature concept transfers directly or nearly directly.
- `PARTIAL` — useful analogue, but important semantics are missing.
- `WEAK` — field touches the problem but does not substantially solve it.
- `—` — not a primary fit.

| Empirical failure class | HTN / hierarchical planning | Mission intent / org memory | Event sourcing / distributed state | Provenance | Statecharts / STPA | Cognitive control | Current LLM agent work |
|---|---|---|---|---|---|---|---|
| **T1 Orientation Drift** | **STRONG** for decomposition; weak for changing authority | **STRONG** for purpose/end-state; routines add continuity | PARTIAL | WEAK | PARTIAL | **STRONG analogue** | **STRONG emerging** via COMPASS/context management |
| **T2 Epistemic-State Drift** | WEAK | PARTIAL | **STRONG** for state/history separation | **STRONG** for lineage | PARTIAL | WEAK | PARTIAL; memory/update/abstention exist but claim-state semantics vary |
| **T3 Authority Drift** | WEAK | PARTIAL | PARTIAL | **STRONG foundation**, incomplete normative authority | **STRONG** for control authority/guards | WEAK | WEAK/PARTIAL |
| **T4 Transition Drift** | PARTIAL | PARTIAL | **STRONG** for command/event state changes | PARTIAL | **STRONG** | PARTIAL | PARTIAL; planning/refusal improving |
| **T5 Negative-Knowledge Loss** | PARTIAL via constraints | PARTIAL/STRONG for institutional memory | PARTIAL via compensating/history | PARTIAL | **STRONG** for forbidden/unsafe actions | WEAK | PARTIAL; forgetting/contradiction research, weak reopen semantics |
| **T6 Metacognitive Drift** | WEAK | PARTIAL | WEAK | WEAK | **STRONG control-loop analogue** | PARTIAL | **STRONG research focus**, but reliability remains conditional |

---

# Transfer observations

## 1. No single field covers the full problem

The strongest coverage comes from **combining**:

```text
hierarchical planning
+ mission intent
+ event-sourced history
+ provenance
+ guarded state transitions
+ safety constraints
+ persistent agent memory
+ externally grounded reflection
```

This is a warning against adopting any one metaphor too literally.

## 2. Event sourcing is strongest for history, not purpose

Event sourcing solves:

```text
WHAT HAPPENED?
HOW DID CURRENT STATE ARISE?
```

It does not solve:

```text
WHAT SHOULD MATTER?
WHO MAY PROMOTE THIS?
WHY IS THIS ROUTE CLOSED?
```

## 3. Mission intent is strongest for purpose, not evidence

Mission intent solves:

```text
WHAT ARE WE TRYING TO ACHIEVE?
WHAT COUNTS AS SUCCESS?
```

It does not establish scientific or repository truth.

## 4. Provenance is strongest for lineage, not normative authority

Provenance solves:

```text
WHERE DID THIS COME FROM?
WHO/WHAT GENERATED OR USED IT?
```

It does not automatically solve:

```text
WHICH SOURCE GOVERNS THIS CLAIM NOW?
```

## 5. State/safety formalisms are strongest for permissible action

Statecharts and STPA naturally ask:

```text
WHAT STATE ARE WE IN?
WHAT ACTION IS PROPOSED?
UNDER WHAT CONDITIONS IS IT SAFE / VALID?
```

This is the closest mature analogue to Transition Drift.

## 6. Current agent memory research is strongest on recall and context management

The current literature is rapidly improving:

- storage;
- retrieval;
- reflection;
- consolidation;
- context organization;
- strategic/tactical role separation.

But our corpus suggests that **authority and transition semantics need to be
first-class**, not left implicit inside retrieved prose.

---

# Candidate design consequence — still not architecture

The comparison suggests that a future system probably needs several distinct
objects rather than one giant `PROJECT_KERNEL.md`:

```text
HISTORY / EVENT LAYER
PROVENANCE / AUTHORITY LAYER
CURRENT-STATE PROJECTION
INTENT / PURPOSE LAYER
TRANSITION / GATE LAYER
NEGATIVE-KNOWLEDGE LAYER
REORIENTATION / REVIEW LAYER
```

The **Project Kernel** may eventually be the compact orientation projection
across those layers.

This is a research implication, not yet a design decision.
