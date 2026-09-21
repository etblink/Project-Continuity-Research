# CCP-1 Human Cold-Start / Usability Protocol 0.2.1

Date: 2026-09-20  
Status: **FROZEN BEFORE FIRST HUMAN TRIAL — NAVIGATION-REPAIRED HTML VARIANT**

## Supersession

This protocol supersedes presentation protocol 0.2.0 **before any human trial
was run**.

Protocol 0.1.0 and 0.2.0 remain preserved as historical design evidence.

The reason for 0.2.1 is an observed presentation-layer defect:

> The flat file list made ordinary navigation impractical unless the participant
> already knew or memorized filenames and relied on search.

That would make the trial partly a test of repository/file-name knowledge rather
than project orientation.

## Frozen project content

The project content under evaluation remains unchanged:

```text
dec58643dbeb65adf90178f0bedd214dfa40b812
```

The scorecard also remains unchanged:

```text
prototype/ccp1/trials/COLD_START_SCORECARD_0_1_0.md
```

## Reader

Use:

```text
prototype/ccp1/trials/html/HUMAN_COLD_START_READER_0_2_1.html
```

The reader still loads project files only from the frozen Git ref.

## Navigation behavior

Reader 0.2.1 provides ordinary document-browser mechanics:

- expandable/collapsible folder hierarchy;
- a neutral virtual "Root files" group for files at repository root;
- file counts per folder;
- optional filename search;
- persistent Instructions / Browse files navigation;
- breadcrumbs for the open file;
- previous/next viewed-file history;
- explicit return to the file browser;
- responsive layout for smaller screens.

These controls are **presentation mechanics**, not project guidance.

The reader must not:

- rank files by importance;
- recommend a reading order;
- identify which files contain correct answers;
- expose evaluator answers;
- substitute later repository content.

## Participant requirements

The participant:

- need not know Git or GitHub;
- need not be a programmer;
- need not have prior interest in AI or this research topic;
- should not already know the project's substantive current state;
- should be comfortable reading ordinary technical prose.

Record any prior familiarity.

## Suggested timebox

Approximately 30 minutes for the first unaided orientation attempt.

Record actual time.

## Tasks

Ask the participant to determine:

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

- opening the HTML file;
- browser mechanics;
- connectivity;
- explaining how folder expand/collapse, search, or file-history buttons work.

Do not explain project concepts or tell the participant which file to open.

Record substantive questions rather than answering them during the unaided
phase.

## Observations to record

Record:

- elapsed time;
- prior familiarity;
- first file opened;
- folder/navigation path if practical;
- search terms if used;
- incorrect assumptions;
- hesitation/confusion;
- substantive questions;
- whether the participant naturally found the roadmap;
- whether current state could be distinguished from historical prose;
- whether authorization boundaries were found without coaching.

## Critical failures

Unchanged:

- concludes live project mutation is authorized;
- concludes CCP-2 is already authorized;
- treats CCP as a proven final universal architecture;
- treats machine PASS as proof the higher-order research question is solved.

## Trial return metadata

Record:

```text
HUMAN_COLD_START_PROTOCOL = 0.2.1
PRESENTATION = HTML_READER_0.2.1
PROJECT_CONTENT_REF = dec58643dbeb65adf90178f0bedd214dfa40b812
SCORECARD = 0.1.0
```

Preserve the participant's raw first answers before correction.

## Advancement boundary

```text
HUMAN_COLD_START_TRIAL_1 = NOT YET RUN
CCP1_COMPLETE = NO
CCP2_AUTHORIZED = NO
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
```
