# CPI-0 Stage-6L Independent Owner-Authority Reducer Re-Audit Report 0.1.0

Date: 2026-10-04
Status: FROZEN INDEPENDENT AUDIT RESULT
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #31
Audit branch: `audit/cpi0-stage6l-independent-owner-authority`

## 1. Evaluator identity / independence

```text
EVALUATOR = Claude Opus 5.5 (Anthropic), configured model id claude-opus-5-5
SESSION = Cowork cloud sandbox, 2026-10-04 (UTC), Linux 6.18.44, Python 3.13.16
STAGE_6K_AUTHORSHIP = NONE (all 14 commits 23f28d9..578ee9c are authored by Evan Kotler)
PRIOR_CONVERSATION_MEMORY_USED_AS_EVIDENCE = NO
```

All findings below were derived in this session from the frozen repository bytes, from
code execution against the committed Stage-6K modules and Stage-6E native HiVenues
fixtures, and from read-only public observation of `etblink/HiVenues`. Stage-6K tests,
CI, qualification records and reports were treated as claims, not proof.

Limitation: no evaluator-provided Stage-6J report bytes were supplied to this session,
so Stage-6J blob `8c6ce04f…` could not be byte-verified here (`git cat-file` does not
find it, nor local commit `698e929…`, in the remote). The Stage-6J S2 findings were
taken from the frozen Stage-6L launch prompt and Stage-6K preregistration and
**independently re-derived** below.

## 2. Exact control identities

```text
LAUNCH_CONTROL_COMMIT (HEAD of audit branch at start) = 578ee9cacb0179dd5954fc3c5e1dfb6b68e79461
STAGE6K_REPAIR_BRANCH HEAD                           = 578ee9cacb0179dd5954fc3c5e1dfb6b68e79461
STAGE6K_CORRECTIVE_REPORT_COMMIT                     = 30358f34a23d386987fa7e0f482582ceab1fd46e (present)
STAGE6K_QUALIFIED_CODE_COMMIT                        = 633922113543b478376411534d03bced887cfb4d (present)
STAGE6J_LAUNCH_CONTROL                               = 23f28d944a2f411ca12437753ec193793559b415 (present; = remote Stage-6J audit branch HEAD)
STAGE6J_EVALUATOR_LOCAL_COMMIT                       = 698e929e51a55ec8ddce9b9cdfd14a5c56a9f3c5 (not present remotely, as declared)
STAGE6J_REPORT_BLOB                                  = 8c6ce04f5bbce93e4534b480a5114b8c23f2cf04 (not available to this session)

Audited blobs (identical at 6339221 and 578ee9c; 633922..578ee9c touches only 3 .md files):
  prototype/cpi0/stage6k/adapter.py      = caee6966e595401719a21a52785b22bdedc275a6
  prototype/cpi0/stage6k/collector.py    = 1cfe132139c0e8049dc065e9d005dca20404d260
  prototype/cpi0/cpi_profile_v0_1_5.py   = 14f18feb90fe511cc888493d8dbd9e9e47df251b
  prototype/cpi0/stage6k/test_stage6k.py = 11e63fcf74c575e34bd51cf12c7e11d17c058001
```

Record inconsistency (S0): the launch prompt and Stage-6K report cite qualification run
`37239950469`; Issue #31 cites `37240123941`. Neither run could be inspected from this
session (GitHub API access to this repository is denied by the session proxy).

## 3. Executable results

```text
$ python -m py_compile prototype/cpi0/cpi_profile_v0_1_5.py prototype/cpi0/stage6k/collector.py \
    prototype/cpi0/stage6k/adapter.py prototype/cpi0/stage6k/test_stage6k.py
PY_COMPILE = PASS (exit 0)

$ python -m unittest -v prototype/cpi0/stage6k/test_stage6k.py
Ran 27 tests in 1.306s
OK
UNITTESTS = 27/27 PASS
```

The committed suite passes, but it does not detect the defects in §§6–13: every
adversarial counterexample below was executed against the same unmodified modules using
the suite's own `_base_state()`, `SequenceTransport`, `_project()` and `_owner_comment()`
seams (harness summarized in Appendix A).

## 4. CPI6J-001 re-adjudication

Independent reproduction (Stage-6E native fixture = live HiVenues identities, see §11):

