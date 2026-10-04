# CPI-0 Stage-6B Independent Source-Contract Sufficiency Audit Report 0.1.0

Date: 2026-10-04
Status: FROZEN INDEPENDENT AUDIT
Governing issue: Project-Continuity-Research #21
Parent research issue: #19
Final disposition: REPAIR_REQUIRED

## 1. Evaluator identity and independence statement

Evaluator: OpenAI ChatGPT, GPT-5.6 Sol
Execution environment: ChatGPT GitHub connector against repository-native GitHub sources
Audit mode: independent, read-only except for this required report on the dedicated audit branch

I did not use prior-conversation project memory as audit evidence and did not ask the Stage-6A adapter author for interpretation. The audit followed the required anti-contamination order:

1. read Issue #21, the Stage-6B launch prompt, and the governing audit packet;
2. reconstruct NFC, FCP, PGH, and HiVenues independently from their native repositories and current GitHub state;
3. freeze those Pass-1 conclusions;
4. inspect the frozen Stage-6A generated projections;
5. only after identifying mismatches, inspect Stage-6A source packets, adapter code, tests, preregistration, and report.

No observed project, Project Observatory, or live external system was mutated.

## 2. Exact audit controls

CPI research control commit:
3795ceda33b808d29a255e9d14b2d25dccf0181b

Stage-6B launch-control commit:
d85c7355119c673159bda750759d7e0ff8408b09

Stage-6A frozen report commit:
aac2a05b25bdf2dfb8b1b979645e64824e07adea

Audit branch:
audit/cpi0-stage6b-independent

Required report path:
prototype/cpi0/stage6b/STAGE6B_INDEPENDENT_SOURCE_CONTRACT_SUFFICIENCY_AUDIT_REPORT_0_1_0.md

The audit treats 3795ceda33b808d29a255e9d14b2d25dccf0181b as the frozen CPI source-preservation comparison boundary and d85c7355119c673159bda750759d7e0ff8408b09 as the branch-start control containing the evaluator prompt.

## 3. Native-source identities inspected

### NFC

Repository:
etblink/Nested-Fibrational-Cosmology

Observed main:
5072d563b0a3dd4a7643be427cd47108216d8793

Material native sources inspected included:
- README.md
- PROVENANCE.md, blob 69cdd64069cd0d24779a344fac0cd309bc54d811
- governance/NFC_PROVENANCE_HARDENING_CLOSURE_V0_1.md
- governance/NFC_PROVENANCE_HARDENING_EXECUTION_V0_1.md
- governance/NFC_PROVENANCE_HARDENING_PREREGISTRATION_V0_1.md
- CITATION.cff

Frozen theorem authority:
archive/nfc-canonical-ed3047c2
commit ed3047c2cbc0abc34d2549dd27754e4d3d05af78
tree 00ef55ff36d5e9663ca1ef2c9566e2bc1396f973

### FCP

Repository:
etblink/Foundational-Convergence-Program

Observed main:
a41bc6101b63140ee2687e0cf67a47ab6be77215

Material native sources inspected included:
- CURRENT_STATE.md, blob b5949af93a1855ae1d072fa4aaa4b1c29033579c
- FCP_CHARTER.md, blob 579819121d1733e1746868941a3a282de2cf1ac9
- EPISTEMIC_RULES.md
- FRAMEWORK_REGISTER.md
- SOURCE_REGISTER.md
- CLAIM_LEDGER.md
- repository governance/handoff indexes and current PGH/FCP routing material

### PGH

Repository:
etblink/Physical-Grammar-Hypothesis

Observed main:
2923875b40ea6901dfafda56a771c36876c4a220

Material native sources inspected included:
- CURRENT_STATE.md, blob 32c799bdd42d6c921140bf13bdb988fefa445169
- README.md
- HYPOTHESIS.md
- RESEARCH_LOG.md
- meta/PGH_CANONICAL_INDEX.json
- handoffs/PGH1_D1_EXPERIMENT_READINESS_PREPARATION_HANDOFF_0_1_0.md
- governance/PGH1_D1_EXPERIMENT_READINESS_PREPARATION_PREREGISTRATION_0_1_0.md
- relevant successor/admission handoffs

### HiVenues

Repository:
etblink/HiVenues

