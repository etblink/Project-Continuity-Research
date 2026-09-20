# Failed Self-Correction Corpus — Pass 0.1.0

Date: 2026-09-20  
Status: Provisional edge-case corpus; not yet a final taxonomy.

## Purpose

A successful correction tells us what can work. A failed self-correction is
different: the AI/process detects some part of the problem, activates a review
or repair behavior, but still lands on the wrong conclusion, declares closure
too early, or lets the corrective process itself become the new source of
drift.

This corpus asks:

> What happens when the metacognitive layer is present but insufficient?

As in the positive-control corpus, **event evidence** and **initiative evidence**
remain separate.

---

## FSC-001 — The audit found the decisive evidence but chose the weaker outcome

- **Project:** Project Observatory / NFC
- **Date:** 2026-09-11
- **Event evidence:** R2
- **Initiative evidence:** R2 at process level; raw-turn attribution pending
- **Evidence:** Project Observatory commit
  `cde62683be53464c7b13c7d3c9683f1fd5eeeb54`

### Sequence

The NFC physical-history source-forcing audit performed the required positive
search, anti-selector search, independence testing, and adversarial reversals.

Most importantly, its Test 4 identified a conservative-extension pattern:
distinct lawful branch extensions could carry distinct dynamical structures
while preserving the common source spine, with no universal actual-history
selector forced by that spine.

The audit nevertheless reported:

```text
B__ONLY_CONDITIONAL_OR_BRANCH_SPECIFIC_SELECTOR_ESTABLISHED
```

The later acceptance/downstream adjudication concluded that the audit's **own
evidence** satisfied the stronger preregistered outcome:

```text
C__SOURCE_NONFORCING_ESTABLISHED_AT_AUDITED_SCOPE
```

The adjudication explicitly says the reported B outcome was scientifically
compatible but **not the strongest preregistered disposition supported by the
audit**.

### Why this is a failed self-correction

The audit had several metacognitive safeguards:

- anti-selector search;
- adversarial reversals;
- independence/countermodel testing;
- a preregistered outcome alphabet.

Those safeguards successfully generated the decisive evidence, yet the local
classification step still under-read its significance.

The process corrected only because a **higher-level adjudication layer** later
re-evaluated the relationship between evidence and disposition.

### Missing function

**Evidence-to-disposition closure checking.**

Before accepting a result label, the process should ask:

> Is there any stronger preregistered disposition whose burden has already been
> met by the evidence I just produced?

### Architectural implication candidate

A review layer should not merely repeat the substantive analysis. It should
perform a distinct **entailment audit**:

```text
evidence set
→ permitted outcome definitions
→ strongest justified outcome
```

### Logos / Agape note

Primarily Logos: the evidence was present, but the representation of what it
established was weaker than warranted.

---

## FSC-002 — Cleanup was declared complete before live metadata was re-swept

- **Project:** Foundational Convergence Program
- **Date:** 2026-08-25
- **Event evidence:** R2 for the repair; R1 for the premature-completion turn
- **Initiative evidence:** R1
- **Evidence:** FCP commit
  `0f8de4cc21a2a00e5794fc151c0ddeb8b6714e4b`
  (`FCP-16 repair live metadata before FCP-17`)

### Sequence

A branch/reference cleanup had been qualified and was treated as complete.
A subsequent audit found that live metadata had not fully caught up:

- `README.md` still recommended FCP-16 rather than FCP-17;
- `FRAMEWORK_REGISTER.md` did not yet reflect the latest FCP-16 null/GR control;
- `SOURCE_REGISTER.md` still pointed to a retired historical research branch
  instead of the exact integrated commit.

Commit `0f8de4cc...` repaired exactly those three live metadata surfaces before
FCP-17.

### Why this is a failed self-correction

The cleanup process successfully handled repository-level branch/ref state but
implicitly treated that as equivalent to **semantic cleanup closure**.

It corrected the visible graph of refs without fully checking the living
documents that routed future reasoning.

### Missing function

**Closure-postcondition sweep across dependent authority surfaces.**

A cleanup is not complete merely because the object being cleaned has changed.
All current-routing surfaces that refer to that object must be checked.

### Architectural implication candidate

Every operation that changes authority, identity, supersession, or routing may
need an explicit **dependent-pointer closure test**:

```text
changed authority object
→ current-state pointers
→ roadmap / next-task pointers
→ provenance pointers
→ successor-facing guidance
```

### Logos / Agape note

Logos-dominant. The repository graph and the semantic routing graph had diverged.

---

## FSC-003 — Succession reconstruction became its own form of drift

- **Project:** HiVenues
- **Date:** 2026-09-17
- **Event evidence:** R1
- **Initiative evidence:** R1

### Sequence

Fresh successor sessions correctly recognized that they needed to reconstruct
state before acting. They repeatedly inspected repository status, doctrine,
roadmaps, frozen state, CI, and predecessor handoffs.

The corrective instinct was sound: do not act from an unverified inherited
story.

But the process over-corrected. Reconstruction and narration became the work.
The user eventually redirected the successor toward:

> minimal drift check, then immediately attempt a repository-changing
> checkpoint.

### Why this is a failed self-correction

The system had correctly learned the lesson:

> "Do not act until oriented."

It had not learned the complementary stopping rule:

> "Once sufficiently oriented, stop reconstructing and act."

A safeguard against **apparent continuity without epistemic continuity**
became **orientation paralysis**.

### Missing function

**Sufficient-orientation criterion.**

The successor needs an explicit threshold for when reconstruction is adequate
for the next bounded action.

### Architectural implication candidate

A cold-start protocol should have both:

```text
MINIMUM REQUIRED ORIENTATION
```

and

```text
STOP RECONSTRUCTING WHEN THESE CONDITIONS ARE SATISFIED
```

without requiring exhaustive project recovery.

### Logos / Agape note

Mixed.

- Logos motivates reconstruction.
- Agape/purpose is lost when the safety process ceases to serve actual project
  progress.

### Verification queue

Archive the raw 2026-09-17 successor turns and bind the first
repository-changing checkpoint that followed the user redirect.

---

## FSC-004 — A circularity was noticed, but the first reaction was still to search inside the same frame

- **Project:** Project Observatory / NFC audit work
- **Date:** 2026-09-12
- **Event evidence:** R1
- **Initiative evidence:** R1

### Sequence

During work around the LS-2 / finite-interface sufficiency question, the
process noticed a circular dependency among the proposed proof route,
Phase-A assumptions, and later reconstruction machinery.

That recognition was itself a self-correction.

However, the immediate response was initially to continue searching for an
independent route inside the same proof-oriented frame before the work was
recast as a countermodel / independence-style audit.

### Why this is useful

This is a subtler failure mode than simple blindness.

The AI can notice:

> "My proof route is circular."

while still retaining the higher-level presupposition:

> "Therefore I should keep trying to prove it by another nearby route."

The deeper correction may require changing the **question type**, not merely
the proof path.

### Missing function

**Problem-form reclassification.**

When repeated proof routes collapse for the same structural reason, the system
should ask whether the correct operation is now:

- proof,
- disproof,
- independence test,
- countermodel construction,
- or underdetermination adjudication.

### Architectural implication candidate

A reorientation surface may need to operate on the **kind of task**, not just
its local plan.

### Logos / Agape note

Logos-dominant: correct recognition of a local defect did not immediately
trigger the correct global epistemic frame.

### Verification queue

Recover the exact audit/preregistration artifact and raw conversation sequence
before promoting beyond R1.

---

# Cross-case findings

## 1. Metacognition can fail one level above the detected problem

The repeated pattern is:

```text
problem detected
→ correction initiated
→ correction remains inside an insufficient frame
→ higher-level review is still needed
```

Examples:

- evidence found, but outcome label under-read;
- refs cleaned, but semantic routing not re-swept;
- succession guarded, but reconstruction never terminated;
- proof circularity noticed, but problem type not immediately reclassified.

This suggests that "reflection" is not one function. It has levels.

## 2. Every safeguard needs an exit condition

A mechanism created to prevent one failure can become a new failure mode:

```text
verification → paralysis
cleanup → stale downstream pointers
conservative classification → underclaiming
proof review → endless alternate proof search
```

## 3. A likely recurring failure class is **frame-preserving correction**

Working definition:

> The system notices an error and changes the local plan while preserving the
> higher-order frame that generated the error.

This is provisional terminology, not a frozen taxonomy label.
