# CPI-0 Stage-6J Independent Authority-Surface and Stabilization Re-Audit Launch Prompt 0.1.0

Date: 2026-10-04
Status: FROZEN EXECUTION PROMPT
Program: CPI-0 — Cross-Project Interoperability

## Role

You are the independent evaluator for CPI-0 Stage 6J.

You did not author Stage 6I.

Your task is to determine whether Stage 6I actually closes all three Stage-6H S2 findings without introducing a new S2/S3 defect.

Treat Stage-6I self-tests, CI, reports, and prior conclusions as claims to be independently checked, not as proof.

Do not use prior conversation memory as audit evidence.

## Controlling evidence

Independent Stage-6H evaluator:

`Grok (xAI)`

Published independent Stage-6H report:

```text
commit =
812be7c178686ebd9971867a21b08b52bedb53b5

blob =
f62d6dda4cee95c21b6b772d24583113cb4176f6

disposition =
REPAIR_REQUIRED
```

Stage-6H findings:

- CPI6H-001 — S2 — review / inline-review surfaces semantically discarded;
- CPI6H-002 — S2 — native-direct provenance / receipts caller-self-attested;
- CPI6H-003 — S2 — no coherent/stabilized observation cut;
- CPI6H-004 — S1 — repository case aliases fail closed.

Stage-6I corrective report commit:

`8de13f30373a886eb47f4180ddbaf91752af6751`

Successful exact-head Stage-6I qualification run:

`37237516543`

## Provenance note

The remote Stage-6H audit branch contains an earlier non-independent OpenAI report commit before the published Grok report.

The Stage-6I repair branch intentionally starts from the clean Stage-6H launch-control lineage and cites the exact independent Grok report blob.

Do not mistake the two-commit remote Stage-6H publication history for a one-commit independent branch.

Assess whether this provenance handling is adequate.

## Read first

1. the exact Stage-6H Grok report at commit/blob above;
2. `prototype/cpi0/stage6i/STAGE6I_AUTHORITY_STABILIZATION_CORRECTIVE_PREREGISTRATION_0_1_0.md`;
3. `prototype/cpi0/stage6i/EXPERIMENT_REPORT_0_1_0.md`;
4. `prototype/cpi0/stage6i/STAGE6I_CLEAN_CHECKOUT_QUALIFICATION_0_1_0.md`;
5. exact Stage-6I implementation:
   - `prototype/cpi0/cpi_profile_v0_1_4.py`
   - `prototype/cpi0/stage6i/collector.py`
   - `prototype/cpi0/stage6i/adapter.py`
   - `prototype/cpi0/stage6i/test_stage6i.py`

Then inspect native project evidence independently.

## A. Required executable validation

Run from a clean checkout:

```text
python -m py_compile \
  prototype/cpi0/cpi_profile_v0_1_4.py \
  prototype/cpi0/stage6i/collector.py \
  prototype/cpi0/stage6i/adapter.py \
  prototype/cpi0/stage6i/test_stage6i.py

python -m unittest -v prototype/cpi0/stage6i/test_stage6i.py
```

Record exact result.

If executable validation is blocked, do not silently waive it.

## B. Re-audit CPI6H-001 — authority-surface survival

Independently verify that every enumerated authority-capable surface is preserved as a first-class source:

- Issue #398 comments;
- Issue #374 comments;
- open-PR conversation comments;
- PR reviews;
- inline PR review comments.

Attempt to reproduce Grok's exact attack:

1. add/inject an OWNER review on current PR #399 with:
   - review state = APPROVED;
   - body = owner acceptance PASS / approved for merge;
2. preserve the existing current rejection/HOLD evidence;
3. verify the review survives collection into a content-bound source;
4. verify current authority adjudication detects conflict and fails closed.

Also test:

- OWNER CHANGES_REQUESTED review;
- owner inline review comment with explicit PASS or FAIL/HOLD language;
- nondecisional owner review/comment remains visible but does not become acceptance;
- historical PR #397 owner evidence does not incorrectly become current PR #399 authority;
- Issue #374 Stage-5D/current-PR evidence is not silently omitted.

Search for any enumerated source kind that can still be discarded before authority adjudication.

## C. Re-audit CPI6H-002 — production native trust boundary

Inspect the actual public current-state API.

Verify:

- production `collect_hivenues_current()` accepts no caller-supplied reader/transport/receipt;
- production `adapt_hivenues_current()` accepts no caller-supplied reader/transport/receipt;
- the production collector constructs the direct GitHub REST transport internally;
- transport returns raw JSON only;
- collector constructs endpoint/page/count/ID/digest receipts itself;
- internal test-transport bundles are permanently nonauthoritative;
- an internal/test bundle is rejected by the authoritative semantic path.

Attempt to reproduce the Stage-6H fake `native_direct` attack through the **public production API without modifying or monkeypatching the CPI implementation**.

If impossible, distinguish that from a hostile same-process code-modification threat, which is outside the declared Stage-6I application/API trust boundary.

Attack receipt integrity:

- endpoint mismatch;
- count mismatch;
- ID mismatch;
- nonempty terminal page;
- noncontiguous pages.

Determine whether caller self-attestation still exists in the production current path.

## D. Re-audit CPI6H-003 — stabilized observation