Observed merged main:
4fed1b4bcd65606124579fe8a643e55828655093

Material native sources inspected included:
- README.md, blob ad9a0c0b64d0e074e0a315450713ddfb3d9c8f6a
- docs/HIVENUES_END_STATE_PRODUCT_DOCTRINE_0_2_0.md
- docs/HIVENUES_CANONICAL_USER_JOURNEY_0_2_0.md
- docs/CURRENT_ARCHITECTURE.md
- docs/HIVENUES_ERA7_STAGE4E_LIVE_PUBLICATION_0_1_0.md
- docs/HIVENUES_ERA7_STAGE5B_REAUTHORIZATION_0_1_0.md
- Issue #342
- Issue #374
- Issue #396
- Issue #398 and its owner-acceptance comment
- PR #397, head e469282b39d533f1803dcd47b61663dbf05043de
- PR #399, head 28eaf662df350e23ed02c25bde17bf78b311fa04

### Historical observer comparator

Repository:
etblink/Project-Observatory

Snapshot:
snapshots/PROJECT_OBSERVATORY_SNAPSHOT_V0_2.md
blob e62a0b86e2317d7b441eb3d5ecf8ee71cc49460a
observed_at 2026-09-14T21:04:00Z

## 4. Pass 1 — independent native reconstruction

### 4.1 NFC

Minimum safe observer state:

- publication main is a publication/citation/provenance surface, not theorem authority;
- frozen theorem authority is archive/nfc-canonical-ed3047c2 at ed3047c2cbc0abc34d2549dd27754e4d3d05af78, tree 00ef55ff36d5e9663ca1ef2c9566e2bc1396f973;
- the restored canonical and historical release tags are provenance/routing facts, not new scientific results;
- the frozen scientific canon has not changed;
- mechanical provenance and representative content continuity are established;
- the human policy motive for the historical remove/re-root event remains unresolved;
- no default-branch presence rule may be used as a proxy for theorem authority.

Current versus historical:
publication main is the current routing surface; the archive ref is the current frozen theorem source; v1.0-canon-rewrite is a historical release anchor.

Dependency/trigger state:
none is required for the safe theorem-authority interpretation at this audited scope.

### 4.2 FCP

Minimum safe observer state:

- Method 0.2.1 is active prospectively;
- the latest canonical scientific operation is FCP_PGH_STAGE2_A_H_TAXONOMY_GATE;
- the previously selected EVIDENCE_TRIGGERED_HOLD is historical and its named PGH trigger has been fulfilled;
- PGH Stage 2 classified the current PGH object as a nonframework physical model/postulate; no FW-PGH exists and PGH empirical truth remains unadjudicated;
- no active scientific operation is running;
- the current next operation is POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION;
- that next operation is authorized under standing Project Lead delegation, but only as a read-only sequencing adjudication;
- no subsequent substantive FCP science is authorized until that sequencing operation selects it;
- FCP27 remains unselected.

Exact current routing assertion from native CURRENT_STATE.md:

ACTIVE_SCIENTIFIC_OPERATION = NONE
NEXT_EXECUTION_STEP = POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION
NEXT_RECOMMENDED_OPERATION = POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION
NEXT_OPERATION_CLASS = READ_ONLY_SCIENTIFIC_SEQUENCING_ADJUDICATION
NEXT_OPERATION_AUTHORIZED = YES__STANDING_PROJECT_LEAD_DELEGATION
NEXT_OPERATION_AUTHORIZATION_BOUNDARY = SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION
NEXT_NUMBERED_PHASE_SELECTED = NO
FCP27_SELECTED = NO
NEXT_SCIENTIFIC_PHASE = NONE__POST_PGH_STAGE2_SEQUENCING_PENDING

Native CURRENT_STATE.md expressly warns that completed-milestone routing fields are preserved as historical snapshots and that present-tense routing is controlled by the live Open dependencies / Next-task status material.

### 4.3 PGH

Minimum safe observer state:

- active candidate grammar: PGH-GRAM-0010;
- active package: PGH-OBJ-0052;
- package is A0-A9 admitted and empirically untested;
- FCP taxonomy outcome is nonframework physical model/postulate, not empirical confirmation or refutation;
- D1 mechanically ganged three-pole switch interface is qualified as the current adversarial physical interface design;
- no actual apparatus is bound;
- TGT-047 is next available but not assigned or reserved;
- target freeze is not complete;
- analysis preregistration is not complete;
- no physical response data exist;
- positive empirical PGH credit is none;
- physical trial execution is not authorized;
- public/web/registry target search remains suspended/forbidden absent a new independent trigger.

Current next scientific operation:
APPARATUS_REALIZATION_AND_TARGET_FREEZE.

Required sequence:
apparatus realization and target freeze, then negative-only analysis preregistration, then and only then physical trial execution and response data.

The readiness package is infrastructure only. Synthetic fixtures do not bind an apparatus, assign a target, produce empirical evidence, or substitute for external physical action.

### 4.4 HiVenues

Minimum safe observer state at audit time:

- canonical merged main remains 4fed1b4bcd65606124579fe8a643e55828655093;
- PR #397 remains open and unmerged and is an older Stage-5C candidate, not canonical main;
- Issue #398 remains the active Stage-5D bounded redesign charter;
- PR #399 is the newer Stage-5D A-C candidate, is draft/unmerged, and has head 28eaf662df350e23ed02c25bde17bf78b311fa04;
- owner acceptance, not machine qualification, governs the #374 usability gate;
- the owner has already rejected the current PR #399 A-C candidate;
- the current owner result is FAIL;
- PR #399 must remain draft/unmerged;
- D-E must not proceed;
- #374 must not be declared satisfied;
- the next bounded product action is redesign/review of the authoring model, not progression past the failed gate.

The decisive Issue #398 owner assertion is:

Current A-C owner acceptance: FAIL.
PR #399 must remain draft/unmerged.
Do not proceed to D-E.
Do not declare #374 satisfied.
Stop for redesign review before further broad implementation.

The ordinary-authoring failure is specifically about the visual-builder interaction model, canvas/preview fidelity, contextual editing, chrome-versus-host-content distinction, and first-run state. It is not merely copy polish.

External-consequence interpretation:
the active Stage-5D candidate work does not itself authorize arbitrary live production mutation. Issue #342 preserves staged consequence gates; PR #399 records no real provider/VPS/DNS/TLS/Hive/payment mutation; the owner rejection stops further broad implementation at the redesign boundary.

## 5. Pass 2 — comparison against Stage-6A projection

The following answers the ten required audit questions for each project.

### 5.1 NFC

Q1 Canonical-source sufficiency — PASS.
The projection preserves publication main versus the exact frozen theorem authority.

Q2 Authority sufficiency — PASS.
Publication/provenance authority and scientific theorem authority are purpose-scoped and distinct.

Q3 Candidate/canonical separation — PASS.
No candidate state is falsely promoted; frozen theorem canon and publication surface remain distinct.

Q4 Negative knowledge — PASS.
HUMAN_POLICY_INTENT = UNRESOLVED is preserved rather than guessed.

Q5 Dependency/trigger sufficiency — PASS.
No decision-critical dependency or trigger is omitted at the audited provenance-routing scope.

Q6 Freshness sufficiency — PASS at the frozen source identity.
The exact main and frozen canon identities are explicit.

Q7 Human-authority sufficiency — PASS.
No human policy motive is fabricated and no project-local authority is invented.

Q8 Consequence boundary — PASS.
The projection cannot be read as moving theorem authority to main or changing scientific status.

Q9 Supersession/historical state — PASS.
Historical release anchoring is not confused with current theorem-source selection.

Q10 Omitted-source discovery — PASS at material scope.
The additional native governance/closure sources inspected did not change the safe projection.

Result: NO MATERIAL NFC OMISSION.

### 5.2 FCP

Q1 Canonical-source sufficiency — FAIL.
The adapter names the correct CURRENT_STATE.md blob but materializes a superseded routing excerpt instead of the controlling present-tense routing from that same immutable blob.

Q2 Authority sufficiency — FAIL.
The projection says the selected post-recurrence sequencing operation is not authorized. Native current state says the actual next operation is post-PGH Stage-2 sequencing and is authorized under standing Project Lead delegation, sequencing-only.

Q3 Candidate/canonical separation — PASS.
FCP27 remains unselected and no new framework is falsely promoted.

