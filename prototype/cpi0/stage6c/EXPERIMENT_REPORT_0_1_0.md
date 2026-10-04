# CPI-0 Stage-6C Corrective Repair Report 0.1.0

Date: 2026-10-04
Status: FROZEN CORRECTIVE RESULT
Program: CPI-0 — Cross-Project Interoperability
Governing repair issue: #22
Parent independent audit: #21
Parent audit commit: 4e4d2c6b73e9e5a55fd2968de2f59a62bf55101c
Repair branch: repair/cpi0-stage6c-audit-findings

## 1. Objective

Repair exactly the four S2 findings frozen by the independent Stage-6B audit without rewriting the failed Stage-6A experiment, mutating any observed project, or modifying Project Observatory.

The governing preregistration is:

`prototype/cpi0/stage6c/STAGE6C_CORRECTIVE_PREREGISTRATION_0_1_0.md`

## 2. Preservation strategy

Stage 6A remains frozen exactly as audited.

The corrective implementation is additive:

- `prototype/cpi0/cpi_profile_v0_1_1.py`
- `prototype/cpi0/stage6c/source_packets.json`
- `prototype/cpi0/stage6c/adapter.py`
- `prototype/cpi0/stage6c/test_stage6c.py`
- `prototype/cpi0/stage6c/generated_projections.json`

No Stage-6A file was edited or deleted.

## 3. CPI6B-001 — FCP source-contract omission

### Defect

Stage 6A cited the correct FCP commit/blob but selected a superseded routing checkpoint from within `CURRENT_STATE.md`.

### Repair

The Stage-6C FCP contract now requires both:

1. the explicit current post-PGH routing markers; and
2. the native precedence rule stating that completed-milestone routing fields are historical snapshots and that present-tense routing is controlled by the `Open dependencies` / `Next-task status` material.

The corrected projection now records:

```text
NEXT_OPERATION = POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION
STATE = selected_authorized
AUTHORIZATION = YES__STANDING_PROJECT_LEAD_DELEGATION
BOUNDARY = SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION
PRIOR_EVIDENCE_TRIGGERED_HOLD = fulfilled historical state
FCP27_SELECTED = NO
```

### Direct regression controls

- missing precedence anchor -> fail closed;
- old post-recurrence routing only -> fail closed;
- current post-PGH operation -> required;
- sequencing-only authorization -> required.

Corrective status:

`CPI6B-001 = REPAIRED_IN_STAGE6C__PENDING_INDEPENDENT_REAUDIT`

## 4. CPI6B-002 — HiVenues source-contract omission

### Defect

Stage 6A stopped at PR #397 and the Issue #398 body while omitting:

- current candidate PR #399;
- owner-decision comment 5981621191;
- the explicit owner rejection and stop boundary.

### Repair

Stage 6C requires five distinct authority/state surfaces:

- merged main;
- Issue #398 work charter;
- owner-decision comment 5981621191;
- prior candidate PR #397;
- current candidate PR #399.

The corrected projection now records:

```text
MERGED_MAIN = 4fed1b4b...
CURRENT_CANDIDATE = PR #399 @ 28eaf662...
PR399_STATE = draft / open / unmerged
OWNER_ACCEPTANCE = FAIL
CURRENT_CANDIDATE_STATE = rejected
NEXT_ACTION = redesign_review_before_further_broad_implementation
DO_NOT_PROCEED_D_E = preserved
DO_NOT_DECLARE_374_SATISFIED = preserved
EXTERNAL_EFFECT_AUTHORITY = none from CPI shadow reconstruction
```

### Direct regression controls

- remove PR #399 -> fail closed;
- remove owner-decision comment -> fail closed;
- change owner association away from OWNER -> inconsistent/fail closed;
- current candidate must be PR #399;
- transition must be rejected rather than pending acceptance.

Corrective status:

`CPI6B-002 = REPAIRED_IN_STAGE6C__PENDING_INDEPENDENT_REAUDIT`

## 5. CPI6B-003 — common projection/schema defect

### Defect

Stage-6A outputs omitted fields required by the existing validator and represented issue/comment authority using repository-commit freshness.

### Repair

Profile `0.1.1` is additive and versioned. Frozen `0.1.0` remains unchanged.

