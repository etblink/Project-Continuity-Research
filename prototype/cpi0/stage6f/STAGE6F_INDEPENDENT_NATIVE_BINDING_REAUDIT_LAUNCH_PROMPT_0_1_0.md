# CPI-0 Stage-6F Independent Native-Binding Re-Audit Launch Prompt 0.1.0

Date: 2026-10-04
Status: FROZEN EXECUTION PROMPT
Program: CPI-0 — Cross-Project Interoperability
Parent independent audit: Stage 6D / Issue #23
Corrective implementation: Stage 6E / Issue #24

## Role

You are the independent evaluator for CPI-0 Stage 6F.

You did not author the Stage-6E repair.

Your task is to determine whether Stage 6E actually closes the two unresolved Stage-6D S2 mechanisms without introducing a new S2/S3 defect.

Do not treat the Stage-6E 42/42 self-qualification as proof.

## Control identities

Stage-6D independent audit commit:

`ab9e4db3359613efcf03ffdf58d36ef8f09a276a`

Stage-6E corrective report commit:

`6ceac2fc650c82a136a28fcc86ec144e66adb94b`

Stage-6E repair branch:

`repair/cpi0-stage6e-native-binding`

The audit must run from the exact Stage-6F launch-control commit containing this prompt.

## Governing evidence

Read first:

1. `prototype/cpi0/stage6d/STAGE6D_INDEPENDENT_CORRECTIVE_REAUDIT_REPORT_0_1_0.md`
2. `prototype/cpi0/stage6e/STAGE6E_NATIVE_BINDING_CORRECTIVE_PREREGISTRATION_0_1_0.md`
3. `prototype/cpi0/stage6e/EXPERIMENT_REPORT_0_1_0.md`
4. `prototype/cpi0/stage6e/STAGE6E_CONNECTOR_QUALIFICATION_0_1_0.md`

Then inspect the implementation and native projects independently.

Do not use prior conversation memory as evidence.

## Finding A — native-source binding / source-set completeness

Stage 6D found that Stage 6C could carry a correct native commit/blob identity while parsing hand-curated semantic text that was not the native object.

Attempt to break the Stage-6E repair.

### Git sources

Verify that the Stage-6E mirrored files are byte-identical to their upstream native blobs:

- NFC PROVENANCE.md
- FCP CURRENT_STATE.md
- FCP FCP_CHARTER.md
- PGH CURRENT_STATE.md
- HiVenues README.md
- Project Observatory Snapshot v0.2

Do not accept filename/path similarity as proof. Verify Git blob identity or an equivalent byte-level binding.

For FCP specifically:

- confirm the mirror is the **full** native CURRENT_STATE.md;
- confirm multiple historical `NEXT_RECOMMENDED_OPERATION` records remain present;
- confirm the adapter can consume that full file rather than depending on a curated excerpt;
- independently verify that it selects the native post-PGH current routing and standing sequencing-only authorization;
- attack the selector for accidental dependence on one convenient occurrence.

### HiVenues non-Git sources

Verify the frozen native GitHub snapshots against repository-native GitHub state at the Stage-6E boundary.

Check the source-set discovery mechanism, not merely the selected result.

At minimum verify:

- complete Issue #398 conversation stream;
- complete open pull-request enumeration;
- complete open-PR conversation-comment streams;
- review/review-comment pagination evidence;
- PR #399 and owner Issue #398 comment 5981621191;
- owner PR #399 comment 5981621690.

Determine whether a material authority source could still be omitted while the Stage-6E collector calls the set complete.

Distinguish later project advancement from a Stage-6E omission.

## Finding B — profile-0.1.2 source revision enforcement

Attempt to break:

`prototype/cpi0/cpi_profile_v0_1_2.py`

Verify that:

- profile 0.1.2 is additive; 0.1.0 and 0.1.1 remain unchanged;
- arbitrary nonempty revisions are rejected;
- each allowed source kind has enforced revision semantics;
- the revision's native object ID must agree with source fields;
- the revision's content digest must agree with the source descriptor fields;
- Git sources retain commit/path/blob identity;
- issue/comment/PR sources use their own native IDs and content-bound digests;
- freshness accepts validated source objects rather than trusting arbitrary caller strings.

Attack with malformed but superficially plausible source records.

## Required executable-code check

