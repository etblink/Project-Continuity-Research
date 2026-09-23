# CCP-1 Human Cold-Start / Usability Protocol 0.3.3

Date: 2026-09-22
Status: **MATCHED ORIENTATION-REPAIR PROTOCOL — EXECUTION BLOCKED ON RE-AUDIT**

## Trial purpose

Test whether an explicit, non-canonical current-orientation projection lets a different unfamiliar human orient to the same historical project state used in Human Trial 1.

## Frozen historical boundary

Original project snapshot:
`dec58643dbeb65adf90178f0bedd214dfa40b812`

Repaired matched content ref:
`e43aef38ae4b6690f6bae8479e9bfb98a47776b6`

The repaired content ref contains the original frozen tree plus the orientation projection/schema only. The projection describes current state relative to the frozen snapshot, not later PCR history.

## Pre-trial objective-clarity repair

Before Trial 2 began, project-lead review found that projection 0.1.2 adequately oriented the reader to current state and evidence, but did not state the **immediate objective** clearly enough.

Projection 0.1.3 adds one explicit layer:

```text
NORTH_STAR = why the program exists
IMMEDIATE_OBJECTIVE = what Phase 4 is trying to establish
NEXT_OPERATION = what bounded action happens next
```

No scorecard, source snapshot, gate status, or pass threshold changed.

## Reader

Use:
`prototype/ccp1/trials/html/HUMAN_COLD_START_READER_0_3_3.html`

Reader 0.3.3 opens `CURRENT_ORIENTATION.md` as the default project entry point and preserves unrestricted browse/search access to the matched frozen corpus.

## Participant

Use a different unfamiliar human from Trial 1.

## Questions and scorecard

Use the same eight questions and unchanged:
`prototype/ccp1/trials/COLD_START_SCORECARD_0_1_0.md`

## Strict source boundary

Participant uses Reader 0.3.3 only. No later GitHub metadata, issues, branches, commit pages, external web search, or facilitator interpretation during the first attempt.

## Additional observations

Record whether the participant:
- can state the immediate objective separately from the North Star and next operation;
- reads the orientation projection;
- follows at least one evidence pointer;
- still feels compelled to read everything.

## Execution gate

```text
ORIENTATION_PROJECTION_0_1_3_BLIND_AUDIT = PENDING
HUMAN_REPAIR_TRIAL_2 = SUSPENDED_PENDING_REAUDIT
CCP1_COMPLETE = NO
CCP2_AUTHORIZED = NO
```