Q4 Negative knowledge — PARTIAL PASS.
The prior evidence-triggered hold is correctly labeled historical rather than current waiting-for-trigger state, but the projection still anchors to an obsolete downstream routing checkpoint.

Q5 Dependency/trigger sufficiency — FAIL.
The native state says the PGH T1 trigger fulfilled the prior hold. The projection omits that fulfilled-trigger consequence and the current post-PGH sequencing boundary.

Q6 Freshness sufficiency — FAIL semantically.
Commit identity is current, but a selected semantic window from within the current file is stale/superseded. Commit equality alone therefore gives a false sense of freshness.

Q7 Human-authority sufficiency — FAIL.
The generic separate-authorization rule is retained, but the current standing Project Lead authorization for the sequencing-only operation is lost.

Q8 Consequence boundary — FAIL at S2, not S3.
The projection is conservative about authorization, so it does not directly authorize a prohibited external effect, but it materially recommends the wrong next operation and wrong authorization state.

Q9 Supersession/historical state — FAIL.
Native CURRENT_STATE.md explicitly says historical checkpoint routing fields are preserved and superseded for present routing. Stage-6A selected one of those superseded values.

Q10 Omitted-source discovery — FAIL.
Reading the full exact CURRENT_STATE.md blob materially changes the projection without requiring any additional repository file.

Result: MATERIAL FCP OMISSION.

### 5.3 PGH

Q1 Canonical-source sufficiency — PASS.
The authoritative current-state source and candidate identity are preserved.

Q2 Authority sufficiency — PASS.
The projection does not substitute derived navigation metadata for canonical markdown/Git authority.

Q3 Candidate/canonical separation — PASS.
PGH-OBJ-0052 is represented as active and empirically untested, not confirmed.

Q4 Negative knowledge — PASS.
The full do_not_assume set is transported, including no empirical support/refutation, no assigned TGT-047, no apparatus, no analysis preregistration, no trial authority, and no strong-PGH confirmation.

Q5 Dependency/trigger sufficiency — PASS for the current action.
Real apparatus is represented as a HARD unsatisfied dependency and apparatus realization is the current trigger.

Q6 Freshness sufficiency — PASS at the frozen native main identity.
The native main inspected still supports the same current action.

Q7 Human/external authority sufficiency — PASS.
The projection requires an external physical prerequisite and does not fabricate apparatus realization.

Q8 Consequence boundary — PASS.
Physical trial execution is explicitly prohibited.

Q9 Supersession/historical state — PASS.
Earlier target-discovery history remains suspended negative knowledge and is not mistaken for the current next operation.

Q10 Omitted-source discovery — PASS at material current-action scope.
The readiness handoff adds the mandatory sequence and implementation detail, but does not change the safe current action or trial prohibition. The do_not_assume list already preserves analysis-preregistration incompleteness.

Result: NO MATERIAL PGH OMISSION.

### 5.4 HiVenues

Q1 Canonical-source sufficiency — FAIL.
Merged main is correct, but the bounded-work source set is incomplete: it stops at PR #397 and Issue #398 body text while omitting the newer PR #399 and the decisive owner-rejection comment on Issue #398.

Q2 Authority sufficiency — PARTIAL FAIL.
The projection correctly says owner acceptance governs the usability gate, but it does not transport the owner’s actual decision: FAIL.

Q3 Candidate/canonical separation — FAIL.
PR #397 is correctly noncanonical, but it is no longer the latest material candidate. PR #399 is a newer draft/unmerged candidate and is the candidate that owner acceptance rejected.

Q4 Negative knowledge — PARTIAL PASS.
Machine qualification is correctly forbidden from substituting for owner acceptance. However, the stronger current negative state — current A-C candidate rejected, do not proceed D-E, do not close #374 — is omitted.

Q5 Dependency/trigger sufficiency — FAIL.
Owner acceptance is represented only as unsatisfied. Native state is stronger: the current candidate has failed owner acceptance and requires redesign before another acceptance attempt.

Q6 Freshness sufficiency — FAIL.
The source contract cannot safely detect issue/comment evolution. PR #399 and the owner-rejection comment existed before Stage-6A froze, so this is not a later-advancement false positive.

