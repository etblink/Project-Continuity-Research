# CPI-0 Stage-6G Live Native Enumeration Corrective Preregistration 0.1.0

Date: 2026-10-04
Status: FROZEN BEFORE IMPLEMENTATION
Governing issue: #26
Parent audit commit: 5de6a9ffe7d3899924426ed8425a4e4150b6ab64

## Objective

Repair only the two S2 mechanisms from Stage 6F:

1. source-set completeness is self-attested by stored snapshots;
2. GitHub issue/comment/PR identity and freshness are not repository-bound.

## Source-set rule

An offline committed snapshot is evidence/fixture only. It cannot by itself assert current GitHub collection completeness.

For current-state reconstruction:

CURRENT_GITHUB_SET_COMPLETENESS = REQUIRES_DIRECT_NATIVE_ENUMERATION

A native enumeration run must read the governing issue, its complete comment stream, all open PRs, and the complete required PR discussion/review surfaces, following pagination to exhaustion.

The enumeration receipt must record repository, query/endpoint identity, pages requested, IDs returned per page, termination, observation time, and mode = native_direct.

A fixture reader must identify itself as mode = fixture.

The current-state semantic adapter must reject fixture-only completeness. If native enumeration is unavailable, it must fail closed rather than substitute a stored Stage-6E snapshot.

## Profile 0.1.3

Add profile 0.1.3 without changing 0.1.0-0.1.2.

GitHub native identities and revisions must include repository identity.

Issue native_id:
github_issue:<repository>:<issue_number>

Issue-comment native_id:
github_issue_comment:<repository>:<comment_id>

PR native_id:
github_pull_request:<repository>:<pr_number>

Their revisions must also include the same repository plus their existing source-specific fields and content SHA-256.

Freshness must require equality of source_kind, repository, native_id, and a valid source-kind revision.

Cross-repository substitution must fail.

## Preservation

Retain Stage-6E full-file Git binding and FCP full-file extraction. Do not mutate NFC, FCP, PGH, HiVenues, Project Observatory, prior profiles, or Stage-6A through Stage-6F evidence.

## Required regressions

At minimum test:

- fixture reader cannot establish current completeness;
- current adapter rejects fixture-only enumeration;
- exhaustive native-direct enumeration is accepted;
- incomplete enumeration fails closed;
- newly returned PR/comment objects are automatically visible;
- no snapshot fallback occurs when native enumeration fails;
- repository-less GitHub identity fails profile validation;
- repository mismatch inside revision fails;
- freshness rejects cross-repository substitution;
- the exact Stage-6F substitution attack fails;
- content changes still change revisions;
- FCP full-file routing remains correct;
- frozen HiVenues result remains rejected/redesign when supplied by a native-direct test reader;
- false bridge remains absent;
- Observatory remains unmodified.

## Acceptance

Stage 6G may report only:

CORRECTIVE_EVIDENCE_PASS__INDEPENDENT_REAUDIT_REQUIRED

A fresh Stage 6H audit is required before any closure or live integration.
