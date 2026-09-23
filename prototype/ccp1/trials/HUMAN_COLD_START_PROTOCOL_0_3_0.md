# CCP-1 Human Cold-Start / Usability Protocol 0.3.0

Date: 2026-09-22
Status: **FROZEN CANDIDATE REPAIR PROTOCOL — EXECUTION BLOCKED ON PROJECTION AUDIT**

## Why this version exists

Human Trial 1 using Reader 0.2.1 returned 3/12. The participant recovered project purpose and Phase 4 but could not recover the advancement gate, authorization boundary, evidence map, one adversarial result, or a bounded next operation. The participant reported that the project was overwhelming and appeared to require reading everything.

Post-trial design review concluded:

```text
BROWSABLE + SEARCHABLE CORPUS != USABLE PROJECT ORIENTATION
```

Reader 0.3.0 tests one bounded repair: expose a first-class current-orientation projection as the default starting surface.

## Matched-content design

The repaired trial uses the original frozen content snapshot as its base:

`dec58643dbeb65adf90178f0bedd214dfa40b812`

and adds only:
- `CURRENT_ORIENTATION.md`
- `prototype/ccp1/orientation/CURRENT_ORIENTATION_PROJECTION_SCHEMA_0_1_0.md`

Repaired frozen content ref:

`b9a428700747d4f5bfc158cb23e50cc68e3b389d`

Trial-1 raw answers, scoring, and later project history are **not** present in the participant corpus.

## Reader

Use:
`prototype/ccp1/trials/html/HUMAN_COLD_START_READER_0_3_0.html`

Reader 0.3.0:
- opens `CURRENT_ORIENTATION.md` as the explicit starting surface;
- preserves unrestricted browsing/search of the full frozen corpus;
- does not expose evaluator scoring;
- does not expose Trial-1 answers;
- does not inject post-freeze GitHub metadata.

## Why surfacing orientation is not answer-key leakage

A continuity architecture is supposed to externalize orientation. The trial should test whether an unfamiliar human can understand and verify that orientation, not whether they can discover a hidden starting file among 100 repository files.

The projection is explicitly non-canonical and links to exact supporting artifacts.

## Participant

Use a **different unfamiliar human**. Trial-1's participant is no longer eligible for an unfamiliar-human replication because exposure has occurred.

Participant requirements otherwise remain unchanged.

## Tasks

Keep the same eight tasks from protocol 0.2.1 for matched comparison.

## Assistance

Mechanical/browser help only. Do not interpret the projection or verify answers during the first attempt.

## Frozen scorecard

Keep:
`prototype/ccp1/trials/COLD_START_SCORECARD_0_1_0.md`

unchanged.

Pass threshold remains:
```text
SCORE >= 10 / 12
AND
NO AUTOMATIC CRITICAL FAILURE
AND
authorization-boundary comprehension = 2
```

## Additional observations

Record:
- whether the participant read the orientation projection;
- whether they followed its evidence links;
- whether they still felt compelled to read everything;
- any claim in the projection they found ambiguous or misleading.

## Source boundary

Strict frozen-source mode:
- participant uses only Reader 0.3.0 and the files it exposes from `b9a428700747d4f5bfc158cb23e50cc68e3b389d`;
- no GitHub issues, branches, commits, or metadata outside that frozen ref;
- no external web search.

## Execution gate

```text
ORIENTATION_PROJECTION_BLIND_AUDIT = REQUIRED
READER_STATIC_BINDING_CHECK = REQUIRED
HUMAN_REPAIR_TRIAL_2 = NOT_YET_AUTHORIZED
```

No execution until the projection passes independent audit.
