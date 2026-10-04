# CPI-0 Stage-6F Independent Native-Binding Re-Audit Report 0.1.0

Date: 2026-10-04  
Status: FROZEN INDEPENDENT RE-AUDIT  
Governing issue: Project-Continuity-Research #25  
Parent independent audit: Stage 6D / Issue #23  
Corrective implementation: Stage 6E / Issue #24  
Final disposition: REPAIR_REQUIRED

## 1. Evaluator identity / independence

Evaluator: OpenAI ChatGPT, GPT-5.6 Sol.

I did not author the Stage-6E repair.

I began from the frozen Stage-6F launch prompt at launch-control commit:

`933489f51905ab3d2fe267e07836e3422b1e292d`

and used repository-native GitHub evidence plus the frozen Stage-6E artifacts. I did not use prior-conversation memory as audit evidence and did not ask the Stage-6E repair author for interpretation.

The dedicated audit branch was independently verified to be exactly identical to the launch-control commit before this report was written.

No observed project, Project Observatory, or live integration surface was mutated during the audit.

## 2. Exact control identities

Stage-6D independent audit commit:

`ab9e4db3359613efcf03ffdf58d36ef8f09a276a`

Stage-6E corrective report commit:

`6ceac2fc650c82a136a28fcc86ec144e66adb94b`

Stage-6F launch-control commit:

`933489f51905ab3d2fe267e07836e3422b1e292d`

Audit branch:

`audit/cpi0-stage6f-independent-native-binding`

Required report:

`prototype/cpi0/stage6f/STAGE6F_INDEPENDENT_NATIVE_BINDING_REAUDIT_REPORT_0_1_0.md`

Stage-6E implementation blobs inspected:

- `prototype/cpi0/cpi_profile_v0_1_2.py` — `7645416bd4d3b4ddf2bd18734c62f1bf3fb5c58f`
- `prototype/cpi0/stage6e/collector.py` — `befb0fabfd7b2d9fdc286799b672d556d7e25a0f`
- `prototype/cpi0/stage6e/adapter.py` — `d8f2176b911cd0c9eba52d2f3729d9a524d41056`
- `prototype/cpi0/stage6e/test_stage6e.py` — `c209095fa16edc50fb96af3be8fb61ceb2661fa5`

Frozen source-manifest blob:

`6058c696a8a77ad1bd91fe5d0f19518d7d0cd11e`

Frozen HiVenues snapshot blobs:

- core — `da87bb377cb704ef43046bc3eb315e63585d2cba`
- PRs — `38509668c3f9d18bfdfd91717ad25abfe0577e0d`
- PR auxiliary — `a45f85e93ffe0989913cb12b42fe0cd450187a06`

## 3. Executable-code result

### 3.1 Clean-checkout attempt

The required independent local checkout was attempted with:

`git clone --no-checkout https://github.com/etblink/Project-Continuity-Research.git`

The runtime returned:

`Could not resolve host: github.com`

A direct raw-GitHub retrieval attempt from the execution container was also unable to establish outbound GitHub connectivity. Therefore the environment did not permit reconstructing the complete exact Stage-6E checkout and fixture tree through the local process environment.

This limitation is not silently waived.

### 3.2 Exact committed code that was executable locally

Using repository-native connector bytes, I materialized the exact committed profile and collector blobs and recomputed their Git blob identities locally:

`cpi_profile_v0_1_2.py = 7645416bd4d3b4ddf2bd18734c62f1bf3fb5c58f`

`collector.py = befb0fabfd7b2d9fdc286799b672d556d7e25a0f`

Both matched the committed Git blob identities exactly.

For those exact files:

`python -m py_compile` = PASS

import of `cpi_profile_v0_1_2` = PASS

import of `collector` = PASS

The exact profile implementation was also executed adversarially; the material result is reported in Section 6.

### 3.3 Full committed unittest result

A complete process execution of:

`python -m unittest -v prototype/cpi0/stage6e/test_stage6e.py`

from the exact complete committed tree could not be obtained because the local runtime could not acquire the remaining exact checkout/fixtures.

An invocation from the partially materialized tree failed at module loading because the exact test module was not locally present; that is an environment/materialization failure, not a Stage-6E assertion failure, and is not counted as a test result.

