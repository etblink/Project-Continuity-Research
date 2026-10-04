# CPI-0 Stage-6G Live Native Enumeration Corrective Report 0.1.0

Date: 2026-10-04
Status: FROZEN CORRECTIVE RESULT — INDEPENDENT RE-AUDIT REQUIRED
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #26
Parent audit commit: 5de6a9ffe7d3899924426ed8425a4e4150b6ab64

## 1. Stage-6F findings addressed

Stage 6F left two S2 mechanisms:

1. source-set completeness was self-attested by stored snapshots;
2. GitHub issue/comment/PR identity and freshness were not repository-bound.

Stage 6G repairs only those mechanisms.

## 2. Source-set completeness correction

Stage 6G explicitly rejects the premise that a committed offline snapshot can prove present-tense native completeness.

The rule is now:

```text
OFFLINE_SNAPSHOT_COMPLETENESS = NONAUTHORITATIVE
CURRENT_GITHUB_COMPLETENESS = DIRECT_NATIVE_ENUMERATION_REQUIRED
```

The current HiVenues collector has no snapshot fallback.

It must receive a reader whose mode is:

`native_direct`

and it must exhaust native pagination for:

- Issue #398 comments;
- Issue #374 comments;
- repository open PRs;
- every open PR's conversation comments;
- every open PR's reviews;
- every open PR's inline review comments.

A valid receipt requires a contiguous page sequence ending in an empty native page.

If enumeration is unavailable, incomplete, or fixture-only, the collector fails closed.

The Stage-6E JSON snapshots remain deterministic fixtures/historical evidence only.

## 3. Native direct implementation

`prototype/cpi0/stage6g/collector.py`

contains a direct GitHub REST reader.

At current reconstruction time it reads GitHub itself rather than a committed claim about what GitHub contained.

A branch-scoped GitHub Actions run exercised that real path against HiVenues with a read-only repository token.

Result:

```text
NATIVE_DIRECT_HIVENUES = PASS
OPEN_PRS = [397, 399]
```

Thus Stage 6G does not merely test a fake enumeration contract; the exact committed code successfully executed the direct native path.

## 4. Discovery behavior

Current PR membership is derived from the native reader output.

No expected PR set is hard-coded into the Stage-6G collector.

Regression tests establish that:

- a newly returned PR automatically appears in the discovered set;
- a newly returned owner comment automatically appears in the source set;
- an incomplete terminal page sequence fails closed;
- native-reader failure does not fall back to Stage-6E snapshot files.

This removes the coherent-omission mechanism Stage 6F demonstrated against a self-reported snapshot.

## 5. Repository-bound profile 0.1.3

Stage 6G adds profile:

`0.1.3`

without rewriting 0.1.0 through 0.1.2.

GitHub identities now include repository.

Examples:

```text
github_issue:etblink/HiVenues:398

github_issue_comment:etblink/HiVenues:5981621191

github_pull_request:etblink/HiVenues:399
```

Repository is also embedded into each source-kind revision.

Freshness now requires equality of:

- source_kind;
- repository;
- native_id;
- validated revision.

The exact Stage-6F cross-repository attack is covered by regression and fails.

A stronger attack in which repository, native_id, and revision are all coherently rebound to another repository also fails during freshness because the observed and current repositories differ.

## 6. Existing closed repairs preserved

### FCP

The full native Stage-6E FCP file remains the regression source.

It still contains:

```text
NEXT_RECOMMENDED_OPERATION occurrence count = 14
```

Stage 6G independently rechecks the controlling full-file values against the already-frozen corrected projection.

The clean-checkout regression passes.

### HiVenues frozen boundary

The real native run still yields:

- open PRs 397 and 399;
- current Stage-5D candidate PR #399;
- owner rejection / hold;
- no D-E progression;
- #374 not satisfied;
- redesign review next.

### NFC / PGH / Observatory

No new scientific/deployment authority is introduced.

The false HiVenues/Hive -> NFC/PGH bridge remains absent.

Project Observatory remains unchanged and nonauthoritative.

## 7. Exact execution

Successful exact-checkout run:

`37233470056`

Qualified code commit:

`ff9f5fbe6d65b8ed1d5a974bfba6c76e3555d13d`

Results:

```text
PY_COMPILE = PASS
UNITTESTS = 15/15 PASS
NATIVE_DIRECT_HIVENUES = PASS
OPEN_PRS = [397, 399]
```

See:

`prototype/cpi0/stage6g/STAGE6G_CI_QUALIFICATION_RECORD_0_1_0.md`

## 8. Mutation audit

```text
NFC = NONE
FCP = NONE
PGH = NONE
HIVENUES = NONE
PROJECT_OBSERVATORY = NONE
STAGE6A_THROUGH_STAGE6F = UNCHANGED
LIVE_FEDERATION = NONE
EXTERNAL_PROJECT_EFFECT = NONE
PROJECT_CONTINUITY_RESEARCH_REPAIR_BRANCH = MUTATED
READ_ONLY_GITHUB_API_QUALIFICATION = YES
```

## 9. Corrective disposition

```text
CPI6F_001_SOURCE_SET_COMPLETENESS =
CORRECTIVE_EVIDENCE_PASS

CPI6F_002_REPOSITORY_BOUND_IDENTITY =
CORRECTIVE_EVIDENCE_PASS

CPI6D_001 =
CORRECTIVE_EVIDENCE_PASS

CPI6D_002 =
CORRECTIVE_EVIDENCE_PASS

CPI6B_003 =
CORRECTIVE_EVIDENCE_PASS

EXACT_CLEAN_CHECKOUT_TESTS =
15/15 PASS

LIVE_READ_ONLY_NATIVE_ENUMERATION =
PASS

INDEPENDENT_CLOSURE =
NOT CLAIMED
```

Final Stage-6G disposition:

`CORRECTIVE_EVIDENCE_PASS__INDEPENDENT_REAUDIT_REQUIRED`

## 10. Next gate

Stage 6H must independently attempt to reproduce:

- the coherent-omission attack;
- fixture fallback;
- incomplete pagination acceptance;
- repository substitution;
- fully coherent cross-repository rebinding;
- current native enumeration;
- FCP full-file regression;
- false-bridge promotion;
- observer-oracle behavior.

No live federation or Observatory integration is authorized before Stage 6H.
