# CPI-0 Stage-6D Independent Corrective Re-Audit Report 0.1.0

Date: 2026-10-04  
Status: FROZEN INDEPENDENT RE-AUDIT  
Governing issue: Project-Continuity-Research #23  
Parent audit: Stage 6B / Issue #21  
Corrective implementation: Stage 6C / Issue #22  
Final disposition: REPAIR_REQUIRED

## 1. Evaluator identity and independence statement

Evaluator: OpenAI ChatGPT, GPT-5.6 Sol

Execution environment: ChatGPT GitHub connector against repository-native GitHub sources.

I did not author the Stage-6C repair.

I did not use prior-conversation project memory as audit evidence and did not ask the Stage-6C repair author for interpretation.

The re-audit was performed by reading the Stage-6D launch contract and Issue #23 first, then independently checking the Stage-6B findings against native project state and the frozen Stage-6C implementation. Stage-6C self-tests were treated as evidence about intended behavior, not as proof of correctness.

No observed project, Project Observatory, or live external system was mutated during the audit.

## 2. Exact control commits and branch

Stage-6B independent audit commit:

`4e4d2c6b73e9e5a55fd2968de2f59a62bf55101c`

Stage-6C corrective report commit:

`d2f452bc6d36175869bf8ef11078aa92c3cb6d4b`

Stage-6D launch-control commit:

`737cd98787760d52d2695f98312609f1dda40b3e`

Stage-6D audit branch:

`audit/cpi0-stage6d-independent-reaudit`

The audit branch was verified to be exactly identical to the launch-control commit before this report was written.

Required report path:

`prototype/cpi0/stage6d/STAGE6D_INDEPENDENT_CORRECTIVE_REAUDIT_REPORT_0_1_0.md`

## 3. Native and control sources inspected

### 3.1 Project-Continuity-Research controls

- Issue #23 and launch comment 5983435560.
- `prototype/cpi0/stage6d/STAGE6D_INDEPENDENT_CORRECTIVE_REAUDIT_LAUNCH_PROMPT_0_1_0.md` at launch-control commit `737cd987...`, blob `1caf1805cd03c84521ca5b8fccf7b38e2435f9de`.
- Stage-6B report at audit commit `4e4d2c6...`, blob `c6589a863258facf6c951f69e5c24aaba28d3183`.
- Stage-6C preregistration at repair commit `d2f452b...`, blob `ff4fbfc8eb71a7621d8c0f825e3b0d401fa0b94e`.
- Stage-6C experiment report, blob `5ff9b9402d59fd3dcc620e1877735e84a341d390`.
- `prototype/cpi0/cpi_profile_v0_1_1.py`, blob `1bce851eace1bf634c60ccd6ae67d932d1e45b0b`.
- `prototype/cpi0/stage6c/source_packets.json`, blob `044a4deba6fe33ce902e4f5ab321f1206ddb5a6e`.
- `prototype/cpi0/stage6c/adapter.py`, blob `93a0a0da492eda880b8a08e328685f12902eada3`.
- `prototype/cpi0/stage6c/test_stage6c.py`, blob `3d4c5d51a8f6eb3f949bc1bb08a4880f061d5312`.
- `prototype/cpi0/stage6c/generated_projections.json`, blob `add76e2af9c9e1dad019842c2c2a74dc432a9b79`.
- Frozen profile 0.1.0 implementation `prototype/cpi0/cpi_profile.py`, blob `77ae65073949b2c8d5827872feadd0f2c2a6196f`, verified identical before and after Stage 6C.

The comparison from Stage-6B audit commit to Stage-6C repair commit shows only seven additive Stage-6C/profile-0.1.1 files and no modification of the frozen profile 0.1.0 or Stage-6A/Stage-6B evidence.

### 3.2 FCP native sources

Repository:

`etblink/Foundational-Convergence-Program`

Audited main:

`a41bc6101b63140ee2687e0cf67a47ab6be77215`

The repository main was verified still identical to that commit during Stage 6D.

Material native sources:

