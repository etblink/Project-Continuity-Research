# Post-Literature Requirements 0.1.0

Date: 2026-09-20  
Status: Derived requirements for later architecture competition.  
Important: These are **requirements**, not an implementation specification.

## Derivation rule

A requirement is admitted here only when it is supported by:

1. at least one recurring empirical failure/positive-control pattern from the
   project corpus; and
2. a plausible analogue or supporting concept in an adjacent field, **or** a
   documented gap in current systems that makes the requirement necessary.

---

## R1 — Preserve hierarchical intent

A successor must be able to recover:

```text
ultimate purpose
→ project objective
→ current phase
→ current operation
→ local task
```

without loading the entire project history.

### Failure pressure
Orientation Drift.

### External support
HTN planning, mission intent, cognitive-control hierarchy, COMPASS.

---

## R2 — Separate working context from durable memory

The architecture must distinguish:

- transient active context;
- durable project state;
- historical evidence;
- retrievable supporting detail.

### Failure pressure
Context swamp, succession loss, local-detail domination.

### External support
Working-memory theory, MemGPT, memory surveys, context-rot research.

---

## R3 — Preserve history without making history current authority

Historical artifacts must remain immutable/discoverable while carrying explicit
relations such as:

```text
CURRENT
HISTORICAL
SUPERSEDED
PARTIALLY_SUPERSEDED
CANDIDATE
FROZEN
```

### Failure pressure
Authority Drift.

### External support
Event sourcing, provenance, versioned state.

---

## R4 — Bind claims to provenance and authority

A material state assertion should answer:

```text
WHAT IS CLAIMED?
WHAT SUPPORTS IT?
WHERE DID THAT SUPPORT COME FROM?
WHO/WHAT HAS AUTHORITY AT THIS SCOPE?
```

Provenance alone is insufficient; governing authority must be represented.

### Failure pressure
Wrong-repository identity, frozen/current confusion, stale handoff.

### External support
W3C PROV plus the identified transfer gap.

---

## R5 — Make supersession scoped

A later object must be able to supersede only the affected claim/subclaim or
interpretation while preserving unaffected prior content.

### Failure pressure
FCP-6/FCP-22 over-subtraction and other stale/current conflicts.

### External support
Event/version semantics; not fully solved by standard provenance.

---

## R6 — Represent project state as typed claims, not one scalar status

The system must distinguish at least conceptually among:

```text
intended
implemented
observed
demonstrated
qualified
accepted
canonical
released
```

with project-specific state vocabularies where needed.

### Failure pressure
Epistemic-State Drift.

### External support
Event/state systems, staged release gates, LongMemEval knowledge-update and
abstention concerns.

---

## R7 — Make transitions explicit and guarded

Every material promotion should be representable as:

```text
FROM_STATE
+ REQUESTED_TRANSITION
+ REQUIRED_EVIDENCE
+ AUTHORITY
+ CONTEXT / PRECONDITIONS
→ TO_STATE
```

### Failure pressure
Transition Drift.

### External support
Statecharts, STPA, command/event processing.

---

## R8 — Preserve legitimate WAIT / HOLD / BLOCKED states

The system must not assume that every healthy project has an immediate next
action.

It must represent:

```text
WAITING_FOR_EVIDENCE
BLOCKED_EXTERNAL
HOLD
NO_AUTHORIZED_NEXT_OPERATION
```

without treating them as failures.

### Failure pressure
Manufactured make-work, premature continuation.

### External support
Planning infeasibility/refusal research, state machines, mission/safety control.

---

## R9 — Store negative knowledge as executable closure semantics

A closed path should preserve:

```text
ROUTE
DISPOSITION
BASIS
AUTHORITY
REOPEN_IF
```

not merely prose such as "we decided against this."

### Failure pressure
Negative-Knowledge Loss.

### External support
Safety constraints, organizational memory, event history; current agent memory
only partially covers this.

---

## R10 — Distinguish reflection from verified correction

A reflective statement should not automatically become durable knowledge.

Where feasible, correction should be tied to:

- external evidence;
- replay/test;
- counterexample;
- independent adjudication;
- changed outcome under controlled intervention.

### Failure pressure
Metacognitive Drift / frame-preserving correction.

### External support
Self-correction literature, Reflexion limits, REFLECT.

---

## R11 — Give every safeguard an exit condition

Safeguards such as:

- reconstruction;
- review;
- cleanup;
- conservative classification;
- quarantine;

must specify when they are complete.

### Failure pressure
Orientation paralysis and other failed self-corrections.

### External support
State machines, procedural-memory misuse, guarded control loops.

---

## R12 — Separate strategic oversight, tactical execution, and context management

One context/process should not be required to carry all three indefinitely.

### Failure pressure
Local optimization overriding purpose; context contamination flowing upward.

### External support
COMPASS, HTN hierarchy, mission command.

---

## R13 — Preserve human agency and project purpose as governing constraints

A technically successful action is not sufficient if it silently changes what
the project is for or substitutes agent preference for human/project intent.

### Failure pressure
Agape/purpose failures.

### External support
Mission-intent ideas and safety/value preservation provide partial analogues,
but this requirement remains more normative than most engineering sources.

---

## R14 — Make current orientation reconstructible from durable state alone

Cold-start criterion:

A fresh successor should be able to determine:

1. what the project is;
2. what it serves;
3. current authoritative state;
4. evidence for that state;
5. open uncertainty;
6. current/held transitions;
7. next authorized operation or reason to wait;
8. what must not be silently reopened.

### Failure pressure
Succession illusion.

### External support
Organizational memory, event-state reconstruction, persistent agent memory.

---

## R15 — Do not make the orientation projection the sole source of truth

A compact kernel/snapshot may be used to orient agents, but it must be
regenerable or auditable against deeper durable evidence.

### Failure pressure
Stale kernel risk—the continuity system itself becoming another stale document.

### External support
Event sourcing snapshots/materialized views.

### Consequence

This may be the most important refinement of the original Project Kernel idea:

> **A kernel should orient. It should not monopolize truth.**

---

# Architecture-phase acceptance test

Any future candidate architecture must demonstrate how it satisfies all fifteen
requirements **without requiring a single ever-growing document or a model to
retain the entire history in active context**.

It should also identify which requirements it intentionally does **not** solve.
