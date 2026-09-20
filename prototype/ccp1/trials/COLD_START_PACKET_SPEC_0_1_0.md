# CCP-1 Cold-Start Trial Packet Specification 0.1.0

Date: 2026-09-20  
Status: **FROZEN BEFORE FIRST TRIAL**

## Frozen-source rule

Every participant must be evaluated against one exact Git ref.

Do not use moving `main` or a moving research branch as the trial source.

The trial issue will name the exact tag/commit.

## Participant packet

The participant gets:

- repository URL;
- frozen Git ref;
- the applicable cold-start protocol.

For the first trial, do not provide a hand-curated list of "important files."
Discoverability is part of the test.

## Contamination controls

Do not provide:

- this conversation;
- predecessor summaries;
- a verbal project overview;
- unpublished expected answers;
- evaluator commentary;
- prior participant responses before the participant submits its own response.

If the participant's environment injects persistent memory about this project,
mark the run `CONTAMINATED` and do not count it as a blind trial.

## Repository access

Read-only web/Git access is allowed.

The participant may use search, grep, or repository browsing.

The question is whether durable artifacts make correct reconstruction possible,
not whether a person can memorize a predetermined navigation path.

## Return artifact naming

Suggested naming:

```text
CCP1_BLIND_AGENT_TRIAL_<N>_RAW.md
CCP1_BLIND_AGENT_TRIAL_<N>_ADJUDICATION.md

CCP1_HUMAN_COLD_START_TRIAL_<N>_RAW.md
CCP1_HUMAN_COLD_START_TRIAL_<N>_ADJUDICATION.md
```

Raw returns must be preserved before adjudication.

## Trial-order rule

Do not modify the orientation architecture in response to a participant's
difficulty until that participant's raw result is frozen.

If a repair is made, run a new participant/trial version rather than editing the
old result.

## Current advancement boundary

```text
BLIND_AGENT_TRIAL = NOT YET RUN
HUMAN_COLD_START_TRIAL = NOT YET RUN
CCP1_COMPLETE = NO
CCP2_AUTHORIZED = NO
```
