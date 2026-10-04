# CPI-0 Stage-6L Independent Owner-Authority Reducer Re-Audit Launch Prompt 0.1.0

Date: 2026-10-04
Status: FROZEN EXECUTION PROMPT
Program: CPI-0 — Cross-Project Interoperability

## Role

You are the independent evaluator for CPI-0 Stage 6L.

You did not author Stage 6K.

Determine whether Stage 6K closes the two Stage-6J S2 findings without introducing a new S2/S3 defect.

Treat Stage-6K tests, CI, qualification records and reports as claims to check, not proof.

Do not use prior conversation memory as audit evidence.

## Controlling independent audit evidence

Stage-6J evaluator:

`Claude Opus 5.5 (Anthropic)`

The evaluator's session could not push to GitHub.

Reported local audit commit:

`698e929e51a55ec8ddce9b9cdfd14a5c56a9f3c5`

Exact Stage-6J report blob independently verified from the evaluator-provided report bytes:

`8c6ce04f5bbce93e4534b480a5114b8c23f2cf04`

Stage-6J launch-control commit:

`23f28d944a2f411ca12437753ec193793559b415`

Stage-6J final disposition:

`REPAIR_REQUIRED`

The remote Stage-6J audit branch remains at launch-control because the evaluator lacked push access and a later Project Lead publication attempt was deliberately reverted when it could not preserve the exact report blob.

Do not assume an audit report exists remotely at the Stage-6J report path. Use the Stage-6K preregistration/report's exact external-evidence declaration plus any evaluator-provided Stage-6J report supplied to your session.

## Stage-6J S2 findings

### CPI6J-001

Current PR conversation comments were preserved as sources but excluded from owner-authority adjudication because they carried `issue_number` while Stage 6I tested `pr_number`.

Claude reproduced an OWNER PASS on PR #399 conversation while prior rejection remained. Stage 6I incorrectly emitted `rejected / redesign`.

### CPI6J-002

All #374 comments were enumerated, but gate authority entered current scope only through brittle literal body references. Explicit later owner PASS could therefore be dropped.

Claude reproduced, among others:

- `Owner acceptance: PASS. The redesigned Stage-5D candidate ... #374 is satisfied.`
- `Owner acceptance: PASS — usability gate satisfied by the #398 redesign.`
- `Accepted. #374 is satisfied for Stage 5D.`
- `PASS`
- `LGTM — ship it.`
- `Stage 5D usability gate passed; the owner would continue using HiVenues.`

Stage 6I could remain `rejected / redesign` after native owner acceptance.

## Stage-6K control

Stage-6K corrective report commit:

`30358f34a23d386987fa7e0f482582ceab1fd46e`

Successful code qualification run:

`37239950469`

Qualified code commit:

`633922113543b478376411534d03bced887cfb4d`

Stage 6K adds:

- profile 0.1.5;
- native-surface owner authority scope;
- temporally ordered owner-decision history;
- `accepted_pending_gate_sync`;
- `accepted`;
- capture-cutoff timing;
- stronger authority revision binding;
- page-SHA receipt validation.

## Read first

1. `prototype/cpi0/stage6k/STAGE6K_OWNER_AUTHORITY_REDUCER_CORRECTIVE_PREREGISTRATION_0_1_0.md`
2. `prototype/cpi0/stage6k/EXPERIMENT_REPORT_0_1_0.md`
3. `prototype/cpi0/stage6k/STAGE6K_CLEAN_CHECKOUT_QUALIFICATION_0_1_0.md`
4. `prototype/cpi0/cpi_profile_v0_1_5.py`
5. `prototype/cpi0/stage6k/collector.py`
6. `prototype/cpi0/stage6k/adapter.py`
7. `prototype/cpi0/stage6k/test_stage6k.py`

Inspect native HiVenues/FCP/NFC/PGH/Project Observatory evidence independently.

## A. Required executable validation

Run:

```text
python -m py_compile \
  prototype/cpi0/cpi_profile_v0_1_5.py \
  prototype/cpi0/stage6k/collector.py \
  prototype/cpi0/stage6k/adapter.py \
  prototype/cpi0/stage6k/test_stage6k.py

python -m unittest -v prototype/cpi0/stage6k/test_stage6k.py
```

Record exact results.

## B. Reproduce CPI6J-001

Independently verify baseline PR #399 owner conversation comment:

`5981621690`

is present in the current authority history and participates in temporal reduction.

Inject a later OWNER PR #399 conversation comment:

`Owner acceptance: PASS. Approved for merge.`

Verify it is not dropped.

With the older #374 FAIL still current, expected safe semantic result is:

```text
state = accepted_pending_gate_sync
D_E_AUTHORIZED_BY_CPI = false
next_action = synchronize explicit #374 owner gate acceptance
```

Then inject a still-later current-candidate FAIL/HOLD and verify the result returns to rejected.

Search for any other current-candidate conversation/review/inline source kind that is preserved but excluded from reduction.

## C. Reproduce CPI6J-002

Verify **all OWNER comments on #374 are gate-lane events because of the native surface**, not because their body names a PR or Stage.

Independently test at minimum:

- hyphenated `Stage-5D` PASS;
- `#398 redesign` PASS;
- `Accepted. #374 is satisfied for Stage 5D.`;
- body exactly `PASS`;
- `LGTM — ship it.`;
- `Stage 5D usability gate passed; the owner would continue using HiVenues.`;
- `The threshold is met; good to go.`.

The last case must classify PASS without a false HOLD from the letters inside `threshold`.

Also test current Issue #374 object rewritten/closed-completed with explicit owner PASS.

## D. Temporal authority reduction

Adversarially test ordering.

Required cases:

### Gate FAIL -> later gate PASS
Latest gate PASS must supersede older gate FAIL.

