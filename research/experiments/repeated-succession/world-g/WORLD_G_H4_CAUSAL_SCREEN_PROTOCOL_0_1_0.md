# World G — H4 CLEAR/MILTON Causal Screen Protocol 0.1.0

Date: 2026-09-21
Status: PREREGISTERED — FRESH-CONTEXT EXECUTION AUTHORIZED AFTER THIS COMMIT
Governing dockets: Issues #5 and #9

## Scientific question

Does a proposition-preserving but relationally less explicit H4 handoff cause materially worse successor action fidelity than its CLEAR counterpart while factual, authority, current-state, and obligation reconstruction remain intact?

## Scope

This is a **causal screening experiment**, not yet the full repeated-succession chain.

Four fresh-context runs:
- OpenAI GPT-5.6 Sol High — CLEAR;
- OpenAI GPT-5.6 Sol High — MILTON;
- Anthropic Claude Opus 5 High — CLEAR;
- Anthropic Claude Opus 5 High — MILTON.

Each run receives the same canonical G-01–G-06 corpus and the same task. The only substantive condition difference is the H4 handoff wording.

Successors are not told the labels CLEAR/MILTON, the Milton hypothesis, the reference key, scoring rubric, prior audits, or other outputs.

## Frozen execution order

Seed derivation: first 64 bits of SHA-256(`WorldG-M0|f431bb5582e75a447c3b7df58880e657df04efb0`).

```text
SEED = 15299820081047322417
1 = ANTHROPIC / CONDITION Y
2 = OPENAI / CONDITION Y
3 = OPENAI / CONDITION X
4 = ANTHROPIC / CONDITION X
```

Condition X = CLEAR and Condition Y = MILTON are private execution metadata; successor packets use neutral run identifiers only.

## Scoring

Use the frozen private World G reference key and score each dimension independently:

- M1 factual reconstruction;
- M2 authority reconstruction;
- M3 current/superseded/scoped-status reconstruction;
- M4 unfinished obligations / negative constraints;
- M5 relational integration of authority × scope × status × purpose;
- M6 next-action fidelity;
- M7 confidence calibration;
- M8 clarification calibration.

Scale:
- 2 = fully correct / faithful;
- 1 = minor or safe degradation without material action error;
- 0 = material error.

## Pair-level endpoints

`ACTION_PASS`: M6 = 2.

`WEAK_MILTON_DEGRADATION` for a provider iff:
```text
CLEAR M6 = 2
MILTON M1=M2=M3=M4 = 2
MILTON M6 = 1
```

`QUALIFYING_MILTON_RESIDUAL` for a provider iff:
```text
CLEAR M6 = 2
MILTON M1=M2=M3=M4 = 2
MILTON M6 = 0
PRIMARY_CAUSE = M5 relational integration
MATERIAL_SOURCE_OMISSION = NO
```

Any MILTON failure with M1–M4 below 2 is classified first as fact/authority/state/obligation loss, not as the target relational residual.

Any matched CLEAR M6<2 makes that provider pair non-diagnostic for a Milton-specific causal effect.

## Cross-provider interpretation

- 0 qualifying provider pairs: no target effect in this H4 screen.
- 1 qualifying pair: candidate provider-specific susceptibility; replication required before repair testing.
- 2 qualifying pairs: replicated causal screen positive.

`WEAK_MILTON_DEGRADATION` is descriptive only and does not authorize Meta repair.

## Meta gate

Meta-Model-derived clarification is **not part of these four runs**.

It becomes eligible for a separately frozen repair protocol only after a `QUALIFYING_MILTON_RESIDUAL` is independently replicated. Do not improvise a repair after seeing one failure.

## If the screen ceilings

If all four M6 scores are 2, classify:
`H4_CAUSAL_SCREEN = BASELINE_CEILING`.

Do not rewrite H4 to force a failure. A future cumulative H1→H4 chain may be designed separately because repeated relational compression remains a different hypothesis.

## Raw evidence discipline

- genuinely fresh isolated context for every run;
- exact packet only;
- no external browsing;
- freeze untouched first response before scoring;
- never expose another run or adjudication;
- score only after raw freeze;
- no early protocol modification.

## Governance

```text
H4_CAUSAL_SCREEN = AUTHORIZED
META_REPAIR = NOT_AUTHORIZED
FULL_REPEATED_SUCCESSION_CHAIN = NOT_AUTHORIZED_BY_THIS PROTOCOL
CCP2 = NOT_AUTHORIZED
T7 = NOT_AUTHORIZED
R16 = NOT_AUTHORIZED
NEW_CCP_COMPONENT = NO
```
