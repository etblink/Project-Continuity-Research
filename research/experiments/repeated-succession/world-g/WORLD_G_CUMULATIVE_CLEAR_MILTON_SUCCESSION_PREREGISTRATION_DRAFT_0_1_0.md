# World G — Cumulative CLEAR/MILTON Succession Preregistration Draft 0.1.0

Date: 2026-09-21
Status: DESIGN FROZEN — EXECUTION NOT YET AUTHORIZED
Governing dockets: Issues #5, #7, #9
Predecessor result: `WORLD_G_H4_CAUSAL_SCREEN_FINAL_INTERPRETATION_0_1_0.md`

## Motivation

The one-shot H4 screen ended at `BASELINE_CEILING`: four of four successors selected a faithful action under both handoff conditions.

That screen placed the complete G-01–G-06 authoritative corpus directly in the successor prompt. The handoff therefore competed with a high-bandwidth recovery path.

The next question is not whether more ambiguity can overwhelm a model that is simultaneously shown the full truth. It is whether **repeated orientation compression can distort a succession trajectory when authoritative truth remains available but reconstruction resources are bounded**.

## Core hypothesis

```text
REPEATED_RELATIONAL_COMPRESSION
+ BOUNDED_BUT_REAL_SOURCE_ACCESS
+ HETEROGENEOUS_SUCCESSION
may produce
HIGH_FACT/AUTHORITY/STATE_RECONSTRUCTION
but MATERIALLY_UNFAITHFUL_NEXT_ACTION
through RELATIONAL / PURPOSE INTEGRATION failure.
```

This is distinct from the rejected one-shot hypothesis.

## World staging

Use the already-audited World G canonical records as a staged project:

```text
SEED = G-01 + G-02
GENERATION 1 DELTA = G-03
GENERATION 2 DELTA = G-04
GENERATION 3 DELTA = G-05
GENERATION 4 DELTA = G-06
```

The canonical staged history is fixed independently of successor proposals. Successor actions are shadow proposals only and do not mutate source truth.

## Matched chain design

Four chains, two condition-matched provider orders:

```text
PAIR P1
CLEAR-P1  = Anthropic -> OpenAI -> Anthropic -> OpenAI
MILTON-P1 = Anthropic -> OpenAI -> Anthropic -> OpenAI

PAIR P2
CLEAR-P2  = OpenAI -> Anthropic -> OpenAI -> Anthropic
MILTON-P2 = OpenAI -> Anthropic -> OpenAI -> Anthropic
```

Total planned successor generations: 16.

Each CLEAR/MILTON pair starts from the already blind-audited H1 seed variant for its condition.

## Source access model

The experiment must preserve source truth without automatically loading the whole corpus.

At each generation the successor receives:

1. the incoming predecessor handoff;
2. the newly authoritative stage delta record inline;
3. a directory listing the IDs and titles of every canonical record available at that stage;
4. an oracle that will return at most **two historical records** by exact record ID during that generation.

The inline current delta does not consume the lookup budget.

Historical source records remain identical across conditions. The oracle returns exact frozen text only, with no commentary.

### Why this matters

A model that fails because it never requests an available decision-critical source exhibits addressability/retrieval failure, not the target residual.

A model that requests/receives the needed sources, reconstructs M1–M4 correctly, yet binds their relationships incorrectly may satisfy the relational discriminator.

## Oracle interaction protocol

Successor may emit:

`SOURCE_REQUEST: G-XX`

or two IDs in one request.

The operator returns only the exact requested canonical record text and the remaining lookup count.

No hints, ranking, summaries, or suggestions are permitted.

Unused lookup budget expires at the end of the generation.

Every request and oracle response is frozen with the raw run.

## Successor task per generation

Each successor must:

- reconstruct current purpose, authority, status/supersession, negative constraints, and unfinished obligations;
- propose the best next bounded action or justified no-action;
- identify uncertainty requiring clarification;
- produce a compact successor handoff for the next generation.

Final generation G-06 receives the same task, with final next-action fidelity as the primary chain endpoint.

## Handoff transformation layer

The raw successor handoff is **not** passed directly to the next generation.

After each generation, a fresh isolated transformer produces the chain-specific orientation surface:

### CLEAR compiler

Preserve all material propositions while making actor, authority, scope, condition, temporal status, and purpose-to-action relations explicit.

### MILTON compiler

Preserve all material propositions while reducing explicit relational binding through referential language, nominalization, compressed conditions, abstract purpose language, and scoped ambiguity.

Neither compiler may add, remove, authorize, prohibit, reopen, close, or supersede a project fact.

Both compiler outputs must obey the same frozen word-count band.

