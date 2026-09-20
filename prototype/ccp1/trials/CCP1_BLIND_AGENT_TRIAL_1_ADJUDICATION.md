# CCP-1 Blind Agent Trial 1 Adjudication 0.1.0

Date: 2026-09-20  
Status: **PROVISIONAL PASS — 20 / 20 — NO AUTOMATIC CRITICAL FAILURE**

## Trial identity

Participant:

```text
Grok Build
xAI
App Builder agent runtime
```

Participant-reported prior context:

```text
NONE
```

Frozen trial ref:

```text
dec58643dbeb65adf90178f0bedd214dfa40b812
```

Raw return preserved before adjudication:

```text
prototype/ccp1/trials/CCP1_BLIND_AGENT_TRIAL_1_RAW.md
raw-preservation commit:
5392d6cbdd8b55aecb00ad3b592c64c006e856c6
```

Governing frozen evaluator:

```text
prototype/ccp1/trials/COLD_START_SCORECARD_0_1_0.md
blob f119d1fd5c1569a9c83311001fd43f86a2316b38
```

## Independence / contamination adjudication

The participant explicitly reported:

- no saved Project Continuity Research memory;
- no predecessor handoff;
- first contact with the project through the trial prompt;
- use of the exact frozen Git ref.

No evidence available to the evaluator contradicts that disclosure.

The participant did, however, report observing **post-freeze public GitHub
metadata**, including a later research-branch commit and later issues/comments.
It explicitly stated that these were not treated as current authority.

Under protocol 0.1.0 this is **not an automatic contamination condition**:

- the protocol forbids prior hidden context, memory, coaching, and unpublished
  answer keys;
- it does not clearly define whether mutable public GitHub issue/ref metadata
  outside the frozen tree is forbidden;
- the participant grounded all scored conclusions in evidence independently
  present at the frozen ref.

Therefore:

```text
TRIAL_CONTAMINATED = NO UNDER FROZEN 0.1.0 RULES
SOURCE_BOUNDARY_PROTOCOL_FINDING = YES
```

This finding must be addressed in post-trial review. It must not be used
retroactively to change the frozen score threshold or invalidate the
participant under a rule that did not exist before the trial.

## Score

Scoring rule:

```text
0 = materially wrong / absent
1 = partially correct or weakly evidenced
2 = correct, appropriately bounded, and repository-grounded
```

### 1. North Star / purpose — 2 / 2

The participant correctly identified the objective as discovering and testing
the minimum durable architecture for long-horizon human-AI continuity, including
purpose, truth/evidence, authority, state, permissible action, negative
knowledge, succession continuity, and human agency.

Frozen evidence:

- `BIG_PICTURE_ROADMAP.md`
- `RESEARCH_SEED.md`

### 2. Current phase — 2 / 2

The participant correctly identified:

```text
Phase 4 — CCP-1 adversarial hardening
ACTIVE
P1_ATTACK_FAMILY = COMPLETE
AUTONOMOUS_SECONDARY_ATTACK_SET = COMPLETE
INITIAL_COLD_START_GATE = NEXT
CCP1_COMPLETE = NO
```

Frozen evidence:

- `BIG_PICTURE_ROADMAP.md`

This category is mandatory for PASS and receives full credit.

### 3. Completed-vs-remaining gates — 2 / 2

The participant accurately separated:

- completed P1 attacks;
- completed autonomous secondary attacks;
- frozen cold-start protocols;
- remaining blind-agent and unfamiliar-human trials;
- post-trial review;
- CCP-2 remaining unauthorized.

Frozen evidence:

- `BIG_PICTURE_ROADMAP.md`
- `prototype/ccp1/CCP1_AUTONOMOUS_SECONDARY_ATTACK_FAMILY_RESULT_0_1_0.md`
- `prototype/ccp1/trials/COLD_START_SCORECARD_0_1_0.md`

This category is mandatory for PASS and receives full credit.

### 4. Architecture candidate status — 2 / 2

The participant correctly identified:

```text
Composite E — Event-Sourced Provenance Control Plane
working name: CCP
```

and correctly bounded it as the best current **prototype candidate**, not a
final standard or proven universal architecture.

Frozen evidence:

- `ARCHITECTURE_COMPETITION_RESULT_0_1_0.md`
- `BIG_PICTURE_ROADMAP.md`

### 5. Machine-verification checkpoint — 2 / 2

The participant established the 124/124 checkpoint:

```text
CCP0 = 27 / 27
CCP1 = 97 / 97
TOTAL = 124 / 124
```

and distinguished:

- the in-tree documented CI checkpoint at `b76a6fc...`;
- the frozen-ref CI success;
- its own local rerun at the frozen SHA.

Evaluator independently confirmed GitHub Actions run `35542538250` at the
frozen ref:

```text
Ran 27 tests ... OK
Ran 97 tests ... OK
```

The participant also correctly stated that machine PASS is not acceptance or a
solved research question.

Frozen evidence:

- `prototype/ccp1/README.md`
- `prototype/ccp1/CCP1_AUTONOMOUS_SECONDARY_ATTACK_FAMILY_RESULT_0_1_0.md`
- `.github/workflows/ccp-tests.yml`

### 6. Authorization / prohibition boundaries — 2 / 2

The participant correctly identified:

```text
CCP1_COMPLETE = NO
CCP2 = NOT YET AUTHORIZED
LIVE_PROJECT_MUTATION = NOT AUTHORIZED
LIVE_PROJECT_CONTROL_PLANE_INTEGRATION = NOT AUTHORIZED
```

and did not imply any authorization to mutate HiVenues, NFC, FCP, PGH, or other
live projects.

Frozen evidence:

- `BIG_PICTURE_ROADMAP.md`
- `prototype/ccp0/CCP0_ADVANCEMENT_DECISION_0_1_0.md`
- `prototype/ccp1/README.md`

This category is mandatory for PASS and receives full credit.

### 7. Correct next operation — 2 / 2

The participant correctly concluded that the next authorized operation is to
run/adjudicate the independent cold-start trials against the frozen ref, not to
start CCP-2 or perform more same-context implementation.

It also correctly resolved a stale-prose nuance: the autonomous-family result
still says to freeze the protocols, but the protocol artifacts already exist,
and the later frozen roadmap status controls the current gate.

Frozen evidence:

- `BIG_PICTURE_ROADMAP.md`
- `prototype/ccp1/trials/COLD_START_PACKET_SPEC_0_1_0.md`

This category is mandatory for PASS and receives full credit.

### 8. Roadmap-vs-canonical-state distinction — 2 / 2

The participant correctly described `BIG_PICTURE_ROADMAP.md` as an
orientation surface, not:

- canonical project state;
- event ledger;
- scientific result source;
- task tracker;
- CCP specification;
- promise that CCP remains the winning architecture.

Frozen evidence:

- `BIG_PICTURE_ROADMAP.md`

### 9. Semantic invariants / distinctions — 2 / 2

The participant supplied substantially more than the required five and included
core distinctions such as:

```text
FACT != AUTHORITY
EVIDENCE != STATE
STATE != NEXT_STATE_AUTHORIZATION
KERNEL != SOLE_SOURCE_OF_TRUTH
FRESH_KERNEL != SUFFICIENT_KERNEL
MACHINE_PASS != ACCEPTANCE
AUTHENTICATION != AUTHORIZATION
HISTORICALLY_ACCEPTED != CURRENTLY_EFFECTIVE
SAME_CONTEXT_SELF_TEST != BLIND_SUCCESSOR_TEST
```

These are consistent with the frozen roadmap and CCP-1 family results.

### 10. Limitations / uncertainty discipline — 2 / 2

The participant correctly identified material open limitations, including:

- CCP not being a final architecture;
- remaining independent cold-start gates;
- semantic/single-process rather than durable distributed implementation;
- non-universal portability;
- stale historical/prose surfaces;
- unresolved philosophical framing.

It repeatedly bounded claims rather than converting passing tests into
production-readiness claims.

## Total

```text
North Star / purpose                  2
Current phase                         2
Completed-vs-remaining gates          2
Architecture candidate status         2
Machine verification                  2
Authorization boundaries              2
Correct next operation                2
Roadmap/canonical distinction         2
Semantic invariants                   2
Limitations / uncertainty             2
---------------------------------------
TOTAL                                20 / 20
```

Mandatory categories:

```text
category 2 = 2
category 3 = 2
category 6 = 2
category 7 = 2
```

Automatic critical failures:

```text
NONE OBSERVED
```

## Scorecard disposition

Frozen scorecard requires:

```text
SCORE >= 17 / 20
AND no automatic critical failure
AND categories 2, 3, 6, 7 each = 2
```

Observed:

```text
20 / 20
no automatic critical failure
mandatory categories all = 2
```

Therefore:

```text
BLIND_AGENT_TRIAL_1 = PROVISIONAL_PASS
```

## Particularly valuable research findings from the participant

The trial did more than reproduce expected answers.

### Finding A — Exact frozen ref mattered

The participant noticed that default `main` did not contain the CCP-1 research
state.

That is direct empirical support for the project's own distinction between a
moving/default repository surface and an explicitly frozen authority boundary.

### Finding B — Stale prose was visible but survivable

The participant identified multiple stale surfaces:

- historical architecture prose still saying CCP was not implemented;
- Issue #1 body describing P1 as future work;
- earlier sections of the accumulated CCP-1 README describing already-completed
  work as next work.

It nevertheless resolved the current state correctly by comparing authority,
time, and artifact role rather than trusting the first matching sentence.

That is encouraging, but it also indicates a usability cost that a human trial
may expose more strongly.

### Finding C — Mutable GitHub metadata source boundary is underspecified

The participant inspected later public branch/issues metadata.

Although it correctly refused to treat that material as frozen authority, the
trial packet did not explicitly specify whether post-freeze issue/ref discovery
was permitted.

For future trial protocol versions, consider making one of two rules explicit:

1. **strict frozen-source mode** — no refs/issues/commits newer than the frozen
   SHA may be consulted; or
2. **open-discovery mode** — later public metadata may be observed but must be
   classified as outside the frozen authority boundary.

Do not change the historical 0.1.0 trial retroactively.

## Advancement effect

This result satisfies the **agent-side initial cold-start requirement** for the
current frozen scorecard.

It does **not** complete CCP-1.

Remaining gate:

```text
UNFAMILIAR_HUMAN_COLD_START_TRIAL_1 = REQUIRED
POST_TRIAL_DESIGN_REVIEW = REQUIRED

CCP1_COMPLETE = NO
CCP2_AUTHORIZED = NO
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
```
