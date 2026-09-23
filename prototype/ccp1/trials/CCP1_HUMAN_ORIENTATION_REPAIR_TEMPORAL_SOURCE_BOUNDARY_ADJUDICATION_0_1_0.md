# CCP-1 Human Orientation Repair — Temporal Source-Boundary Adjudication 0.1.0

Date: 2026-09-22
Status: AUDIT-PACKET CONSTRUCTION DEFECT CONFIRMED

## Trigger

Blind re-audit 0.1.1 returned:
`FAIL_CURRENT_STATE_OR_GATE_DISTORTION`

Raw re-audit freeze:
`a58c8f49c515070c1cbb84c61a817b3679f424e9`

## Exact frozen-snapshot verification

Matched human-repair base snapshot:
`dec58643dbeb65adf90178f0bedd214dfa40b812`

Tree:
`60e674aad847f2f02c5046b7a2f9661addf04eae`

Within that exact tree, the cold-start-related files include:
- `prototype/ccp1/trials/COLD_START_SCORECARD_0_1_0.md`
- `prototype/ccp1/trials/HUMAN_COLD_START_PROTOCOL_0_1_0.md`

The tree does **not** contain:
- `CCP1_BLIND_AGENT_TRIAL_1_RAW.md`
- `CCP1_BLIND_AGENT_TRIAL_1_ADJUDICATION.md`
- later cold-start gate status files recording the provisional pass.

The frozen roadmap at this ref states:
- blind-agent cold-start remains required;
- unfamiliar-human cold-start remains required;
- CCP-1 remains incomplete.

The autonomous-family result at this ref likewise records both external cold-start gates as required.

## Root cause

The first projection audit packet (0.1.0) accidentally mixed temporal boundaries:
- candidate projection intended to summarize `dec58643...`;
- audit sources were pulled from the later `research/ccp1-adversarial-hardening` branch, after Blind-Agent Trial 1 had provisionally passed.

That first auditor therefore correctly judged the packet it received, but the packet did not represent the matched trial boundary.

The subsequent repair imported the later provisional-pass state into the historical matched corpus, creating the exact distortion caught by re-audit 0.1.1.

## Classification

```text
PRIMARY = AUDIT_PACKET_TEMPORAL_SOURCE_BOUNDARY_DEFECT
SECONDARY = EPISTEMIC_STATE / CURRENT-VS-HISTORICAL MIXING
PROJECTION_0_3_1 = INVALID_FOR_MATCHED_TRIAL
AUDITOR_0_1_1 = CORRECT_RELATIVE_TO_PACKET
```

This is not evidence that the orientation-projection concept failed. It is evidence that the repair pipeline itself violated:

```text
HISTORICAL_TRUTH != CURRENT_AUTHORITY
SOURCE_BOUNDARY != LATER_PROJECT_STATE
MATCHED_TRIAL_SNAPSHOT != TODAY'S_PROJECT_STATE
```

## Correct repair target

For the matched human repair trial, `CURRENT_ORIENTATION.md` must mean:

> current orientation **relative to the frozen trial snapshot** `dec58643...`.

Therefore it must preserve the state actually available there:
- Phase 4 active;
- P1 complete;
- autonomous secondary set complete;
- blind-agent cold-start still required;
- unfamiliar-human cold-start still required;
- CCP-1 incomplete;
- CCP-2 unauthorized;
- next operation: complete/freeze reproducible cold-start protocols and hand them to independent participants, with no advancement until both results return.

The later real-world program state remains preserved elsewhere and must not leak into this matched historical trial.

## Recovery

1. rebuild the projection from the exact `dec58643...` source boundary;
2. keep only the two intended added files in the matched content corpus;
3. bind a new Reader 0.3.2 to that content ref;
4. construct the next blind audit from exact `dec58643...` sources only;
5. require `ORIENTATION_PROJECTION_PASS` before Human Trial 2.

No human repair trial has been run under the defective projection.
