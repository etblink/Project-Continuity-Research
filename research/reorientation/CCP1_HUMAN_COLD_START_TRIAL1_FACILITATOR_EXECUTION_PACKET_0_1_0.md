# CCP-1 Human Cold-Start Trial 1 — Facilitator Execution Packet 0.1.0

Date: 2026-09-22
Status: EXECUTION LOGISTICS ONLY — DOES NOT MODIFY FROZEN TRIAL

## Frozen trial identity

```text
HUMAN_COLD_START_PROTOCOL = 0.2.1
PRESENTATION = HTML_READER_0.2.1
PROJECT_CONTENT_REF = dec58643dbeb65adf90178f0bedd214dfa40b812
SCORECARD = 0.1.0
```

Authoritative frozen files remain on branch `research/ccp1-adversarial-hardening`:

- `prototype/ccp1/trials/HUMAN_COLD_START_PROTOCOL_0_2_1.md`
- `prototype/ccp1/trials/html/HUMAN_COLD_START_READER_0_2_1.html`
- `prototype/ccp1/trials/COLD_START_SCORECARD_0_1_0.md`

This packet adds no trial content, answers, rankings, or guidance.

## Participant eligibility

Use one person who:
- did not create the project;
- does not already know its substantive current state;
- can read ordinary technical prose;
- need not know Git, programming, or AI research.

Record any prior familiarity before starting.

The project inventor may facilitate but may not answer substantive project questions during the unaided phase.

## Before participant begins

1. Open the exact frozen HTML reader 0.2.1.
2. Confirm it displays snapshot `dec58643…`.
3. Give the participant control of the reader.
4. Start elapsed-time recording.
5. Record prior familiarity.
6. Do not identify important files or suggest a reading order.

## Permitted facilitator help

Only:
- opening the HTML file;
- browser/connectivity mechanics;
- explaining folder expand/collapse, search, file history, or navigation controls.

Do not:
- explain project concepts;
- explain CCP;
- tell the participant which document to read;
- provide search terms;
- confirm whether an answer is correct;
- interpret repository history;
- reveal the scorecard during the unaided attempt.

If the participant asks a substantive question, record it and say that it should remain unanswered until the first attempt is complete.

## Participant task

The frozen reader already displays the eight trial questions. Do not paraphrase them into hints.

Suggested first-attempt timebox: approximately 30 minutes. Record actual elapsed time even if the participant finishes earlier or continues somewhat longer.

## Evidence preservation rule

Before any correction, explanation, or discussion:
1. preserve the participant's complete first answers verbatim;
2. preserve navigation/observation notes;
3. record elapsed time;
4. record any substantive questions;
5. record whether the participant naturally found the roadmap;
6. record whether they distinguished current state from historical prose;
7. record whether they found authorization boundaries without coaching.

Do not score from memory if a raw answer can be preserved.

## After raw freeze

Only after the participant's first answers are frozen may an evaluator use `COLD_START_SCORECARD_0_1_0.md`.

Human dimensions:
1. purpose comprehension;
2. current phase/gate comprehension;
3. authorization-boundary comprehension;
4. ability to locate evidence/current state;
5. ability to explain one attack with its limitation;
6. plausible next operation without inventor coaching.

Pass threshold remains:
```text
SCORE >= 10 / 12
AND
NO AUTOMATIC CRITICAL FAILURE
AND
authorization-boundary comprehension = 2
```

A pass is necessary but not sufficient for CCP-2. The frozen protocol requires post-trial design review.

## Automatic critical failures

Preserve exactly:
- concludes live project mutation is authorized;
- concludes CCP-2 is already authorized;
- treats CCP as a proven final universal architecture;
- treats machine PASS as proof the higher-order research question is solved.

## Return package

Return four things without correction or cleanup:
1. participant raw answers;
2. facilitator observation log;
3. elapsed time + prior familiarity;
4. any technical/browser failure encountered.

The project lead will freeze those materials before scoring.

## Current program boundary

```text
HUMAN_COLD_START_TRIAL_1 = READY_FOR_EXTERNAL_PARTICIPANT
CCP1_COMPLETE = NO
CCP2_AUTHORIZED = NO
WORLD_G_CUMULATIVE = HOLD__PROGRAM_REORIENTATION
```