Q7 Human-authority sufficiency — FAIL in status transport.
The authority role is correct; the authoritative human decision is missing.

Q8 Consequence boundary — PARTIAL PASS.
The projection says shadow reconstruction cannot authorize external effects, which is safe. But its project-state transition complete_pending_acceptance overstates the product state and could encourage progression rather than redesign.

Q9 Supersession/historical state — FAIL.
The older PR #397 candidate is retained as the only candidate while the newer rejected PR #399 bounded state is absent.

Q10 Omitted-source discovery — FAIL.
Reading current Issue #398 comments and current open PRs materially changes the projection.

Result: MATERIAL HIVENUES OMISSION.

## 6. Stage-6A boundary versus later project advancement

The two principal project-state failures are not caused by post-Stage-6A drift.

### FCP

The Stage-6A packet cites the exact native CURRENT_STATE.md blob b5949af93a1855ae1d072fa4aaa4b1c29033579c at main a41bc6101b63140ee2687e0cf67a47ab6be77215.

That same immutable blob already contains the controlling post-PGH routing and the explicit rule that older milestone routing text is historical. The packet selected a stale semantic window from inside the correct file.

### HiVenues

PR #399 was created at 2026-10-04T05:37:58Z.

Issue #398 has updated_at 2026-10-04T15:30:48Z, and the Stage-6A preregistration/source packet itself freezes Issue #398 with that exact updated_at value.

The Stage-6A report commit aac2a05b25bdf2dfb8b1b979645e64824e07adea is later, at 2026-10-04T17:45:47Z.

Therefore the newer candidate and owner-rejection state were already inside the Stage-6A observation period. This is a source-contract sufficiency failure, not a later-freshness penalty.

## 7. Positive controls

### NFC positive control

The projection successfully distinguishes:
publication main 5072d563... from frozen theorem authority archive/nfc-canonical-ed3047c2@ed3047c2..., and preserves unresolved human policy intent.

This demonstrates that the audit is not rejecting every projection.

### FCP positive control

The projection correctly preserves Method 0.2.1 prospectively, FCP27 not selected, and the prior evidence-triggered hold as a historical marker rather than a current waiting-for-trigger state.

The failure is narrower: it selects the wrong superseded next-routing checkpoint.

### PGH positive control

The projection correctly carries:
PGH-OBJ-0052 empirically untested, real apparatus HARD/UNSATISFIED, target search suspended, and physical trials prohibited.

### HiVenues positive control

The projection correctly keeps merged main distinct from PR #397 and correctly preserves that owner acceptance cannot be replaced by machine qualification.

The failure is that the source contract did not follow the active bounded-work state far enough to include PR #399 and the owner’s actual rejection.

## 8. Pass 3 — source-contract / extraction / profile diagnosis

### 8.1 FCP diagnosis

Stage-6A source_packets.json materializes only selected lines from CURRENT_STATE.md and specifically includes the obsolete post-recurrence routing markers.

The adapter then prerequires those exact markers and extracts NEXT_RECOMMENDED_OPERATION from that bounded text.

The Stage-6A tests likewise assert the obsolete post-recurrence operation.

This is not a native-governance ambiguity. Native CURRENT_STATE.md explicitly identifies which material is controlling and which milestone routing fields are historical.

Primary cause: source-contract omission / wrong semantic window.

### 8.2 HiVenues diagnosis

The Stage-6A contract preregisters:
- main README;
- Issue #398;
- PR #397.

It does not require:
- current open PR discovery for the active issue/workstream;
- current Issue #398 comments/owner decision;
- candidate supersession/rejection state.

The packet records Issue #398 updated_at 2026-10-04T15:30:48Z while reducing the issue evidence to three body sentences. The decisive owner comment is therefore outside the semantic window even though the issue revision time is inside the frozen packet.

The adapter also hardcodes the Stage-5D transition as complete_pending_acceptance, a state no longer supported by native authority and not safely derivable from the selected issue-body excerpt alone.

Primary cause: source-contract omission, with an extraction overstatement downstream.

### 8.3 CPI projection/profile diagnosis

prototype/cpi0/cpi_profile.py requires every projection to contain:
- producer;
- observed_at;
- observed_sources;
and requires each observed source to carry a commit identity.