- `CURRENT_STATE.md`, blob `b5949af93a1855ae1d072fa4aaa4b1c29033579c`.
- `FCP_CHARTER.md`, blob `579819121d1733e1746868941a3a282de2cf1ac9`.

The native `CURRENT_STATE.md` contains the controlling present-tense state:

```text
EVIDENCE_TRIGGER_PGH = T1_STABLE_NEW_FOUNDATIONAL_COMPETITOR_CANDIDATE__FULFILLED
ACTIVE_SCIENTIFIC_OPERATION = NONE
NEXT_EXECUTION_STEP = POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION
NEXT_RECOMMENDED_OPERATION = POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION
NEXT_OPERATION_CLASS = READ_ONLY_SCIENTIFIC_SEQUENCING_ADJUDICATION
NEXT_OPERATION_AUTHORIZED = YES__STANDING_PROJECT_LEAD_DELEGATION
NEXT_OPERATION_AUTHORIZATION_BOUNDARY = SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION
FCP27_SELECTED = NO
NEXT_SCIENTIFIC_PHASE = NONE__POST_PGH_STAGE2_SEQUENCING_PENDING
```

The same native file expressly states that operational-routing fields inside completed-milestone sections are historical snapshots and that present-tense routing is controlled by the live Open-dependencies / Next-task material.

The full native file contains 14 exact `NEXT_RECOMMENDED_OPERATION =` records and 6 exact `NEXT_OPERATION_AUTHORIZED =` records.

### 3.3 HiVenues native sources

Repository:

`etblink/HiVenues`

Merged main:

`4fed1b4bcd65606124579fe8a643e55828655093`

The repository main was verified still identical to that commit during Stage 6D.

Material native sources:

- `README.md`, blob `ad9a0c0b64d0e074e0a315450713ddfb3d9c8f6a`.
- Issue #398, still open.
- Issue #398 owner-decision comment `5981621191`.
- Issue #374, still open; owner approval remains the Stage-5 exit requirement.
- Issue #342, preserving staged external-effect authority.
- PR #397, still open/unmerged, head `e469282b39d533f1803dcd47b61663dbf05043de`.
- PR #399, still open, draft, unmerged, head `28eaf662df350e23ed02c25bde17bf78b311fa04`.
- PR #399 owner review comment `5981621690`, which independently repeats the HOLD/redesign result.

The decisive Issue #398 owner comment states:

```text
Current A-C owner acceptance: FAIL
PR #399 must remain draft/unmerged.
Do not proceed to D-E.
Do not declare #374 satisfied.
Stop for redesign review before further broad implementation.
```

PR #399 comment 5981621690 is concordant: keep the PR draft/unmerged, do not proceed to D-E, and redesign the authoring surface.

### 3.4 NFC native source

Repository:

`etblink/Nested-Fibrational-Cosmology`

Publication main:

`5072d563b0a3dd4a7643be427cd47108216d8793`

Main was verified still identical during Stage 6D.

`PROVENANCE.md`, blob `69cdd64069cd0d24779a344fac0cd309bc54d811`, still routes scientific theorem authority to:

`archive/nfc-canonical-ed3047c2@ed3047c2cbc0abc34d2549dd27754e4d3d05af78`

tree:

`00ef55ff36d5e9663ca1ef2c9566e2bc1396f973`

and retains:

`HUMAN_POLICY_INTENT = UNRESOLVED`

plus the explicit rule not to use default-branch presence as a proxy for scientific authority.

### 3.5 PGH native source

Repository:

`etblink/Physical-Grammar-Hypothesis`

Main:

`2923875b40ea6901dfafda56a771c36876c4a220`

Main was verified still identical during Stage 6D.

`CURRENT_STATE.md`, blob `32c799bdd42d6c921140bf13bdb988fefa445169`, still states:

```text
NEXT_SCIENTIFIC_OPERATION = APPARATUS_REALIZATION_AND_TARGET_FREEZE
PHYSICAL_TRIAL_EXECUTION_AUTHORIZED = NO
WEB_TARGET_SEARCH = FORBIDDEN_WITHOUT_NEW_INDEPENDENT_TRIGGER
```

The current capsule still has no bound actual apparatus and `physical_trials_authorized = false`.