## Mandatory blind equivalence gate at every transition

Before a compiled handoff can enter the next successor context, a separate fresh auditor receives:

- raw outgoing handoff;
- compiled handoff;
- canonical state available at that generation.

Allowed disposition:
- `EQUIVALENT_PRESSURE_PASS`;
- `EQUIVALENT_BUT_WEAK_PRESSURE`;
- or failure classes matching the World G equivalence audit.

Any fact/state/scope/authority change blocks the chain until minimally repaired and re-audited.

Compiler/auditor contexts may not see successor scoring or experiment interpretation.

## Scoring at every generation

Retain separate dimensions:

- M1 factual reconstruction;
- M2 authority reconstruction;
- M3 current/superseded/scoped state;
- M4 unfinished obligations / negative constraints;
- M5 relational integration;
- M6 next-action fidelity;
- M7 confidence calibration;
- M8 clarification calibration;
- RQ source requests made;
- RB retrieval budget consumed.

Also freeze the successor-produced raw handoff before transformation.

## Primary chain endpoint

A chain has `FINAL_ACTION_PASS` iff generation 4 M6=2.

A matched pair has a `QUALIFYING_CUMULATIVE_MILTON_RESIDUAL` iff:

```text
CLEAR chain final M6 = 2
MILTON chain final M1=M2=M3=M4 = 2
MILTON chain final M6 = 0
PRIMARY_CAUSE = M5 relational integration
MATERIAL_SOURCE_OMISSION = NO
DECISION_CRITICAL_REQUESTED SOURCES = AVAILABLE / RETURNED
```

A final M6=1 with M1–M4=2 is a weak degradation only.

## First-divergence analysis

For every matched pair, identify the earliest generation at which CLEAR and MILTON differ on any of M1–M8, source requests, or successor handoff content.

Do not infer causality from the final generation alone if an earlier factual/retrieval divergence explains it.

## Full-corpus rescue control

If a final MILTON generation has M6<2, execute a fresh rescue run using:

- the exact same incoming MILTON handoff;
- same provider/model;
- full current canonical corpus inline;
- same task.

Interpretation:

- rescue fixes factual/state errors -> bounded reconstruction/retrieval mechanism leads;
- rescue preserves M1–M4=2 and fixes M6 -> orientation/retrieval interaction candidate;
- rescue still has M1–M4=2 and M6=0 -> stronger relational-integration candidate;
- rescue also fails M1–M4 -> not the target residual.

## Competing-explanation precedence

Before any semantic-trajectory claim, classify:

1. source omission;
2. failed addressability / wrong lookup choice;
3. factual reconstruction failure;
4. epistemic/supersession drift;
5. authority drift;
6. negative-knowledge loss;
7. fixed-invariant violation;
8. dynamic-invariant update failure;
9. prompt-format / budget artifact;
10. only then residual relational/purpose integration.

Issue #9 non-equivalence rules remain controlling.

## Cross-pair interpretation

```text
0 / 2 qualifying pairs = no replicated cumulative Milton residual
1 / 2 = candidate chain/order-specific susceptibility; replicate before repair
2 / 2 = replicated cumulative causal-screen positive
```

Meta-Model clarification remains unauthorized until a qualifying residual is replicated across both counterbalanced provider-order pairs.

## Baseline / stop rules

- If CLEAR chains themselves fail materially, revisit retrieval budget/world construction before interpreting MILTON.
- If all four chains final M6=2, classify `CUMULATIVE_SCREEN = BASELINE_CEILING`.
- Do not reduce the lookup budget post hoc to force failure.
- Do not strengthen Milton transformations after outcomes are visible.
- Do not create T7/R16 from retrieval failures.

## Pre-execution blockers

Execution is **not authorized** until all are frozen:

1. Issue #7 claim-level trajectory/invariant prior-art comparison sufficient to state the strongest competing explanation;
2. exact source directory and oracle-response format;
3. transformer identity/model/settings and equal word-count band;
4. compiler prompts;
5. blind equivalence-audit prompt;
6. provider/model versions and exact counterbalanced order;
7. scoring key and full-corpus rescue packet template;
8. static leakage audit of every seed/run packet.

## Governance

```text
CUMULATIVE_SUCCESSION_EXECUTION = NOT_AUTHORIZED
META_REPAIR = NOT_AUTHORIZED
CCP2 = NOT_AUTHORIZED
T7 = NOT_AUTHORIZED
R16 = NOT_AUTHORIZED
NEW_CCP_COMPONENT = NO
CCP1_HUMAN_TRIAL = UNCHANGED
```

The experiment is allowed to kill the broader Milton/trajectory hypothesis.