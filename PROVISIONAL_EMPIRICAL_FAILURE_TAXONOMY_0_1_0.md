# Provisional Empirical Failure Taxonomy 0.1.0

Date: 2026-09-20  
Status: **PROVISIONAL EMPIRICAL TAXONOMY**  
Authority: Research classification only; not a Project Kernel specification.

## Purpose

This is the first attempt to classify the observed long-horizon AI project
failures after:

- the initial incident corpus;
- corroboration;
- positive controls;
- failed self-corrections;
- silent successes;
- the targeted transition/authority/negative-knowledge pass.

The taxonomy is intentionally small. It classifies recurring **failure
structures**, not every surface symptom.

The mandatory `OTHER` category remains active.

---

## T1 — Orientation Drift

### Definition

The active problem frame ceases to reflect the correct project-level purpose,
phase, or stopping condition.

### Common manifestations

- micro-task becomes the effective project objective;
- successor reconstructs too little and acts from inherited narrative;
- successor reconstructs too much and never returns to action;
- current work is selected from adjacency rather than roadmap purpose;
- a locally successful safeguard becomes the new objective.

### Representative incidents

- HiVenues local implementation/CI detail overriding Era purpose;
- succession reconstruction becoming orientation paralysis;
- visual/product North Star needing explicit re-anchoring.

### Missing function

**Hierarchical orientation with a sufficiency/exit condition.**

---

## T2 — Epistemic-State Drift

### Definition

The represented status of a claim or project ceases to match what the evidence
actually establishes.

### Common manifestations

- intended → treated as implemented;
- implemented → treated as demonstrated;
- demonstrated → treated as qualified;
- qualified subsystem → treated as whole-product acceptance;
- machine pass → treated as semantic acceptance;
- decisive evidence is produced but the disposition under-reads it.

### Representative incidents

- HiVenues functional qualification vs product readiness;
- release-name defect surviving earlier machine gates;
- NFC source-forcing audit reporting B when its own evidence met C.

### Missing function

**Typed claim states plus explicit evidence-to-state promotion rules.**

---

## T3 — Authority Drift

### Definition

A fact, artifact, or instruction is interpreted under the wrong authority
relation.

### Common manifestations

- wrong repository/source identity;
- historical artifact treated as present authority;
- frozen doctrine confused with mutable current routing;
- latest document assumed to wholly supersede earlier still-valid subclaims;
- representational overlap treated as identity authority;
- recovered historical artifact mistaken for newly executed evidence.

### Representative incidents

- NFC `b8587ce...` sentinel misread inside FCP recurrence work;
- FCP-22 partial supersession of FCP-6;
- Project Observatory v0.2 provenance recovery;
- HiVenues living docs vs frozen doctrine vs live GitHub state.

### Missing function

**Explicit authority typing and scoped supersession.**

---

## T4 — Transition Drift

### Definition

The system moves a project, claim, phase, or operation into a new state without
the transition predicate required for that move.

### Common manifestations

- premature next-phase activation;
- premature closure;
- scientific classification promotion beyond the reopened criteria;
- "selected" silently becoming "authorized";
- candidate silently becoming canonical;
- positive relation silently becoming framework identity.

### Representative incidents

- OBJ-CAT-11 existing-framework mapping → corrected to deferred remainder;
- HiVenues #272 holding #271/#267 despite functional acceptance;
- Observatory separating selection, preregistration, execution, adjudication,
  and downstream mutation.

### Missing function

**Explicit state-transition graph with evidence-bound guards.**

---

## T5 — Negative-Knowledge Loss

### Definition

Knowledge about what must **not** currently be done is forgotten, weakened, or
detached from the condition that would justify reopening it.

### Common manifestations

- exhausted search path reopened because it becomes salient again;
- held phase treated as available;
- forbidden scope leaks into an executor task;
- historical false route repeatedly rediscovered;
- "do not do X" preserved without the reason or reopen condition;
- program invents substitute work because inactivity feels incomplete.

### Representative incidents / controls

- FCP evidence-triggered hold and explicit `REOPEN ONLY IF` predicates;
- FCP-27 forbidden by numbering alone;
- recurrence reopening blocked absent a new slot/supersession/method defect;
- HiVenues #271/#267 hold states;
- FCP refusing to manufacture a next scientific operation.

### Missing function

**Active negative memory: closure reason + reopen predicate + authority.**

---

## T6 — Metacognitive Drift

### Definition

The system detects a problem or invokes a corrective mechanism, but the
correction remains inside an insufficient higher-order frame.

### Common manifestations

- reflection notices local defect but not task-type defect;
- review generates decisive evidence but chooses the wrong disposition;
- cleanup fixes the object but not dependent live pointers;
- verification becomes endless reconstruction;
- safety mechanism has no exit condition.

### Provisional subtype

**Frame-preserving correction**

> The local plan changes while the higher-order framing error survives.

### Representative incidents

- source-forcing audit B→C acceptance correction;
- FCP cleanup followed by live-metadata repair;
- succession reconstruction paralysis;
- circular proof route initially provoking more proof search.

### Missing function

**Multi-level reflection with explicit reframing and termination tests.**

---

# Cross-cutting axes

These are **not taxonomy classes**. They describe how an incident should be
coded.

## A. Evidence level

```text
R0 recollection only
R1 cross-chat / retained-history reconstruction
R2 durable artifact corroboration
R3 raw original conversation evidence
R4 raw conversation + durable artifact corroboration
```

## B. Correction origin

```text
HUMAN_RESCUE
SCAFFOLDED_SELF_CORRECTION
UNSCAFFOLDED_SELF_CORRECTION
UNKNOWN
```

## C. Logos relevance

Does the failure break fidelity between representation and reality/evidence?

## D. Agape relevance

Does the failure break alignment between execution and the human/community
purpose the project exists to serve?

## E. Authority/action relevance — `OTHER` remains open

The corpus repeatedly contains a concern not reducible to truth or purpose:

> Given what is known, what am I authorized to conclude, promote, change, or do?

This remains an empirical axis under investigation. It is **not yet promoted**
to a third philosophical first principle.

---

# Important non-equivalences now strongly supported by the corpus

```text
FACT != AUTHORITY
EVIDENCE != STATE
STATE != NEXT-STATE AUTHORIZATION
SELECTION != EXECUTION
CANDIDATE != CANONICAL
MACHINE PASS != ACCEPTANCE
FUNCTIONAL SUCCESS != PRODUCT READINESS
REPRESENTABILITY != IDENTITY
HISTORICAL TRUTH != CURRENT AUTHORITY
SUPERSESSION != WHOLE-DOCUMENT REPLACEMENT
HOLD != FORGOTTEN TASK
NO ACTION != FAILURE
```

These appear across multiple projects and are no longer isolated anecdotes.

---

# What this taxonomy does not yet claim

It does not claim:

- completeness;
- statistical prevalence;
- independence of all six classes;
- universality beyond the current project corpus;
- that Logos/Agape are sufficient philosophical foundations;
- that a Project Kernel is the correct implementation;
- that every failure should be prevented with more documentation.

The next phase should test this taxonomy against external/adjacent theory and
then design competing continuity architectures from the requirements, not from
the labels themselves.