The Stage-6A generated projections omit producer and observed_at, so they do not pass the existing common projection validator as emitted.

More importantly for source-contract sufficiency, commit-only source revision is not adequate for GitHub issues/comments. The HiVenues Issue #398 source is projected with commit = 4fed1b4b..., which is the repository main commit, not an issue revision. The standard freshness classifier compares source.commit to a current revision, so it cannot detect a material issue comment/update while main is unchanged.

This is a common-profile/source-identity defect, not merely a HiVenues parser typo.

### 8.4 Observatory-comparison diagnosis

Project Observatory Snapshot v0.2 says:

FCP_PROJECT_STATE = WAITING_FOR_EVIDENCE
and
FCP remains on EVIDENCE_TRIGGERED_HOLD.

It names the same exact FCP canonical commit:
a41bc6101b63140ee2687e0cf67a47ab6be77215.

The snapshot observed_at is 2026-09-14T21:04:00Z. The exact FCP commit was already committed on 2026-09-11 and its immutable CURRENT_STATE.md contains the fulfilled PGH trigger and current post-PGH routing.

Stage-6A compare_observatory_snapshot checks only the HiVenues commit and then emits a global-looking:
historical_validity = VALID_AT_OBSERVATION_BOUNDARY.

That historical-validity classification is too broad. It cannot certify the FCP component of Snapshot v0.2.

The frozen Observatory snapshot must not be rewritten; the correct response is to preserve it as historical evidence while refusing blanket validity where native same-commit semantics contradict it.

## 9. Formal findings

### FINDING CPI6B-001

FINDING_ID = CPI6B-001
PROJECT = FCP
PRIMARY_CLASS = SOURCE_CONTRACT_OMISSION
SEVERITY = S2
NATIVE_SOURCE = etblink/Foundational-Convergence-Program@a41bc6101b63140ee2687e0cf67a47ab6be77215:CURRENT_STATE.md, blob b5949af93a1855ae1d072fa4aaa4b1c29033579c
EXACT_NATIVE_ASSERTION = NEXT_RECOMMENDED_OPERATION = POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION; NEXT_OPERATION_AUTHORIZED = YES__STANDING_PROJECT_LEAD_DELEGATION; NEXT_OPERATION_AUTHORIZATION_BOUNDARY = SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION; PRIOR EVIDENCE_TRIGGERED_HOLD fulfilled by PGH T1; FCP27_SELECTED = NO
WHAT_THE_PROJECTION_SAYS_OR_OMITS = Projection reports POST_RECURRENCE_SCIENTIFIC_SEQUENCING_ADJUDICATION with state selected_not_authorized and omits the controlling post-PGH routing and standing sequencing-only authorization.
WHY_IT_MATTERS = The projection gives the wrong current next action, wrong authorization state, and wrong supersession position even though it cites the correct immutable native blob.
COUNTERFACTUAL_WRONG_ACTION_OR_INFERENCE = A downstream observer could recommend or wait on the old post-recurrence sequencing step and could incorrectly conclude that the actual post-PGH sequencing operation is not yet authorized.
PROPOSED_REMEDIATION = Bind the FCP contract to an explicit current-routing capsule or authoritative section with precedence rules; reject multiple/superseded NEXT_RECOMMENDED_OPERATION occurrences unless the controlling current section is identified; test the actual current routing from the full source identity rather than a hand-selected stale excerpt.
REQUIRES_PROFILE_CHANGE = NO

### FINDING CPI6B-002