### 3.6 Project Observatory native source

Repository:

`etblink/Project-Observatory`

`snapshots/PROJECT_OBSERVATORY_SNAPSHOT_V0_2.md`

Current blob:

`e62a0b86e2317d7b441eb3d5ecf8ee71cc49460a`

The snapshot remains frozen and unmodified. It still says:

- `FCP_PROJECT_STATE = WAITING_FOR_EVIDENCE`
- `FCP_CANONICAL_COMMIT = a41bc6101b63140ee2687e0cf67a47ab6be77215`
- `HIVENUES_CANONICAL_COMMIT = bf9a0b4e61d57eed6bb5a81504d6e030f8b6ff7c`

The exact FCP commit named by the snapshot itself contains the fulfilled PGH trigger and post-PGH sequencing state.

### 3.7 False-bridge control source

Project-Continuity-Research Issue #19 still states:

`HiVenues/Hive -> NFC/PGH scientific bridge: HELD / UNESTABLISHED`

Repository-native searches for `HiVenues` in NFC, FCP, and PGH returned no scientific bridge source.

## 4. Re-adjudication of CPI6B-001 — FCP source-contract omission

### Result

`CPI6B-001 = REPAIR_INCOMPLETE`

Severity:

`S2`

### What Stage 6C gets right

The generated FCP projection now gives the correct frozen-boundary answer:

- current operation = `POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION`;
- transition state = `selected_authorized`;
- authorization basis = `YES__STANDING_PROJECT_LEAD_DELEGATION`;
- authorization boundary = `SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION`;
- prior evidence-triggered hold = fulfilled historical state;
- `FCP27_SELECTED = NO`.

Those values independently match the native FCP source.

The Stage-6C adapter also fails if its packet omits the expected precedence string.

### Why the repair is not sufficient

The Stage-6B failure was not merely that the wrong string had been chosen. The defect was that a hand-selected semantic window from the correct immutable blob could be mistaken for the controlling native state.

Stage 6C still relies on that same class of upstream semantic selection.

The Stage-6C `source_packets.json` FCP `current_state.text` is not the native `CURRENT_STATE.md` blob. It is a synthesized packet assembled from separated native regions:

- the current routing material around the live post-PGH state;
- the later Historical immutability / precedence rule.

It also introduces packet labels:

`[CURRENT ROUTING WINDOW]`

and

`[PRECEDENCE RULE]`

that do not exist in the native file.

The full native `CURRENT_STATE.md` has 14 exact `NEXT_RECOMMENDED_OPERATION` records. The Stage-6C adapter function `one(name)` requires exactly one occurrence in the packet text. Therefore the adapter cannot consume the full native file under its own extraction rule; it succeeds only because an upstream packet author has already selected the desired occurrence and discarded the others.

The adapter verifies only:

- an internal packet fingerprint;
- a SHA-256 of the packet's own `text`.

It does not verify that the supplied packet text is the content of the declared Git blob, nor does it verify a deterministic/verbatim derivation from that blob.

Thus the declared revision:

`git:a41bc610...:blob:b5949af...`

does not content-bind the semantic text actually interpreted by the adapter.

### Material consequence

The same immutable FCP blob can still be paired with differently curated packet text, and the adapter has no native-source check that proves the selected semantic window is the controlling one.

That is materially the Stage-6B failure mode: a consumer can obtain the wrong next action or authorization interpretation while carrying a correct Git commit/blob identity.

The frozen Stage-6C output happens to be correct; the source contract still does not prove it from the native source.

## 5. Re-adjudication of CPI6B-002 — HiVenues source-contract omission

### Result

`CPI6B-002 = CLOSED`

### Native-boundary verification

At the frozen boundary and at Stage-6D recheck:

- merged main is `4fed1b4...`;
- PR #397 is older and remains open/unmerged;
- PR #399 is the Stage-5D A-C candidate at head `28eaf662...`;
- PR #399 is draft/open/unmerged;
- Issue #398 comment 5981621191 is an owner rejection;
- owner result = `FAIL`;
- D-E must not proceed;
- #374 must not be declared satisfied;
- the next action is redesign review rather than acceptance/progression.

