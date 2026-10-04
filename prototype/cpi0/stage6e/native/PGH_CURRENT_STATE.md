# CURRENT STATE

## Project status

```text
PROJECT = Physical Grammar Hypothesis
CURRENT_PHASE = PGH-1_D1_ADVERSARIAL_PHYSICAL_INTERFACE_QUALIFIED__AWAITING_APPARATUS_REALIZATION
ACTIVE_FORMAL_GRAMMAR_CANDIDATE = PGH-GRAM-0010
ACTIVE_CONDITIONAL_BRIDGE = PGH-OBJ-0051
ACTIVE_STRONG_PGH_CANDIDATE_PACKAGE = PGH-OBJ-0052
PGH_OBJ_0052_ADMISSION = A0_A9_PASS
PGH_OBJ_0052_EMPIRICAL_STATUS = UNTESTED
SELECTED_PHYSICAL_INTERFACE_CLASS = D1__MECHANICALLY_GANGED_THREE_POLE_SWITCH_INTERFACE
SELECTED_DESIGN_ID = PGH-EXP-DESIGN-0001
ACTUAL_APPARATUS = NONE_BOUND
ACTUAL_CHANNEL_IDS = NONE_BOUND
TARGET_ID = NONE
NEXT_AVAILABLE_TARGET_ID = TGT-047
TGT_047_RESERVED = NO
TARGET_FREEZE = NOT_YET_POSSIBLE
TARGET_VALUES_ACCESSED = NO
PHYSICAL_RESPONSE_DATA = NONE
POSITIVE_EMPIRICAL_PGH_CREDIT = NONE
EMPIRICAL_REFUTATION = NONE
STRONG_PGH_CONFIRMED = NO
R2B = UNSATISFIED

FCP_FRAMEWORK_ADMISSION = FAIL
FCP_CONTROLLING_CRITERION = G__FRAMEWORK_DISTINCTNESS
FCP_TOP_LEVEL_OUTCOME = B__CLASSIFY_AS_NONFRAMEWORK_PHYSICAL_MODEL_OR_POSTULATE
FW_PGH = DOES_NOT_EXIST
FCP_EXISTING_FRAMEWORK_HOST = NONE_ESTABLISHED
FCP_EMPIRICAL_EFFECT = NONE
```

## Current boundary

The exact current candidate `PGH-GRAM-0010 / PGH-OBJ-0052` remains A0-A9 admitted and empirically untested. FCP's classification of the object as a nonframework physical model/postulate remains a taxonomy result only and creates no positive or negative empirical credit.

The earlier public/network target-discovery search remains suspended after the zero-target result and the failed closed-record resumption-trigger reassessment. That suspension still forbids opportunistic web/registry widening.

A later, separately preregistered adversarial physical-interface design gate did **not** resume that target search. Instead, under unchanged frozen interface criterion `I`, it qualified a concrete physical interface class already available in principle for a direct hostile test:

```text
OUTCOME = A__D1_MECHANICALLY_GANGED_THREE_POLE_SWITCH_QUALIFIES
INTERFACE_CLASS = THREE_POLE_TWO_POSITION_MECHANICALLY_GANGED_DRY_CONTACT_INTERFACE
COMMON_PHYSICAL_STATE = ONE_MECHANICALLY_SHARED_TWO_POSITION_ACTUATOR
PHYSICAL_CONTACT_POLES = 3
RAW_CHANNEL_ALPHABET = {OPEN,CLOSED}
PLANNED_TRIAL_COUNT = 512
ODD_TRIALS = ACTUATOR_POSITION_0
EVEN_TRIALS = ACTUATOR_POSITION_1
DEFAULT_SETTLE_INTERVAL = 1000 ms
ONE_JOINT_SAMPLE_PER_TRIAL = YES
```

That design gate is the latest controlling scientific state on `main`. Its expectation of common-bit behavior is explicitly zero empirical evidence.

## Required next scientific sequence

The controlling design gate freezes this order:

```text
APPARATUS_REALIZATION_AND_TARGET_FREEZE
-> NEGATIVE_ONLY_ANALYSIS_PREREGISTRATION
-> ONLY_THEN_PHYSICAL_TRIAL_EXECUTION_AND_RESPONSE_DATA
```

The next scientific operation requires external physical action: a real three-pole switch interface and acquisition hardware must exist so that exact apparatus identity, channel identifiers, wiring, custody, and protocol metadata can be bound prospectively.

Before target freeze, a future apparatus-realization artifact must bind at least:

```text
APPARATUS_NAME_AND_VERSION
SWITCH_MANUFACTURER_MODEL_OR_UNIQUE_DESCRIPTION
SWITCH_SERIAL_OR_PHOTO_ID
ACQUISITION_DEVICE_IDENTITY
EXACT_THREE_CHANNEL_IDENTIFIERS
WIRING_MANIFEST
INTERFACE_SCHEMA_VERSION
SETTLE_INTERVAL
TRIAL_COUNT_AND_SCHEDULE
VALIDITY_RULE_VERSION
CUSTODY_PATH
PUBLIC_OR_AUDITABLE_ACCESS_PATH
HASH_ALGORITHM
```

