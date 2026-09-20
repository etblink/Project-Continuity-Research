# Targeted Pass — Transition, Authority/Supersession, and Negative Knowledge 0.1.0

Date: 2026-09-20  
Status: Empirical targeted pass; not an architecture specification.

## Purpose

The edge-case pass suggested that three structures might be distinct recurring
sources of long-horizon AI failure:

1. **transition failure** — moving a project into the wrong state;
2. **authority / supersession failure** — using the wrong source, scope, time
   layer, or authority relation;
3. **negative-knowledge failure** — forgetting what is already known not to be
   authorized, not to be justified, or not to be worth reopening.

This pass tests those structures against additional project evidence rather
than assuming they are real categories.

The existing R0–R4 evidence ladder still applies.

---

# TP-001 — Wrong repository identity entered a scientific gate

- **Project:** Foundational Convergence Program / NFC boundary
- **Date:** 2026-08-27
- **Primary structure:** Authority identity failure
- **Event evidence:** R1 for the failed run; R2 for the corrected guard
- **Initiative evidence:** R1

## Reconstruction

A program-level recurrence operation initially encountered:

```text
b8587ce3409e34c0dd4e56c61ee585c07798b0e5
message = remove
```

and interpreted it as if it were the FCP remote state.

That SHA is actually a commit in:

```text
etblink/Nested-Fibrational-Cosmology
```

not the FCP repository.

The corrected recurrence artifact later made repository identity a first-class
gate and explicitly recorded:

```text
REMOTE_REPOSITORY = etblink/Foundational-Convergence-Program
REMOTE_REPOSITORY_IDENTITY = PASS
FRESH_CLONE_USED = YES

WRONG_REPOSITORY_SENTINEL =
b8587ce3409e34c0dd4e56c61ee585c07798b0e5

WRONG_REPOSITORY_SENTINEL_PRESENT_AS_ORIGIN_MAIN = NO
```

Evidence:

- NFC sentinel:
  https://github.com/etblink/Nested-Fibrational-Cosmology/commit/b8587ce3409e34c0dd4e56c61ee585c07798b0e5
- corrected FCP recurrence:
  https://github.com/etblink/Foundational-Convergence-Program/commit/46300a1fde35ccf1ebfa63807e5a203f13cd6498

## Why this matters

The data itself was real. The error was **referential authority**.

A correct commit SHA became misleading because it was interpreted inside the
wrong repository identity.

This is stronger evidence that long-horizon continuity needs not only
fact-preservation but **fact-to-authority binding**.

Candidate invariant:

```text
FACT WITHOUT AUTHORITY IDENTITY IS NOT SUFFICIENT STATE
```

---

# TP-002 — Whole-object supersession over-subtracted still-current evidence

- **Project:** Foundational Convergence Program
- **Date:** 2026-08-27
- **Primary structure:** Supersession-scope failure
- **Secondary structure:** Transition / closure failure
- **Event evidence:** R2 for corrected current interpretation; R1 for the first
  over-subtracted candidate

## Reconstruction

During program-level recurrence recomputation, the NFC/AQFT current slot was at
risk of treating FCP-22 as though it wholly superseded FCP-6.

The corrected recurrence record says instead:

```text
FCP6 = HISTORICAL_ARTIFACT_IMMUTABLE
FCP22 = PARTIAL_CURRENT_SUBCLAIM_SUPERSESSION

CURRENT_NFC_AQFT_SLOT =
FCP6_UNAFFECTED_RELATIONS_PLUS_FCP22_DELTA
```

It explicitly restores still-current FCP-6 generic E5 support at:

```text
K1; K2; K3; K7; K8
```

while allowing the FCP-22 delta to govern the affected subclaims.

Evidence:

- https://github.com/etblink/Foundational-Convergence-Program/commit/46300a1fde35ccf1ebfa63807e5a203f13cd6498

## Why this matters

Supersession is not necessarily a Boolean relation between documents.

A later artifact can supersede:

- one claim;
- one interpretation;
- one method;
- one time-indexed status;

without superseding every still-valid statement in the earlier artifact.

Candidate requirement:

```text
SUPERSESSION MUST HAVE SCOPE
```

and possibly:

```text
CURRENT STATE = UNAFFECTED PRIOR CONTENT + SUPERSEDING DELTA
```

rather than:

```text
CURRENT STATE = LATEST DOCUMENT ONLY
```

---

# TP-003 — Representability was over-promoted into framework identity

