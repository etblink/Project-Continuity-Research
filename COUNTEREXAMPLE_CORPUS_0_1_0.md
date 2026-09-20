# Counterexample Corpus — Pass 0.1.0

Date: 2026-09-20
Status: Provisional positive-control corpus

## Purpose

A failure taxonomy alone can tell us what breaks, but not which mechanisms
already work.

This corpus therefore records cases where the AI/process **caught, resisted, or
contained drift without the user first supplying the specific correction**.

Because initiative is difficult to prove from repository artifacts alone, each
entry separates:

- **event evidence** — evidence that the correction/safety action occurred;
- **initiative evidence** — evidence about whether the AI/process noticed it
  before the user did.

The latter remains conservative until raw chat transcripts are archived.

---

## CE-001 — Green CI did not end semantic review

- **Project:** HiVenues
- **Date:** 2026-09-03
- **Event evidence:** R2
- **Initiative evidence:** R1
- **Related incident:** INC-003

### Successful behavior

The Project Lead workflow continued inspecting current-facing semantics after
automated qualification and did not treat green CI as sufficient.

The resulting Issue #132 naming amendment explicitly made unresolved
release-facing legacy identity a blocker even if CI was green.

The audit coverage was then strengthened in commit
`21855ee59c78a2357f255a1c2e47c51c931080d2`, and the diagnostic workflow was
requalified at `da39f8326fb1aa1066582d7c0d6b093821d51751`.

### Why this matters

This is evidence that **an independent semantic review layer can catch defects
outside the machine oracle**.

### Candidate enabling mechanism

```text
automated gate
→ independent Project Lead review
→ semantic inconsistency found
→ oracle coverage repaired
→ requalification
```

### Hypothesis

Self-correction becomes more likely when the process explicitly requires a
second review whose job is **not identical to the first gate**.

---

## CE-002 — Functional success was refused as a proxy for product success

- **Project:** HiVenues
- **Date:** 2026-09-15
- **Event evidence:** R2
- **Initiative evidence:** R1/R2 mixed
- **Related incident:** INC-008

### Successful behavior

Issue #272 records that the candidate was functionally qualified, but Project
Lead visual review still declared the pre-Astra product gate premature and held
Astra regression.

The issue re-anchored the work to the product's larger purpose: frontend
factory for Hive, host-first public territory, and a serious 2026 creative
Studio.

### Why this matters

The system successfully resisted Goodhart-like pressure to let one measurable
success dimension stand in for the whole objective.

### Candidate enabling mechanism

A **North-Star-bearing acceptance rubric** existed outside the functional test
suite.

### Hypothesis

Purpose drift is easier to catch when the acceptance process asks:

> "What larger claim does this evidence *not* establish?"

rather than merely:

> "Did this gate pass?"

---

## CE-003 — Occupied production-adjacent infrastructure triggered a fail-closed stop

- **Project:** HiVenues
- **Date:** 2026-09-19
- **Event evidence:** R2
- **Initiative evidence:** R1

### Successful behavior

Before first-bootstrap mutation, the deployment path gained a read-only
suitability test for unexpected public listeners and pre-existing services.

Commit:

`70503ee2037aa08c14aec7e932677f0825ccf660`

fails closed when an ostensibly new target is already occupied.

### Why this matters

This is a concrete example of local execution being prevented from blindly
following its own current objective when the surrounding environment would make
that objective unsafe.

### Candidate enabling mechanism

**External-state preconditions** attached to mutation authority.

### Hypothesis

Some of the executive function currently supplied by a human can be encoded as:

```text
intent to act
→ inspect environment
→ classify preconditions
→ withhold authority if reality contradicts assumptions
```

This is stronger than merely reminding the model to be careful.

---

## CE-004 — FCP method review corrected its own abstract admission law

- **Project:** Foundational Convergence Program
- **Date:** 2026-08-30
- **Event evidence:** R2
- **Initiative evidence:** R2 for process-level self-correction; human/agent initiation not yet transcript-resolved
- **Related incident:** INC-012

### Successful behavior

Method 0.2.1 records that the existing framework-admission criterion failed an
invariance test against an already-canonical framework, `FW-CST`.

Rather than forcing the canonical case to fit the rule or changing the current
scientific result, the process:

1. identified the pre-existing counterexample;
2. revised the method prospectively;
3. preserved historical results;
4. froze the new rule before affected adjudication;
5. explicitly changed no scientific taxonomy result at that boundary.

### Why this matters

This is one of the strongest examples in the current corpus of an **explicit
metacognitive control loop** working as intended.

### Candidate enabling mechanism

```text
governance rule
→ regression against canonical cases
→ contradiction detected
→ METHOD_REVIEW trigger
→ prospective rule repair
→ adjudication remains held
```

### Hypothesis

A continuity system should not merely preserve rules. It should preserve the
**conditions under which rules themselves must be challenged**.

---

## CE-005 — Misleading green Windows tests did not override a failing dependency audit

- **Project:** HiVenues
- **Date:** 2026-09-04
- **Event evidence:** R1
- **Initiative evidence:** R1

### Successful behavior

Retained conversation history records a case where Windows tests were fully
green while the npm audit path hung / returned an external 503.

The assistant refused to merge, used bounded retries, and preserved the
fail-closed acceptance posture rather than declaring overall success from the
green test count.

### Why this matters

The model/process resisted **selective evidence aggregation**.

### Candidate enabling mechanism

Independent required gates with no scalar "majority green" override.

### Verification queue

Retrieve the original workflow run and raw conversation turns.

---

## CE-006 — Functional equivalence was rejected when the contract was intentionally literal

- **Project:** HiVenues
- **Date:** 2026-09-04
- **Event evidence:** R1
- **Initiative evidence:** R1
- **Related incident:** INC-004

### Successful behavior

Retained history records that delegating the top-level `check` command through
`check:deterministic` preserved effective execution but violated a frozen
literal oracle.

The assistant treated that as a real contract break rather than arguing that
the two forms were "basically the same."

### Why this matters

This is a counterexample to abstraction overreach: the system recognized that
sometimes the exact representation is itself part of the interface.

### Candidate enabling mechanism

Explicit classification of requirements as:

```text
SEMANTIC_CONTRACT
LITERAL_CONTRACT
```

### Verification queue

Recover the exact frozen oracle, package diff, and original turns.

---

# Cross-counterexample observation

The early positive controls do **not** look like spontaneous, free-floating
intuition.

They repeatedly involve **scaffolds**:

- a separate Project Lead review;
- a North-Star-bearing visual rubric;
- a hard pre-tag naming audit;
- a method-review trigger;
- canonical regression cases;
- fail-closed environmental preconditions;
- independently required qualification gates.

This suggests a more precise hypothesis:

> Long-horizon AI self-correction may be made reliable less by asking the model
> to "remember the big picture" and more by constructing recurring
> **reorientation surfaces** that force reality, purpose, authority, and
> evidence back into the decision loop.

That is highly consistent with the original context/framing observation, but it
is now grounded in observed project behavior rather than analogy alone.

# Next verification priorities

1. Archive raw turns for CE-001 through CE-006 so initiative attribution can be
   promoted beyond R1.
2. Search for **failed self-corrections**: cases where the AI noticed a problem
   but still chose the wrong remedy.
3. Search for **silent successes**: long stretches where drift did *not* occur,
   to identify which structures may have prevented it.
4. Compare projects with strong frozen governance (FCP/NFC) against product work
   with rapidly changing state (HiVenues) to see whether the failure profile
   differs.