The Stage-6C generated projection transports those consequences correctly.

The adapter fails closed if the expected PR #399 packet or expected owner-decision packet is removed.

### Additional native source found

PR #399 also contains owner comment `5981621690`, omitted from the Stage-6C packet.

That omission does not change the safe consequence: it independently repeats HOLD/redesign, draft/unmerged, and no D-E progression.

Therefore the omission is not an additional S2 at this frozen boundary.

### Caveat moved to new-defect search

Although the specific Stage-6B HiVenues omission is closed, the general mechanism still depends on hand-selected issue/PR/comment materialization and does not prove that the selected source set is complete. That cross-cutting source-contract weakness is recorded separately below because it can re-create a future Stage-6B-style omission.

## 6. Re-adjudication of CPI6B-003 — projection/profile defect

### Result

`CPI6B-003 = REPAIR_INCOMPLETE`

Severity:

`S2`

### What Stage 6C gets right

Profile 0.1.1 is additive. Frozen profile 0.1.0 remains byte-identical.

Profile 0.1.1 requires:

- `producer`;
- `observed_at`;
- `source_kind`;
- `revision`.

It retains `commit` for Git sources.

It allows non-Git source kinds for:

- GitHub issue;
- GitHub issue comment;
- GitHub pull request;
- derived snapshot.

The generated HiVenues projection no longer pretends Issue #398, its owner comment, or PR #399 are revised by repository `main`.

`classify_freshness` compares `revision` strings, so if a caller supplies a changed comment/issue revision while main stays fixed, the projection becomes stale.

All four frozen Stage-6C project projections satisfy the structural validator as written.

### Why the repair is not sufficient

The profile claims source-native revision semantics but does not validate them.

For every source kind, the validator only checks:

- that `source_kind` is in the allowed set;
- that `revision` is non-empty.

There is no source-kind-specific revision grammar or identity check.

For example, a source declared as:

`source_kind = github_issue_comment`

can pass validation with an arbitrary non-empty `revision`, including a Git-style or unrelated token.

Therefore profile 0.1.1 does not enforce the Stage-6C preregistration requirement that the revision actually be source-native/content-bound.

The Stage-6C HiVenues revisions are also timestamp/state tokens rather than content-addressed identities:

- Issue #398: `github_issue:398:updated_at:...`
- owner comment: `github_issue_comment:5981621191:updated_at:...`
- PR #399: head + `updated_at` + state + draft.

The source packets separately contain `content_sha256`, but those content fingerprints are not carried into the profile's observed-source revision and are not used by `classify_freshness`.

The projected owner-comment source also does not preserve the owner-association predicate that the adapter used to decide that the comment is authoritative.

### Material consequence

A profile-conformant consumer can accept a non-Git source carrying a non-native or weak revision token and then classify it as fresh by string equality.

That can reproduce the Stage-6B-003 failure: a human-authority source can change semantically while a consumer believes the accepted revision token is authoritative and fresh.

The changed-revision unit test proves that the comparator reacts when the token changes; it does not prove that the profile requires the token to change whenever the authority-bearing source changes.

The schema-level guarantee is therefore incomplete.

## 7. Re-adjudication of CPI6B-004 — Observatory comparison defect

### Result

`CPI6B-004 = CLOSED`

### Verification

Project Observatory Snapshot v0.2 remains unchanged at blob:

`e62a0b86e2317d7b441eb3d5ecf8ee71cc49460a`

Stage 6C does not rewrite it.

The Stage-6C comparison now separates project/claim validity:

#### FCP

Snapshot claim:

`WAITING_FOR_EVIDENCE`

Referenced native commit:

`a41bc6101b63140ee2687e0cf67a47ab6be77215`

Native state at that same commit:

`POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION`

Stage-6C result:

`CONTRADICTED_BY_REFERENCED_NATIVE_STATE`

This independently matches the native FCP file.

#### HiVenues

Snapshot canonical identity:

`bf9a0b4e61d57eed6bb5a81504d6e030f8b6ff7c`

Current main:

`4fed1b4bcd65606124579fe8a643e55828655093`

Stage-6C preserves the older historical identity separately and marks current freshness stale.

#### Overall

`MIXED__NO_BLANKET_VALIDITY`

No blanket historical-validity label remains.

## 8. Positive controls

### 8.1 Native project identities remain independently recoverable

During Stage 6D, each audited native main remained identical to the frozen project identity used by Stage 6B/6C:

- NFC main = `5072d563...`
- FCP main = `a41bc610...`
- PGH main = `2923875b...`
- HiVenues main = `4fed1b4b...`

The project states can be reconstructed without Project Observatory or CPI.

### 8.2 NFC authority separation

PASS.

Publication main remains distinct from frozen theorem authority.

No projection or Stage-6C repair promotes publication main into theorem authority.

### 8.3 PGH external-action prohibition

PASS.

The current native source and Stage-6C projection both preserve:

- no actual bound apparatus;
- physical trial execution not authorized;
- target/web search forbidden absent a new independent trigger.

### 8.4 HiVenues consequence boundary

PASS at the frozen state.

The Stage-6C projection carries no CPI authority to merge PR #399, proceed D-E, close #374, or perform external deployment effects.

### 8.5 Additive preservation

PASS.

Stage 6C adds the 0.1.1 profile and Stage-6C artifacts without modifying frozen profile 0.1.0.

The Stage-6B-to-Stage-6C compare shows only additive files.

### 8.6 Observatory non-rewrite

PASS.

Snapshot v0.2 remains unchanged.

## 9. New-defect search

The audit did not stop after checking the four original findings.

### CPI6D-001 — native-source binding and source-set completeness

`PRIMARY_CLASS = NEW_SOURCE_CONTRACT_DEFECT`

`SEVERITY = S2`

#### Evidence

Stage-6C source packets contain hand-selected/synthesized semantic text while declaring native GitHub/Git revision identities.

For FCP, the semantic packet is not the native blob and is deliberately narrowed so repeated routing fields disappear.

For HiVenues:

- the Issue #398 packet is an excerpt rather than the complete issue object;
- the owner-comment packet is selected independently;
- the PR #397/#399 packet `text` values are synthesized summaries rather than the native PR bodies;
- the native PR #399 owner comment 5981621690 is not part of the selected source set.

The adapter checks packet-internal hashes, not provenance from the declared native object.

There is no Stage-6C collector/discovery proof demonstrating that all decision-bearing issue comments, reviews, current candidate PRs, or relevant native file regions were materialized.

#### Consequence

A source packet can remain internally self-consistent while omitting a later or competing authority source, or while presenting a curated semantic view under a correct native revision label.

That can change next action, authority interpretation, or state conclusion.

This is the cross-cutting reason CPI6B-001 remains incomplete and a continuing risk for future HiVenues-style authority changes even though the frozen CPI6B-002 facts are currently correct.

### CPI6D-002 — revision semantics not enforced by profile 0.1.1

`PRIMARY_CLASS = NEW_PROFILE_SCHEMA_DEFECT`

`SEVERITY = S2`

#### Evidence

`validate_projection` validates allowed `source_kind` and only non-emptiness of `revision`.

It does not enforce that:

- a Git revision actually corresponds to its declared commit/blob/tree;
- a GitHub issue revision names the declared issue;
- a comment revision names the declared comment;
- a PR revision names the declared PR/head/state;
- a non-Git revision contains a content fingerprint or other content-bound identity.

`classify_freshness` then trusts the supplied revision string.

#### Consequence

A structurally valid 0.1.1 projection can reintroduce commit-like or arbitrary freshness semantics for non-Git authority.

That undermines the profile-level guarantee required to close CPI6B-003.

### Nonmaterial additional source observation

The omitted PR #399 owner comment 5981621690 is concordant with the included Issue #398 owner comment 5981621191.

At this boundary it does not change the next action and is not separately classified S2.

### New S3 search

No S3 defect was found.

No Stage-6C path was found that authorizes or encourages prohibited canonical mutation or external consequence solely from CPI/Observatory state.

## 10. False-bridge control

