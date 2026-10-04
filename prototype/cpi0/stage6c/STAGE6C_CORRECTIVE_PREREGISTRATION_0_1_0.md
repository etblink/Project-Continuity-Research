# CPI-0 Stage-6C Corrective Preregistration 0.1.0

Date: 2026-10-04
Status: FROZEN BEFORE CORRECTIVE IMPLEMENTATION
Program: CPI-0 — Cross-Project Interoperability
Governing repair issue: #22
Parent independent audit: #21
Audit commit: 4e4d2c6b73e9e5a55fd2968de2f59a62bf55101c

## 1. Objective

Repair exactly the four S2 findings frozen by the independent Stage-6B audit without changing the observed projects, Project Observatory, or the frozen Stage-6A/Stage-6B evidence.

The repair must correct the evidence-contract failure modes, not merely hard-code the audited answers.

## 2. Findings under repair

### CPI6B-001 — FCP source-contract omission

Required correction:

- preserve the exact FCP commit/blob identity;
- bind present-tense routing to an explicit current-routing contract;
- include the native precedence rule stating that routing fields inside completed-milestone sections are historical snapshots;
- require the fulfilled PGH trigger and current post-PGH routing markers;
- do not select the first or most convenient occurrence of a repeated `NEXT_RECOMMENDED_OPERATION`;
- emit the current sequencing operation as authorized under standing Project Lead delegation with a sequencing-only consequence ceiling.

Regression requirement:

A source packet containing only the old post-recurrence routing markers must fail `INCOMPLETE`, even if it comes from the correct commit/blob.

### CPI6B-002 — HiVenues source-contract omission

Required correction:

- preserve merged main separately from candidates;
- include PR #397 as the older candidate lineage where useful;
- include current Stage-5D candidate PR #399 and its exact head/state/draft status;
- include the authoritative owner-decision comment on Issue #398;
- represent the owner result as `FAIL`, not merely pending/unsatisfied;
- preserve the explicit stop boundary:
  - PR #399 remains draft/unmerged;
  - do not proceed to D-E;
  - do not declare #374 satisfied;
  - stop for redesign review;
- fail incomplete when the issue revision/comment set needed for the authority decision is absent.

Regression requirement:

Removing the owner-decision comment or PR #399 must fail closed rather than regress to `complete_pending_acceptance`.

### CPI6B-003 — projection schema / source revision defect

Required correction:

Introduce profile version `0.1.1` while preserving the frozen `0.1.0` implementation unchanged.

Every 0.1.1 projection must contain:

- `producer`;
- `observed_at`;
- `profile_version`;
- exact source identities.

Every 0.1.1 observed source must contain:

- `source_id`;
- `repository`;
- `ref`;
- `role`;
- `source_kind`;
- `revision`.

For `source_kind = git`, `commit` remains required.

For non-Git authority surfaces, `revision` must be the source-native/content-bound revision identity rather than the repository main commit.

Initial allowed source kinds:

- `git`;
- `github_issue`;
- `github_issue_comment`;
- `github_pull_request`;
- `derived_snapshot`.

Freshness comparison for profile 0.1.1 must compare `revision`, not assume every source is commit-addressed.

The profile must reject missing or unsupported source kinds/revisions.

Regression requirement:

A changed Issue #398/comment revision with unchanged repository main must classify as stale.

All Stage-6C generated project projections must pass the 0.1.1 validator.

### CPI6B-004 — Observatory blanket historical-validity defect

Required correction:

Do not emit one blanket `VALID_AT_OBSERVATION_BOUNDARY` status for Snapshot v0.2.

Return claim/project-level comparison results.

At minimum:

- HiVenues canonical-identity claim:
  - historical identity may remain valid at the snapshot boundary;
  - current freshness is stale relative to later main;
- FCP project-state claim:
  - snapshot says `WAITING_FOR_EVIDENCE`;
  - exact referenced FCP commit already contains the fulfilled trigger/current post-PGH routing;
  - classify the FCP state claim as contradicted by its referenced native state;
- overall snapshot comparison:
  - `MIXED__NO_BLANKET_VALIDITY`;
  - frozen snapshot rewrite remains unauthorized.

Regression requirement:

A snapshot may not receive blanket validity merely because one checked project identity is historically correct.

## 3. Preservation rule

Do not edit or delete:

- `prototype/cpi0/cpi_profile.py`;
- any Stage-6A artifact;
- the Stage-6B report;
- Project Observatory Snapshot v0.2.

Corrections must be additive/versioned.

## 4. Implementation targets

Expected new artifacts:

- `prototype/cpi0/cpi_profile_v0_1_1.py`;
- `prototype/cpi0/stage6c/source_packets.json`;
- `prototype/cpi0/stage6c/adapter.py`;
- `prototype/cpi0/stage6c/test_stage6c.py`;
- `prototype/cpi0/stage6c/generated_projections.json`;
- `prototype/cpi0/stage6c/EXPERIMENT_REPORT_0_1_0.md`.

No additional core protocol object is authorized by this repair.

## 5. Required corrective tests

At minimum test:

1. FCP current routing resolves to `POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION`.
2. FCP transition state is `selected_authorized`.
3. FCP authorization boundary is sequencing-only.
4. FCP prior evidence hold is retained as fulfilled historical state.
5. FCP packet lacking the precedence/current-routing anchor fails closed.
6. HiVenues current candidate is PR #399.
7. HiVenues owner acceptance result is `FAIL`.
8. HiVenues transition state is `rejected` or another explicit non-progressing state defined by profile 0.1.1.
9. HiVenues stop boundaries D-E / #374 / redesign review are transported as negative knowledge.
10. Removing PR #399 fails closed.
11. Removing owner-decision comment fails closed.
12. All four project projections pass profile-0.1.1 validation.
13. All projections contain producer and observed_at.
14. Issue/comment/PR sources use non-Git revision identities.
15. Changed issue/comment revision with unchanged main is detected as stale.
16. FCP snapshot component is marked contradicted by referenced native state.
17. HiVenues snapshot identity is stale but not retroactively rewritten.
18. Observatory overall validity is `MIXED__NO_BLANKET_VALIDITY`.
19. false HiVenues/Hive -> NFC/PGH dependency remains NONE / held.
20. no observed-project mutation occurs.

## 6. Profile-version rule

`0.1.1` is a corrective semantic-profile version.

It does not claim protocol finality.

The frozen 0.1.0 implementation remains historical evidence of the defect found by Stage 6B.

## 7. Acceptance

Stage 6C may report `CORRECTIVE_PASS` only if:

- every CPI6B finding has at least one direct regression test;
- all generated projections validate under profile 0.1.1;
- the source-removal/revision-skew controls fail closed;
- Stage-6A artifacts remain unchanged;
- no observed project or Observatory mutation occurs.

Self-testing in Stage 6C is not sufficient for a final PASS.

## 8. Next gate

After a Stage-6C corrective pass, require a fresh independent Stage-6D re-audit.

Stage 6D must verify that:

- all four Stage-6B S2 findings are actually closed;
- the repairs did not create a new authority/freshness defect;
- federation optionality and the false-bridge negative control still pass.

No live integration is authorized before that re-audit.