- **Project:** Foundational Convergence Program
- **Date:** 2026-08-29
- **Primary structure:** Wrong promotion / transition failure
- **Secondary structure:** Authority-scope failure
- **Event evidence:** R2
- **Initiative evidence:** R2 at process level

## Reconstruction

`OBJ-CAT-11` had initially been mapped to existing `FW-GPTOPT` / `FW-CQM`
framework identity.

The bounded re-adjudication found that the evidence established categorical or
operational **representability**, but not existing-framework **identity
coverage**.

The correction changed:

```text
OBJ_CAT_11_G_OLD = FAIL
OBJ_CAT_11_G_NEW = PASS

OBJ_CAT_11_DISPOSITION_OLD = EXISTING_FRAMEWORK_MAPPING
OBJ_CAT_11_DISPOSITION_NEW = DEFERRED_REMAINDER
```

while keeping the frozen admission result failed because criterion C remained
failed and no other A–H criterion was reopened.

Evidence:

- https://github.com/etblink/Foundational-Convergence-Program/commit/4f73ea29cf4b89e42bf52876b4ad7c782030edbc

## Why this matters

The failure was not lack of evidence. It was an invalid **promotion relation**:

```text
REPRESENTABLE_IN_X
!=
IDENTITY_IS_X
```

This supports a general distinction between:

```text
evidence relation
classification relation
state transition
```

A true relation does not automatically license every stronger transition built
on top of it.

---

# TP-004 — Functional acceptance did not authorize the next product phase

- **Project:** HiVenues
- **Date:** 2026-09-15
- **Primary structure:** Transition gating
- **Secondary structure:** Negative-knowledge preservation
- **Event evidence:** R2

## Reconstruction

Issue #272 records:

```text
FUNCTIONAL_REMEDIATION = ACCEPTED
PRE_ASTRA_VISUAL_GATE = FAIL / PREMATURE
ASTRA_REGRESSION_271 = HOLD
FIRST_CUSTOMER_267 = HOLD
```

The accepted functional state therefore did **not** authorize transition into
independent Astra regression or the first-customer trial.

The issue required an explicit Project Lead visual decision before #271 could
resume.

Evidence:

- https://github.com/etblink/HiVenues/issues/272
- https://github.com/etblink/HiVenues/issues/271
- https://github.com/etblink/HiVenues/issues/267

## Why this matters

A project phase can be locally successful while the transition predicate for
the next phase remains false.

Candidate rule:

```text
PHASE_SUCCESS
!=
NEXT_PHASE_AUTHORIZED
```

The transition itself is a separate claim with its own evidence burden.

---

# TP-005 — Negative knowledge was preserved as explicit reopen predicates

- **Project:** Foundational Convergence Program
- **Date:** 2026-09-10
- **Primary structure:** Negative-knowledge preservation
- **Event evidence:** R2

## Reconstruction

The post-recurrence sequencing adjudication selected:

```text
EVIDENCE_TRIGGERED_HOLD__NO_IMMEDIATE_NEW_SCIENTIFIC_OPERATION_SELECTED
```

and explicitly prohibited:

```text
FCP27_SELECTED = NO
NEW_EXTERNAL_SOURCE_SEARCH_SELECTED = NO
RECURRENCE_REOPENED = NO
PROCESS_MATRIX_STAGE2_REOPENED = NO
EMPIRICAL_ESCALATION_SELECTED = NO
TENSOR_FRAMEWORK_ESCALATION_SELECTED = NO
CATEGORY_B_RECURRENCE_CONSISTENCY_DOCKETS_PROMOTED = NO
```

More importantly, it preserved **conditions under which these routes could be
reopened**.

For recurrence:

> Reopen only if a new pairwise slot, supersession event, E-class change,
> missing/double-counted slot, or material recurrence-method defect is
> established.

For FCP-27:

```text
FCP27_SELECTION_BY_SEQUENCE_NUMBER = FORBIDDEN
```

Evidence:

- https://github.com/etblink/Foundational-Convergence-Program/commit/98e02f288b12948dc382be7c0c23f105dddb801b

## Why this matters

This is stronger than remembering:

> "We decided not to do X."

The durable object is:

```text
X IS CLOSED UNDER CURRENT EVIDENCE
REOPEN X ONLY IF CONDITION Y BECOMES TRUE
```

That is executable negative knowledge.

---

# TP-006 — HiVenues held later trials rather than merely remembering that they were "not next"

- **Project:** HiVenues
- **Date:** 2026-09-15
- **Primary structure:** Negative-knowledge / hold-state preservation
- **Event evidence:** R2