Required control:

```text
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

Result:

PASS.

Basis:

- Project-Continuity-Research Issue #19 still records the bridge as HELD / UNESTABLISHED.
- No `HiVenues` scientific dependency source was found in the native NFC, FCP, or PGH repositories.
- NFC authority remains internal to its frozen theorem/provenance model.
- PGH physical-trial authority remains internal to PGH's external-apparatus sequence.
- FCP current sequencing authority does not depend on HiVenues/Hive.
- HiVenues owner acceptance or deployment state does not authorize NFC/PGH science.

No false scientific bridge promotion was observed.

## 11. Federation optionality

`FEDERATION_OPTIONALITY = PASS`

I independently reconstructed the controlling project states from native repositories:

### NFC

Native provenance identifies the publication surface, frozen theorem authority, and unresolved historical human-policy intent.

### FCP

Native `CURRENT_STATE.md` plus charter identify the fulfilled PGH trigger, current post-PGH sequencing action, standing sequencing-only authorization, and no selected FCP27.

### PGH

Native `CURRENT_STATE.md` identifies the real-apparatus dependency, next operation, and trial prohibition.

### HiVenues

Native main, Issues #398/#374/#342, PRs #397/#399, and owner comments recover the current rejected-candidate/redesign state.

Project Observatory and CPI remain derived and optional. They are not needed as the sole intelligibility layer.

## 12. Mutation audit

### Mutations performed by this Stage-6D evaluation before the required report commit

- NFC: NONE
- FCP: NONE
- PGH: NONE
- HiVenues: NONE
- Project Observatory: NONE
- live infrastructure/external systems: NONE
- Stage-6A artifacts: NONE
- Stage-6B report: NONE
- Stage-6C implementation: NONE
- merge: NONE
- live integration: NONE

### Stage-6C preservation check

Stage 6C was verified additive relative to the Stage-6B audit commit.

Frozen profile 0.1.0 remained blob-identical.

### Stage-6D authorized mutation

Exactly this required report on:

`audit/cpi0-stage6d-independent-reaudit`

No repair is performed by this audit.

## 13. Finding summary

### Original Stage-6B findings

- `CPI6B-001` — `REPAIR_INCOMPLETE` — S2
- `CPI6B-002` — `CLOSED`
- `CPI6B-003` — `REPAIR_INCOMPLETE` — S2
- `CPI6B-004` — `CLOSED`

### New-defect search

- `CPI6D-001` — `NEW_SOURCE_CONTRACT_DEFECT` — S2
- `CPI6D-002` — `NEW_PROFILE_SCHEMA_DEFECT` — S2
- S3 findings — 0

CPI6D-001 is cross-cutting and is also the reason CPI6B-001 cannot be considered closed. CPI6D-002 is cross-cutting and is also the reason CPI6B-003 cannot be considered closed. They are not independent evidence counts for purposes of inflating severity; they identify the unresolved mechanisms.

## 14. Architecture consideration

`ARCHITECTURE_RECONSIDERATION_REQUIRED` was considered because the remaining defects are systematic source-contract/revision-semantics problems.

It is not selected at this gate.

Reason:

- no S3 authority leak was found;
- federation optionality still passes;
- native projects remain independently intelligible;
- the false bridge remains absent;
- the defects are concrete and appear repairable without making Project Observatory authoritative or collapsing project-local governance.

A future repair would need to establish, at minimum, native-object/content binding and a completeness/discovery contract for decision-bearing source sets, plus source-kind-specific revision validation. This report does not implement those repairs.

## 15. Final disposition

`REPAIR_REQUIRED`

Reason:

At least two material S2 mechanisms remain unresolved.

Stage 6C produces the correct frozen FCP and HiVenues answers, and it correctly fixes the Observatory blanket-validity output, but it does not yet prove those answers from sufficiently bound native sources or enforce the promised non-Git revision semantics at the profile level.

Therefore the Stage-6D rules prohibit either PASS disposition.

Stop boundary:

DO NOT REPAIR FINDINGS.  
DO NOT MERGE.  
DO NOT PROCEED TO LIVE INTEGRATION.
