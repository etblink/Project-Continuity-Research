# CPI-0 Stage-6K Owner-Authority Reducer Corrective Preregistration 0.1.0

Date: 2026-10-04
Status: FROZEN BEFORE IMPLEMENTATION
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #30

## Controlling independent evidence

Evaluator: Claude Opus 5.5 (Anthropic)

Independent report was produced in an environment without push authorization.

Reported evaluator-local commit:
`698e929e51a55ec8ddce9b9cdfd14a5c56a9f3c5`

Exact report blob independently verified from the uploaded report bytes:
`8c6ce04f5bbce93e4534b480a5114b8c23f2cf04`

Final disposition:
`REPAIR_REQUIRED`

The Stage-6J audit branch remains at launch-control because the evaluator could not publish. This repair therefore starts from the clean launch-control commit:

`23f28d944a2f411ca12437753ec193793559b415`

and treats the exact external report blob above as controlling audit evidence.

## 1. Findings in scope

### CPI6J-001 — S2

Current-candidate PR conversation comments are content-bound sources but are excluded from current owner-authority scope because they expose `issue_number` while the Stage-6I scope predicate tests `pr_number`.

### CPI6J-002 — S2

Governing #374 gate authority is selected through brittle text matching rather than by native surface. Explicit owner acceptance can therefore be enumerated and then excluded. The reducer also lacks temporal supersession, so later acceptance cannot replace earlier rejection cleanly.

## 2. Native-surface authority model

Authority scope must be derived from the source's native location, not from whether its prose mentions a magic phrase.

For the current Stage-5D candidate:

### Gate surface

All OWNER-authored comments on Issue #374 are gate-authority events.

The Issue #374 object itself is also a gate-authority event when its body/state explicitly records an acceptance decision.

### Work surface

All OWNER-authored comments on governing Issue #398 are Stage-5D work-authority events.

### Current-candidate surface

All OWNER-authored:

- PR conversation comments;
- PR review submissions;
- inline PR review comments

on the current candidate PR are current-candidate authority events.

Historical PRs remain visible but are not current-candidate authority.

## 3. Decision grammar

Decision classification must use word/phrase boundaries rather than arbitrary substrings.

PASS-family evidence includes explicit forms such as:

- PASS / PASSED;
- ACCEPT / ACCEPTED / ACCEPTANCE GRANTED;
- APPROVE / APPROVED;
- LGTM;
- SHIP IT;
- GOOD TO GO;
- gate satisfied / #374 satisfied;
- owner would continue using the product.

FAIL/HOLD-family evidence includes explicit forms such as:

- FAIL / FAILED;
- NOT ACCEPTED / ACCEPTANCE NOT GRANTED;
- REJECT / REJECTED;
- HOLD;
- CHANGES REQUESTED;
- REDESIGN REQUIRED;
- DO NOT PROCEED;
- owner would EXIT / QUIT the product.

A source with both material PASS and FAIL/HOLD signals is AMBIGUOUS and fails closed.

A source with neither is NONDECISIONAL and remains visible.

The classifier must not infer HOLD from the letters inside words such as `threshold`.

## 4. Temporal reduction

Each authority event receives a native event time.

Use the strongest available native time consistently:

- review: submitted_at;
- issue/review comment: updated_at, falling back to created_at;
- issue object: updated_at.

Events are sorted by event time and stable source ID tie-break.

Within each authority lane, the latest decisional event supersedes earlier decisional events.

The reducer must preserve an auditable event history and explicit latest-decision selection.

## 5. Final gate semantics

Issue #374 remains the final acceptance gate.

Let:

- `gate_latest` = latest decisional #374 event;
- `candidate_latest` = latest decisional event among #398 + current-candidate PR surfaces.

Required result:

### Any later FAIL/HOLD

If the latest decisive owner event across the current authority universe is FAIL/HOLD:

`STATE = rejected`

`D_E_AUTHORIZED = NO`

### Candidate PASS newer than unresolved/older gate FAIL

If a current-candidate PASS is newer than the last gate decision but #374 has not yet recorded/synchronized PASS:

`STATE = accepted_pending_gate_sync`

`D_E_AUTHORIZED = NO`

