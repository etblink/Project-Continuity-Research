# CPI-0 Stage-6E Native-Source Binding Corrective Report 0.1.0

Date: 2026-10-04  
Status: FROZEN CORRECTIVE RESULT — INDEPENDENT RE-AUDIT REQUIRED  
Program: CPI-0 — Cross-Project Interoperability  
Governing issue: #24  
Parent independent re-audit: #23  
Parent audit commit: ab9e4db3359613efcf03ffdf58d36ef8f09a276a

## 1. Objective

Repair the two systematic S2 mechanisms that remained after Stage 6D:

- CPI6D-001: native-source binding and source-set completeness;
- CPI6D-002: profile revision semantics not enforced.

These are also the unresolved mechanisms behind CPI6B-001 and CPI6B-003.

## 2. Architecture correction

Stage 6E adds an explicit read-only boundary:

```text
NATIVE PROJECT SOURCE
    -> CONTENT-BOUND COLLECTOR SNAPSHOT
    -> SEMANTIC ADAPTER
    -> CPI PROJECTION
```

The semantic adapter no longer accepts hand-written source text carrying someone else's native identity.

## 3. Native Git source binding

Stage 6E mirrors complete authoritative files, not excerpts.

All six mirror blobs are byte-identical to upstream because their Git blob SHAs match exactly.

Most importantly, FCP now supplies the entire native CURRENT_STATE.md with all 14 repeated NEXT_RECOMMENDED_OPERATION records intact.

The adapter must recover current routing from the native trigger/current block plus the native precedence rule.

This removes the Stage-6C behavior where an upstream packet author had already selected the desired semantic window.

## 4. HiVenues discovery completeness

The collector begins with declared governing Issue #398 and performs explicit bounded discovery.

Frozen discovery demonstrates:

- complete Issue #398 conversation stream;
- complete open-PR set;
- complete PR conversation-comment streams;
- review and inline-comment pagination checks;
- exact native object storage.

Open PRs at the boundary are exactly:

```text
397
399
```

The two material owner decisions are both present:

- Issue #398 comment 5981621191 — owner acceptance FAIL;
- PR #399 comment 5981621690 — HOLD / redesign required.

The latter was the concordant source that Stage 6D noted Stage 6C had omitted.

The adapter sees both before deriving the rejected/redesign state.

## 5. Profile 0.1.2

Profile 0.1.2 is additive. Profiles 0.1.0 and 0.1.1 remain historical and unchanged.

0.1.2 requires every observed source to carry:

- source_kind;
- native_id;
- content_sha256;
- revision.

It enforces source-kind-specific revision construction.

Examples:

```text
git:<commit>:blob:<blob_sha>:sha256:<content_sha256>

github_issue:<number>:updated_at:<time>:sha256:<content_sha256>

github_issue_comment:<comment_id>:issue:<issue_number>:
updated_at:<time>:sha256:<content_sha256>

github_pull_request:<number>:head:<head>:base:<base>:
state:<state>:draft:<bool>:updated_at:<time>:sha256:<content_sha256>
```

An arbitrary nonempty revision is no longer profile-conformant.

Freshness now accepts validated current source objects, not unvalidated revision strings.

## 6. Content binding

For Git sources:

- collector recomputes native Git blob SHA from bytes;
- declared upstream blob must match;
- SHA-256 of the same full bytes becomes part of the CPI revision.

For GitHub sources:

- the complete frozen native JSON object is canonicalized;
- SHA-256 is computed over that canonical object;
- the digest becomes part of the source revision.

Thus a changed authority-bearing comment or PR body changes the revision even if repository main does not move.

## 7. FCP corrective result

The full native FCP file contains 14 exact NEXT_RECOMMENDED_OPERATION records.

Without deleting any historical record, the native-bound adapter resolves:

```text
CURRENT_OPERATION =
POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION

AUTHORIZATION =
YES__STANDING_PROJECT_LEAD_DELEGATION

BOUNDARY =
SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION

PRIOR_EVIDENCE_HOLD =
FULFILLED_HISTORY

FCP27_SELECTED =
NO
```

Stage-6D's central objection—correct answer from a curated source window—is therefore directly removed.

## 8. HiVenues corrective result

The complete discovery set yields:

```text
MERGED_MAIN = 4fed1b4b...
CURRENT_STAGE5D_CANDIDATE = PR #399
PR399 = open / draft / unmerged
OWNER_ACCEPTANCE = FAIL
CONCORDANT_PR_OWNER_RESULT = HOLD / redesign required
DO_NOT_PROCEED_D_E = preserved
DO_NOT_DECLARE_374_SATISFIED = preserved
NEXT_ACTION = redesign review before further broad implementation
```

CPI grants no external-effect authority.

## 9. Observatory preservation

Project Observatory Snapshot v0.2 is still untouched.

The comparison remains:

```text
FCP component =
CONTRADICTED_BY_REFERENCED_NATIVE_STATE

HiVenues historical identity =
VALID_IDENTITY_AT_OBSERVATION_BOUNDARY + stale now

OVERALL =
MIXED__NO_BLANKET_VALIDITY
```

## 10. Qualification

Direct native-source/GitHub connector qualification:

```text
42 / 42 PASS
```

See:

`prototype/cpi0/stage6e/STAGE6E_CONNECTOR_QUALIFICATION_0_1_0.md`

The committed Python regression suite is present at:

`prototype/cpi0/stage6e/test_stage6e.py`

Its process execution is deliberately not claimed in this report because the current environment did not provide a local checkout path for executing the committed module itself.

Stage 6F must independently execute/inspect it.

## 11. Mutation audit

```text
NFC_MUTATION = NONE
FCP_MUTATION = NONE
PGH_MUTATION = NONE
HIVENUES_MUTATION = NONE
PROJECT_OBSERVATORY_MUTATION = NONE

STAGE6A_REWRITTEN = NO
STAGE6B_REWRITTEN = NO
STAGE6C_REWRITTEN = NO
STAGE6D_REWRITTEN = NO

PROJECT_CONTINUITY_RESEARCH_REPAIR_BRANCH = MUTATED
LIVE_FEDERATION = NONE
LIVE_EXTERNAL_EFFECT = NONE
```

## 12. Stage-6E disposition

```text
CPI6D_001_NATIVE_SOURCE_BINDING =
CORRECTIVE_EVIDENCE_PASS

CPI6D_002_PROFILE_REVISION_ENFORCEMENT =
CORRECTIVE_EVIDENCE_PASS

CPI6B_001_FCP_MECHANISM =
CORRECTIVE_EVIDENCE_PASS

CPI6B_003_PROFILE_MECHANISM =
CORRECTIVE_EVIDENCE_PASS

CONNECTOR_QUALIFICATION =
42/42 PASS

INDEPENDENT_CLOSURE =
NOT YET CLAIMED
```

Final Stage-6E disposition:

`CORRECTIVE_EVIDENCE_PASS__STAGE6F_REQUIRED`

## 13. Next gate

Stage 6F must be performed by an evaluator who did not author Stage 6E.

It must attempt to falsify:

1. exact native Git content binding;
2. non-Git canonical-object content binding;
3. bounded source-set completeness;
4. profile-0.1.2 source-kind revision enforcement;
5. full-file FCP routing extraction;
6. HiVenues current-candidate / human-authority extraction;
7. observer optionality;
8. false-bridge nonpromotion.

It must also execute or independently validate the committed Stage-6E code path.

No live integration is authorized before Stage 6F.
