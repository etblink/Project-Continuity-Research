# Silent-Success Corpus — Pass 0.1.0

Date: 2026-09-20  
Status: Provisional positive-control corpus.

## Purpose

A visible self-correction is useful evidence, but an even stronger architecture
may prevent the failure from becoming salient in the first place.

This corpus looks for periods where:

- the system faced many opportunities to drift;
- the work crossed context/session/phase boundaries;
- the expected failure did not occur;
- a durable scaffold plausibly explains why.

Absence of failure is difficult to prove. These cases therefore avoid claiming
that a scaffold was the *only* cause. They record bounded success and the
mechanisms that were present.

---

## SS-001 — Project Observatory reconstructed four projects without mutating them

- **Project:** Project Observatory
- **Period:** 2026-09-11 through 2026-09-14
- **Event evidence:** R2
- **Initiative evidence:** not applicable; this is a process-level silent success
- **Evidence:**
  - method freeze `421a1237805d41365d02105d293711c72ea116b1`
  - v0.2 canonical merge `d9d7c6f272f1982d9e644d1987b3308ef51ca324`

### Risk environment

The Observatory was explicitly examining:

- NFC;
- FCP;
- PGH;
- HiVenues;

while resolving stale/superseded artifacts, repository divergence, dependency
questions, uncertainty registers, and post-freeze scientific findings.

This created many opportunities to "helpfully" repair observed projects while
reconstructing them.

### Scaffold

The frozen charter required:

```text
do not mutate an observed repository
do not repair inconsistencies while discovering them
record discrepancies first
bind conclusions to exact repository/ref/commit/path
do not use memory when the repository can answer
```

It also separated:

```text
OBSERVATORY FINDING
!= OBSERVED-PROJECT FINDING
```

and required separate authorization for any downstream repair.

### Observed outcome

The v0.2 snapshot explicitly records:

```text
OBSERVED_NFC_MUTATION_BY_THIS_PASS = NONE
OBSERVED_FCP_MUTATION_BY_THIS_PASS = NONE
OBSERVED_PGH_MUTATION_BY_THIS_PASS = NONE
OBSERVED_HIVENUES_MUTATION_BY_THIS_PASS = NONE

PROJECT_OBSERVATORY_MUTATION = YES
```

At the same time, the Observatory successfully updated its own reconstruction
and recovered exact historical provenance.

### Why this matters

This is strong evidence for an **authority firewall**.

The system did not need to continuously remember "don't change those repos."
The rule was part of the operating frame and the resulting state was audited
against it.

### Logos / Agape note

- Logos: observation and intervention remained distinct.
- Agape: restraint served the autonomy/governance of the observed projects.

---

## SS-002 — FCP remained intentionally idle rather than manufacturing a next operation

- **Project:** FCP as observed by Project Observatory
- **Period:** through Project Observatory v0.2
- **Event evidence:** R2
- **Evidence:** Project Observatory method freeze and v0.2 snapshot

### Risk environment

Long-running AI projects strongly reward activity. When a major research phase
finishes, a model can easily infer a new task simply because the conversation
expects continuation.

### Scaffold

The Observatory charter's external-trigger discipline says:

> If progress genuinely depends on an external event, record the dependency
> rather than manufacturing substitute work.

In the v0.2 snapshot:

```text
FCP_PROJECT_STATE = WAITING_FOR_EVIDENCE
```

and:

```text
No FCP-27 or immediate new FCP scientific operation is selected.
```

The uncertainty register similarly records the FCP evidence trigger as
`OPEN__EVIDENCE_GATED` and explicitly says internal make-work cannot resolve it.

### Observed outcome

The system preserved a **legitimate non-action state** instead of treating
"nothing authorized to do" as an error that needed to be filled.

### Why this matters

This may be a critical long-horizon capability:

> A continuity system must preserve the right to *wait*.

Without an explicit WAITING/BLOCKED state, action pressure can itself become a
source of epistemic drift.

### Logos / Agape note

Strongly both:

- Logos: absence of new evidence remained absence of new evidence.
- Agape: activity was not substituted for meaningful progress.

---

## SS-003 — HiVenues v1 release used staged promotion instead of one global PASS

- **Project:** HiVenues
- **Date:** 2026-09-03
- **Event evidence:** R2
- **Evidence:** Issue #132, PR #134, and Issue #132 completion record

### Risk environment

The release combined:

- fresh-start venue creation;
- local media handling;
- Studio authoring;
- offline readiness;
- package identity;
- product naming;
- Windows/Ubuntu CI;
- visual review;
- accessibility;
- exact-head qualification;
- canonical integration;
- immutable release tagging.

A single "tests green" signal could easily have collapsed these into a false
release claim.

