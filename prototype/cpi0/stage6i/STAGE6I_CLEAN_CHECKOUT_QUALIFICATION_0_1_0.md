# CPI-0 Stage-6I Clean-Checkout Qualification Record 0.1.0

Date: 2026-10-04
Status: FROZEN SELF-QUALIFICATION EVIDENCE
Governing issue: #28

## Qualified code commit

`bbd9f4708bd9e8e66c1764ae472c5cb74fb8e129`

GitHub Actions workflow:

`CPI-0 Stage 6I qualification`

Run:

`37237412842`

Final run conclusion:

`SUCCESS`

## Clean-checkout executable result

GitHub Actions checked out the exact code commit and used Python 3.12.

Compilation:

```text
prototype/cpi0/cpi_profile_v0_1_4.py
prototype/cpi0/stage6i/collector.py
prototype/cpi0/stage6i/adapter.py
prototype/cpi0/stage6i/test_stage6i.py

RESULT = PASS
```

Committed regression suite:

```text
python -m unittest -v prototype/cpi0/stage6i/test_stage6i.py

Ran 23 tests
OK
```

## Real production native path

The same clean-checkout job invoked:

`adapt_hivenues_current()`

through the production Stage-6I collector.

No fake reader/transport was passed to the public current-state API.

Result:

```text
STABILIZED_NATIVE_HIVENUES = PASS
OPEN_PRS = [397, 399]

STABLE_DIGEST =
3b6439322c5c0497552a8e9f973ddf372e937f2a1e4ee04638ae41f91fcd3530

WINDOW_START =
2026-10-04T21:46:12Z

WINDOW_END =
2026-10-04T21:46:25Z

PR_REVIEW_SOURCES = 11
INLINE_REVIEW_COMMENT_SOURCES = 12
ISSUE374_COMMENT_SOURCES = 8
```

The live semantic result remained:

```text
CURRENT_STAGE5D_CANDIDATE = PR #399
OWNER_RESULT = FAIL_OR_HOLD
STATE = rejected
NEXT_ACTION = redesign_review_before_further_broad_implementation
```

## Stage-6H attack coverage

The committed regression suite directly covers:

- every enumerated PR review becomes a source object;
- every enumerated inline review comment becomes a source object;
- every Issue #374 comment becomes a source object;
- injected OWNER APPROVED review conflicts with existing rejection and fails closed;
- OWNER CHANGES_REQUESTED review is treated as FAIL/HOLD;
- nondecisional OWNER inline comment remains visible;
- production collector has no reader/transport/receipt injection parameter;
- production adapter has no reader/transport/receipt injection parameter;
- internal fake-transport bundle is nonauthoritative and rejected by the authoritative path;
- receipts are constructed from returned rows;
- two identical sweeps stabilize;
- A/B/B stabilizes only on B/B;
- A/B/C/D fails closed;
- authority-comment changes alter the sweep digest;
- review changes alter the sweep digest;
- projection uses stable-window language rather than `complete_at_observation`;
- profile 0.1.4 requires stabilized observation metadata for GitHub-source projections;
- profile 0.1.4 validates review/review-comment identities;
- repository substitution remains closed;
- FCP full-file routing remains correct;
- false bridge remains absent.

## Epistemic status

This is self-authored qualification evidence.

It does not independently close Stage-6H findings.

Stage 6J is required.
