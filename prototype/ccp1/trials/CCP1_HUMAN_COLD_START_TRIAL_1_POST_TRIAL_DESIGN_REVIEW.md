# CCP-1 Human Cold-Start Trial 1 — Post-Trial Design Review 0.1.0

Date: 2026-09-22
Status: POST-TRIAL DESIGN REVIEW — HUMAN ORIENTATION REPAIR REQUIRED

Raw return freeze:
`0db21e6cae42d00fe95a5551399f951526646bbc`

Scoring adjudication:
`57559a12b1d095bfd9bc52dd4b9d91c12575c49c`

Frozen trial content:
`dec58643dbeb65adf90178f0bedd214dfa40b812`

## 1. Trial result

```text
HUMAN_SCORE = 3 / 12
AUTOMATIC_CRITICAL_FAILURE = NO
AUTHORIZATION_BOUNDARY = 0 / 2
PROVISIONAL_HUMAN_USABILITY_PASS = NO
```

The participant recovered:
- project purpose;
- Phase 4.

The participant did not recover:
- the actual advancement gate;
- whether CCP/live control is authorized;
- where current/evidence/machine/history surfaces live;
- one completed adversarial attack and its limitation;
- a bounded next operation.

The participant's proposed continuation was:
> I'd have to read **EVERYTHING** and try to understand what is going on.

The participant's usability report was:
> I found it difficult to find the information I was supposed to be looking for. I feel overwhelmed and that the amount of work to sift through all this is too high.

## 2. Trial-validity note

The participant explicitly reported no prior project knowledge and a first-attempt elapsed time of 00:16:42.66.

The supplied return did not include the requested first-file/navigation/search/facilitator-help log. Therefore:

```text
TRIAL_CONTENT_RESULT = USABLE
PROCESS_OBSERVATION_COMPLETENESS = PARTIAL
CONTAMINATION = NOT OBSERVED, BUT NOT FULLY AUDITABLE FROM RETURN
```

The missing process metadata does not explain away the substantive failures, but it limits fine-grained attribution of where navigation broke down.

## 3. Pretrial repair did not solve the higher-order problem

Reader 0.2.0 had already exposed:

```text
COMPLETE FILE ACCESS != USABLE INFORMATION DISCOVERY
FILENAME SEARCH != PROJECT NAVIGATION FOR AN UNFAMILIAR HUMAN
```

Reader 0.2.1 repaired browser mechanics with folder hierarchy, breadcrumbs, file history, and full-text search.

The formal participant nevertheless still reported inability to locate the required information.

Thus the new result is stronger:

```text
BROWSABLE + SEARCHABLE CORPUS != USABLE PROJECT ORIENTATION
```

## 4. Structural load in the frozen snapshot

Frozen snapshot `dec58643...` exposes:

```text
TOTAL_FILES = 100
ROOT_FILES = 33
CCP1_FILES = 51
MARKDOWN_FILES = 65
```

Reader 0.2.1 intentionally:
- did not rank files;
- did not recommend a reading order;
- did not identify important files;
- did not summarize current project orientation.

Those constraints avoided answer-key leakage, but they also removed an explicit orientation path.

## 5. Missing architecture-facing surface

The frozen snapshot contains:
- `BIG_PICTURE_ROADMAP.md`;
- `prototype/ccp1/README.md`;
- individual attack/result files;
- CI checkpoints;
- historical research artifacts.

It does **not** contain a current CCP-1 orientation projection for Project Continuity Research itself that binds, in one auditable surface:
- North Star;
- current phase;
- completed-vs-remaining gates;
- architecture-candidate status;
- authorization prohibitions;
- current bounded next operation;
- machine-verification checkpoint;
- open uncertainty/limitations;
- links to exact supporting evidence/history.

The only generated Project Kernel in the frozen corpus is the earlier CCP-0 Project Observatory shadow kernel. It does not serve as current PCR/CCP-1 orientation.

Therefore the participant had to synthesize current orientation manually across multiple document classes.

## 6. Core diagnosis

```text
PRIMARY = ORIENTATION-SURFACE SUFFICIENCY FAILURE
SECONDARY = INFORMATION-DISCOVERY / PRESENTATION FAILURE
PARTICIPANT_DEFICIT = NOT THE DESIGN INTERPRETATION
```

This is consistent with the project's own architectural hypothesis:

```text
KERNEL / ORIENTATION PROJECTION != SOLE SOURCE OF TRUTH
```

but the opposite mistake has now appeared:

```text
NOT SOLE SOURCE OF TRUTH
!=
NO EXPLICIT ORIENTATION ENTRY POINT
```

A projection may be non-authoritative while still being the deliberate starting surface for a successor.

## 7. Relationship to machine results

CCP-1's autonomous suite had reached 124 / 124 PASS at the frozen checkpoint, including orientation-contract quality.

The human result establishes:

```text
MACHINE-VERIFIED ORIENTATION CONSTRAINTS
!=
UNFAMILIAR-HUMAN ORIENTATION USABILITY
```

This is not a contradiction. The machine tests show bounded semantic properties; the human trial tests discoverability, synthesis burden, and practical orientation.

## 8. Repair principle

Do not merely make search better again.

The repair should externalize the missing executive function:

> provide a first-class, human-readable, freshness-bound CURRENT ORIENTATION projection whose job is to tell an unfamiliar successor where the project is, what governs it, what remains unauthorized, what the next bounded operation is, and where to verify each claim.

This surface must:
- be generated or mechanically checkable from durable state where possible;
- carry freshness/provenance identity;
- remain explicitly non-canonical / non-sole-source-of-truth;
- link to authoritative evidence rather than replacing it;
- distinguish current state from historical results;
- expose prohibitions/holds prominently;
- expose the next authorized operation or correct reason to wait;
- remain understandable without filename knowledge.

## 9. Reader implication

A repaired human reader should open with the current-orientation projection as the explicit project entry point, then allow unrestricted evidence browsing.

That is not an answer-key leak if the projection is a real architectural output intended for ordinary successors. Hiding the orientation surface to make the trial harder would test repository archaeology rather than the intended continuity architecture.

## 10. Repair experiment

Authorize a bounded CCP-1 human-orientation repair:

1. define the minimum current-orientation projection schema;
2. materialize one projection for PCR/CCP-1 from current durable state;
3. bind it to exact source artifacts / freshness identity;
4. externally audit the projection for omission and misleading authority;
5. create Reader 0.3.0 with the projection as the default entry surface;
6. preserve unrestricted browse/search access to the full frozen evidence corpus;
7. keep `COLD_START_SCORECARD_0_1_0.md` unchanged for comparability;
8. freeze a new project-content ref;
9. run the repaired trial on a **different unfamiliar human participant**;
10. preserve raw first answers before scoring.

The first participant is no longer eligible as an unfamiliar-human replication subject because exposure has occurred.

## 11. Advancement boundary

```text
CCP1_HUMAN_COLD_START_1 = FAIL
CCP1_HUMAN_ORIENTATION_REPAIR = AUTHORIZED
CCP1_COMPLETE = NO
CCP2_AUTHORIZED = NO
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
WORLD_G_CUMULATIVE = HOLD__PROGRAM_REORIENTATION
```

No CCP-2 decision is permitted until the repaired human-orientation path is independently tested and the result receives its own post-trial review.
