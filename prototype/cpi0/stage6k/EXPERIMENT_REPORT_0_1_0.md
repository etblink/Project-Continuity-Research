# CPI-0 Stage-6K Owner-Authority Reducer Corrective Report 0.1.0

Date: 2026-10-04
Status: FROZEN CORRECTIVE RESULT — INDEPENDENT RE-AUDIT REQUIRED
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #30

## 1. Controlling independent evidence

Independent evaluator:

`Claude Opus 5.5 (Anthropic)`

The evaluator lacked repository push authorization.

Reported evaluator-local commit:

`698e929e51a55ec8ddce9b9cdfd14a5c56a9f3c5`

Exact uploaded report blob independently verified from the user-provided report bytes:

`8c6ce04f5bbce93e4534b480a5114b8c23f2cf04`

Final Stage-6J disposition:

`REPAIR_REQUIRED`

The remote Stage-6J audit branch remains at launch-control:

`23f28d944a2f411ca12437753ec193793559b415`

because the evaluator could not push and the Project Lead publication attempt could not preserve the exact report blob through the text connector. The branch was restored to launch-control.

Stage 6K therefore cites the exact external report blob rather than manufacturing a different audit artifact.

## 2. Stage-6J result adopted

Claude found:

```text
CPI6H-001 = NOT_CLOSED

CPI6H-002 = CLOSED

CPI6H-003 = CLOSED
  (S1 residual)

CPI6H-004 = S1 unchanged

S3 = 0
S2 = 2
S1 = 4
S0 = 1

FINAL = REPAIR_REQUIRED
```

The two S2 findings controlling Stage 6K are:

- CPI6J-001 — current PR conversation comments excluded from owner-authority adjudication;
- CPI6J-002 — explicit owner acceptance on governing #374 can be excluded by brittle scope/classification.

## 3. Repair principle

Stage 6K replaces body-text scoping with a native-surface authority model.

Scope is now determined by where the OWNER event lives:

- every OWNER comment on #374 -> gate lane;
- every OWNER comment on #398 -> candidate/work lane;
- every OWNER conversation comment, review, or inline review comment on the current candidate PR -> candidate lane.

Historical PRs remain preserved but are not current-candidate authority.

Text is used only to classify an already-in-scope event.

## 4. CPI6J-001 repair

Stage 6I tested:

`source.pr_number == current_pr_number`

for PR-scoped authority.

PR conversation comments are GitHub issue-comment objects and carry:

`issue_number = <PR number>`

not `pr_number`.

Stage 6K explicitly scopes:

```text
github_issue_comment
AND issue_number == current_pr_number
=> candidate authority
```

The live Stage-6K production projection now contains the previously missing owner decision as the latest candidate event:

```text
source =
pr399-comment-5981621690

classification =
FAIL_OR_HOLD

lane =
candidate

event_time =
2026-10-04T15:30:51Z
```

A synthetic later OWNER PASS on the same PR conversation channel is also captured.

Corrective evidence:

`CPI6J-001 = CORRECTIVE_EVIDENCE_PASS`

## 5. CPI6J-002 repair

### Native gate scope

Every OWNER comment on #374 is now a gate event.

No body reference to:

- #399;
- PR #399;
- Stage 5D;
- Stage-5D

is required for scope.

### Decision grammar

Stage 6K recognizes ordinary explicit owner decision forms including:

- PASS / PASSED in a decision context;
- ACCEPTED;
- acceptance granted;
- APPROVED;
- LGTM;
- ship it;
- good to go;
- gate passed/satisfied;
- owner would continue using.

FAIL/HOLD includes:

- FAIL;
- NOT ACCEPTED;
- acceptance not granted;
- REJECTED;
- HOLD;
- CHANGES REQUESTED;
- redesign required;
- do not proceed;
- owner would exit/quit.

Negative constructions are masked before positive-token matching.

PASS is not recognized merely because the prose says `next pass`.

HOLD is matched as a word, so `threshold` does not trigger it.

### Issue object

The #374 issue object itself participates when its current body explicitly records a decision. A closed/completed issue alone does not infer PASS.

Corrective evidence:

`CPI6J-002 = CORRECTIVE_EVIDENCE_PASS`

## 6. Temporal owner-authority reducer

Stage 6K records an ordered owner-authority history.

Native event time is derived from:

- review submitted_at;
- comment/review-comment updated_at with created_at fallback;
- issue updated_at.

Within each lane the latest decisional event supersedes earlier decisional events.

The reducer tracks:

- `gate_latest`;
- `candidate_latest`;
- `latest_overall`.

### Rejected

If the latest decisive owner event is FAIL/HOLD:

`state = rejected`

### Candidate PASS pending gate synchronization

If the latest decisive event is candidate PASS while #374's latest gate state is not PASS:

```text
state =
accepted_pending_gate_sync

D_E_AUTHORIZED_BY_CPI =
false

next_action =
synchronize_explicit_issue_374_owner_gate_acceptance
```

CPI no longer continues saying `rejected / redesign` after a newer native candidate PASS.

### Gate PASS

If #374's latest decision is PASS and no later candidate FAIL/HOLD supersedes it:

`state = accepted`

Even then:

`D_E_AUTHORIZED_BY_CPI = false`

CPI can reconstruct acceptance but cannot grant native project execution authority.

## 7. Profile 0.1.5

Profile 0.1.5 is additive.

0.1.0 through 0.1.4 remain unchanged.

Hardening includes:

- `accepted` and `accepted_pending_gate_sync` transition states;
- `author_association` bound into issue-comment/review/review-comment revisions;
- known review-state validation;
- malformed integer IDs normalized to CPIValidationError;
- observation `capture_cutoff`;
- ISO-8601 ordering:
  `window_start <= capture_cutoff <= window_end`;
- `observed_at == capture_cutoff`.

## 8. Collector hardening

Stage 6K uses:

`capture_cutoff = final equal sweep started_at`

rather than presenting the final sweep end as the guaranteed capture time.

Receipt validation now recomputes every page SHA-256 from the actual returned row slice and validates the empty terminal page digest.

## 9. Exact clean-checkout qualification

Qualified code commit:

`633922113543b478376411534d03bced887cfb4d`

Workflow run:

`37239950469`

Result:

```text
COMPILE = PASS
UNITTESTS = 27/27 PASS
LIVE_STABILIZED_NATIVE_PATH = PASS

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

LATEST_GATE =
issue374-comment-5981621424 / FAIL_OR_HOLD

LATEST_CANDIDATE =
pr399-comment-5981621690 / FAIL_OR_HOLD
```

See:

`prototype/cpi0/stage6k/STAGE6K_CLEAN_CHECKOUT_QUALIFICATION_0_1_0.md`

## 10. Existing controls

Repository substitution remains closed.

FCP full-file routing remains:

```text
POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION
YES__STANDING_PROJECT_LEAD_DELEGATION
SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION
```

NFC theorem/publication authority separation remains intact.

PGH physical trials remain unauthorized.

The false HiVenues/Hive -> NFC/PGH dependency remains absent.

Project Observatory remains unmodified and nonauthoritative.

## 11. Mutation audit

```text
NFC = NONE
FCP = NONE
PGH = NONE
HIVENUES = NONE
PROJECT_OBSERVATORY = NONE

STAGE6A_THROUGH_STAGE6J = UNCHANGED
LIVE_FEDERATION = NONE
LIVE_OBSERVATORY_INTEGRATION = NONE
EXTERNAL_PROJECT_EFFECT = NONE

PROJECT_CONTINUITY_RESEARCH_STAGE6K_BRANCH = MUTATED
READ_ONLY_NATIVE_GITHUB_QUALIFICATION = YES
```

## 12. Stage-6K disposition

```text
CPI6J_001_CURRENT_PR_CONVERSATION_AUTHORITY =
CORRECTIVE_EVIDENCE_PASS

CPI6J_002_GATE_SCOPE_AND_ACCEPTANCE =
CORRECTIVE_EVIDENCE_PASS

CPI6J_003_CAPTURE_CUTOFF_S1 =
HARDENED

CPI6J_004_AUTHORITY_TIME_BINDING_S1 =
PARTIALLY_HARDENED

CPI6J_005_TEST_PROVENANCE_S1 =
UNCHANGED

CPI6H_004_REPOSITORY_CASE_ALIAS_S1 =
UNCHANGED

CLEAN_CHECKOUT =
27/27 PASS

LIVE_NATIVE =
PASS

INDEPENDENT_CLOSURE =
NOT CLAIMED
```

Final Stage-6K disposition:

`CORRECTIVE_EVIDENCE_PASS__INDEPENDENT_REAUDIT_REQUIRED`

## 13. Next gate

Stage 6L must independently attack:

- PR conversation authority;
- #374 surface-defined authority;
- ordinary acceptance grammar;
- temporal supersession;
- candidate PASS pending gate sync;
- gate PASS;
- later reversal after PASS;
- issue-object acceptance;
- profile 0.1.5 authority binding;
- capture-cutoff semantics;
- page-SHA receipt integrity;
- prior FCP/NFC/PGH/false-bridge/federation controls.

No live federation or Project Observatory integration is authorized before Stage 6L.