FINDING_ID = CPI6B-002
PROJECT = HiVenues
PRIMARY_CLASS = SOURCE_CONTRACT_OMISSION
SEVERITY = S2
NATIVE_SOURCE = etblink/HiVenues Issue #398 current owner-acceptance comment; PR #399 head 28eaf662df350e23ed02c25bde17bf78b311fa04; merged main 4fed1b4bcd65606124579fe8a643e55828655093
EXACT_NATIVE_ASSERTION = Current A-C owner acceptance: FAIL; PR #399 must remain draft/unmerged; do not proceed to D-E; do not declare #374 satisfied; stop for redesign review before further broad implementation.
WHAT_THE_PROJECTION_SAYS_OR_OMITS = Projection includes only PR #397 as candidate, marks Stage-5D complete_pending_acceptance, and represents owner acceptance merely as unsatisfied. It omits PR #399 and the owner rejection.
WHY_IT_MATTERS = The omitted human decision changes the project’s bounded next action from acceptance/progression to redesign and preserves an explicit stop boundary.
COUNTERFACTUAL_WRONG_ACTION_OR_INFERENCE = A downstream observer could infer that Stage-5D implementation is complete and only awaits owner approval, or could prepare D-E/progression rather than returning to redesign.
PROPOSED_REMEDIATION = Define bounded-work discovery to include the current active candidate set and authoritative owner-decision comments/reviews for the governing issue; represent rejected/superseded candidate state explicitly; fail incomplete when issue revision metadata changed but the decision-bearing comment set was not materialized.
REQUIRES_PROFILE_CHANGE = NO

### FINDING CPI6B-003

FINDING_ID = CPI6B-003
PROJECT = CPI-0 common projection / all Stage-6A project projections
PRIMARY_CLASS = PROJECTION_SCHEMA_DEFECT
SEVERITY = S2
NATIVE_SOURCE = CPI protocol source prototype/cpi0/cpi_profile.py@3795ceda33b808d29a255e9d14b2d25dccf0181b plus frozen Stage-6A generated_projections.json
EXACT_NATIVE_ASSERTION = validate_projection requires producer and observed_at; observed sources require source_id, repository, ref, commit, role; classify_freshness uses observed source commit as the revision token.
WHAT_THE_PROJECTION_SAYS_OR_OMITS = Stage-6A generated projections omit producer and observed_at and therefore do not conform to the existing validator. For HiVenues, Issue #398 is represented with the repository main commit as its source revision, so issue/comment changes are invisible to commit-based freshness.
WHY_IT_MATTERS = A compliant CPI consumer rejects the emitted objects; a consumer that bypasses validation can misclassify issue-based human authority as fresh while its decision-bearing comments changed.
COUNTERFACTUAL_WRONG_ACTION_OR_INFERENCE = Main can remain at 4fed1b4b... while owner authority on Issue #398 changes from pending to explicit FAIL, yet a commit-only freshness check can still report the issue-derived state as fresh.
PROPOSED_REMEDIATION = Require Stage-6A adapters to emit validator-conformant projections and validate them in qualification. Extend or version the common source-identity model for non-Git sources with source kind plus a stable issue/PR/comment revision identity, such as updated_at plus content fingerprint or a content-addressed source snapshot, and make freshness compare that identity rather than repository main.
REQUIRES_PROFILE_CHANGE = YES

### FINDING CPI6B-004

FINDING_ID = CPI6B-004
PROJECT = Project Observatory shadow comparison / FCP
PRIMARY_CLASS = EXTRACTION_DEFECT
SEVERITY = S2
NATIVE_SOURCE = Project Observatory Snapshot v0.2 blob e62a0b86e2317d7b441eb3d5ecf8ee71cc49460a and FCP CURRENT_STATE.md at the snapshot’s exact named commit a41bc6101b63140ee2687e0cf67a47ab6be77215
EXACT_NATIVE_ASSERTION = Snapshot v0.2 says FCP remains on EVIDENCE_TRIGGERED_HOLD, while the exact immutable FCP commit it names says the prior hold is fulfilled by PGH and current routing is post-PGH sequencing.
WHAT_THE_PROJECTION_SAYS_OR_OMITS = Stage-6A OBSERVATORY_COMPARISON emits historical_validity = VALID_AT_OBSERVATION_BOUNDARY after checking only the HiVenues canonical commit divergence. It does not test FCP semantic validity at the snapshot boundary.
WHY_IT_MATTERS = A blanket stale-but-valid label can preserve a materially incorrect observer state as trustworthy historical reconstruction even when same-commit native evidence disproves one project component.
COUNTERFACTUAL_WRONG_ACTION_OR_INFERENCE = A downstream consumer could use Snapshot v0.2 to classify FCP as still waiting for evidence even though the exact referenced FCP commit already records the trigger as fulfilled.
PROPOSED_REMEDIATION = Make observer historical-validity classification per project/source claim, not global from a single HiVenues revision check; verify every claimed canonical identity and a minimal set of decision-critical semantic anchors before labeling that project component valid at the observation boundary. Preserve the frozen snapshot unchanged and record discrepancy externally.
REQUIRES_PROFILE_CHANGE = NO

