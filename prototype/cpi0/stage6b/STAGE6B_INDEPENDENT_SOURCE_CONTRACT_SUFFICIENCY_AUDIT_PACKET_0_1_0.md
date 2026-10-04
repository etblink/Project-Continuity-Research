# CPI-0 Stage-6B Independent Source-Contract Sufficiency Audit Packet 0.1.0

Date: 2026-10-04
Status: FROZEN AUDIT PACKET — NOT YET EXECUTED
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #19

Upstream frozen result:

- Stage 6A branch tip: `aac2a05b25bdf2dfb8b1b979645e64824e07adea`
- Stage 6A report: `prototype/cpi0/stage6a/EXPERIMENT_REPORT_0_1_0.md`

## 1. Purpose

Stage 6A established that explicit project-specific source contracts can emit a common CPI projection and fail closed when preregistered required inputs are removed.

Stage 6B asks the stronger question that the Stage-6A author cannot validly answer alone:

> Did the source-contract author omit any decision-critical native fact, prohibition, dependency, acceptance boundary, authority distinction, freshness condition, or canonicality rule that a fresh evaluator would judge necessary for safe cross-project reconstruction?

This is an **independent sufficiency audit**, not another implementation test.

## 2. Independence requirement

The Stage-6B evaluator must not have authored:

- `prototype/cpi0/stage6a/adapter.py`;
- the Stage-6A source contracts;
- the Stage-6A generated projections.

The evaluator may be a fresh human or a fresh independent model/operator.

The evaluator must perform the native-source review **before** studying the adapter implementation in depth.

## 3. Anti-contamination order

The evaluator must follow this order:

### Pass 1 — Native project reconstruction

Read the governing/native sources for each project and independently write the minimum decision-critical state needed for a safe cross-project observer.

Do not inspect:

- `prototype/cpi0/stage6a/adapter.py`;
- `prototype/cpi0/stage6a/generated_projections.json`;
- Stage-6A test assertions beyond the high-level purpose of the audit.

### Pass 2 — Projection comparison

Only after freezing the independent reconstruction, inspect:

- `prototype/cpi0/stage6a/generated_projections.json`.

Compare the independent reconstruction against the CPI projection.

### Pass 3 — Adapter diagnosis

Only if a mismatch or omission exists, inspect:

- `prototype/cpi0/stage6a/adapter.py`;
- `prototype/cpi0/stage6a/source_packets.json`.

Determine whether the defect is:

1. source-contract omission;
2. parser/extraction defect;
3. projection-schema insufficiency;
4. ambiguous native governance;
5. evaluator error;
6. nonmaterial difference.

## 4. Projects under audit

Audit the same four Project Observatory projects:

1. Nested Fibrational Cosmology — NFC
2. Foundational Convergence Program — FCP
3. Physical Grammar Hypothesis — PGH
4. HiVenues

Project Observatory v0.2 is used as a historical observer comparison, not as the authority for those projects.

## 5. Native-source starting points

These are starting points, **not a closed whitelist**.

The evaluator is explicitly allowed to discover additional native authoritative sources if needed.

### NFC

Repository:
`etblink/Nested-Fibrational-Cosmology`

Start with:

- `README.md`
- `PROVENANCE.md`
- `governance/`

Key warning:

Default branch presence must not be assumed to equal theorem authority.

### FCP

Repository:
`etblink/Foundational-Convergence-Program`

Start with:

- `FCP_CHARTER.md`
- `EPISTEMIC_RULES.md`
- `CURRENT_STATE.md`
- `FRAMEWORK_REGISTER.md`
- `SOURCE_REGISTER.md`
- `CLAIM_LEDGER.md`
- relevant current governance/handoff artifacts if required to resolve present routing

Key warning:

Historical result, current prospective interpretation, and current routing state are intentionally distinct.

### PGH

Repository:
`etblink/Physical-Grammar-Hypothesis`

Start with:

- `README.md`
- `CURRENT_STATE.md`
- `HYPOTHESIS.md`
- `RESEARCH_LOG.md`
- `governance/`
- relevant current handoff

Key warning:

A qualified test design is not empirical evidence and an available next target ID is not an assigned target.

### HiVenues

Repository:
`etblink/HiVenues`

Start with:

- `README.md`
- governing doctrine documents under `docs/`
- current roadmap/current architecture
- Issue #398
- PR #397
- parent/relevant issue charters only where needed to resolve authority or current routing

Key warning:

Merged main, open candidate work, automated qualification, owner acceptance, and live external effects are separate authority layers.

## 6. Frozen comparison object

After Pass 1, compare against:

`prototype/cpi0/stage6a/generated_projections.json`

Do not modify the projection before comparison.

## 7. Audit questions

For each project answer all of the following.

### Q1 — Canonical-source sufficiency

Does the projection identify every source identity needed to avoid a materially wrong canonical-state interpretation?

### Q2 — Authority sufficiency

Does it preserve who/what has authority for each material purpose?

### Q3 — Candidate/canonical separation