Verify the production semantics no longer claim an atomic GitHub instant.

Required current claim:

`stable_across_two_consecutive_complete_native_sweeps`

with:

- window_start;
- window_end;
- stable_digest;
- consecutive_equal_sweeps >= 2.

Reproduce:

### A/A
Two identical sweeps should stabilize.

### A/B/B
Must not accept A/B. It may accept only after B/B.

### A/B/C/D
Must fail closed if no consecutive pair is equal within the bound.

### Authority mutation
Change an owner comment or PR review between sweeps. The digest must change.

### Current-source race analysis
Actively inspect whether a materially changing native source can still be omitted while the system claims the weaker stable-window property.

Do not hold Stage 6I to an atomic-snapshot guarantee it explicitly no longer claims.

However, report any S2 if the stated stable-window semantics themselves can materially misrepresent the collected current authority.

Inspect pagination races and source-set ordering carefully.

## E. Exercise the real production GitHub path

Where possible, call the exact Stage-6I production path against live HiVenues read-only GitHub state.

Verify:

- production, not a fake transport, is exercised;
- two consecutive sweeps stabilize;
- open PR set is independently reconstructed;
- PR reviews and inline review comments appear as observed sources;
- Issue #374 comments appear as observed sources;
- the current semantic state is independently reconstructed.

If HiVenues legitimately advances after Stage 6I, distinguish later advancement from a Stage-6I mechanism defect.

## F. Profile 0.1.4

Adversarially inspect:

- new PR-review source identity/revision;
- new inline-review-comment source identity/revision;
- content digest binding;
- repository binding;
- stable observation metadata requirement for GitHub-source projections;
- cross-repository substitution from Stage 6F;
- malformed review/review-comment descriptors.

Ensure 0.1.4 did not weaken 0.1.3.

## G. Previously closed project controls

### FCP

Reconfirm full native-file routing with historical multiplicity:

```text
POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION
YES__STANDING_PROJECT_LEAD_DELEGATION
SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION
```

### HiVenues

At the relevant frozen/native boundary, independently determine:

- merged main vs candidate;
- current Stage-5D candidate;
- owner acceptance state;
- D-E authorization;
- #374 status;
- next safe action.

### NFC

Publication main must remain distinct from theorem-bearing authority.

### PGH

Physical trials remain unauthorized; apparatus remains a real prerequisite.

### Project Observatory

Must remain derived, unmodified, and non-oracular.

## H. False-bridge control

Absent new theory-specific native evidence:

```text
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

for HiVenues/Hive -> NFC/PGH.

## I. Federation optionality

Required unless independently falsified:

`FEDERATION_OPTIONALITY = PASS`

Native projects must remain reconstructible without CPI/Project Observatory as controlling authority.

## J. CPI6H-004

Re-evaluate the S1 repository-case alias limitation.

It may remain an S1 if it still only fails closed.

Do not upgrade it merely because it remains unfixed; upgrade only if you establish material wrong-state/authority consequences.

## K. New-defect search

Actively search for new S2/S3 defects, especially:

- owner-decision heuristic false-positive/false-negative behavior;
- a review surface preserved as a source but still excluded from current authority scope;
- current PR selection ambiguity;
- test-only seams leaking into production authority;
- collector receipt/data mismatch;
- stabilization digest omitting a material source surface;
- two equal sweeps over a materially incomplete declared universe;
- pagination instability;
- live source changes between sweeps;
- profile/adapter disagreement;
- derived observer authority leakage.

## Finding severity

- S0 — cosmetic;
- S1 — orientation degradation / fail-closed inconvenience;
- S2 — materially wrong next action, authority interpretation, or state conclusion;
- S3 — prohibited canonical mutation or external consequence could be authorized/encouraged.

## Required output

Commit exactly one report:

`prototype/cpi0/stage6j/STAGE6J_INDEPENDENT_AUTHORITY_STABILIZATION_REAUDIT_REPORT_0_1_0.md`

The report must include:

1. evaluator identity and independence statement;
2. exact control commits/blobs;
3. executable results;
4. CPI6H-001 re-adjudication;
5. CPI6H-002 re-adjudication;
6. CPI6H-003 re-adjudication;
7. CPI6H-004 disposition;
8. real production GitHub-path audit;
9. profile-0.1.4 adversarial audit;
10. previously closed project controls;
11. new-defect search;
12. false-bridge control;
13. federation optionality;
14. mutation audit;
15. final disposition.

## Final disposition

Use exactly one:

- `PASS__STAGE6H_S2_FINDINGS_CLOSED`
- `PASS_WITH_NONMATERIAL_FINDINGS`
- `REPAIR_REQUIRED`
- `ARCHITECTURE_RECONSIDERATION_REQUIRED`
- `INSUFFICIENT_AUDIT`

Any unresolved S2 means at least `REPAIR_REQUIRED`.

## Write boundary

Write only the required Stage-6J report to the dedicated Stage-6J audit branch.

Do not repair findings.
Do not merge.
Do not mutate NFC, FCP, PGH, HiVenues, or Project Observatory.
Do not enter live federation or live Observatory integration.

## Stop rule

After committing the Stage-6J report, stop.

Report:

- audit commit;
- report blob;
- executable result;
- finding count/severity;
- final disposition.
