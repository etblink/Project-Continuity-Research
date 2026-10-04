# CPI-0 Stage-6E Connector Qualification Record 0.1.0

Date: 2026-10-04  
Status: FROZEN SELF-QUALIFICATION EVIDENCE  
Governing issue: #24

## Scope

This record qualifies the Stage-6E native-source binding repair directly against the frozen GitHub artifacts using the connected GitHub source.

It is not an independent audit.

## Exact native Git mirror result

All six mirrored Git files have the exact same Git blob SHA as their upstream native source:

- NFC PROVENANCE.md: 69cdd64069cd0d24779a344fac0cd309bc54d811 — exact
- FCP CURRENT_STATE.md: b5949af93a1855ae1d072fa4aaa4b1c29033579c — exact
- FCP FCP_CHARTER.md: 579819121d1733e1746868941a3a282de2cf1ac9 — exact
- PGH CURRENT_STATE.md: 32c799bdd42d6c921140bf13bdb988fefa445169 — exact
- HiVenues README.md: ad9a0c0b64d0e074e0a315450713ddfb3d9c8f6a — exact
- Project Observatory Snapshot v0.2: e62a0b86e2317d7b441eb3d5ecf8ee71cc49460a — exact

Because Git blob identity is content-addressed, these mirrors are byte-identical to the upstream blobs. They are not semantic paraphrases or selected windows.

## Full-source FCP trap

The exact mirrored FCP CURRENT_STATE.md contains:

```text
NEXT_RECOMMENDED_OPERATION occurrence count = 14
```

The native-bound current selector resolves:

```text
EVIDENCE_TRIGGER_PGH =
T1_STABLE_NEW_FOUNDATIONAL_COMPETITOR_CANDIDATE__FULFILLED

NEXT_RECOMMENDED_OPERATION =
POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION

NEXT_OPERATION_AUTHORIZED =
YES__STANDING_PROJECT_LEAD_DELEGATION

NEXT_OPERATION_AUTHORIZATION_BOUNDARY =
SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION

FCP27_SELECTED = NO
NEXT_SCIENTIFIC_PHASE =
NONE__POST_PGH_STAGE2_SEQUENCING_PENDING
```

Thus the corrected result is recovered while all 13 competing historical/current repeated routing records remain present.

## HiVenues source-set completeness

At the frozen collection boundary:

```text
open PR page 1 count = 2
open PR page 2 count = 0
open PR set = {397, 399}

Issue #398 comment page 1 count = 1
Issue #398 comment page 2 count = 0
Issue #398 comment IDs = {5981621191}

PR #399 conversation comment page 1 count = 1
PR #399 conversation comment page 2 count = 0
PR #399 conversation comment IDs = {5981621690}
```

Review and inline-comment second pages for PRs #397 and #399 were also empty.

The collector stores the complete native objects, not summaries.

## Content-bound non-Git identities

Canonical-JSON SHA-256 values frozen into Stage-6E revisions:

```text
Issue #398 =
9af92f821d2acf0a5b260bf1e701b4970c4e80e39ef29b78f13258f28aead231

Issue #374 =
ec4054131d84f540e599476272e6da7db0b0a8f5994fcf8a68ca293abfb89f45

PR #397 =
65bfea553059fbee8c666c2d1ec0c0ad08321b5a0c93276da57ca454ebf3e008

PR #399 =
87f1ed377b82fdb2d480d786a3b770966491e37a6a646d0b62a969a335a8b109

Issue #398 owner comment 5981621191 =
b4c9bfc750813f87d0a581cec9f90aad9269e857b07ed65abe50b34f2f6360f9

PR #399 owner comment 5981621690 =
5c790858775adcf1180c58ac0e814c2113f53573a71458f80f53a77500ec05ff
```

Both owner sources independently preserve the stop/redesign result.

## Exact Git-source SHA-256 values

```text
NFC PROVENANCE =
808beb4fd50b28c4b7e398ed6bc34afaa666c2974945920c71b2507fc31f2910

FCP CURRENT_STATE =
5f4b33e7194a31bdb601f22932690d1bf87a3acad7715cfc349fcb62b2f606f4

FCP CHARTER =
cf51596d591b1165dfd834016dbe13103a570f54a62f9e203bcb5ed300fea05a

PGH CURRENT_STATE =
fc9747c6919654008823b3a83d2a742b83977c72884ff6532a38fe2c042d4363

HiVenues README =
da3b6ceed2da44a215b3ddb023d4471745e808f1ca7afcd2956bf779efddf5d6

Observatory Snapshot v0.2 =
20d28d0f98502fa1ad8f2060f7396063cd0df08c62568d29aa1af71406a1979e
```

## Connector-side assertion run

A 42-assertion qualification pass was executed directly against:

- the frozen native snapshots;
- Stage-6E generated projections;
- profile-0.1.2 revision rules.

Result:

```text
PASSED = 42
TOTAL = 42
FAILURES = 0
```

Covered assertions include:

- profile version / producer / observation identity;
- source-kind revision grammar for every emitted source;
- complete PR/comment enumeration;
- exact content-digest agreement with stored native objects;
- owner association and decision semantics;
- FCP post-PGH routing and authorization;
- HiVenues rejection/redesign state;
- Project Observatory mixed/no-blanket validity;
- absence of the false Hive -> NFC/PGH dependency;
- changed comment body changes content digest;
- changed PR body changes content digest.

## Execution caveat

The committed file:

`prototype/cpi0/stage6e/test_stage6e.py`

contains the preregistered Python regression suite.

The current execution environment did not provide a local checkout/network path that allowed that committed Python test module itself to be invoked as a process.

Therefore:

```text
CONNECTOR_NATIVE_EVIDENCE_QUALIFICATION = 42/42 PASS
COMMITTED_PYTHON_SUITE = PRESENT
COMMITTED_PYTHON_SUITE_PROCESS_EXECUTION = NOT_CLAIMED
```

Stage 6F must treat executable-code validation as part of its independent audit.

No result in this record upgrades self-qualification into independent closure.