If those cannot be bound prospectively, target freeze fails rather than being inferred.

## Experiment-readiness infrastructure

A bounded pre-data readiness package now exists under:

```text
empirical/d1_readiness/
```

It provides templates, structural schema validation, custody procedure, and synthetic dry-run fixtures only. It does **not** bind an apparatus, reserve or assign `TGT-047`, choose the finite-sample `T_ind` decision functional, generate response data, or award a scientific verdict.

The readiness package is subordinate to the scientific sequence above. Its synthetic fixtures are visibly non-empirical and use reserved synthetic identities/timestamps.

## Hard boundary

```text
NEXT_SCIENTIFIC_OPERATION = APPARATUS_REALIZATION_AND_TARGET_FREEZE
NEXT_SCIENTIFIC_OPERATION_REQUIRES_EXTERNAL_PHYSICAL_ACTION = YES
APPARATUS_REALIZATION_COMPLETE = NO
TARGET_FREEZE_COMPLETE = NO
ANALYSIS_PREREGISTRATION_COMPLETE = NO
PHYSICAL_TRIAL_EXECUTION_AUTHORIZED = NO
PUBLIC_TARGET_SEARCH = SUSPENDED
WEB_TARGET_SEARCH = FORBIDDEN_WITHOUT_NEW_INDEPENDENT_TRIGGER
REGISTRY_TARGET_SEARCH = FORBIDDEN_WITHOUT_NEW_INDEPENDENT_TRIGGER
CANDIDATE_REVISION = NOT_AUTHORIZED
TARGET_VALUES = NO
EMPIRICAL_DATA = NO
NO_TRIGGER_SUPPORTS_PGH = NO
NO_TRIGGER_COUNTS_AGAINST_PGH = NO
```

## Navigation state

```text
LATEST_CONTROLLING_SCIENTIFIC_OPERATION = PGH1_ADVERSARIAL_PHYSICAL_INTERFACE_DESIGN_GATE
LATEST_CONTROLLING_SCIENTIFIC_COMMIT = d8a16161f33d3bb8f97c15f095ca651c169f5896
LATEST_CONTROLLING_HANDOFF = handoffs/PGH1_ADVERSARIAL_PHYSICAL_INTERFACE_DESIGN_GATE_HANDOFF_0_1_0.md
PREVIOUS_REGISTERED_NAVIGATION_OPERATION = POST_PGH1_POST_FCP_TRIGGER_REASSESSMENT_NAVIGATION_RECONCILIATION
PREVIOUS_REGISTERED_NAVIGATION_ID = PGH-OP-0116
```

No new PGH operation number is invented here for the already-merged design gate; this reconciliation records the actual controlling Git state.

<!-- PGH_CURRENT_STATE_CAPSULE_BEGIN -->
```json
{"capsule_schema_version":"0.2.0","project":"Physical Grammar Hypothesis","current_phase":"PGH-1_D1_ADVERSARIAL_PHYSICAL_INTERFACE_QUALIFIED__AWAITING_APPARATUS_REALIZATION","canonical_hypothesis":"HYPOTHESIS.md","active_candidate_grammar":"PGH-GRAM-0010","active_candidate_package":"PGH-OBJ-0052","selected_design_id":"PGH-EXP-DESIGN-0001","selected_interface_class":"D1__MECHANICALLY_GANGED_THREE_POLE_SWITCH_INTERFACE","actual_apparatus":null,"target_id":null,"next_available_target_id":"TGT-047","physical_response_data":false,"current_handoff":"handoffs/PGH1_ADVERSARIAL_PHYSICAL_INTERFACE_DESIGN_GATE_HANDOFF_0_1_0.md","source_bound_status":"PGH_OBJ_0052_A0_A9_PASS__FCP_OUTCOME_B_NONFRAMEWORK__D1_INTERFACE_QUALIFIED__EMPIRICALLY_UNTESTED__AWAITING_APPARATUS_REALIZATION","fcp_relationship":"FCP_OUTCOME_B__NONFRAMEWORK_PHYSICAL_MODEL_OR_POSTULATE__NO_HOST__NO_EMPIRICAL_CREDIT","next_scientific_operation":"APPARATUS_REALIZATION_AND_TARGET_FREEZE","physical_trials_authorized":false,"do_not_assume":["PGH_IS_AN_FCP_FRAMEWORK","PGH_OBJ_0052_HAS_EMPIRICAL_SUPPORT","PGH_OBJ_0052_IS_REFUTED","D1_DESIGN_EXPECTATION_IS_EVIDENCE","TGT_047_IS_ASSIGNED","ACTUAL_APPARATUS_IS_BOUND","ANALYSIS_PREREGISTRATION_IS_COMPLETE","PHYSICAL_TRIALS_ARE_AUTHORIZED","TARGET_SEARCH_SHOULD_RESUME","R2B_HAS_PASSED","STRONG_PGH_IS_CONFIRMED"]}
```
<!-- PGH_CURRENT_STATE_CAPSULE_END -->

Truth over PGH.