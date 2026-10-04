# CPI-0 Stage-6B Independent Evaluator Launch Prompt 0.1.0

Date: 2026-10-04
Status: FROZEN EXECUTION PROMPT
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #19
Governing audit packet:
`prototype/cpi0/stage6b/STAGE6B_INDEPENDENT_SOURCE_CONTRACT_SUFFICIENCY_AUDIT_PACKET_0_1_0.md`

## Role

You are the **independent Stage-6B evaluator** for CPI-0.

You did not author the Stage-6A adapters.

Your task is to determine whether the Stage-6A source contracts and generated CPI projections omit or misrepresent any decision-critical native project semantics.

You are not asked to improve the system during this pass.

You are asked to try to **break the sufficiency claim**.

## Independence boundary

Do not rely on prior conversation memory, prior summaries, or assertions from the adapter author.

Treat the native repositories, issues, PRs, and frozen CPI audit packet as the evidence base.

If you recognize prior context from another interaction, ignore it unless you independently re-establish it from the sources.

Do not ask the Stage-6A author to explain what an adapter was intended to mean before you freeze your independent reconstruction.

## Repositories under audit

Inspect these four projects read-only:

1. `etblink/Nested-Fibrational-Cosmology`
2. `etblink/Foundational-Convergence-Program`
3. `etblink/Physical-Grammar-Hypothesis`
4. `etblink/HiVenues`

Project Observatory is a historical comparison source:

5. `etblink/Project-Observatory`

CPI-0 control repository:

6. `etblink/Project-Continuity-Research`

## CPI research identity

Use the CPI research state containing the completed source preservation and Stage-6B packet:

```text
repository = etblink/Project-Continuity-Research
branch = research/cross-project-interoperability
commit = 3795ceda33b808d29a255e9d14b2d25dccf0181b
```

Read the governing Stage-6B packet first.

## Strict anti-contamination sequence

### PASS 1 — Native reconstruction only

For NFC, FCP, PGH, and HiVenues:

1. inspect the project-native sources;
2. identify what is currently authoritative and for what purpose;
3. reconstruct the minimum state a safe cross-project observer would need;
4. record decision-critical negative knowledge, blockers, dependencies, triggers, authority boundaries, candidate/canonical distinctions, and external-effect ceilings;
5. identify any source whose omission would materially change a safe next action or state interpretation.

During Pass 1, **do not inspect**:

- `prototype/cpi0/stage6a/adapter.py`
- `prototype/cpi0/stage6a/generated_projections.json`
- `prototype/cpi0/stage6a/source_packets.json`
- `prototype/cpi0/stage6a/test_stage6a.py`

Do not use the NotebookLM transcript as authority for any project.

Freeze your Pass-1 reconstruction in your working notes before continuing.

### PASS 2 — Compare against generated projections

Now inspect:

`prototype/cpi0/stage6a/generated_projections.json`

For each project compare your independent reconstruction against the generated projection.

Answer all ten audit questions in the governing packet.

Look especially for:

- missing authority sources;
- omitted negative knowledge;
- incorrect current-state selection from historical prose;
- candidate/canonical collapse;
- missing owner/human acceptance rules;
- omitted external prerequisites;
- absent non-dependencies;
- hidden supersession assumptions;
- freshness ambiguity;
- consequence-class ambiguity.

### PASS 3 — Diagnose only after finding

Only after you have frozen a mismatch may you inspect:

- `prototype/cpi0/stage6a/adapter.py`
- `prototype/cpi0/stage6a/source_packets.json`
- `prototype/cpi0/stage6a/test_stage6a.py`

Classify each mismatch using exactly one primary class:

- `NO_MATERIAL_OMISSION`
- `SOURCE_CONTRACT_OMISSION`
- `EXTRACTION_DEFECT`
- `PROJECTION_SCHEMA_DEFECT`
- `NATIVE_GOVERNANCE_AMBIGUITY`
- `NONMATERIAL_DETAIL_DIFFERENCE`
- `EVALUATOR_UNCERTAINTY`

Use severity:

- S0 — cosmetic / no decision effect
- S1 — orientation degradation but safe action unchanged
- S2 — could cause a materially wrong next action, authority interpretation, or project-state conclusion
- S3 — could authorize or encourage a prohibited canonical mutation or external consequence