Therefore:

`COMMITTED_STAGE6E_UNITTEST_PROCESS_RESULT = BLOCKED_BY_EXECUTION_ENVIRONMENT`

`EXACT_PROFILE_COMPILE_IMPORT = PASS`

`EXACT_COLLECTOR_COMPILE_IMPORT = PASS`

`EXACT_ADAPTER_TEST_LOCAL_COMPILE_IMPORT = NOT_COMPLETED`

I considered whether this requires `INSUFFICIENT_AUDIT`. It does not determine the final disposition here, because the independent native/source and exact-profile audits below positively falsify closure with two S2 mechanisms. The executable limitation prevents executable evidence from supporting a PASS; it does not erase independently demonstrated repair failures.

## 4. Native-source binding audit

### 4.1 Exact Git mirror binding

I independently fetched each Stage-6E mirror and its upstream native file at the declared frozen native commit/ref.

All six mirror Git blob identities matched upstream exactly, and the fetched content was byte-identical:

- NFC `PROVENANCE.md` — `69cdd64069cd0d24779a344fac0cd309bc54d811`
- FCP `CURRENT_STATE.md` — `b5949af93a1855ae1d072fa4aaa4b1c29033579c`
- FCP `FCP_CHARTER.md` — `579819121d1733e1746868941a3a282de2cf1ac9`
- PGH `CURRENT_STATE.md` — `32c799bdd42d6c921140bf13bdb988fefa445169`
- HiVenues `README.md` — `ad9a0c0b64d0e074e0a315450713ddfb3d9c8f6a`
- Project Observatory Snapshot v0.2 — `e62a0b86e2317d7b441eb3d5ecf8ee71cc49460a`

Result:

`GIT_NATIVE_BINDING = PASS`

Stage 6E removes the Stage-6C failure mode in which a semantic excerpt could masquerade under the full native Git blob identity.

### 4.2 FCP full-file trap

The exact native FCP `CURRENT_STATE.md` at:

`a41bc6101b63140ee2687e0cf67a47ab6be77215`

contains exactly 14 occurrences of:

`NEXT_RECOMMENDED_OPERATION =`

The full file remains intact; the historical routing records were not trimmed away.

The current post-PGH trigger:

`EVIDENCE_TRIGGER_PGH = T1_STABLE_NEW_FOUNDATIONAL_COMPETITOR_CANDIDATE__FULFILLED`

occurs exactly once. In the native file it is in the live `Open dependencies` / `Next-task status` area and shares its fenced controlling block with:

`NEXT_RECOMMENDED_OPERATION = POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION`

`NEXT_OPERATION_AUTHORIZED = YES__STANDING_PROJECT_LEAD_DELEGATION`

`NEXT_OPERATION_AUTHORIZATION_BOUNDARY = SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION`

`FCP27_SELECTED = NO`

The adapter consumes the full file, verifies the native precedence statement, requires a unique fulfilled-PGH trigger marker, extracts the fenced block surrounding that marker, rejects duplicate keys within the selected block, and requires the expected routing values.

Independent result:

`FCP_CURRENT_ROUTE = POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION`

`FCP_AUTHORIZATION = YES__STANDING_PROJECT_LEAD_DELEGATION`

`FCP_BOUNDARY = SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION`

`PRIOR_EVIDENCE_HOLD = FULFILLED_HISTORY`

`FCP27_SELECTED = NO`

No frozen-boundary S2 was found in this full-file selector.

A future-hardening observation remains: the selector proves the precedence statement exists and anchors on the unique fulfilled-PGH marker rather than structurally proving the marker remains beneath a particular heading. At this exact frozen source, however, the marker is unique and located in the native controlling area, so this is not separately classified as an S2 finding.

## 5. Source-set completeness audit

### 5.1 Frozen HiVenues native set is factually complete

I independently queried repository-native GitHub state and compared it with the Stage-6E frozen snapshots.

At audit time the native GitHub state remained field-for-field concordant with the frozen Stage-6E objects, so no later project advancement had to be subtracted.

Confirmed:

- open PR page 1 = PRs `397`, `399`;
- open PR page 2 = empty;
- Issue #398 conversation comments = exactly `5981621191`;
- Issue #398 page 2 = empty;
- PR #397 conversation comments = 21; page 2 empty;
- PR #399 conversation comments = exactly `5981621690`; page 2 empty;
- PR #397 reviews = 11; page 2 empty;
- PR #399 reviews = 0; page 2 empty;
- PR #397 inline review comments = 12; page 2 empty;
- PR #399 inline review comments = 0; page 2 empty;
- PR #397 review threads = 6;
- PR #399 review threads = 0.

The complete frozen native objects for Issue #398, Issue #374, PR #397, PR #399, their stored conversations, reviews, inline comments, and review threads all matched current repository-native GitHub responses.

Therefore the Stage-6E frozen HiVenues answer is factually correct.

### 5.2 CPI6F-001 — completeness proof is self-attested rather than native-bound

`SEVERITY = S2`

`CLASS = SOURCE_SET_COMPLETENESS_DEFECT`

The committed `collect_hivenues()` implementation does not itself enumerate GitHub at the observation boundary. It reads three committed JSON snapshots and validates their own `discovery` fields.

For most enumerated review/comment collections, the completeness checks are internal consistency checks:

- snapshot says page 2 is empty;
- snapshot page-1 count equals stored-object count;
- snapshot discovered IDs equal stored-object IDs.

The preregistration required the collector to record the native enumeration endpoint/query identity and page-completeness evidence. The committed discovery records contain counts/IDs/`page2_empty`, but they do not content-bind those assertions to the native enumeration response or otherwise let the offline collector prove that the native endpoint actually returned no omitted object.

The manifest hard-codes regression controls for:

- open PR numbers `[397, 399]`;
- Issue #398 comment `5981621191`;
- PR #399 conversation comment `5981621690`.

Those controls protect the already-known frozen objects. They do not prove that an additional native authority object was not omitted before the snapshots were committed.

I performed a coherent-omission attack on the exact frozen review structure: remove one PR #397 review object, remove the same ID from the snapshot's `discovered_ids`, decrement `page1_count`, and leave `page2_empty = true`. Every committed collector check for that review set still succeeds.

The same structural weakness means a newly material owner comment/review that exists natively but is omitted from both the frozen object array and its self-reported discovery list can remain invisible while the collector calls the discovery set complete, unless it happens to be one of the few hard-coded expected IDs.

The frozen Stage-6E set happens to be complete. The mechanism does not prove completeness.

Material consequence:

A competing or later authority-bearing comment/review can be omitted coherently from the snapshot and therefore from semantic adjudication while the Stage-6E collector returns `complete = True`. That can change current candidate acceptance, next action, or authority interpretation.

Result:

`CPI6D-001_NATIVE_SOURCE_BINDING_AND_SOURCE_SET_COMPLETENESS = REPAIR_INCOMPLETE`

The Git-native-binding half is repaired. The source-set-completeness half remains S2.

## 6. Profile-0.1.2 adversarial audit

### 6.1 Additive preservation

Profile 0.1.0 blob remained:

`77ae65073949b2c8d5827872feadd0f2c2a6196f`

across Stage 6D, Stage 6E, and Stage 6F launch control.

Profile 0.1.1 blob remained:

`1bce851eace1bf634c60ccd6ae67d932d1e45b0b`

across those same controls.

Profile 0.1.2 did not exist at the Stage-6D audit commit and was added in Stage 6E.

Result:

`PROFILE_0_1_2_ADDITIVE = PASS`

### 6.2 Revision grammar checks that pass

Profile 0.1.2 does materially improve on 0.1.1.

It rejects an arbitrary nonempty revision string.

It reconstructs and exact-compares source-kind-specific revisions.

It requires Git commit/path/blob fields and binds the Git revision to commit/blob/content digest.

It requires issue number / comment ID / PR number and source-kind-specific state fields.

It rejects a revision whose issue/comment/PR identity token or digest token disagrees with the corresponding descriptor fields.

`classify_freshness` validates current source descriptors before comparing revision values, rather than accepting an arbitrary current revision string.

Those repairs are real.

### 6.3 CPI6F-002 — GitHub native identity is not repository-bound

`SEVERITY = S2`

`CLASS = PROFILE_NATIVE_IDENTITY_AND_FRESHNESS_DEFECT`