### Scaffold

Issue #132 defined distinct gates and explicitly stated that acceptance was not
implied by candidate construction.

Its later naming amendment made unresolved legacy product identity a hard
pre-tag blocker even if CI was green.

The completion record then separately bound:

- accepted candidate commit/tree;
- exact-head CI;
- Track A and Track B visual review;
- accessibility;
- artifact digests;
- canonical merge commit/tree;
- post-merge CI;
- release identity;
- immutable tag custody.

### Observed outcome

The release state was promoted only after each required evidence class had an
appropriate result.

### Why this matters

This is a silent success of **typed promotion**.

The process did not need to infer that a green subsystem result meant the
whole release was complete because the architecture refused to represent the
project with one undifferentiated status.

### Logos / Agape note

- Logos: each claim had its own evidence burden.
- Agape: product-facing quality and operator experience remained part of the
  release definition rather than being sacrificed to machine convenience.

---

## SS-004 — Independent HiVenues experimentation stayed quarantined until adjudication

- **Project:** Project Observatory / HiVenues
- **Period:** 2026-09-11 through 2026-09-14
- **Event evidence:** R2
- **Evidence:** Project Observatory charter and v0.2 snapshot

### Risk environment

An independent GPT-6 Astra greenfield HiVenues challenge was intentionally
designed to provide evidence uncontaminated by the existing implementation.

The obvious failure mode was context leakage: using existing HiVenues
architecture, screenshots, issues, or implementation decisions to "help" the
independent run.

### Scaffold

The Observatory charter created an explicit **Astra quarantine**:

- Observatory could record that the experiment existed;
- existing implementation details must not be fed into the independent
  challenge;
- unfinished Astra work could not be used as canonical evidence about the
  existing project.

### Observed outcome

The v0.2 snapshot records that the independent Fable and GPT-6 Astra greenfield
results were frozen and **blind-adjudicated before model identities were
revealed**. Only then was the prior quarantine retired.

### Why this matters

This is evidence that a strong **information-boundary scaffold** can preserve
experimental independence across a multi-session, multi-project environment.

### Logos / Agape note

Primarily Logos, with an Agape component: the experiment's integrity was
preserved rather than sacrificing it for convenience.

---

## SS-005 — Historical provenance and current authority were allowed to coexist

- **Project:** Project Observatory
- **Period:** v0.1 → v0.2
- **Event evidence:** R2
- **Evidence:** v0.2 merge/snapshot

### Risk environment

Several exact historical Observatory artifacts were no longer present on the
current main lineage even though downstream NFC/FCP records referred to them.

Two tempting but damaging responses would have been:

1. declare the historical artifacts irrelevant because they were absent from
   current main; or
2. rewrite history so the current lineage appeared to have always contained
   them.

### Scaffold

The snapshot discipline and supersession discipline required immutable
historical provenance and explicit current-lineage reconstruction.

### Observed outcome

V0.2 recovered four exact historical Observatory artifacts by immutable SHA,
while explicitly stating that:

- their original commits remain the historical execution/provenance identities;
- recovery does **not** mean the audits were newly executed;
- v0.1 was not rewritten.

### Why this matters

This is a silent success of the distinction:

```text
HISTORICAL TRUTH
!= CURRENT DISCOVERABILITY
!= CURRENT AUTHORITY
```

The architecture could improve current orientation without falsifying history.

---

# Cross-case findings

## 1. Silent success is usually scaffolded restraint

The strongest cases are not examples of the AI being unusually wise.

They involve structures that made the wrong move harder:

- read-only authority firewall;
- WAITING_FOR_EVIDENCE as a legitimate state;
- staged promotion;
- information quarantine;
- immutable historical provenance.

## 2. "Do nothing" is a first-class successful outcome

At least one long-horizon failure mode comes from assuming that continuity
requires motion.

FCP's evidence-triggered hold suggests that a mature continuity protocol must
represent:

```text
WAIT
BLOCKED
NO AUTHORIZED NEXT OPERATION
```

without semantic pressure to invent progress.

## 3. Negative constraints can carry more continuity than summaries

Several silent successes were preserved by statements of what **must not**
happen:

```text
do not mutate
do not promote
do not leak context
do not rewrite history
do not invent substitute work
```

This suggests negative knowledge is not merely archival. It may be part of the
active control plane.

## 4. A candidate concept: reorientation surfaces

Across successful cases, the process periodically encounters a surface that
forces one of four questions back into view:

- **Reality:** what is actually established?
- **Purpose:** what is this project for?
- **Authority:** what am I allowed to change or promote?
- **Boundary:** what information/actions must remain isolated?

The term is still provisional.