`NEXT_ACTION = synchronize explicit #374 owner gate acceptance`

CPI must not continue saying `rejected / redesign`.

### Gate PASS

If the latest #374 gate decision is PASS and no later current-candidate FAIL/HOLD supersedes it:

`STATE = accepted`

The CPI projection may represent gate acceptance, but CPI itself still has no external-effect authority. Any D-E execution remains subject to native project authorization.

### Unknown / ambiguous

Unknown or ambiguous decisive authority fails closed.

## 6. Issue-object participation

For Issue #374, explicit acceptance/rejection statements in the issue body plus meaningful gate state must participate.

A closed/completed #374 whose current body explicitly records owner acceptance PASS must not remain projected as rejected merely because old comments exist.

Issue closure alone without acceptance semantics is not sufficient to infer PASS.

## 7. Profile 0.1.5 hardening

Profile 0.1.5 is additive. Profiles 0.1.0 through 0.1.4 remain unchanged.

### Authority identity binding

For authority-bearing GitHub comments/reviews/review-comments, `author_association` must be included in the validated revision.

### Observation timing

GitHub projections must carry:

- window_start;
- capture_cutoff;
- window_end;
- observed_at = capture_cutoff.

Require valid ISO-8601 ordering:

`window_start <= capture_cutoff <= window_end`

The capture cutoff is the start of the final equal sweep, not the end of the sweep.

### Review-state validation

Review state must be from a known accepted GitHub review-state set.

### Integer validation

Malformed integer identifiers must raise CPIValidationError rather than leaking raw ValueError.

## 8. Collector hardening

Receipt validation must recompute and check each recorded page SHA-256 against the actual page-row slice represented by that receipt.

The stabilized observation bundle must expose:

- previous sweep start/end/digest;
- final sweep start/end/digest;
- capture_cutoff = final sweep started_at.

## 9. Required regressions

At minimum:

1. baseline PR #399 conversation owner HOLD 5981621690 appears in current decision history;
2. explicit OWNER PASS in a PR #399 conversation comment is not dropped;
3. an OWNER PASS on PR #399 newer than the gate FAIL yields accepted_pending_gate_sync, not rejected;
4. a later OWNER FAIL/HOLD after candidate PASS returns rejected;
5. every OWNER comment on #374 is in gate authority scope regardless of wording;
6. #374 PASS text using `Stage-5D` hyphenation is recognized;
7. #374 PASS text using `#398 redesign` is recognized;
8. `Accepted. #374 is satisfied for Stage 5D.` is recognized as PASS;
9. `PASS` alone is recognized as PASS;
10. `LGTM — ship it.` is recognized as PASS;
11. `Stage 5D usability gate passed; the owner would continue using HiVenues.` is PASS;
12. `The threshold is met; good to go.` is PASS and does not generate HOLD;
13. Issue #374 closed/completed plus explicit PASS body is accepted;
14. historical PR #397 authority remains historical only;
15. later decisions supersede earlier decisions within a lane;
16. candidate PASS with older gate FAIL yields pending_gate_sync;
17. gate PASS with no later candidate FAIL yields accepted;
18. later candidate FAIL after gate PASS yields rejected;
19. author_association mutation without revision update fails profile validation;
20. observation timestamps are ordered and observed_at equals capture_cutoff;
21. final-sweep late change is not falsely claimed observed after capture_cutoff;
22. page_sha256 tampering is rejected;
23. malformed integer fields produce CPIValidationError;
24. Stage-6F repository substitution remains closed;
25. FCP full-file routing remains correct;
26. false bridge remains absent;
27. Project Observatory remains unmodified/nonauthoritative.

## 10. Preservation

No mutation to:

- NFC;
- FCP;
- PGH;
- HiVenues;
- Project Observatory;
- profiles 0.1.0 through 0.1.4;
- Stage-6A through Stage-6J evidence.

## 11. Acceptance

Stage 6K may report only:

`CORRECTIVE_EVIDENCE_PASS__INDEPENDENT_REAUDIT_REQUIRED`

after a clean-checkout suite and real read-only stabilized GitHub qualification pass.

A fresh independent Stage 6L audit is mandatory before closure or live integration.