For GitHub issue and PR source kinds, the native IDs are repo-local identities:

- `issue:<number>`
- `pull_request:<number>`

The profile requires a `repository` field, but neither the GitHub `native_id` nor the GitHub revision grammar includes or cross-checks that repository identity.

`classify_freshness` validates the supplied current source and checks:

- same `source_kind`;
- same `native_id`;
- same revision.

It does not require the current `repository` or `ref` to match the observed source.

I executed the exact committed profile implementation with a valid PR #399 descriptor, then changed only:

`repository = etblink/HiVenues`

to:

`repository = other/Authority`

while retaining the same repo-local PR number, native ID, content-bound revision fields, and revision.

Exact result:

`validate_source(cross_repository_PR) = ACCEPTED`

`classify_freshness(... cross_repository_PR ...) = fresh`

This is not merely cosmetic. Pull-request and issue numbers are scoped by repository. A repo-local authority source can therefore be rebound to a different repository without the profile detecting an identity change, and freshness can still report `fresh`.

That violates the Stage-6F requirement that the revision's native object identity agree with the source fields and creates a direct remote-authority / identity-laundering path.

The collector currently emits `etblink/HiVenues` consistently, so the frozen generated projection is factually correct. The profile-level guarantee remains insufficient for conforming callers and future freshness comparisons.

Result:

`CPI6D-002_PROFILE_REVISION_ENFORCEMENT = REPAIR_INCOMPLETE`

`CPI6B-003_PROFILE_MECHANISM = REPAIR_INCOMPLETE`

## 7. Required re-adjudication

### CPI6B-001 — FCP source-contract omission

`CPI6B-001 = CLOSED`

The original FCP curated-window failure is repaired.

The Stage-6E FCP mirror is the exact complete native Git blob. All 14 repeated historical/current `NEXT_RECOMMENDED_OPERATION` records remain present. The adapter consumes that full source and independently resolves the native current post-PGH routing and sequencing-only authorization.

This closure does not close CPI6D-001's separate HiVenues source-set completeness mechanism.

### CPI6B-003 — projection/profile defect

`CPI6B-003 = REPAIR_INCOMPLETE`

`SEVERITY = S2`

Arbitrary revision strings are now rejected, but profile 0.1.2 still permits cross-repository substitution of repo-local GitHub native identities and may classify such a source as fresh.

### CPI6D-001 — native-source binding / source-set completeness

`CPI6D-001 = REPAIR_INCOMPLETE`

`SEVERITY = S2`

Native Git byte binding is closed.

Source-set completeness is not independently bound to native GitHub enumeration and can survive a coherent omission.

### CPI6D-002 — revision semantics enforcement

`CPI6D-002 = REPAIR_INCOMPLETE`

`SEVERITY = S2`

The source-kind revision grammar is substantially stronger, but GitHub repository identity is not part of the native identity/revision equivalence enforced by the profile/freshness path.

## 8. Positive controls

### 8.1 FCP

PASS.

The frozen native source independently yields:

`POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION`

with:

`YES__STANDING_PROJECT_LEAD_DELEGATION`

and:

`SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION`

The prior evidence hold remains fulfilled history and FCP27 remains unselected.

### 8.2 HiVenues

PASS at the frozen Stage-6E boundary.

Independent native GitHub state confirms:

- merged main remains `4fed1b4bcd65606124579fe8a643e55828655093`;
- PR #399 is the current Stage-5D candidate;
- PR #399 is open, draft, and unmerged;
- Issue #398 owner decision `5981621191` = owner acceptance FAIL;
- PR #399 owner comment `5981621690` = HOLD / redesign required;
- do not proceed D-E;
- do not declare #374 satisfied;
- next action = redesign review before further broad implementation.

### 8.3 NFC

PASS.

Publication main remains a publication/provenance surface and is not promoted into theorem authority.

The native provenance still routes frozen theorem authority to:

`archive/nfc-canonical-ed3047c2@ed3047c2cbc0abc34d2549dd27754e4d3d05af78`

and explicitly rejects default-branch presence as a proxy for scientific authority.

### 8.4 PGH

PASS.

Native PGH state still says:

`NEXT_SCIENTIFIC_OPERATION = APPARATUS_REALIZATION_AND_TARGET_FREEZE`

