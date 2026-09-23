# CCP-1 Human Cold-Start / Usability Protocol 0.3.2

Date: 2026-09-22
Status: **MATCHED ORIENTATION-REPAIR PROTOCOL — EXECUTION BLOCKED ON BLIND PROJECTION AUDIT**

## Trial purpose

Test whether an explicit, non-canonical current-orientation projection lets a different unfamiliar human orient to the same historical project state that was used in Human Trial 1.

## Frozen historical boundary

Original project snapshot:
`dec58643dbeb65adf90178f0bedd214dfa40b812`

Repaired matched content ref:
`883c4d78e7b55811bc6303c3cb182e9c1fde1fa1`

The repaired content ref contains the original frozen tree plus only:
- `CURRENT_ORIENTATION.md`
- `prototype/ccp1/orientation/CURRENT_ORIENTATION_PROJECTION_SCHEMA_0_1_0.md`

The projection describes **current state relative to the frozen snapshot**, not the later real-world state of PCR.

## Reader

Use:
`prototype/ccp1/trials/html/HUMAN_COLD_START_READER_0_3_2.html`

Reader 0.3.2 opens `CURRENT_ORIENTATION.md` as the default project entry point and preserves unrestricted browse/search access to the matched frozen corpus.

## Participant

Use a different unfamiliar human. Trial-1's participant is no longer eligible as an unfamiliar replication subject.

## Questions and scorecard

Use the same eight task questions and the unchanged:
`prototype/ccp1/trials/COLD_START_SCORECARD_0_1_0.md`

No score threshold changes are allowed.

## Source boundary

Strict frozen-source mode:
- participant uses only Reader 0.3.2;
- all project documents come from `883c4d78e7b55811bc6303c3cb182e9c1fde1fa1`;
- no GitHub issues, branches, commit pages, or other later metadata;
- no web search;
- no facilitator interpretation during the first attempt.

## Additional observation

Record whether the participant:
- understands that the orientation page is a projection, not canonical truth;
- follows at least one evidence pointer to verify a claim;
- still feels compelled to read everything.

## Execution gate

```text
ORIENTATION_PROJECTION_BLIND_AUDIT = PENDING
HUMAN_REPAIR_TRIAL_2 = NOT_AUTHORIZED
CCP1_COMPLETE = NO
CCP2_AUTHORIZED = NO
```
