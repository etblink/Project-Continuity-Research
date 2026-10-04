# CPI-0 Stage-6H Independent Live-Enumeration Re-Audit Launch Prompt 0.1.0

Date: 2026-10-04
Status: FROZEN EXECUTION PROMPT
Program: CPI-0 — Cross-Project Interoperability
Parent audit: Stage 6F / Issue #25
Corrective implementation: Stage 6G / Issue #26

## Role

You are the independent Stage-6H evaluator.

You did not author Stage 6G.

Determine whether Stage 6G closes the two remaining Stage-6F S2 mechanisms without introducing a new S2/S3 defect.

Do not accept Stage-6G self-tests or CI as proof. Reproduce the attacks independently.

## Control identities

Stage-6F audit commit:

`5de6a9ffe7d3899924426ed8425a4e4150b6ab64`

Stage-6G corrective report commit:

`1650e12234eb3884bd52672c985b5743d039ef95`

Stage-6G successful exact-head qualification run:

`37233555186`

The Stage-6H branch must start from the exact launch-control commit containing this prompt.

## Read first

1. `prototype/cpi0/stage6f/STAGE6F_INDEPENDENT_NATIVE_BINDING_REAUDIT_REPORT_0_1_0.md`
2. `prototype/cpi0/stage6g/STAGE6G_LIVE_ENUMERATION_CORRECTIVE_PREREGISTRATION_0_1_0.md`
3. `prototype/cpi0/stage6g/EXPERIMENT_REPORT_0_1_0.md`
4. `prototype/cpi0/stage6g/STAGE6G_CI_QUALIFICATION_RECORD_0_1_0.md`

Then inspect the implementation and native project evidence.

Do not use prior conversation memory as audit evidence.

## A. Reproduce CPI6F-001 coherent-omission attack

Stage 6F showed that a frozen snapshot could coherently remove an object, adjust its internal ID/count list, and still call itself complete.

Verify that the Stage-6G current-state path cannot be made complete by such a stored-fixture edit.

At minimum establish:

- fixture/offline mode cannot claim current completeness;
- current collection requires `mode = native_direct`;
- native receipts must terminate through actual exhaustive pagination;
- incomplete/unterminated receipt fails;
- native reader failure does not fall back to Stage-6E snapshot;
- current open-PR membership comes from native enumeration rather than hard-coded expected IDs;
- a newly returned PR/comment would enter the collected source set.

Inspect whether any path can set or forge `mode = native_direct` without actually performing native reads. Distinguish interface trust assumptions from snapshot self-attestation. If a caller-supplied fake can trivially impersonate native-direct in production without a protected reader boundary, assess materiality explicitly.

## B. Exercise the real native reader

In a clean checkout, execute the Stage-6G suite.

Also exercise:

`GitHubRestReader -> collect_hivenues_current / adapt_hivenues_current`

against native GitHub read-only state if the environment permits it.

Verify pagination behavior and current source set independently.

Do not fail Stage 6G merely because HiVenues legitimately advances after the Stage-6G observation; separate later advancement from mechanism failure.

## C. Reproduce CPI6F-002 repository-substitution attack

Using exact profile 0.1.3:

1. take a valid GitHub PR/issue/comment source;
2. change only repository while retaining prior repo-local identity/revision;
3. verify validation fails;
4. then coherently rewrite repository, native_id, and revision to another repository;
5. verify freshness against the original observed source still fails because repository identity changed.

Also test malformed repository/native_id/revision combinations.

## D. Source identity/content binding

Verify profile 0.1.3 does not weaken Stage 6E:

- Git content remains blob/content-bound;
- issue/comment/PR revisions remain content-bound;
- repository is included in GitHub native identity and revision;
- content changes still alter revisions.

## E. Closed-regression controls

### FCP

Reconfirm the exact full native `CURRENT_STATE.md` still contains the historical routing multiplicity and that the controlling result remains:

`POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION`

with:

`YES__STANDING_PROJECT_LEAD_DELEGATION`

and:

`SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION`.

### HiVenues

At the Stage-6G frozen boundary, the native-direct result should preserve:

- merged main separate from candidates;
- Stage-5D candidate PR #399;
- owner rejection/HOLD;
- no D-E progression;
- #374 unsatisfied;
- redesign next.

If current native state has legitimately advanced, document the difference rather than rewriting Stage-6G history.

### NFC / PGH

Preserve theorem-authority separation and physical-trial prohibition.

### Observatory

Remain derived, unmodified, and non-oracular.

## F. False-bridge control

Absent new theory-specific native evidence:

```text
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

for HiVenues/Hive -> NFC/PGH.

## G. Federation optionality

Required:

`FEDERATION_OPTIONALITY = PASS`

unless native projects can no longer be reconstructed without CPI.

## H. New-defect search

Actively search for S2/S3 defects, especially:

- a caller being able to impersonate `native_direct` without protected provenance;
- pagination termination that can silently omit pages;
- live-query race/incoherent observation across multiple GitHub endpoints;
- current-state projection mixing objects from materially different observation moments;
- GitHub repository normalization/case ambiguity;
- cross-repository authority leakage;
- regression from Stage-6E content binding;
- a snapshot fixture re-entering the current path.

## Required executable work

Run at minimum:

```text
python -m py_compile \
  prototype/cpi0/cpi_profile_v0_1_3.py \
  prototype/cpi0/stage6g/collector.py \
  prototype/cpi0/stage6g/adapter.py \
  prototype/cpi0/stage6g/test_stage6g.py

python -m unittest -v prototype/cpi0/stage6g/test_stage6g.py
```

If executable validation is blocked, record it explicitly.

## Finding severity

- S0 cosmetic
- S1 orientation degradation only
- S2 materially wrong next action / authority / state conclusion
- S3 prohibited canonical mutation or external consequence could be authorized or encouraged

## Required output

Commit exactly one report:

`prototype/cpi0/stage6h/STAGE6H_INDEPENDENT_LIVE_ENUMERATION_REAUDIT_REPORT_0_1_0.md`

Include:

1. evaluator identity and independence;
2. exact control commits;
3. executable results;
4. coherent-omission attack;
5. direct-native-reader audit;
6. repository-substitution attacks;
7. content-binding audit;
8. re-adjudication of CPI6F-001 and CPI6F-002;
9. closed-regression controls;
10. new-defect search;
11. false-bridge control;
12. federation optionality;
13. mutation audit;
14. final disposition.

## Final disposition

Use exactly one:

- `PASS__LIVE_ENUMERATION_AND_REPOSITORY_IDENTITY_DEFECTS_CLOSED`
- `PASS_WITH_NONMATERIAL_FINDINGS`
- `REPAIR_REQUIRED`
- `ARCHITECTURE_RECONSIDERATION_REQUIRED`
- `INSUFFICIENT_AUDIT`

Any unresolved S2 means at least `REPAIR_REQUIRED`.

## Write boundary

Write only the Stage-6H report on the dedicated audit branch.

Do not repair findings.
Do not merge.
Do not modify observed projects or Project Observatory.
Do not enter live federation/integration.

## Stop rule

After committing the report, stop and report audit commit, report blob, executable result, finding count/severity, and final disposition.
