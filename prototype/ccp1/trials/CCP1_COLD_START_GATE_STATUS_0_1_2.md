# CCP-1 Cold-Start Gate Status 0.1.2

Date: 2026-09-20  
Status: **AGENT SIDE PASSED — HUMAN TRIAL PREPARED / NOT YET RUN**

## Current state

A prospective unfamiliar-human participant is available but reported that
Git/GitHub navigation would itself be a significant usability barrier.

Before the first human trial began, the project therefore introduced a
versioned HTML-reader presentation variant.

```text
BLIND_AGENT_TRIAL_1 = PROVISIONAL_PASS
HUMAN_COLD_START_TRIAL_1 = PREPARED / NOT_YET_RUN

HUMAN_PROTOCOL = 0.2.0
PRESENTATION = HTML_READER_0.2.0
PROJECT_CONTENT_REF =
dec58643dbeb65adf90178f0bedd214dfa40b812

SCORECARD = COLD_START_SCORECARD_0_1_0
```

## What changed

Only the participant-facing presentation layer changed.

The HTML reader:

- presents ordinary browser navigation;
- exposes the complete frozen project file tree;
- provides filename search;
- reads the exact frozen repository snapshot;
- does not rank files;
- does not provide expected answers;
- does not supply a recommended-reading path.

## What did not change

```text
PROJECT_CONTENT = UNCHANGED
TRIAL_QUESTIONS = MATERIALLY_UNCHANGED
PASS_THRESHOLD = UNCHANGED
CRITICAL_FAILURES = UNCHANGED
FIRST_ATTEMPT_MUST_BE_UNCOACHED = YES
```

Protocol 0.1.0 remains preserved as historical evidence.

Protocol 0.2.0 records the browser-reader variant.

## Methodological interpretation

The need for an HTML reader is itself usability evidence:

```text
GIT_FLUENCY != PROJECT_ORIENTATION_CAPABILITY
```

If the target architecture is intended for ordinary humans, requiring Git
navigation merely to test comprehension would confound project
comprehensibility with repository-tool expertise.

Removing that confound does not mean removing discoverability from the test:
the participant must still decide which project artifacts matter.

## Advancement boundary

The human trial has not started and no result should be inferred yet.

```text
HUMAN_COLD_START_TRIAL_1 = NOT_YET_RUN

CCP1_COMPLETE = NO
CCP2_AUTHORIZED = NO
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
```

## Next event

The next admissible human-trial event is the participant beginning the unaided
HTML-reader trial.

Preserve:

- prior familiarity disclosure;
- start/end time;
- browser/device;
- any mechanical assistance;
- substantive questions;
- raw first answers before correction.
