# CCP-1 Human Cold-Start / Usability Protocol 0.2.0

Date: 2026-09-20  
Status: **FROZEN BEFORE FIRST HUMAN TRIAL — HTML READER VARIANT**

## Why this version exists

Before the first human cold-start trial began, the prospective participant
reported that Git/GitHub navigation would itself be a substantial barrier.

That is relevant usability evidence.

The project is intended for people who may not know Git, so protocol 0.2.0
changes only the **presentation layer** of the human trial.

Protocol 0.1.0 remains preserved as historical evidence and is not rewritten.

## Frozen project content

The project content being evaluated remains exactly:

```text
dec58643dbeb65adf90178f0bedd214dfa40b812
```

The HTML reader must load project files only from that frozen Git ref.

No later repository content may be substituted for the project material being
evaluated.

## Reader

Use:

```text
prototype/ccp1/trials/html/HUMAN_COLD_START_READER_0_2_0.html
```

The reader:

- presents the trial instructions in ordinary browser language;
- exposes the complete file tree from the frozen repository snapshot;
- provides filename search;
- loads file contents from the exact frozen Git ref;
- does not rank files by importance;
- does not provide expected answers;
- does not provide a hand-curated recommended-reading path.

This preserves discoverability as part of the trial while removing Git
mechanics as a prerequisite.

## Participant requirement

Prefer a participant who:

- has not followed Project Continuity Research;
- has not read the design conversation;
- is comfortable reading ordinary technical prose;
- does not need Git, programming, or AI-research expertise.

Record any prior familiarity.

Lack of prior interest in the topic is **not** disqualifying.

## Suggested timebox

Approximately 30 minutes for the first unaided orientation attempt.

Record the actual time.

## Tasks

Using the HTML reader, ask the participant to determine:

1. In their own words, what problem is this project trying to solve?
2. What phase is the project currently in?
3. What has to happen before the next major phase may begin?
4. Is the current CCP architecture already authorized to control a live
   project? Why or why not?
5. Where would they look to distinguish:
   - big-picture roadmap;
   - exact current research result;
   - machine verification;
   - historical research artifacts?
6. Pick one completed adversarial attack and explain:
   - what failure it tested;
   - what passed;
   - what the result still does **not** prove.
7. What would they do next if asked to continue the project without the
   inventor present?
8. Name anything they found confusing, redundant, hard to locate, or easy to
   misinterpret.

## Assistance rule

During the first attempt, the facilitator may help only with:

- opening the HTML reader;
- browser mechanics;
- internet/connectivity problems;
- explaining how to click or search within the reader.

Do not provide substantive project guidance.

If the participant asks a substantive question, record it before answering it
after the unaided phase.

## Observations to record

Record:

- elapsed time;
- first file opened;
- navigation/search path if practical;
- incorrect assumptions;
- points of hesitation;
- substantive questions;
- confusion/friction;
- whether the roadmap helped;
- whether exact state could be distinguished from orientation prose;
- whether the participant found the current authorization boundary without
  coaching.

## Critical failures

The critical-failure semantics are unchanged from protocol 0.1.0.

Record a critical failure if the participant concludes that:

- live project mutation is currently authorized;
- CCP-2 is already authorized;
- CCP is a proven final universal architecture;
- machine test PASS proves the higher-order research question is solved.

## Scoring

Continue to use the already frozen:

```text
prototype/ccp1/trials/COLD_START_SCORECARD_0_1_0.md
```

The outcome criteria and pass threshold have not changed.

## Trial return

Preserve the participant's first answers before correction.

Record:

```text
HUMAN_COLD_START_PROTOCOL = 0.2.0
PRESENTATION = HTML_READER_0.2.0
PROJECT_CONTENT_REF = dec58643dbeb65adf90178f0bedd214dfa40b812
```

Also record:

- participant prior familiarity;
- actual elapsed time;
- any facilitator assistance;
- browser/device used;
- complete first answers;
- any substantive questions asked during the trial.

## Interpretation

A pass under protocol 0.2.0 is evidence about whether an unfamiliar human can
orient from the **same frozen project information through an ordinary browser
interface**.

It should not be described as evidence that the person can navigate GitHub or
Git.

Conversely, failure caused by confusing project content remains valid usability
evidence even though Git mechanics have been removed.

## Advancement boundary

```text
HUMAN_COLD_START_TRIAL_1 = NOT YET RUN
CCP1_COMPLETE = NO
CCP2_AUTHORIZED = NO
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
```
