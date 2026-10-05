# CCP-1 Human Cold-Start Current Routing 0.1.0

Date: 2026-10-05
Status: CURRENT PROGRAM ROUTING RECORD

## 1. Why this record exists

The program-level roadmap on `main` lagged behind preserved CCP-1 human-trial evidence on the retained research lineage.

This record reconciles the current parent-program orientation without merging the full historical research branch into `main`.

Historical experiment artifacts remain on:

`research/ccp1-human-orientation-repair`

Matched participant content remains frozen at:

`e43aef38ae4b6690f6bae8479e9bfb98a47776b6`

## 2. Trial 1 is complete and failed

Raw participant return:

- path: `prototype/ccp1/trials/CCP1_HUMAN_COLD_START_TRIAL_1_RAW.md`
- blob: `1fcabf3cfc2c6bc3563684d18ecb44fa717ba1f4`

Adjudication:

- path: `prototype/ccp1/trials/CCP1_HUMAN_COLD_START_TRIAL_1_ADJUDICATION.md`
- blob: `46062a552c8320a1352f9d13170a8869fec46328`

Result:

```text
HUMAN_COLD_START_TRIAL_1 = FAIL
HUMAN_SCORE = 3 / 12
AUTOMATIC_CRITICAL_FAILURE = NO
AUTHORIZATION_BOUNDARY = 0 / 2
FAILURE_KIND = ORIENTATION / USABILITY FAILURE
PARTICIPANT_ERROR_BLAME = NONE
```

The participant recovered project purpose and Phase 4, but did not recover the advancement gate, live-control authorization boundary, evidence/current-state map, one bounded adversarial result, or a plausible bounded next operation.

The participant explicitly reported feeling overwhelmed and believed they would need to read everything.

## 3. Post-Trial-1 design review

Design review:

- path: `prototype/ccp1/trials/CCP1_HUMAN_COLD_START_TRIAL_1_POST_TRIAL_DESIGN_REVIEW.md`
- blob: `2231b5143d49ac9f50659deaa19603f21c7da861`

Diagnosis:

```text
PRIMARY = ORIENTATION-SURFACE SUFFICIENCY FAILURE
SECONDARY = INFORMATION-DISCOVERY / PRESENTATION FAILURE
PARTICIPANT_DEFICIT = NOT THE DESIGN INTERPRETATION
```

Key lesson:

```text
BROWSABLE + SEARCHABLE CORPUS != USABLE PROJECT ORIENTATION
NOT_SOLE_SOURCE_OF_TRUTH != NO_EXPLICIT_ORIENTATION_ENTRY_POINT
```

The repair experiment required a first-class, explicitly non-canonical current-orientation projection with exact evidence pointers and freshness identity.

## 4. Orientation repair status

Final audited orientation projection packet:

- path: `prototype/ccp1/trials/CCP1_CURRENT_ORIENTATION_PROJECTION_BLIND_AUDIT_PACKET_0_1_3.md`
- blob: `ea1f2bd3110bc85a876757e4065e60995853b015`

Independent blind-audit raw return:

- path: `prototype/ccp1/trials/audits/CCP1_CURRENT_ORIENTATION_PROJECTION_BLIND_AUDIT_RAW_0_1_3.md`
- blob: `77b390702ca7a591df519e1e1f71dbb17ea4f5a2`
- disposition: `ORIENTATION_PROJECTION_PASS`

Passing audit freeze:

`5faaada352faa39ef7697b895c77e863068aa0fb`

Matched repaired participant-content ref:

`e43aef38ae4b6690f6bae8479e9bfb98a47776b6`

## 5. Trial 2 is authorized but not run

Final Trial-2 authorization:

- path: `prototype/ccp1/trials/CCP1_HUMAN_ORIENTATION_REPAIR_TRIAL2_FINAL_AUTHORIZATION_0_1_1.md`
- blob: `7529d0a1cf663df61560bb8fe3dfd5b508da10bc`

Execution status:

- path: `prototype/ccp1/trials/CCP1_HUMAN_ORIENTATION_REPAIR_EXECUTION_STATUS_0_1_2.md`
- blob: `eb99b46cae9d003aa29e701b27d2e1361f77c2db`

Current state:

```text
ORIENTATION_PROJECTION_0_1_3 = PASS
HUMAN_REPAIR_TRIAL_2 = AUTHORIZED
HUMAN_REPAIR_TRIAL_2_COMPLETED = NO
DIFFERENT_UNFAMILIAR_HUMAN = REQUIRED
NO_MORE_PRETRIAL_PROJECTION_EDITS = YES
CCP1_COMPLETE = NO
CCP2_AUTHORIZED = NO
```

## 6. Frozen Trial-2 presentation

Protocol:

`prototype/ccp1/trials/HUMAN_COLD_START_PROTOCOL_0_3_3.md`

Protocol blob:

`39180ba68c7f34c2a0d8b8e4a9017aa4fe716a65`

Reader:

`prototype/ccp1/trials/html/HUMAN_COLD_START_READER_0_3_3.html`

Reader blob:

`341c5f8931b9745b1f5b030972c31fe8a4ec6b8d`

Raw-return template:

`prototype/ccp1/trials/CCP1_HUMAN_ORIENTATION_REPAIR_TRIAL2_RAW_RETURN_TEMPLATE_0_1_1.md`

Raw-return-template blob:

`35a19f13af8ea79eef592f6a46a785823cee3355`

Scorecard remains unchanged:

`prototype/ccp1/trials/COLD_START_SCORECARD_0_1_0.md`

Scorecard blob:

`f119d1fd5c1569a9c83311001fd43f86a2316b38`

## 7. Trial-2 participant boundary

Trial 2 must use a different unfamiliar human from Trial 1.

The participant should:

- have no substantive prior PCR knowledge;
- need no Git/GitHub knowledge;
- be comfortable reading ordinary technical prose.

During the first attempt, use Reader 0.3.3 only.

Do not provide:

- issue pages;
- branch/commit pages;
- external web search;
- later PCR state;
- Trial-1 result;
- scorecard;
- explanatory coaching.

Facilitator assistance is limited to browser mechanics.

## 8. Raw evidence requirement

Before scoring, correction or debrief, freeze:

- prior familiarity;
- start/end/elapsed time;
- all eight answers verbatim;
- first file opened;
- navigation path;
- search terms;
- substantive questions;
- hesitation/confusion;
- whether `CURRENT_ORIENTATION.md` was read;
- whether immediate objective was understood separately from North Star;
- whether an evidence pointer was followed;
- whether the roadmap was found;
- whether current vs historical state was distinguished;
- whether authorization boundaries were recovered;
- whether the participant felt compelled to read everything;
- facilitator help;
- technical/browser problems.

## 9. Current parent-program gate

```text
PCR_ACTIVE_PHASE = PHASE_4__CCP1_ADVERSARIAL_HARDENING
BLIND_AGENT_TRIAL_1 = PROVISIONAL_PASS
HUMAN_COLD_START_TRIAL_1 = FAIL
HUMAN_ORIENTATION_REPAIR = PASS_AT_PROJECTION_AUDIT
CURRENT_PARENT_GATE = REPAIRED_UNFAMILIAR_HUMAN_TRIAL_2
POST_TRIAL_2_DESIGN_REVIEW = REQUIRED
CCP1_COMPLETE = NO
CCP2_AUTHORIZED = NO
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
CPI0 = PARKED
```

Trial 2 is therefore the next empirical operation.

No advancement decision is authorized merely because the repair projection passed its blind audit.
