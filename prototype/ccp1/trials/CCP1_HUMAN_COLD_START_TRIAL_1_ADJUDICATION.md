# CCP-1 Human Cold-Start Trial 1 — Scoring Adjudication 0.1.0

Date: 2026-09-22
Status: FROZEN FIRST HUMAN TRIAL SCORING
Raw return freeze: `0db21e6cae42d00fe95a5551399f951526646bbc`
Frozen project content: `dec58643dbeb65adf90178f0bedd214dfa40b812`
Scorecard: `prototype/ccp1/trials/COLD_START_SCORECARD_0_1_0.md` (blob `f119d1fd5c1569a9c83311001fd43f86a2316b38`)

## Score

```text
1. purpose comprehension                    = 2
2. current phase/gate comprehension         = 1
3. authorization-boundary comprehension     = 0
4. ability to locate evidence/current state = 0
5. attack + limitation comprehension        = 0
6. plausible next operation                 = 0

TOTAL = 3 / 12
AUTOMATIC_CRITICAL_FAILURE = NO
AUTHORIZATION_BOUNDARY_SCORE = 0
PROVISIONAL_HUMAN_USABILITY_PASS = NO
```

## Dimension rationale

### 1. Purpose comprehension = 2

Participant:
> This project is attempting to discover the minimum durable information architecture necessary for a succession of intelligent but context-limited agents to preserve purpose, truth, state, and direction across arbitrarily long projects.

This is substantively faithful to the frozen project purpose and North Star.

### 2. Current phase/gate comprehension = 1

Participant correctly identified:
> Phase 4

But for the gate answered only:
> I need to complete these questions

The frozen roadmap states that the remaining CCP-1 exit requirements include independent cold-start evidence and post-trial review before CCP-2. Identifying the current trial as personally pending is not enough to reconstruct the program-level advancement gate.

### 3. Authorization-boundary comprehension = 0

Participant:
> I'm not sure

The frozen snapshot repeatedly states:
`CCP2_AUTHORIZED = NO` and `LIVE_PROJECT_MUTATION = NOT_AUTHORIZED`.

The participant did not incorrectly conclude authorization, so no automatic critical failure is triggered. But the required authorization-boundary comprehension is absent.

### 4. Ability to locate evidence/current state = 0

Participant:
> I couldn't say.

The frozen roadmap explicitly distinguishes the big-picture orientation surface from exact current work, while the CCP-1 README/result artifacts expose machine verification and historical/result evidence. The participant could not identify where to locate these classes.

### 5. Ability to explain one attack with its limitation = 0

Participant:
> I can't find the answer

No attack, result, or limitation was recovered.

### 6. Plausible next operation without inventor coaching = 0

Participant:
> I'd have to read **EVERYTHING** and try to understand what is going on.

This does not identify a bounded next operation. It is directly contrary to the project's intended orientation function: a successor should not need exhaustive reconstruction before acting. The frozen CCP-1 state identifies independent cold-start trials as the next gate.

## Pass-gate adjudication

Frozen human pass gate:

```text
SCORE >= 10 / 12
AND
NO AUTOMATIC CRITICAL FAILURE
AND
authorization-boundary comprehension = 2
```

Observed:

```text
SCORE = 3 / 12
AUTOMATIC_CRITICAL_FAILURE = NO
authorization-boundary comprehension = 0
```

Disposition:

```text
HUMAN_COLD_START_TRIAL_1 = FAIL
FAILURE_KIND = ORIENTATION / USABILITY FAILURE
PARTICIPANT_ERROR_BLAME = NONE
CCP1_COMPLETE = NO
CCP2_AUTHORIZED = NO
```

## High-value qualitative evidence

Elapsed time: `00:16:42.66`.

Participant reported:
> I found it difficult to find the information I was supposed to be looking for. I feel overwhelmed and that the amount of work to sift through all this is too high.

This is direct usability evidence that the frozen presentation did not provide an unfamiliar human with a sufficiently usable route from project purpose to authoritative current orientation.

## Important boundary

This result does not show that the underlying repository lacks the relevant facts. The frozen snapshot contains them.

The failure is that an unfamiliar participant could not reliably discover and organize those facts into:
- advancement gate;
- authorization boundary;
- evidence map;
- bounded next action.

Therefore the first post-trial question is architectural/presentation sufficiency, not whether the participant should have read more.