Every 0.1.1 projection now requires:

- `producer`;
- `observed_at`;
- typed `source_kind`;
- source-native `revision`.

Allowed initial source kinds:

- git;
- github_issue;
- github_issue_comment;
- github_pull_request;
- derived_snapshot.

Git sources still require `commit`.

Freshness under 0.1.1 compares `revision`, not a universal commit field.

Therefore an Issue #398/comment change can become stale even while HiVenues `main` remains unchanged.

All four Stage-6C project projections pass the 0.1.1 validator.

Corrective status:

`CPI6B-003 = REPAIRED_IN_STAGE6C__PENDING_INDEPENDENT_REAUDIT`

## 6. CPI6B-004 — Observatory blanket validity defect

### Defect

Stage 6A checked HiVenues revision divergence and emitted a global-looking:

`VALID_AT_OBSERVATION_BOUNDARY`

even though the same frozen Snapshot v0.2 contains an FCP state contradicted by the exact FCP commit it cites.

### Repair

Stage 6C makes historical validity project/claim-specific.

Result:

### FCP component

```text
SNAPSHOT_STATE = WAITING_FOR_EVIDENCE
REFERENCED_COMMIT = a41bc610...
NATIVE_STATE_AT_SAME_COMMIT = POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION
HISTORICAL_VALIDITY = CONTRADICTED_BY_REFERENCED_NATIVE_STATE
FRESHNESS = same_revision_semantic_conflict
```

### HiVenues identity component

```text
HISTORICAL_VALIDITY = VALID_IDENTITY_AT_OBSERVATION_BOUNDARY
FRESHNESS = stale
REWRITE_AUTHORIZED = false
```

### Snapshot comparison overall

```text
OVERALL_VALIDITY = MIXED__NO_BLANKET_VALIDITY
REWRITE_AUTHORIZED = false
```

The frozen Project Observatory snapshot itself was not changed.

Corrective status:

`CPI6B-004 = REPAIRED_IN_STAGE6C__PENDING_INDEPENDENT_REAUDIT`

## 7. Regression execution

Execution:

```text
python -m unittest -v
```

Result:

```text
Ran 26 tests
OK
```

Python compile validation also passed for:

- `cpi_profile_v0_1_1.py`;
- `stage6c/adapter.py`;
- `stage6c/test_stage6c.py`.

The test suite includes direct controls for all four Stage-6B findings plus preservation controls for:

- NFC theorem-authority separation;
- PGH physical-trial prohibition;
- false HiVenues/Hive -> physics dependency nonpromotion;
- no CPI shadow external-effect authority.

## 8. Stage-6C result

```text
CPI6B_001_FCP_SOURCE_CONTRACT = CORRECTIVE_PASS
CPI6B_002_HIVENUES_SOURCE_CONTRACT = CORRECTIVE_PASS
CPI6B_003_PROFILE_NON_GIT_REVISION = CORRECTIVE_PASS
CPI6B_004_OBSERVATORY_VALIDITY = CORRECTIVE_PASS

REGRESSION_TESTS = 26/26 PASS
PROFILE_VERSION = 0.1.1
STAGE6A_REWRITTEN = NO
STAGE6B_AUDIT_REWRITTEN = NO
OBSERVED_PROJECT_MUTATION = NONE
PROJECT_OBSERVATORY_MUTATION = NONE
LIVE_FEDERATION = NONE
```

Stage-6C disposition:

`CORRECTIVE_PASS__INDEPENDENT_REAUDIT_REQUIRED`

## 9. What is not yet established

Stage 6C is authored by the project lead who implemented the repair.

Therefore it does not independently establish closure of the Stage-6B findings.

It also does not establish:

- automatic source discovery;
- malicious-adapter resistance;
- generality beyond the audited project set;
- safe live federation;
- final protocol adequacy.

## 10. Next gate

Stage 6D must be a fresh independent re-audit.

It should inspect the Stage-6B findings first and then attempt to falsify each claimed repair.

Required question:

> Does profile 0.1.1 plus the Stage-6C source contracts actually close CPI6B-001 through CPI6B-004 without introducing a new S2/S3 defect?

No live Observatory integration is authorized until that gate is independently passed.