### Gate FAIL -> later candidate PASS
Must become `accepted_pending_gate_sync`, not rejected and not externally authorized.

### Gate PASS -> later candidate FAIL/HOLD
Must become rejected.

### Candidate FAIL -> later gate PASS
Must become accepted, while CPI still grants no external-effect authority.

### Multiple decisions
Test equal/near-equal timestamps and stable source-ID tie-breaking. Determine whether tie semantics can produce materially wrong authority.

### Edited comments
Because comment revision uses updated_at, test whether editing an older comment can incorrectly outrank a later decision. Assess whether updated_at is the right event-order semantic or whether created_at/edit history matters.

### Ambiguous single event
A source with explicit PASS and explicit FAIL/HOLD must fail closed.

Search for any chronology rule that can leave a materially stale owner decision current.

## E. Authority grammar adversarial audit

Stage 6K deliberately recognizes ordinary language. Search for false positives and false negatives.

At minimum test:

- `next pass should redesign` must not be PASS;
- `NOT ACCEPTED` must not be both PASS and FAIL;
- `threshold` must not be HOLD;
- `not approved` must not be PASS;
- `do not approve` must not be PASS;
- `PASS, but do not proceed` should not silently become accepted;
- quoted/historical acceptance language inside a rejection comment;
- Markdown emphasis/punctuation variants;
- lowercase/uppercase variants.

Any grammar defect that materially changes next action/authority is S2.

## F. Final-gate semantics

Independently assess the Stage-6K rule:

- #374 is the final acceptance gate;
- candidate-level PASS can create `accepted_pending_gate_sync`;
- only gate PASS can create `accepted`;
- CPI never grants D-E/external-effect authorization.

Determine whether this matches native HiVenues governance.

If a later owner PASS on PR/#398 clearly intends to satisfy #374 itself, assess whether the pending-sync representation is materially wrong or a safe/readable synchronization state.

## G. Profile 0.1.5

Attack:

- author_association mutation on issue comment;
- author_association mutation on review;
- author_association mutation on inline review comment;
- review-state enum;
- malformed integer IDs;
- repository rebinding;
- revision/content mismatch;
- observation timestamp parsing/order;
- observed_at != capture_cutoff;
- missing capture_cutoff.

Confirm 0.1.5 is additive and does not weaken 0.1.4.

## H. Collector / observation hardening

Attack receipt page-SHA validation.

Verify:

- page content change with unchanged IDs/count is detected;
- forged page_sha256 is rejected;
- empty terminal-page digest is validated;
- capture_cutoff = start of final equal sweep;
- observed_at = capture_cutoff;
- late-in-final-sweep mutation is not represented as observed after the cutoff.

Recheck stabilized-window semantics from Stage 6J.

## I. Real native production path

Where possible, execute Stage-6K production collection against live HiVenues read-only GitHub.

Independently verify:

- current open PR set;
- current candidate;
- #374/#398/current-PR owner authority sources;
- baseline temporal decision history;
- baseline state/next action.

Distinguish legitimate later HiVenues advancement from a Stage-6K defect.

## J. Previously closed controls

Recheck:

- FCP full native routing and 14 historical/current routing records;
- NFC publication vs theorem authority;
- PGH physical-trial prohibition/apparatus prerequisite;
- Project Observatory derived/non-oracular status;
- Stage-6F repository substitution closure.

## K. False bridge

Absent new native theory-specific evidence:

```text
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

for HiVenues/Hive -> NFC/PGH.

## L. Federation optionality

Required unless independently falsified:

`FEDERATION_OPTIONALITY = PASS`

## M. New-defect search

Actively search for S2/S3 defects, especially:

- lexical authority false positives;
- authority false negatives;
- wrong timestamp supersession;
- edited-comment chronology;
- gate/candidate precedence errors;
- accepted_pending_gate_sync becoming accidental authorization;
- issue object and comment disagreement;
- duplicate/tied events;
- owner identification errors;
- profile/adapter mismatch;
- source preserved but absent from reduction;
- receipt/digest holes;
- observer authority leakage.

## Severity

- S0 cosmetic;
- S1 fail-closed/orientation degradation without materially wrong safe next action;
- S2 materially wrong owner authority/state/next action;
- S3 prohibited external/canonical consequence could be authorized or encouraged.

## Required output

Commit exactly one report:

`prototype/cpi0/stage6l/STAGE6L_INDEPENDENT_OWNER_AUTHORITY_REAUDIT_REPORT_0_1_0.md`

Include:

1. evaluator identity / independence;
2. exact control identities;
3. executable results;
4. CPI6J-001 re-adjudication;
5. CPI6J-002 re-adjudication;
6. temporal-reducer audit;
7. authority-grammar audit;
8. final-gate semantics;
9. profile-0.1.5 audit;
10. collector/stabilization audit;
11. live native audit;
12. previously closed controls;
13. new-defect search;
14. false bridge;
15. federation optionality;
16. mutation audit;
17. final disposition.

## Final disposition

Use exactly one:

- `PASS__STAGE6J_S2_FINDINGS_CLOSED`
- `PASS_WITH_NONMATERIAL_FINDINGS`
- `REPAIR_REQUIRED`
- `ARCHITECTURE_RECONSIDERATION_REQUIRED`
- `INSUFFICIENT_AUDIT`

Any unresolved/new S2 means at least `REPAIR_REQUIRED`.

## Write boundary

Write only the Stage-6L audit report to the dedicated audit branch.

Do not repair.
Do not merge.
Do not mutate observed projects or Project Observatory.
Do not enter live federation/integration.

## Stop rule

After committing the report, stop and report:

- audit commit;
- report blob;
- executable result;
- findings by severity;
- final disposition.