```text
B0 baseline                                    rejected | gate=issue374-comment-5981621424 FAIL | cand=pr399-comment-5981621690 FAIL
   -> 5981621690 is in history (lane=candidate, FAIL_OR_HOLD, 2026-10-04T15:30:51Z) and is the latest candidate event.
B1 + later OWNER PR#399 conversation comment
   "Owner acceptance: PASS. Approved for merge."  accepted_pending_gate_sync | next=synchronize_explicit_issue_374_owner_gate_acceptance | DE=False
B2 + still-later PR#399 "HOLD — new blocker"     rejected
B3 + still-later CHANGES_REQUESTED review         rejected
B4 + still-later inline review comment
   "Do not proceed until this is fixed."         rejected
B5 OWNER APPROVED review (empty body)             accepted_pending_gate_sync
B7 non-owner APPROVED review                      ignored (rejected)
```

Other current-candidate surfaces preserved but excluded from reduction: the PR #399
object (title/body) and the #398 issue object. Both are agent/charter text in native
practice and their exclusion is consistent with the preregistered model (the #374
object is the asymmetric case — see CPI6L-002). Review *dismissal* and other timeline
events are not collected (see CPI6L-007).

```text
CPI6J-001 = CLOSED
```

The `issue_number`/`pr_number` scope defect is repaired: current-PR conversation
comments, reviews and inline review comments all enter the candidate lane and the
temporal reducer. Residual risk on this channel arises only from the grammar and
owner-identification findings below, not from scoping.

## 5. CPI6J-002 re-adjudication

Native-surface scope: **closed.** Every OWNER comment on #374 enters the gate lane
regardless of wording (`"Informational note only."` → lane=gate, NONDECISIONAL).