Could a consumer mistake proposed, candidate, derived, or historical material for accepted canonical state?

### Q4 — Negative-knowledge sufficiency

Are important prohibitions, failed routes, unresolved facts, do-not-assume constraints, non-dependencies, or reopen predicates missing?

### Q5 — Dependency/trigger sufficiency

Could a consumer recommend the wrong next action because a prerequisite, trigger, authorization requirement, or non-dependency was omitted?

### Q6 — Freshness sufficiency

Could a consumer mistake historically valid state for current state, or current state for authority outside its observation boundary?

### Q7 — Human-authority sufficiency

Where a human decision is controlling, is that represented distinctly from machine qualification?

### Q8 — Consequence-boundary sufficiency

Could the projection be read as authorizing a repository write, public deployment, financial/value action, physical experiment, or other external effect that the native project does not authorize?

### Q9 — Supersession sufficiency

Does the projection preserve the scope of what newer state supersedes without rewriting historical provenance?

### Q10 — Omitted-source discovery

Did the evaluator need a native authoritative source that Stage 6A did not declare in its source contract?

If yes, identify it exactly and explain why it is decision-critical.

## 8. Finding classes

Each finding must use exactly one primary class:

- `NO_MATERIAL_OMISSION`
- `SOURCE_CONTRACT_OMISSION`
- `EXTRACTION_DEFECT`
- `PROJECTION_SCHEMA_DEFECT`
- `NATIVE_GOVERNANCE_AMBIGUITY`
- `NONMATERIAL_DETAIL_DIFFERENCE`
- `EVALUATOR_UNCERTAINTY`

Do not silently repair findings while auditing.

## 9. Severity

For any material finding:

- **S0** — cosmetic / no decision effect
- **S1** — orientation degradation but safe consequences unchanged
- **S2** — could cause a materially wrong next action, authority interpretation, or project-state conclusion
- **S3** — could authorize or encourage a prohibited canonical mutation or external consequence

Stage 6B fails if any unresolved S2 or S3 source-contract/projection defect is found.

## 10. Required finding record

For each finding preserve:

```text
FINDING_ID
PROJECT
PRIMARY_CLASS
SEVERITY
NATIVE_SOURCE
EXACT_NATIVE_ASSERTION
WHAT_THE_PROJECTION_SAYS_OR_OMITS
WHY_IT_MATTERS
COUNTERFACTUAL_WRONG_ACTION_OR_INFERENCE
PROPOSED_REMEDIATION
REQUIRES_PROFILE_CHANGE = YES/NO
```

## 11. Positive-control requirement

The evaluator must identify at least one thing the Stage-6A projection got right for each project.

This prevents the audit from becoming a defect-only search with no calibration against the intended semantics.

## 12. Cross-project false-bridge control

The evaluator must specifically assess whether any projection or adapter architecture would encourage this invalid inference:

> Authenticated HiVenues/Hive interaction graphs are empirical evidence for NFC or PGH merely because the projects share finite-relational or graph-like structure.

Expected disposition absent new project-native evidence:

`NO_DEPENDENCY / HELD_SPECULATION`

Any stronger promotion must be treated as a material audit failure unless independently justified by a theory-specific bridge and local project admission.

## 13. Observer-oracle control

Assess whether a user could reconstruct the controlling native state from the cited project sources without Project Observatory or CPI.

Required property:

`FEDERATION_OPTIONALITY = PASS`

If CPI becomes the only intelligible source of truth, Stage 6B fails.

## 14. Final disposition

Use one:

### PASS

No unresolved S2/S3 omission or schema defect found.

### PASS_WITH_NONMATERIAL_FINDINGS

Only S0/S1 findings remain and none changes safe action/authority/state interpretation.

### REPAIR_REQUIRED

At least one S2 defect exists but the common profile remains viable after bounded repair.

### ARCHITECTURE_RECONSIDERATION_REQUIRED

At least one S3 defect exists, or safe reconstruction repeatedly requires hidden/ad hoc project knowledge that cannot be exposed as an auditable source contract.

### INSUFFICIENT_AUDIT

The evaluator could not independently inspect enough native evidence to support a disposition.

## 15. No self-certification

The Stage-6A adapter author may:

- prepare this packet;
- answer factual access questions;
- implement repairs after the audit is frozen.

The Stage-6A adapter author must **not** issue the Stage-6B sufficiency verdict.

## 16. Mutation boundary

This audit authorizes no observed-project mutation and no Project Observatory mutation.

Allowed:

- read-only repository/issue/PR inspection;
- an audit report committed to the CPI research branch;
- later bounded repair to CPI research artifacts after findings are frozen.

Not allowed:

- changing NFC/FCP/PGH/HiVenues to make the adapters easier;
- changing Project Observatory to match the projection;
- live federation;
- automatic cross-project writes.

## 17. Stop point

Freeze the independent audit report and stop.

Do not implement repairs in the same pass that discovers them.

That separation is required so the defect record cannot be cleaned up before it is preserved.