The Stage-6E author could not claim local process execution of:

`prototype/cpi0/stage6e/test_stage6e.py`

The independent evaluator must therefore attempt to execute the committed Stage-6E code/test path in a clean local checkout.

At minimum run:

```text
python -m unittest -v prototype/cpi0/stage6e/test_stage6e.py
```

or an equivalent invocation from the correct working directory.

Also compile/import:

- `prototype/cpi0/cpi_profile_v0_1_2.py`
- `prototype/cpi0/stage6e/collector.py`
- `prototype/cpi0/stage6e/adapter.py`
- `prototype/cpi0/stage6e/test_stage6e.py`

If the environment prevents executable validation, do not silently waive it. Record the limitation and decide whether `INSUFFICIENT_AUDIT` is required.

## Original project-state controls

Recheck independently:

### FCP

Expected frozen-boundary current route:

`POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION`

with:

`YES__STANDING_PROJECT_LEAD_DELEGATION`

and:

`SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION`

while the prior evidence hold remains fulfilled history and FCP27 remains unselected.

### HiVenues

Expected Stage-6E frozen-boundary result:

- merged main remains distinct from candidates;
- current Stage-5D candidate is PR #399;
- PR #399 is draft/unmerged;
- owner acceptance = FAIL;
- concordant owner PR result = HOLD / redesign required;
- do not proceed D-E;
- do not declare #374 satisfied;
- next action = redesign review.

### NFC

Publication main must not become theorem authority.

### PGH

Physical trials remain unauthorized and real apparatus remains required.

### Project Observatory

Snapshot v0.2 must remain unmodified.

Its FCP component must not receive blanket historical validity where its exact native FCP commit contradicts the snapshot state.

## False-bridge negative control

Absent new theory-specific native evidence:

```text
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

for HiVenues/Hive -> NFC/PGH.

## Federation optionality

Required:

`FEDERATION_OPTIONALITY = PASS`

Native projects must remain independently intelligible.

## New-defect search

Actively search for new S2/S3 defects, especially:

- a "complete" discovery contract that can omit authoritative comments/reviews;
- snapshot digests computed over paraphrases rather than native objects;
- source-kind revision grammar that validates inconsistent fields;
- content digests that are not recomputed from collected native objects;
- FCP selector logic that still needs a human-curated semantic window;
- derived-source identity laundering;
- remote authority becoming local authority;
- Project Observatory becoming an oracle.

## Severity

- S0 — cosmetic
- S1 — orientation degradation, safe consequence unchanged
- S2 — materially wrong next action / authority / state conclusion
- S3 — prohibited canonical mutation or external consequence could be authorized or encouraged

## Required output

Commit exactly one report:

`prototype/cpi0/stage6f/STAGE6F_INDEPENDENT_NATIVE_BINDING_REAUDIT_REPORT_0_1_0.md`

Report:

1. evaluator identity / independence;
2. exact control commits;
3. executable-code result;
4. native-source binding audit;
5. source-set completeness audit;
6. profile-0.1.2 adversarial audit;
7. re-adjudication of CPI6B-001 / CPI6B-003 / CPI6D-001 / CPI6D-002;
8. positive controls;
9. new-defect search;
10. false-bridge control;
11. federation optionality;
12. mutation audit;
13. final disposition.

## Final disposition

Use exactly one:

- `PASS__NATIVE_BINDING_AND_REVISION_DEFECTS_CLOSED`
- `PASS_WITH_NONMATERIAL_FINDINGS`
- `REPAIR_REQUIRED`
- `ARCHITECTURE_RECONSIDERATION_REQUIRED`
- `INSUFFICIENT_AUDIT`

Any unresolved S2 means at least `REPAIR_REQUIRED`.

Any S3 or systematic reliance on hidden/ad-hoc authority should trigger consideration of `ARCHITECTURE_RECONSIDERATION_REQUIRED`.

## Write boundary

Write only the Stage-6F audit report to the dedicated Stage-6F audit branch.

Do not modify:

- observed projects;
- Project Observatory;
- Stage-6A through Stage-6E artifacts.

Do not repair.
Do not merge.
Do not enter live integration.

## Stop rule

After committing the report, stop and report:

- audit commit;
- report blob;
- executable test result;
- finding count/severity;
- final disposition.