Required cases (single later OWNER #374 comment, 2026-10-04T23:00:00Z):

```text
"Owner acceptance: PASS. The redesigned Stage-5D candidate …; #374 is satisfied."   PASS -> accepted
"Owner acceptance: PASS — usability gate satisfied by the #398 redesign."            PASS -> accepted
"Accepted. #374 is satisfied for Stage 5D."                                          PASS -> accepted
"PASS"                                                                               PASS -> accepted
"LGTM — ship it."                                                                    PASS -> accepted
"Stage 5D usability gate passed; the owner would continue using HiVenues."           PASS -> accepted
"The threshold is met; good to go."                                                  PASS -> accepted (no false HOLD)
Issue #374 object rewritten "Owner acceptance: PASS. #374 is satisfied.", closed/completed   accepted
```

But the CPI6J-002 harm — CPI stays `rejected / redesign` after explicit native owner
acceptance — remains reproducible through two independent mechanisms:

```text
"pass" / "Pass" / "Pass." / "Passed." / "passed"       NONDECISIONAL -> rejected
"PASS\n" / "PASS\r\n" / " PASS" / "**Pass**"           NONDECISIONAL -> rejected
"✅ PASS" / "Decision: PASS" / "Gate: PASS" / "#374: PASS" / "Owner acceptance: ✅ PASS"   NONDECISIONAL -> rejected
```
(CPI6L-003: "body exactly PASS" is only recognized for exact uppercase with no surrounding whitespace.)

```text
Explicit OWNER #374 PASS comment, then #374 closed as completed (body unchanged)     -> rejected (gate_latest = issue374 object, FAIL)
Explicit OWNER #374 PASS comment, then any later #374 activity / 1-second skew       -> rejected
Charter body + appended "Owner acceptance: PASS. #374 is satisfied.", closed         -> AdapterIncomplete (ambiguous)
```
(CPI6L-002: the #374 charter is classified FAIL via the word `fail-closed` and is timed by `issue.updated_at`.)

```text
CPI6J-002 = NOT CLOSED
  scope component      = CLOSED
  acceptance component = NOT CLOSED (CPI6L-002, CPI6L-003)
```

## 6. Temporal-reducer audit

```text
D1 gate FAIL -> later gate PASS                 accepted                     (correct)
D2 gate FAIL -> later candidate PASS            accepted_pending_gate_sync   (correct)
D3 gate PASS -> later candidate FAIL            rejected                     (correct)
D4 candidate FAIL -> later gate PASS            accepted, DE=False           (correct)
D5 gate PASS -> later cand FAIL -> later cand PASS   accepted                (CPI6L-008)
D6 same-second gate PASS / cand FAIL            rejected  (tie broken by "pr399…" > "issue374…")
D7 same-second gate FAIL / cand PASS            accepted_pending_gate_sync (same lexical tie-break)
D8 same-lane same-second, ids 999999999 FAIL vs 1000000000 PASS   FAIL wins (string compare of ids)
D9 same-second cand comment PASS vs CHANGES_REQUESTED review      review wins ("review" > "comment")
D10 old gate PASS edited after a later gate FAIL                   accepted  (CPI6L-005)
D11b baseline HOLD 5981621690 typo-edited after a later gate PASS  rejected  (CPI6L-005)
D12 gate PASS comment then close-completed #374                    rejected  (CPI6L-002)
D13 gate PASS comment then label change on #374                    rejected  (CPI6L-002)
D14 candidate PASS then any #374 activity                          rejected  (CPI6L-002)
M6  gate PASS comment with #374 updated_at +1s                     rejected  (CPI6L-002)
D15 "PASS, but HOLD on merge." (single source)                     FAIL_OR_HOLD (bare PASS not recognized) -> rejected
D15c "Accepted, but do not proceed until #374 is updated."          AMBIGUOUS -> AdapterIncomplete (fail closed)
```

Chronology assessment:

- `updated_at` is the wrong event-order semantic for a decision. It is a *last-edit*
  time, so a typo fix or formatting edit re-dates an old decision and lets it outrank
  a later one in either direction (CPI6L-005). Decision order should be `created_at`
  (or `submitted_at`), with an edit after a later decision treated as ambiguity
  requiring fail-closed re-confirmation, not as supersession.
- For the issue object, `updated_at` is not even an edit time: GitHub bumps it on new
  comments, label/assignee/state changes, etc. In the live baseline the #374 object
  already ties the latest #374 comment (`15:30:49Z`), and the comment wins only because
  `"issue374" < "issue374-comment-…"` lexicographically. Any skew or later activity
  makes the charter text the latest gate decision (CPI6L-002).
- Ties are resolved by `source_id` string order, which encodes surface names and
  digit counts rather than chronology (D6–D9). Conflicting decisive events with equal
  timestamps should fail closed (CPI6L-009).
- Ambiguous events fail closed only when they are a lane's latest decisive event; an
  ambiguous event followed by a later decisive event is silently superseded, which is
  acceptable.

## 7. Authority-grammar audit

Required cases:

```text
"next pass should redesign"          NONDECISIONAL   ok
"NOT ACCEPTED" / "**NOT ACCEPTED**"  FAIL_OR_HOLD    ok (not both)
"threshold"                          no HOLD         ok
"Not approved."                      NONDECISIONAL   ok (not PASS; but not FAIL either)
"Do not approve." / "I do NOT approve."  NONDECISIONAL  ok (not PASS)
"PASS, but do not proceed."          FAIL_OR_HOLD    safe
"Owner acceptance: PASS, but do not proceed until #374 is updated."   AMBIGUOUS (fail closed)
quoted historical PASS inside a rejection   AMBIGUOUS (fail closed, S1 availability)
"_Accepted_"                          NONDECISIONAL  (markdown emphasis false negative)
"pass"/"Pass"/"Passed."               NONDECISIONAL  (case false negative — CPI6L-003)
```

Defects found (all executed against `_classify_owner_source`; end-to-end effects in §13):

False PASS from negated, conditional or interrogative approval language — only six
exact negative phrases are masked:

```text
"I don't approve this."            PASS        "Not LGTM."                     PASS
"I can't approve this yet."        PASS        "Don't ship it." / "Do not ship it yet."  PASS
"I cannot approve this."           PASS        "Not good to go."               PASS
"Never approved."                  PASS        "Is this good to go?"           PASS
"This is not yet accepted."        PASS        "The gate is not yet satisfied." PASS
"This isn't accepted."             PASS        "Before I can approve, the canvas must match Preview."  PASS
"Would you approve this if the canvas matched?"  PASS
```

False NONDECISIONAL for explicit refusal or withdrawal (stale prior PASS stays current):

```text
"Approval withdrawn." / "I withdraw my acceptance." / "I revoke the earlier approval — do not merge."
"I would stop using HiVenues at this point." / "I would abandon the product here."
"I would not continue using HiVenues." / "Owner acceptance: NOT PASS" / "This doesn't pass."
"Does not pass the gate." / "Declined." / "Blocked." / "Needs redesign."
```

False FAIL/AMBIGUOUS from engineering prose (fail-closed but availability-destroying):
`fail-closed`, `failed run`, `previous HOLD is lifted`, `Rejection of Stage 5C stands …`
→ AMBIGUOUS → `AdapterIncomplete` for the whole HiVenues projection.

Implementation defect (`adapter.py` line 276):

```python
standalone = re.sub(r"[\\s*_`.!]+", "", pass_text).lower()
```

In a raw string `\\s` is a literal backslash plus the letter `s`, so the class strips
lowercase `s` and does **not** strip whitespace: `"pass"→"pa"`, `"Passed."→"Paed"`,
`"PASS\n"→"PASS\n"`. Only exact uppercase `PASS`/`PASSED` survives (the suite's test_008
uses exactly that). This is the same escaping class as the earlier commit
`3fdf59e Fix Stage-6K regex word-boundary escaping`.

Grammar assessment: an open-vocabulary lexical classifier over free prose cannot
reliably handle negation scope, conditionals, questions, quotation or withdrawal; the
Stage-6K masking list repairs specific strings, not the class.

## 8. Final-gate semantics

Native HiVenues governance (read from the frozen native objects): #398 body states
"owner acceptance governs #374"; #374 comment 5975499775 states the exit gate is
"explicit owner approval of the end-to-end lifecycle"; #374 was declared the
acceptance authority. The Stage-6K rule set — #374 is the final gate; a newer
candidate-level PASS yields `accepted_pending_gate_sync`; only a gate PASS yields
`accepted`; CPI never sets `d_e_authorized_by_cpi = true` — matches that governance.

`accepted_pending_gate_sync` is a safe, readable synchronization state: it retains
`forbidden: proceed_to_D_E`, sets `d_e_authorized_by_cpi = false`, and asks for an
explicit #374 record. If an owner PASS on PR #399 clearly intends to satisfy #374 itself,
pending-sync is conservative rather than materially wrong (S1 orientation at most).
It never became accidental authorization in any tested path.

Deviation: the reducer selects `accepted` whenever `gate_latest == PASS` and the latest
overall decision is PASS, even when a candidate FAIL/HOLD intervened after the gate PASS
(D5). By the preregistered rule ("gate PASS and no later current-candidate FAIL/HOLD
supersedes it") the intervening rejection supersedes the gate PASS, and the later
candidate PASS should produce `accepted_pending_gate_sync`, exactly as in D2
(CPI6L-008).

## 9. Profile-0.1.5 audit

```text
G1  issue-comment author_association mutated alone           CPIValidationError   ok
G1b author_association + revision co-mutated                 ACCEPTED   (self-attesting binding)
G2  review author_association mutated                        CPIValidationError   ok
G3a review state lowercase w/o revision                      CPIValidationError   ok
G3b review state lowercase co-mutated                        ACCEPTED   (enum upper()-normalized)
G3c review state MERGED                                      CPIValidationError   ok
G4  inline review comment author_association mutated          CPIValidationError   ok
G5  pr_number 'abc' / None                                    CPIValidationError   ok
G5  pr_number '399' / ' 399 '                                 ACCEPTED   (string ints)
G5b comment_id 5981621690.9                                   ACCEPTED   (float truncated)
G5c issue_number True with matching revision                 ACCEPTED   (bool as int)
G6  repository case alias                                     CPIValidationError   ok
G6b repository rebinding inside projection                    CPIValidationError   ok
G7  revision/content mismatch (updated_at)                    CPIValidationError   ok
G8a capture_cutoff before window_start                        CPIValidationError   ok
G8c naive (no-tz) timestamps throughout                       ACCEPTED
G8d mixed naive/aware timestamps                              LEAK TypeError (not CPIValidationError)
G8e date-only timestamps                                      ACCEPTED
G9  missing capture_cutoff                                    CPIValidationError   ok
G10 rejected-history projection relabelled accepted + d_e_authorized_by_cpi=True   ACCEPTED
G10b HiVenues transition state selected_authorized            ACCEPTED
G11 consecutive_equal_sweeps = "two"                          LEAK ValueError (not CPIValidationError)
```

Additivity: `git diff 23f28d9..578ee9c` adds `cpi_profile_v0_1_5.py` only; profiles
0.1.0–0.1.4 and all Stage-6A–6J paths are byte-unchanged. The 0.1.5 diff against 0.1.4
only adds checks/states. 0.1.5 does not weaken 0.1.4.

Assessment: author-association binding protects against accidental single-field
mutation only; because the profile cannot recompute `content_sha256` (raw `_object` is
not in the projection) a coordinated rewrite passes. The profile does not constrain
transition authority (`d_e_authorized_by_cpi`, state vs. OWNER-AUTHORITY-HISTORY),
so the no-external-authority invariant is enforced only in adapter code (CPI6L-012/013).

## 10. Collector / stabilization audit

```text
H1  body changed, same IDs/count, between sweeps     detected (digest differs); stabilizes only on changed state
H1b alternating A/B/A/B                              CollectorError (never stabilizes)   ok
H2  forged terminal empty-page digest                CollectorError   ok
H3  row content tampered vs receipt                  CollectorError (page SHA mismatch)   ok
H4  coherent forged receipt + rows                   ACCEPTED (receipt is self-attesting)
H5' mutation after the object's read in final sweep  not represented; mutation is after capture_cutoff  ok
H6  mutation before the object's read in final sweep forces another sweep; represented   ok
capture_cutoff = final equal sweep started_at; observed_at = capture_cutoff   verified in code and output
stabilization block exposes previous/current start, end, digest              verified
```

Stabilized-window semantics are now stated correctly: every object read in the final
sweep was read after `capture_cutoff` and equals its read in the previous sweep (before
`capture_cutoff`), so modulo an A→B→A change between the two reads the value held at
`capture_cutoff`. The ABA window and the self-attesting receipt (computed and validated
by the same process from the same rows; it detects nothing in production that the
sweep digest does not) are S1 residuals (CPI6L-014). Stage-6J capture-cutoff finding:
HARDENED.

## 11. Live native audit

```text
PRODUCTION_COLLECTOR (api.github.com) = NOT EXECUTABLE FROM THIS SESSION
  reason: session egress proxy returns 403 "GitHub access to this repository is not
  enabled for this session" for api.github.com/repos/etblink/HiVenues/*.
```

Independent read-only corroboration that was possible:

```text
git ls-remote https://github.com/etblink/HiVenues.git (2026-10-04 ~22:40Z)
  refs/heads/main            = 4fed1b4bcd65606124579fe8a643e55828655093  == fixture main source
  refs/pull/399/head         = 28eaf662df350e23ed02c25bde17bf78b311fa04  == fixture PR #399 head
  refs/pull/397/head         = e469282b39d533f1803dcd47b61663dbf05043de  == fixture PR #397 head
  refs/pull/{397,399}/merge  present; refs/pull/{391,393,395} have head refs only
  -> consistent with OPEN_PRS = [397, 399]

github.com/etblink/HiVenues/pull/399 (public HTML, read-only):
  Draft; "Stage 5D A–C: operator workspace and exact website publishing journey";
  latest owner conversation comment = "Owner review result — HOLD / redesign required"
  (abandonment), no later owner decision visible.
github.com/etblink/HiVenues/issues/398: body contains "owner acceptance governs #374".
```

The public HTML for #374 did not render its comment thread through the fetch tool, so
#374 comments were not independently re-observed live; the Stage-6E/6K fixture copies
were used. Within those limits the baseline (current candidate PR #399; latest gate
`issue374-comment-5981621424` FAIL; latest candidate `pr399-comment-5981621690` FAIL;
state `rejected`; next action `redesign_review_before_further_broad_implementation`)
is consistent with live HiVenues, and no later legitimate HiVenues advancement was
observed. The Stage-6K live qualification claim itself remains self-reported.

## 12. Previously closed controls

```text
FCP full native routing            adapt_fcp(): POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION /
                                   YES__STANDING_PROJECT_LEAD_DELEGATION /
                                   SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION;
                                   NEXT_RECOMMENDED_OPERATION records = 14         HOLDS
NFC publication vs theorem         authority_map: publication_and_provenance vs
                                   frozen_theorem_bearing_corpus; no transitions    HOLDS
PGH physical trial                 PHYSICAL_TRIAL_EXECUTION = prohibited;
                                   APPARATUS_REALIZATION_AND_TARGET_FREEZE = blocked_external;
                                   real-apparatus HARD UNSATISFIED                  HOLDS
Project Observatory                stage6e native snapshot FROZEN, unchanged since f1e7150;
                                   no Stage-6K write path (collector is GET-only)   HOLDS (derived, non-oracular)
Stage-6F repository substitution   G6/G6b and test_024 reject rebinding             HOLDS
```

## 13. New-defect search

Severity per launch prompt. S3 rationale used below: CPI emitting `accepted` for
HiVenues removes `forbidden: proceed_to_D_E` and `forbidden: declare_issue_374_satisfied`
and routes next action to `native_project_post_acceptance_authorization_gate`. When the
owner's latest explicit decision is a refusal, that encourages a prohibited canonical
consequence (declaring #374 satisfied / advancing toward D–E) even though
`d_e_authorized_by_cpi` stays false. If the Project Lead rules that an `accepted`
projection cannot "encourage", CPI6L-001/004/005 downgrade to S2; the final disposition
is unchanged.

### CPI6L-001 — S3 — negated/conditional/interrogative approval is classified PASS

Only six exact negative phrases are masked. A single OWNER comment on #374:
`"I don't approve this yet."`, `"This is not yet accepted — the canvas still diverges
from Preview."`, `"The gate is not yet satisfied."` or `"Not good to go."` →
`state = accepted`, `next_action = native_project_post_acceptance_authorization_gate`,
negative knowledge reduced to the two generic entries. On PR #399/#398 the same text
yields `accepted_pending_gate_sync` over a standing rejection (S2 there).

### CPI6L-002 — S2 — #374 issue object is a decisive gate event timed by `issue.updated_at`

The #374 charter body is classified `FAIL_OR_HOLD` (it contains "fail-closed safety
boundaries") and enters the gate lane with `event_time = issue.updated_at`, which
GitHub bumps on any later issue activity. Explicit OWNER #374 PASS followed by closing
#374 as completed, a label change, any later (even non-owner) #374 comment, or ordinary
one-second skew → `gate_latest = issue374 (FAIL)` → `rejected / redesign`. The baseline
only works because the object ties the latest comment and loses on string order. Charter
plus an appended PASS → AMBIGUOUS → `AdapterIncomplete`. The most natural acceptance
workflow (comment PASS, then close #374 completed) is projected as a rejection.

### CPI6L-003 — S2 — PASS normalization escaping bug; ordinary PASS forms unrecognized

`adapter.py:276` `r"[\\s*_`.!]+"` strips the letter `s` and not whitespace. Lowercase or
title-case `pass`/`Passed.`, a trailing newline, leading space, emoji, or `Decision:` /
`Gate:` / `#374:` labels → NONDECISIONAL → stale `rejected / redesign` after explicit
owner acceptance. This is the CPI6J-002 harm persisting.

### CPI6L-004 — S3 — explicit refusal/withdrawal is NONDECISIONAL; stale PASS stays current

After a gate PASS, an OWNER PR #399 comment `"Approval withdrawn."`,
`"I withdraw my acceptance; the canvas regression is back."`,
`"I would stop using HiVenues at this point."`, `"Owner acceptance: NOT PASS"` or
`"This doesn't pass."` leaves `state = accepted` (M3c). After a candidate PASS the same
text leaves `accepted_pending_gate_sync` (M3d). On #374 itself these cases currently
reach `rejected` only accidentally, via CPI6L-002.

### CPI6L-005 — S3 — edited comments re-date decisions (`updated_at` ordering)

An OWNER #374 PASS created 23:00 and typo-edited at 23:10, with an OWNER #374 FAIL at
23:05 → `accepted` (D10). Conversely, a cosmetic edit of the baseline HOLD 5981621690
after a later gate PASS → `rejected` (D11b, S2 direction).

### CPI6L-006 — S2 — owner identification: agent/engineering status under the OWNER account is treated as owner decision

Native HiVenues practice posts agent and CI-corrective prose as `etblink`/OWNER (e.g.
PR #397: `"@codex review"`, `"## CI #1657 + P1 corrective … CI #1657 failed …"`, all
OWNER; #374 comment 5975901037 "Owner acceptance candidate"; PR #399 body). Transplanting
the native PR #397 comment 5975729903 text onto PR #399 after a gate PASS → `rejected`
(M1). Agent-style status such as `"All checks passed; Stage 5D candidate is good to go
for owner review."` or `"CI approved; candidate ready for owner testing."` → PASS.
Neither native surface nor `author_association` separates the human owner's decision
from automation acting through the owner's account.

### CPI6L-007 — S2 — dismissed reviews still carry body-derived authority

An OWNER review with `state = DISMISSED` and body `"Looks good — approved."` → candidate
PASS → `accepted_pending_gate_sync` over a standing rejection (M4). A dismissal is a
native revocation; its time is not collected (event time stays `submitted_at`).

### CPI6L-008 — S2 — intervening candidate rejection does not supersede an earlier gate PASS

Gate PASS → candidate FAIL → candidate PASS → `accepted` (D5); preregistered semantics
and D2 symmetry require `accepted_pending_gate_sync`.

### CPI6L-009 — S1 — same-second ties resolved by `source_id` string order

`"pr399…" > "issue374…"`, `"review" > "comment"`, `"issue374" < "issue374-comment-…"`,
and digit-length string comparison of ids (D6–D9) decide conflicting same-second
decisions. Should fail closed.

### CPI6L-010 — S1 — over-broad AMBIGUOUS causes whole-projection unavailability

A PASS mentioning `fail-closed`, a lifted HOLD, a quoted prior decision, or
`"Accepted, but do not proceed …"` → `AdapterIncomplete`; no HiVenues projection at all.

### CPI6L-011 — S1 — brittle candidate binding

Candidate selection requires literal `#398` and `Stage 5D` in PR text and
`draft is True`; after acceptance, marking PR #399 ready-for-review → `AdapterInconsistent`
(M5). `Stage-5D` titling → empty candidate set.

### CPI6L-012 — S1 — profile hygiene

Co-mutation of `author_association`+`revision` accepted; string/float/bool integers
accepted (float truncated); naive and date-only timestamps accepted; mixed naive/aware
leaks `TypeError`; non-integer `consecutive_equal_sweeps` leaks `ValueError` (contrary to
preregistration §7 malformed-integer rule).

### CPI6L-013 — S1 — profile does not bind transition authority

A HiVenues projection with `state = accepted`, `d_e_authorized_by_cpi = true`, or
`state = selected_authorized`, over a rejected authority history, passes
`validate_projection`. The no-external-authority invariant is adapter-only.

### CPI6L-014 — S1 — receipt self-attestation and ABA residual

Page-SHA validation is computed and checked by the same process from the same rows;
only the cross-sweep digest has evidential value. A→B→A between sweep reads is undetectable.

### CPI6L-015 — S0 — qualification run identifier inconsistency

`37239950469` (launch prompt, Stage-6K report) vs `37240123941` (Issue #31).

### CPI6L-016 — S0 — escaping regression recurrence not covered by tests

test_008 exercises only exact uppercase `PASS`; no test covers case, whitespace or
negation variants, so CPI6L-001/003 were invisible to the committed suite.

### Carried-forward S1 (unchanged, not re-adjudicated in depth)

CPI6J-004 authority time binding (partially hardened; superseded in substance by
CPI6L-002/005), CPI6J-005 test provenance, CPI6H-004 repository case alias.

## 14. False bridge

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

No dependency, negative knowledge or transition in the HiVenues projection names NFC,
PGH or physics; test_026 and independent inspection agree. No new native
theory-specific evidence was found.

## 15. Federation optionality

```text
FEDERATION_OPTIONALITY = PASS
```

All four projections are produced independently from native sources; no projection
requires another project's projection or a federation service, and none was falsified.

## 16. Mutation audit

```text
NFC = NONE
FCP = NONE
PGH = NONE
HIVENUES = NONE (read-only: git ls-remote, public HTML fetch; no API writes, no API reads possible)
PROJECT_OBSERVATORY = NONE
STAGE6A_THROUGH_STAGE6K = UNCHANGED
LIVE_FEDERATION = NONE
LIVE_OBSERVATORY_INTEGRATION = NONE
EXTERNAL_PROJECT_EFFECT = NONE
REPAIRS = NONE
MERGES = NONE
PROJECT_CONTINUITY_RESEARCH = this single report file on audit/cpi0-stage6l-independent-owner-authority only
```

All adversarial harness code ran in a scratch directory outside the repository.

## 17. Final disposition

```text
STAGE6K_SUITE = 27/27 PASS (does not detect the findings below)
CPI6J_001 = CLOSED
CPI6J_002 = NOT CLOSED (scope closed; acceptance recognition and gate chronology not closed)
CAPTURE_CUTOFF = HARDENED
PAGE_SHA_RECEIPT = HARDENED (self-attesting residual S1)
PROFILE_0_1_5 = ADDITIVE, NOT WEAKENING (S1 hygiene residuals)
FINAL_GATE_SEMANTICS = MATCHES NATIVE GOVERNANCE (except CPI6L-008)
ACCEPTED_PENDING_GATE_SYNC_AS_AUTHORIZATION = NOT OBSERVED
LIVE_PRODUCTION_COLLECTOR = NOT EXECUTED (session egress denial); git/HTML corroboration only
FALSE_BRIDGE = NONE / NOT ESTABLISHED — HELD SPECULATION
FEDERATION_OPTIONALITY = PASS

S3 = 3   (CPI6L-001, CPI6L-004, CPI6L-005)
S2 = 5   (CPI6L-002, CPI6L-003, CPI6L-006, CPI6L-007, CPI6L-008)
S1 = 6   (CPI6L-009 … CPI6L-014)
S0 = 2   (CPI6L-015, CPI6L-016)
```

Final disposition:

`ARCHITECTURE_RECONSIDERATION_REQUIRED`

Rationale: the native-surface lanes, temporal reducer skeleton, capture-cutoff collector
and additive profile are sound and should be kept. The authority-*recognition* layer is
not repairable by further phrase lists. Three successive stages have produced S2
authority defects in it, and this audit finds (a) unbounded negation/withdrawal
false positives and false negatives in open-vocabulary prose, (b) no way to tell the
human owner's decision from automation posting as OWNER, and (c) decision chronology
built on mutable `updated_at` values. Recommended direction for the repair stage (not
performed here): require an explicit, structured, owner-only native decision record
(for example, a fixed decision line or label on #374/the candidate, with a documented
convention that automation never emits it); treat all other prose as nondecisional
context; order by creation/submission time; and fail closed on edits after a later
decision, same-second conflicts, and dismissed reviews. At minimum, REPAIR_REQUIRED
applies regardless of how the S3 rationale is adjudicated.

## Appendix A — reproduction harness (summary)

Run from `prototype/cpi0/stage6k` with that directory and `prototype/cpi0` on `sys.path`:

```python
import copy, test_stage6k as T, adapter as A
B = T._base_state
def oc(cid, body, t, n=399, created=None):
    c = T._owner_comment(cid, body, t, issue_number=n)
    if created: c["created_at"] = created
    return c
def run(s):
    p = T._project(s); t = p["transitions"][0]; return t["state"], t["next_action"]
GP = "Owner acceptance: PASS. #374 is satisfied."

# CPI6L-001
s = B(); s["issue374_comments"].append(oc(2, "I don't approve this yet.", "2026-10-04T23:00:00Z", n=374))
s["issue374"]["updated_at"] = "2026-10-04T23:00:00Z"; run(s)   # ('accepted', ...)

# CPI6L-002
s = B(); s["issue374_comments"].append(oc(20, GP, "2026-10-04T23:00:00Z", n=374))
s["issue374"].update(state="closed", state_reason="completed", updated_at="2026-10-04T23:01:00Z"); run(s)   # ('rejected', ...)

# CPI6L-003
A._classify_owner_source({"source_kind": "github_issue_comment", "_object": {"body": "pass"}})   # NONDECISIONAL

# CPI6L-004
s = B(); s["issue374_comments"].append(oc(3, GP, "2026-10-04T23:00:00Z", n=374)); s["issue374"]["updated_at"] = "2026-10-04T23:00:00Z"
s["pr_comments"][399].append(oc(4, "Approval withdrawn.", "2026-10-04T23:30:00Z")); run(s)   # ('accepted', ...)

# CPI6L-005
s = B(); s["issue374_comments"].append(oc(10, GP, "2026-10-04T23:10:00Z", n=374, created="2026-10-04T23:00:00Z"))
s["issue374_comments"].append(oc(11, "Owner acceptance result — NOT ACCEPTED. HOLD.", "2026-10-04T23:05:00Z", n=374))
s["issue374"]["updated_at"] = "2026-10-04T23:10:00Z"; run(s)   # ('accepted', ...)

# CPI6L-008
s = B(); s["issue374_comments"].append(oc(1, GP, "2026-10-04T23:00:00Z", n=374)); s["issue374"]["updated_at"] = "2026-10-04T23:00:00Z"
s["pr_comments"][399] += [oc(2, "Owner acceptance result — NOT ACCEPTED. HOLD.", "2026-10-04T23:01:00Z"),
                          oc(3, "Owner acceptance: PASS. Approved for merge.", "2026-10-04T23:02:00Z")]
run(s)   # ('accepted', ...) — expected accepted_pending_gate_sync
```