## 10. Finding counts

Total findings: 4

By severity:
- S0: 0
- S1: 0
- S2: 4
- S3: 0

By primary class:
- SOURCE_CONTRACT_OMISSION: 2
- EXTRACTION_DEFECT: 1
- PROJECTION_SCHEMA_DEFECT: 1
- NATIVE_GOVERNANCE_AMBIGUITY: 0
- NONMATERIAL_DETAIL_DIFFERENCE: 0
- EVALUATOR_UNCERTAINTY: 0

No S3 authority leak or prohibited external consequence was found.

## 11. False-bridge negative control

Candidate bridge:
HiVenues / Hive activity -> NFC or PGH scientific dependency or authorization.

Result:

DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION

Basis:
- Issue #19 expressly records HiVenues/Hive -> NFC/PGH scientific bridge as HELD / UNESTABLISHED.
- Native NFC, FCP, and PGH sources inspected do not establish a load-bearing scientific dependency from HiVenues/Hive activity.
- HiVenues product/deployment work provides no local scientific authorization in NFC or PGH.
- The Stage-6A projections do not establish such a bridge.

Negative control: PASS.

## 12. Observer-independence oracle

FEDERATION_OPTIONALITY = PASS

I was able to recover the safe current state of all four projects from native project sources without Project Observatory or CPI being the sole intelligibility layer.

NFC:
native provenance routes theorem authority exactly.

FCP:
native CURRENT_STATE.md and charter recover the current method, fulfilled trigger, current next operation, and authorization ceiling.

PGH:
native CURRENT_STATE.md and handoff recover the apparatus dependency and trial prohibition.

HiVenues:
native main, active issues, current PRs, and owner decision recover canonical/candidate separation and the current failed usability gate.

The fact that the independent native reconstruction exposes both a Stage-6A FCP omission and an Observatory v0.2 FCP discrepancy is positive evidence for the architectural invariant that the observer/federation must remain optional and non-authoritative.

## 13. Mutation audit

Observed project mutation:
- NFC: NONE
- FCP: NONE
- PGH: NONE
- HiVenues: NONE

Project Observatory mutation:
NONE

Live external effect:
NONE

Stage-6A repair:
NONE

Merge:
NONE

Live integration:
NONE

Project-Continuity-Research mutation:
exactly this required Stage-6B report on audit/cpi0-stage6b-independent.

## 14. Interpretation

Stage-6A established that an explicit source-contract implementation could pass its preregistered assertions and omission controls. Stage-6A itself explicitly did not establish full-repository semantic completeness.

Stage-6B falsifies the stronger sufficiency claim at the tested boundary.

The central failure mode is not that project-specific adapters are impossible. It is that an exact Git identity plus a hand-selected semantic window is not enough when:

- the same native file contains preserved historical routing and a separately defined current routing surface;
- active human authority lives in issue comments/reviews and newer candidate PRs rather than repository main;
- the common source identity model treats all freshness as commit-like even for non-Git authority surfaces;
- a frozen observer snapshot can be historically wrong about one project even while carrying the correct immutable project commit.

These defects are material, but they are bounded and repairable within the current architectural direction. I did not find an S3 authority leak, a requirement to make the Observatory authoritative, or evidence that interoperability necessarily collapses project-local governance.

## 15. Final disposition

REPAIR_REQUIRED

Reason:

Four unresolved S2 findings remain. The Stage-6B rules therefore forbid PASS or PASS_WITH_NONMATERIAL_FINDINGS.

ARCHITECTURE_RECONSIDERATION_REQUIRED is not yet forced because:
- no S3 finding was observed;
- native projects remain independently intelligible;
- the false scientific bridge remains held/unestablished;
- the failures can be addressed by stronger source contracts, explicit supersession/current-state anchoring, profile-level non-Git revision semantics, validator conformance, and per-project observer validity checks.

No repairs are performed by this audit.

Stop boundary:

DO NOT REPAIR FINDINGS.
DO NOT MERGE.
DO NOT PROCEED TO LIVE INTEGRATION.
