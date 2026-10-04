# CPI-0 Stage-6I Authority-Surface and Stabilized-Observation Corrective Report 0.1.0

Date: 2026-10-04
Status: FROZEN CORRECTIVE RESULT — INDEPENDENT RE-AUDIT REQUIRED
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #28

## 1. Controlling audit evidence

Independent Stage-6H evaluator:

`Grok (xAI)`

Published report:

```text
commit =
812be7c178686ebd9971867a21b08b52bedb53b5

blob =
f62d6dda4cee95c21b6b772d24583113cb4176f6

disposition =
REPAIR_REQUIRED
```

Stage 6H found:

- CPI6H-001 — S2 — reviews/inline review comments discarded before authority adjudication;
- CPI6H-002 — S2 — native-direct provenance and receipts caller-self-attested;
- CPI6H-003 — S2 — sequential live reads lacked a coherent/stabilized observation cut;
- CPI6H-004 — S1 — repository case alias limitation.

## 2. Stage-6H publication-history preservation

The published remote Stage-6H audit branch is two commits ahead of launch-control because an earlier non-independent OpenAI report commit remained in remote history.

The final Grok report blob is exact independent audit content, but that remote branch is not represented as one-commit-clean.

Stage 6I intentionally began from the clean Stage-6H launch-control commit:

`19d7a2ec1854d003191f39f3cff07a1ec26fc28c`

and referenced the exact Grok blob as controlling evidence.

No Stage-6H audit artifact was rewritten.

## 3. CPI6H-001 — authority surfaces

### Defect

Stage 6G enumerated PR reviews and inline review comments but discarded their objects before semantic authority adjudication.

### Repair

Stage 6I introduces profile 0.1.4 source kinds:

- `github_pull_request_review`;
- `github_pull_request_review_comment`.

Every enumerated:

- Issue #398 comment;
- Issue #374 comment;
- open-PR conversation comment;
- PR review;
- inline PR review comment

is materialized as a content-bound source object and carried into `observed_sources`.

The live qualified projection contained:

```text
PR_REVIEW_SOURCES = 11
INLINE_REVIEW_COMMENT_SOURCES = 12
ISSUE374_COMMENT_SOURCES = 8
```

### Authority classifier

Current owner acceptance adjudication is scoped to:

- governing Stage-5D Issue #398;
- Issue #374 items tied to Stage 5D / current PR #399;
- the current Stage-5D candidate PR's conversation/review/inline surfaces.

Historical PR #397 owner evidence remains visible but does not become current PR #399 authority.

OWNER review state:

- APPROVED -> PASS candidate;
- CHANGES_REQUESTED -> FAIL_OR_HOLD candidate.

Explicit acceptance/merge/pass or fail/hold/redesign text is also classified.

Material simultaneous PASS and FAIL/HOLD fails closed.

Regression reproducing Grok's attack:

```text
inject OWNER review on PR #399:
state = APPROVED
body = Owner acceptance: PASS. Approved for merge.

existing current rejection/HOLD remains

result =
CONFLICT DETECTED
ADAPTER FAILS CLOSED
```

Corrective evidence status:

`CPI6H-001 = CORRECTIVE_EVIDENCE_PASS`

## 4. CPI6H-002 — production native trust boundary

### Defect

Stage 6G's public current-state API accepted an injected `NativeReader`; `mode = native_direct` and receipts were caller assertions.

### Repair

Stage 6I removes reader/transport injection from the production API.

Public production signatures expose only configuration:

```text
collect_hivenues_current(token=None, max_sweeps=4)

adapt_hivenues_current(token=None, max_sweeps=4)
```

The production collector constructs its own GitHub REST transport internally.

The transport returns only raw JSON.

The collector—not the caller—constructs:

- endpoint URLs;
- pagination sequence;
- page IDs;
- page counts;
- per-page SHA-256;
- empty-page termination;
- receipts.

Receipt validation binds endpoint/count/IDs to the actual rows returned.

### Test seam

An internal fake-transport seam remains for deterministic tests.

Its resulting bundle is always:

`authoritative = false`

and the authoritative semantic path rejects it.

This repairs the application/API trust boundary.

It is not presented as protection against hostile code already able to monkeypatch or modify the running CPI implementation itself.

Corrective evidence status:

`CPI6H-002 = CORRECTIVE_EVIDENCE_PASS`

## 5. CPI6H-003 — stabilized observation window

### Defect

Stage 6G sequentially read native GitHub surfaces then emitted a later point-like observation time without proving one coherent instant.

### Repair

Stage 6I explicitly abandons the atomic-snapshot claim.

One complete native sweep collects every required source surface and computes one content-bound digest over the complete normalized raw source set.

The collector performs repeated complete sweeps until two consecutive sweep digests are identical.

Acceptance condition:

`digest[n-1] == digest[n]`

If no consecutive equal pair occurs within the bounded maximum, current-state reconstruction fails closed.

### Claim semantics

The projection now emits:

```text
mode =
stabilized_native_window

status =
stable_across_two_consecutive_complete_native_sweeps

window_start
window_end
stable_digest
consecutive_equal_sweeps = 2
```

It does not emit or claim:

`complete_at_observation`

or an atomic GitHub transaction.

### Live qualification

```text
WINDOW_START =
2026-10-04T21:46:12Z

WINDOW_END =
2026-10-04T21:46:25Z

STABLE_DIGEST =
3b6439322c5c0497552a8e9f973ddf372e937f2a1e4ee04638ae41f91fcd3530

CONSECUTIVE_EQUAL_SWEEPS =
2
```

Regression controls include:

- A/A -> stable;
- A/B/B -> stable only on B/B;
- A/B/C/D -> fail closed;
- changed owner comment -> digest changes;
- changed PR review -> digest changes.

Corrective evidence status:

`CPI6H-003 = CORRECTIVE_EVIDENCE_PASS`

## 6. Profile 0.1.4

Profile 0.1.4 is additive.

Profiles 0.1.0 through 0.1.3 remain unchanged.

0.1.4 adds content-bound native identities for PR reviews and inline review comments.

Any projection containing GitHub-native sources must also carry stabilized observation metadata with:

- `mode = stabilized_native_window`;
- repository;
- window start/end;
- stable SHA-256 digest;
- at least two consecutive equal sweeps.

Repository-bound identity/content-binding rules from 0.1.3 remain intact.

## 7. Existing closed controls

### Repository substitution

Remains closed.

Both partial and coherent cross-repository rebind attacks remain rejected.

### FCP

The exact frozen full native FCP file still contains 14 historical/current `NEXT_RECOMMENDED_OPERATION` records.

Stage 6I rechecks the same controlling values:

```text
POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION

YES__STANDING_PROJECT_LEAD_DELEGATION

SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION
```

### NFC / PGH

No theorem-authority collapse or physical-trial authorization is introduced.

### False bridge

No HiVenues/Hive -> NFC/PGH dependency is introduced.

### Project Observatory

No mutation and no oracle authority.

## 8. Clean-checkout qualification

Workflow:

`CPI-0 Stage 6I qualification`

Run:

`37237412842`

Qualified code commit:

`bbd9f4708bd9e8e66c1764ae472c5cb74fb8e129`

Result:

```text
COMPILE = PASS
UNITTESTS = 23/23 PASS

STABILIZED_NATIVE_HIVENUES = PASS
OPEN_PRS = [397, 399]

PR_REVIEW_SOURCES = 11
INLINE_REVIEW_COMMENT_SOURCES = 12
ISSUE374_COMMENT_SOURCES = 8

STATE = rejected
NEXT = redesign review
```

See:

`prototype/cpi0/stage6i/STAGE6I_CLEAN_CHECKOUT_QUALIFICATION_0_1_0.md`

## 9. Mutation audit

```text
NFC = NONE
FCP = NONE
PGH = NONE
HIVENUES = NONE
PROJECT_OBSERVATORY = NONE

STAGE6A_THROUGH_STAGE6H = UNCHANGED
LIVE_FEDERATION = NONE
PROJECT_OBSERVATORY_INTEGRATION = NONE
EXTERNAL_PROJECT_EFFECT = NONE

PROJECT_CONTINUITY_RESEARCH_REPAIR_BRANCH = MUTATED
READ_ONLY_NATIVE_GITHUB_QUALIFICATION = YES
```

## 10. CPI6H-004

Repository case alias normalization remains an S1 limitation.

It is fail-closed and was not necessary to close the three S2 defects, so it was not broadened into Stage 6I.

## 11. Stage-6I disposition

```text
CPI6H_001_AUTHORITY_SURFACE_PRESERVATION =
CORRECTIVE_EVIDENCE_PASS

CPI6H_002_NATIVE_PRODUCTION_BOUNDARY =
CORRECTIVE_EVIDENCE_PASS

CPI6H_003_STABILIZED_OBSERVATION =
CORRECTIVE_EVIDENCE_PASS

CPI6H_004_CASE_ALIAS =
S1_UNCHANGED

CLEAN_CHECKOUT_TESTS =
23/23 PASS

LIVE_STABILIZED_NATIVE_PATH =
PASS

INDEPENDENT_CLOSURE =
NOT CLAIMED
```

Final Stage-6I disposition:

`CORRECTIVE_EVIDENCE_PASS__INDEPENDENT_REAUDIT_REQUIRED`

## 12. Next gate

Stage 6J must independently attack:

1. review/inline-source survival;
2. conflicting OWNER approval versus rejection;
3. the public production API for reader/receipt impersonation;
4. internal test seams leaking into current authority;
5. collector-generated receipt integrity;
6. A/B/B and unstable sweep behavior;
7. semantic correctness of stable-window claims;
8. repository-bound identities;
9. FCP regression controls;
10. false-bridge and federation optionality.

No live federation or Project Observatory integration is authorized before Stage 6J.
