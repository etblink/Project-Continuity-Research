# CPI-0 Stage-6D Independent Corrective Re-Audit Launch Prompt 0.1.0

Date: 2026-10-04
Status: FROZEN EXECUTION PROMPT
Program: CPI-0 — Cross-Project Interoperability
Parent audit: Stage 6B / Issue #21
Corrective implementation: Stage 6C / Issue #22

## Role

You are the independent evaluator for CPI-0 Stage 6D.

Your task is to determine whether the Stage-6C repair actually closes all four Stage-6B S2 findings **without introducing a new S2/S3 defect**.

You did not author the Stage-6C repair.

Do not assume that passing self-tests proves correctness.

## Control identities

Stage-6B independent audit commit:

`4e4d2c6b73e9e5a55fd2968de2f59a62bf55101c`

Stage-6C corrective report commit:

`d2f452bc6d36175869bf8ef11078aa92c3cb6d4b`

Repair branch:

`repair/cpi0-stage6c-audit-findings`

Required Stage-6D audit branch:

`audit/cpi0-stage6d-independent-reaudit`

## Governing evidence

Read first:

1. `prototype/cpi0/stage6b/STAGE6B_INDEPENDENT_SOURCE_CONTRACT_SUFFICIENCY_AUDIT_REPORT_0_1_0.md`
2. `prototype/cpi0/stage6c/STAGE6C_CORRECTIVE_PREREGISTRATION_0_1_0.md`
3. `prototype/cpi0/stage6c/EXPERIMENT_REPORT_0_1_0.md`

Then independently inspect the native project sources required to verify each finding.

Do not use prior conversation memory as evidence.

## Findings that must be re-adjudicated

### CPI6B-001 — FCP source-contract omission

Verify independently that Stage 6C now:

- identifies the controlling present-tense routing rather than a historical checkpoint;
- reconstructs `POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION`;
- preserves `YES__STANDING_PROJECT_LEAD_DELEGATION`;
- preserves the sequencing-only boundary;
- preserves the prior evidence-triggered hold as fulfilled history;
- fails closed if the current-routing precedence anchor is absent.

Inspect native FCP sources, not only Stage-6C fixtures.

### CPI6B-002 — HiVenues source-contract omission

Verify independently that Stage 6C now:

- includes PR #399 as the current Stage-5D candidate at the frozen boundary;
- includes the owner decision comment 5981621191;
- preserves owner result `FAIL`;
- preserves draft/unmerged status;
- preserves “do not proceed D–E” and “do not declare #374 satisfied”;
- represents the next action as redesign review rather than pending acceptance/progression;
- fails closed if PR #399 or the owner-decision source is absent.

Inspect native HiVenues issue/PR/comment state.

### CPI6B-003 — projection/profile defect

Verify independently that profile `0.1.1`:

- is additive and does not rewrite frozen 0.1.0;
- requires `producer` and `observed_at`;
- requires typed `source_kind` and source-native `revision`;
- retains commit identity for Git sources;
- can represent issue/comment/PR authority without pretending repository main is that source's revision;
- detects a changed comment/issue revision while main remains unchanged;
- validates all Stage-6C generated project projections.

Look for any new ambiguity caused by the revision model.

### CPI6B-004 — Observatory comparison defect

Verify independently that Stage 6C:

- does not rewrite Snapshot v0.2;
- does not give it blanket historical validity;
- marks the FCP state component as contradicted by the exact native FCP commit it cites;
- preserves the HiVenues historical identity separately as stale relative to current main;
- returns `MIXED__NO_BLANKET_VALIDITY`.

## New-defect search

Do not limit the audit to confirming the four repairs.

Actively search for new S2/S3 defects, especially:

- source revision identities that are not sufficiently content-bound;
- source-contract selection that still depends on hand-picked excerpts in a way that can silently miss later authority;
- owner/human authority that can change without revision detection;
- PR state that can change without revision detection;
- FCP current-routing extraction that could again choose a stale repeated field;
- profile validator behavior inconsistent with generated projections;
- invalid source-kind assumptions;
- cross-project authority leakage;
- observer-oracle behavior;
- false HiVenues/Hive -> NFC/PGH scientific bridge promotion.

## False-bridge control

Required absent new native scientific evidence:

```text
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

## Federation optionality

Reconstruct controlling state from native project sources.

Required:

`FEDERATION_OPTIONALITY = PASS`

CPI/Observatory must remain derived and optional.

## Severity

- S0 — cosmetic / no decision effect
- S1 — orientation degradation but safe consequence unchanged
- S2 — materially wrong next action, authority interpretation, or state conclusion
- S3 — prohibited canonical mutation or external consequence could be authorized/encouraged

## Finding classes

Use one primary class per finding:

- `CLOSED`
- `REPAIR_INCOMPLETE`
- `NEW_SOURCE_CONTRACT_DEFECT`
- `NEW_EXTRACTION_DEFECT`
- `NEW_PROFILE_SCHEMA_DEFECT`
- `NATIVE_GOVERNANCE_AMBIGUITY`
- `NONMATERIAL_DETAIL_DIFFERENCE`
- `EVALUATOR_UNCERTAINTY`

## Required output

Commit exactly one report:

`prototype/cpi0/stage6d/STAGE6D_INDEPENDENT_CORRECTIVE_REAUDIT_REPORT_0_1_0.md`

The report must include:

1. evaluator identity and independence statement;
2. exact control commits;
3. native sources inspected;
4. adjudication of CPI6B-001 through CPI6B-004 individually;
5. positive controls;
6. new-defect search;
7. false-bridge control;
8. federation-optionality result;
9. mutation audit;
10. final disposition.

## Final disposition

Use exactly one:

- `PASS__ALL_STAGE6B_FINDINGS_CLOSED`
- `PASS_WITH_NONMATERIAL_FINDINGS`
- `REPAIR_REQUIRED`
- `ARCHITECTURE_RECONSIDERATION_REQUIRED`
- `INSUFFICIENT_AUDIT`

Any unresolved S2 means at least `REPAIR_REQUIRED`.

Any S3 or systematic dependence on hidden/ad hoc semantics should trigger consideration of `ARCHITECTURE_RECONSIDERATION_REQUIRED`.

## Write boundary

Write only the required Stage-6D report on:

`audit/cpi0-stage6d-independent-reaudit`

Do not modify:

- NFC;
- FCP;
- PGH;
- HiVenues;
- Project Observatory;
- Stage-6A artifacts;
- Stage-6B report;
- Stage-6C implementation.

Do not merge.

## Stop rule

After committing the Stage-6D report, stop.

Do not repair findings.
Do not merge.
Do not proceed to live integration.
