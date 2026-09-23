# Project Continuity Research — Current Orientation

Projection version: 0.1.0  
Source snapshot: `dec58643dbeb65adf90178f0bedd214dfa40b812`  
Status: **ORIENTATION PROJECTION — NOT CANONICAL PROJECT STATE**

## Why this project exists

Project Continuity Research is trying to discover the minimum durable architecture needed for successive humans and AI agents to preserve purpose, truth/evidence, authority, current state, permissible action, negative knowledge, succession continuity, and human agency across arbitrarily long projects.

The system should work for someone who did not invent it without requiring the originator to remain the permanent executive-function patch.

Verify: `BIG_PICTURE_ROADMAP.md`.

## Where the project is now

```text
CURRENT_PHASE = Phase 4 — CCP-1 adversarial hardening
P1_ATTACK_FAMILY = COMPLETE
AUTONOMOUS_SECONDARY_ATTACK_SET = COMPLETE
CCP1_COMPLETE = NO
```

Verify:
- `BIG_PICTURE_ROADMAP.md`
- `prototype/ccp1/README.md`
- `prototype/ccp1/CCP1_AUTONOMOUS_SECONDARY_ATTACK_FAMILY_RESULT_0_1_0.md`

## Cold-start gate state before the next major phase

```text
BLIND_AGENT_TRIAL_1 = PROVISIONAL_PASS
HUMAN_COLD_START_TRIAL_1 = PREPARED / NOT_YET_RUN
POST_TRIAL_DESIGN_REVIEW = REQUIRED AFTER THE HUMAN TRIAL
CCP1_COMPLETE = NO
```

The first blind-agent cold-start trial has already produced a provisional pass. That result does not complete CCP-1.

The remaining external gate is the unfamiliar-human cold-start / usability trial, followed by the required post-trial design review.

Only after CCP-1 survives its full exit gate may CCP-2 be considered.

Verify:
- `BIG_PICTURE_ROADMAP.md`
- `prototype/ccp1/CCP1_AUTONOMOUS_SECONDARY_ATTACK_FAMILY_RESULT_0_1_0.md`
- `prototype/ccp1/trials/COLD_START_SCORECARD_0_1_0.md`

## What is *not* authorized

```text
CCP2_AUTHORIZED = NO
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
LIVE_PROJECT_CONTROL_PLANE_INTEGRATION = NOT_AUTHORIZED
CCP_IS_FINAL_UNIVERSAL_ARCHITECTURE = NO
```

Passing machine tests does not authorize the next phase or live control.

Verify:
- `BIG_PICTURE_ROADMAP.md`
- `prototype/ccp1/README.md`
- `prototype/ccp0/CCP0_ADVANCEMENT_DECISION_0_1_0.md`

## Current bounded next operation

Run and adjudicate the unfamiliar-human cold-start / usability trial against the frozen project state, then perform the required post-trial design review.

Do not rerun Blind-Agent Trial 1 merely because it is provisional, and do not begin CCP-2 merely because the autonomous attack suites are green.

Verify:
- `BIG_PICTURE_ROADMAP.md`
- `prototype/ccp1/CCP1_AUTONOMOUS_SECONDARY_ATTACK_FAMILY_RESULT_0_1_0.md`

## Machine-verification checkpoint

At this frozen snapshot, the autonomous CCP-1 program reports:

```text
CCP0_REGRESSION_SUITE = 27 / 27 PASS
CCP1_ADVERSARIAL_SUITE = 97 / 97 PASS
TOTAL = 124 / 124 PASS
```

This is a bounded machine-verification checkpoint, not proof that CCP is complete, human-usable, production-ready, or universally correct.

Verify:
- `prototype/ccp1/README.md`
- `prototype/ccp1/CCP1_AUTONOMOUS_SECONDARY_ATTACK_FAMILY_RESULT_0_1_0.md`

## Where to look

### Big-picture orientation

`BIG_PICTURE_ROADMAP.md`

Use this to understand the program's North Star, phase map, advancement gates, and major prohibitions.

### Exact CCP-1 state and machine checkpoint

`prototype/ccp1/README.md`

Use this as the CCP-1 working summary, then verify important claims in the named result artifacts.

### Completed adversarial attacks

Look under `prototype/ccp1/` for paired `*_ATTACK_*.md` and `*_RESULT_*.md` files.

Major completed attack families include:
- authority spoofing;
- bad-policy enforcement;
- stale/concurrent transitions;
- kernel omission;
- reopen-predicate brittleness;
- evidence authenticity;
- accepted-event correction;
- authority durability / identity boundary;
- orientation-contract quality;
- supersession graph scale;
- project-agnostic portability.

A result file should state both what passed and what the bounded result does **not** establish.

### Historical research

Root-level research artifacts preserve the empirical taxonomy, adjacent-field review, requirements, architecture competition, and earlier reasoning. Historical truth does not automatically equal current authority.

## Open limitations

CCP remains a prototype candidate. The frozen snapshot does not establish:
- human usability;
- durable distributed storage correctness;
- production readiness;
- universal architecture validity;
- authorization to control a live project.

## Orientation rule

Start here, but verify consequential claims in the linked source artifacts.

```text
ORIENTATION_PROJECTION != SOLE_SOURCE_OF_TRUTH
```