## Required project-specific checks

### NFC

Independently determine:

- whether default `main` is theorem-bearing authority;
- the exact theorem-bearing authority source;
- whether publication/provenance authority differs from theorem authority;
- unresolved provenance/intent facts;
- whether any governance source needed for safe interpretation is absent from the Stage-6A projection.

### FCP

Independently determine:

- the distinction among historical result, current prospective result, and current routing state;
- current method/version relevance;
- whether future scientific work requires separate bounded authorization;
- whether the current recommended operation is actually authorized;
- whether historical `EVIDENCE_TRIGGERED_HOLD` language could be mistaken for current routing;
- whether any current register, handoff, claim, or source artifact materially changes the projection.

### PGH

Independently determine:

- active candidate identity;
- empirical status;
- apparatus binding state;
- next scientific operation;
- whether physical trials are authorized;
- target-search restrictions;
- machine-readable `do_not_assume` state;
- whether any current handoff/governance artifact adds a missing decision-critical constraint.

### HiVenues

Independently determine:

- current merged main identity;
- active candidate PR identity and merge state;
- active owner-facing redesign charter;
- who controls the usability acceptance gate;
- relationship among doctrine, roadmap, issues, tests, and owner/operator acceptance;
- whether any live external effect is authorized;
- whether any later issue/PR than #397/#398 changes the current bounded state;
- whether the Stage-6A projection omitted a decision-critical deployment, authority, or consequence boundary.

## Freshness requirement

The native projects may have advanced after the Stage-6A observation boundary.

If so, distinguish:

1. **Stage-6A sufficiency at its frozen observation boundary**, from
2. **current project state now**.

Do not fail Stage 6A merely because a project legitimately advanced later.

But do report if the source contract lacked a mechanism needed to detect or represent that advancement safely.

## False-bridge negative control

The NotebookLM synthesis proposed that HiVenues/Hive interaction graphs could serve as empirical input for NFC/PGH.

Absent independent project-native support for a theory-specific bridge, preserve:

```text
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

Do not promote shared graph-like structure into scientific dependence.

## Observer-oracle control

Confirm that each project remains intelligible from its own native sources.

Required:

```text
FEDERATION_OPTIONALITY = PASS
```

If CPI/Project Observatory becomes the only place from which controlling state can be reconstructed, treat that as a material failure.

## Positive controls

For each project identify at least one important semantic distinction the Stage-6A projection preserved correctly.

This is mandatory.

## Output artifact

Produce exactly one frozen report:

`prototype/cpi0/stage6b/STAGE6B_INDEPENDENT_SOURCE_CONTRACT_SUFFICIENCY_AUDIT_REPORT_0_1_0.md`

The report must contain:

1. evaluator identity/model/environment;
2. exact audit date;
3. exact CPI control commit;
4. native source identities inspected;
5. Pass-1 independent reconstruction for each project;
6. Pass-2 comparison;
7. positive controls;
8. finding records;
9. false-bridge control;
10. observer-oracle control;
11. mutation audit;
12. final disposition.

## Finding record format

For every finding:

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

Do not implement remediation during the audit pass.

## Final disposition

Use exactly one:

- `PASS`
- `PASS_WITH_NONMATERIAL_FINDINGS`
- `REPAIR_REQUIRED`
- `ARCHITECTURE_RECONSIDERATION_REQUIRED`
- `INSUFFICIENT_AUDIT`

Rules:

- unresolved S2 => at least `REPAIR_REQUIRED`;
- any S3, or repeated reliance on hidden/ad hoc knowledge that cannot be made auditable => consider `ARCHITECTURE_RECONSIDERATION_REQUIRED`;
- inability to inspect enough native evidence => `INSUFFICIENT_AUDIT`.

## Write boundary

You may write only the Stage-6B audit report to the designated independent audit branch in Project-Continuity-Research.

Do not modify:

- NFC;
- FCP;
- PGH;
- HiVenues;
- Project Observatory;
- Stage-6A adapters;
- Stage-6A projections;
- the governing audit packet.

Do not merge anything.

## Stop rule

After freezing the audit report, stop.

Do not repair findings.
Do not update the CPI profile.
Do not merge the audit branch.
Do not proceed to live Observatory integration.

Report the audit branch, commit, exact finding count/severity, and final disposition to the project owner.
