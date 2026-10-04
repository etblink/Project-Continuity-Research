# CPI-0 Stage-6K Clean-Checkout Qualification Record 0.1.0

Date: 2026-10-04
Status: FROZEN SELF-QUALIFICATION EVIDENCE
Governing issue: #30

## Qualified code commit

`633922113543b478376411534d03bced887cfb4d`

Workflow:

`CPI-0 Stage 6K qualification`

Successful run:

`37239950469`

## Exact execution

```text
PY_COMPILE = PASS
UNITTESTS = 27/27 PASS
LIVE_STABILIZED_NATIVE_PATH = PASS
```

Real production GitHub result:

```text
STAGE6K_NATIVE = PASS
OPEN_PRS = [397, 399]

STABLE_DIGEST =
3b6439322c5c0497552a8e9f973ddf372e937f2a1e4ee04638ae41f91fcd3530

WINDOW_START =
2026-10-04T22:25:24Z

CAPTURE_CUTOFF =
2026-10-04T22:25:29Z

WINDOW_END =
2026-10-04T22:25:33Z

BASELINE_STATE = rejected
BASELINE_OWNER_RESULT = FAIL_OR_HOLD

AUTHORITY_EVENT_COUNT = 11

LATEST_GATE =
issue374-comment-5981621424
FAIL_OR_HOLD
2026-10-04T15:30:49Z

LATEST_CANDIDATE =
pr399-comment-5981621690
FAIL_OR_HOLD
2026-10-04T15:30:51Z
```

## Stage-6J attack coverage

The committed 27-test suite establishes:

- current PR #399 conversation comment 5981621690 is in current authority history;
- a later OWNER PASS in PR #399 conversation is not dropped;
- candidate-level PASS newer than an older gate FAIL becomes `accepted_pending_gate_sync`, not `rejected`;
- later FAIL/HOLD supersedes earlier PASS;
- every OWNER #374 comment is in gate scope regardless of wording;
- Stage-5D hyphenation does not control scope;
- ordinary acceptance forms (Accepted, PASS, LGTM/ship it, gate passed, good to go, continue using) are recognized;
- `threshold` does not accidentally trigger HOLD;
- a current #374 issue object explicitly rewritten to PASS/completed participates;
- historical PR #397 authority does not control PR #399;
- later decisions supersede earlier decisions;
- explicit #374 PASS can produce `accepted`;
- `author_association` mutation without revision update is rejected;
- capture-cutoff ordering and `observed_at == capture_cutoff` are enforced;
- receipt page-SHA tampering is rejected;
- malformed integer fields raise CPIValidationError;
- review state enum is enforced;
- cross-repository substitution remains closed;
- FCP full-file routing remains correct;
- false bridge remains absent;
- Project Observatory remains unmodified.

## Development failures before qualification

Earlier branch runs failed before freeze due:

1. negative decision phrases such as `NOT ACCEPTED` also matching lexical `accepted`;
2. bare word `pass` incorrectly matching iterative prose such as `next pass`;
3. one issue-object test fixture retaining old rejection prose while appending new PASS prose.

All were repaired before the controlling successful run.

These failed runs are retained as implementation history, not qualification evidence.

## Epistemic status

This is self-authored qualification evidence.

It does not independently close the Claude Stage-6J findings.

Stage 6L is required.
