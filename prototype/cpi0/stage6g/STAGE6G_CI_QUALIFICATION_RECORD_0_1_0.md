# CPI-0 Stage-6G CI Qualification Record 0.1.0

Date: 2026-10-04
Status: FROZEN SELF-QUALIFICATION EVIDENCE
Governing issue: #26

## Exact qualified code commit

`ff9f5fbe6d65b8ed1d5a974bfba6c76e3555d13d`

GitHub Actions workflow:

`CPI-0 Stage 6G qualification`

Successful run:

`37233470056`

## Clean-checkout execution

GitHub Actions checked out the exact branch commit and ran Python 3.12.

Compile step:

```text
prototype/cpi0/cpi_profile_v0_1_3.py
prototype/cpi0/stage6g/collector.py
prototype/cpi0/stage6g/adapter.py
prototype/cpi0/stage6g/test_stage6g.py
RESULT = PASS
```

Regression suite:

```text
python -m unittest -v prototype/cpi0/stage6g/test_stage6g.py
Ran 15 tests
OK
```

## Real native GitHub integration

The same exact-checkout workflow then instantiated the direct GitHub REST reader using the workflow's read-only GitHub token.

Result:

```text
NATIVE_DIRECT_HIVENUES = PASS
OPEN_PRS = [397, 399]
```

The live integration required the native-direct enumeration receipts and derived the frozen-boundary HiVenues result:

```text
CURRENT_STAGE5D_CANDIDATE = PR #399
TRANSITION_STATE = rejected
NEXT_ACTION = redesign_review_before_further_broad_implementation
```

No stored Stage-6E snapshot was used as the current-completeness authority.

## Regression coverage

The 15-test suite includes:

- fixture reader cannot assert current completeness;
- exhaustive native-direct reader is accepted;
- incomplete enumeration fails closed;
- native API failure does not fall back to snapshot fixture;
- newly returned PR is automatically visible;
- newly returned owner comment is automatically visible;
- current HiVenues result remains rejected/redesign;
- repository-less GitHub identity is rejected;
- Stage-6F cross-repository substitution attack fails;
- even a fully rebound alternate-repository source is rejected by freshness;
- comment-content change changes revision;
- PR-content change changes revision;
- FCP full-file regression remains correct with 14 repeated routing records;
- false bridge remains absent;
- fixture status is explicitly nonauthoritative for current completeness.

## Historical failed runs

Runs 1 and 2 failed before freeze because an FCP regression helper incorrectly rejected unrelated duplicate keys inside the long native routing block.

That implementation defect was repaired narrowly by applying duplicate detection only to the controlling routing keys.

The successful run above is the controlling qualification evidence.

## Epistemic status

This is self-authored qualification evidence, not independent closure.

Stage 6H remains required.