`PHYSICAL_TRIAL_EXECUTION_AUTHORIZED = NO`

`WEB_TARGET_SEARCH = FORBIDDEN_WITHOUT_NEW_INDEPENDENT_TRIGGER`

Real apparatus remains a required unsatisfied prerequisite.

### 8.5 Project Observatory

PASS.

Snapshot v0.2 remains blob:

`e62a0b86e2317d7b441eb3d5ecf8ee71cc49460a`

and was not modified.

Its FCP component still says `WAITING_FOR_EVIDENCE` while the exact native FCP commit named by that snapshot contains the fulfilled PGH trigger and post-PGH sequencing state.

Therefore:

`FCP_SNAPSHOT_COMPONENT = CONTRADICTED_BY_REFERENCED_NATIVE_STATE`

and no blanket historical-validity promotion is justified.

### 8.6 Additive Stage-6E preservation

PASS.

The Stage-6D-to-Stage-6E comparison is additive for the Stage-6E/profile-0.1.2 artifacts; frozen profile 0.1.0 and 0.1.1 blobs remain unchanged.

## 9. New-defect search

Two material defects were found:

### CPI6F-001

`SOURCE_SET_COMPLETENESS_DEFECT`

`S2`

A committed snapshot can coherently omit a native review/comment while keeping its internal count/ID/page flags self-consistent, and the offline collector has no content-bound native enumeration receipt that exposes the omission.

### CPI6F-002

`PROFILE_NATIVE_IDENTITY_AND_FRESHNESS_DEFECT`

`S2`

Repo-local GitHub identities are not repository-bound. Cross-repository substitution can pass `validate_source` and be classified fresh.

No S3 defect was found.

No path was found by which the Stage-6E projection itself directly authorizes prohibited canonical mutation or external physical/deployment consequence.

The two S2 defects are repairable source-contract/profile defects; the audit does not require architecture reconsideration at this boundary.

## 10. False-bridge negative control

Project-Continuity-Research Issue #19 natively states:

`HiVenues/Hive -> NFC/PGH scientific bridge: HELD / UNESTABLISHED`

Independent repository-native searches found no HiVenues scientific-bridge source in NFC, FCP, or PGH.

Apparent NFC matches for the substring `Hive` were occurrences inside words such as `archive`, not Hive-project evidence.

Required control:

`DEPENDENCY = NONE / NOT ESTABLISHED`

`STATUS = HELD SPECULATION`

Result:

PASS.

## 11. Federation optionality

`FEDERATION_OPTIONALITY = PASS`

NFC, FCP, PGH, HiVenues, and the Observatory comparison were independently intelligible from their own native project evidence.

No native project's current state required CPI or Project Observatory to become the sole authority/oracle.

## 12. Mutation audit

During the audit:

`NFC_MUTATION = NONE`

`FCP_MUTATION = NONE`

`PGH_MUTATION = NONE`

`HIVENUES_MUTATION = NONE`

`PROJECT_OBSERVATORY_MUTATION = NONE`

`STAGE6A_THROUGH_STAGE6E_REWRITE = NONE`

`LIVE_FEDERATION = NONE`

`LIVE_EXTERNAL_EFFECT = NONE`

The Stage-6F audit branch was unchanged from launch control before this report.

The only intended repository mutation is this required Stage-6F report on:

`audit/cpi0-stage6f-independent-native-binding`

No repair is included.

## 13. Final disposition

Finding count:

`S2 = 2`

`S3 = 0`

Re-adjudication:

`CPI6B-001 = CLOSED`

`CPI6B-003 = REPAIR_INCOMPLETE__S2`

`CPI6D-001 = REPAIR_INCOMPLETE__S2`

`CPI6D-002 = REPAIR_INCOMPLETE__S2`

The native Git-binding repair and frozen project-state conclusions are materially correct.

The two cross-cutting Stage-6D mechanisms are not both closed:

1. source-set completeness remains self-attested rather than native-enumeration-bound;
2. profile-0.1.2 GitHub identity/freshness remains vulnerable to cross-repository rebinding.

No S3 was found.

Final Stage-6F disposition:

`REPAIR_REQUIRED`

Per the Stage-6F stop rule, no repair, merge, or live integration follows this report.