## Reconstruction

The #272 visual-convergence gate did not merely say "visual work comes first."

It explicitly encoded:

```text
ASTRA_REGRESSION_271 = HOLD
FIRST_CUSTOMER_267 = HOLD
```

and required:

```text
#272 visual convergence
→ Project Lead visual gate PASS
→ #271 independent regression
→ acceptance
→ #267 first-customer trial
```

Issue #271 independently says that regression readiness is not first-customer
acceptance, and #267 preserves its own clean-room and truthfulness boundaries.

Evidence:

- https://github.com/etblink/HiVenues/issues/272
- https://github.com/etblink/HiVenues/issues/271
- https://github.com/etblink/HiVenues/issues/267

## Why this matters

"Not yet" is not a weak note. It is a state with a release condition.

Candidate rule:

```text
HOLD = NEGATIVE KNOWLEDGE + REOPEN CONDITION
```

---

# TP-007 — Observatory target selection, preregistration, and execution were separated into distinct transitions

- **Project:** Project Observatory / NFC
- **Date:** 2026-09-11
- **Primary structure:** Transition-control positive case
- **Event evidence:** R2

## Reconstruction

Commit `1a8cad05...` selected `OBS-U001` while explicitly recording:

```text
TARGET_SELECTED
AUDIT_NOT_PREREGISTERED
AUDIT_NOT_EXECUTED
```

The next commit `89c799c2...` preregistered the audit while still recording:

```text
PREREGISTERED
AUDIT_NOT_EXECUTED
```

Evidence:

- https://github.com/etblink/Project-Observatory/commit/1a8cad05a8fba93f9bd9ef476222efccaa8d7782
- https://github.com/etblink/Project-Observatory/commit/89c799c2d6d03a300971db01760f95e6aee05739

## Why this matters

This is a clean positive control for **non-collapsed transitions**.

The following were represented as different states:

```text
candidate exists
→ target selected
→ audit preregistered
→ audit executed
→ result adjudicated
→ downstream mutation considered
```

The system was not allowed to jump directly from "interesting question" to
"new scientific conclusion."

---

# TP-008 — Historical provenance was recovered without becoming newly executed/current authority

- **Project:** Project Observatory
- **Date:** 2026-09-14
- **Primary structure:** Authority / supersession positive case
- **Event evidence:** R2

## Reconstruction

Snapshot v0.2 recovered four exact historical Observatory artifacts into the
current lineage because downstream records already referenced them.

The snapshot explicitly preserved the distinction:

- the original SHAs remain the historical execution/provenance identities;
- recovery onto the current lineage does not mean the audits were newly
  executed;
- Snapshot v0.1 is not rewritten;
- v0.2 supersedes v0.1 only as the **current reconstruction layer**.

Evidence:

- https://github.com/etblink/Project-Observatory/commit/d9d7c6f272f1982d9e644d1987b3308ef51ca324

## Why this matters

The same artifact can have several different relations to the present:

```text
historically true
historically executed
currently discoverable
currently authoritative
currently superseded
```

Collapsing these relations produces authority drift.

---

# Targeted-pass result

The three candidate structures survive targeted sampling as **distinct but
interacting** phenomena.

## Transition failure

Working definition:

> A project, claim, artifact, or operation is moved into a stronger or later
> state without satisfying the transition predicate for that move.

Examples:

- existing-framework promotion for OBJ-CAT-11;
- functional acceptance treated as insufficient for visual/Astra transition;
- selection kept separate from preregistration/execution.

## Authority / supersession failure

Working definition:

> Information is interpreted using the wrong repository, source hierarchy,
> temporal authority, supersession scope, or current/historical relation.

Examples:

- wrong-repository sentinel;
- partial FCP-6/FCP-22 supersession;
- historical Observatory provenance recovered without becoming new execution.

## Negative-knowledge failure

Working definition:

> A route known to be held, rejected, exhausted, forbidden, or unjustified
> loses its closure condition and becomes available again merely because it is
> locally salient.

Positive controls show that robust negative knowledge is not just a sentence.
It has the form:

```text
ROUTE = CLOSED / HELD
BASIS = ...
REOPEN_IF = ...
```

---

# Strongest new empirical inference

A long-horizon project state is not adequately represented by a list of facts.

It needs at least:

```text
FACT
STATUS
AUTHORITY
TIME / SCOPE
ALLOWED TRANSITIONS
FORBIDDEN TRANSITIONS
REOPEN CONDITIONS
```

This is still an empirical inference, not yet an architectural specification.
