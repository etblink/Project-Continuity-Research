# CCP-1 Human Orientation Repair — Projection Audit Pass and Trial-2 Authorization 0.1.0

Date: 2026-09-22
Status: HUMAN REPAIR TRIAL 2 AUTHORIZED

Raw blind audit freeze:
`feff372c91b6007198cff881ffc24423ac121ccb`

Disposition:
`ORIENTATION_PROJECTION_PASS`

Audited frozen source snapshot:
`dec58643dbeb65adf90178f0bedd214dfa40b812`

Matched repaired content ref:
`883c4d78e7b55811bc6303c3cb182e9c1fde1fa1`

Reader:
`prototype/ccp1/trials/html/HUMAN_COLD_START_READER_0_3_2.html`

Scorecard:
`prototype/ccp1/trials/COLD_START_SCORECARD_0_1_0.md` — unchanged.

## Gate advancement

The orientation projection has passed independent source-faithfulness audit against the correct frozen historical boundary.

Therefore:

```text
ORIENTATION_PROJECTION_BLIND_AUDIT = PASS
HUMAN_REPAIR_TRIAL_2 = AUTHORIZED
CCP1_COMPLETE = NO
CCP2_AUTHORIZED = NO
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
```

## Trial-2 participant

Use a different unfamiliar human from Trial 1.

Required:
- no substantive prior knowledge of PCR;
- comfortable reading ordinary technical prose;
- no Git/programming knowledge required.

Trial-1 participant is ineligible for this repaired unfamiliar-human trial because prior exposure has occurred.

## Strict source boundary

During the unaided first attempt:
- use Reader 0.3.2 only;
- use only files exposed from `883c4d78...`;
- no GitHub issue/branch/commit pages;
- no external web search;
- facilitator gives browser/mechanical help only;
- no substantive project coaching.

## Primary comparison

Keep the same eight human questions and the same 0.1.0 scorecard.

This is a repair comparison, not a new easier scorecard.

## Required raw evidence before scoring

Preserve:
1. prior familiarity statement;
2. start/end/elapsed time;
3. complete answers to all eight questions verbatim;
4. first file opened;
5. navigation path notes;
6. search terms used;
7. substantive questions;
8. hesitation/confusion;
9. whether CURRENT_ORIENTATION.md was read;
10. whether at least one evidence pointer was followed;
11. whether the roadmap was found;
12. whether current vs historical material was distinguished;
13. whether authorization boundaries were found without coaching;
14. whether the participant still felt compelled to read everything;
15. any facilitator help;
16. technical/browser failures.

Freeze all raw evidence before scoring or correction.

## Post-trial rule

Regardless of pass/fail, perform a new post-trial design review.

A pass is necessary but not automatically sufficient for CCP-2.
