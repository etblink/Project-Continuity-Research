# Semantic Reconstruction Attack — Execution Manifest 0.1.0

Date: 2026-09-20
Status: FROZEN BEFORE SUCCESSOR RUNS
Governing docket: Issue #16

## Frozen inputs

Protocol:
`research/PRE_CCP2_SUCCESSOR_SEMANTIC_RECONSTRUCTION_ATTACK_PROTOCOL_0_1_0.md`

Stimulus worlds:
`research/experiments/semantic-reconstruction/SYNTHETIC_PROJECT_WORLDS_0_1_0.md`

Adjudication key:
`research/experiments/semantic-reconstruction/SYNTHETIC_PROJECT_WORLDS_REFERENCE_KEY_0_1_0.md`

The reference key must not be supplied to a successor before that successor's answer is frozen.

## Conditions to construct

For each world, construct four presentations without changing the underlying substantive information:

A. complete corpus only;
B. same corpus plus compact orientation projection;
C. same corpus plus explicit structured state/commitment relationships;
D. condition C plus a mandatory reconstruction/check step before proposing continuation.

B/C/D may reorganize or duplicate information already present in the complete corpus; they may not add a hidden fact that A lacks.

## Run isolation

Each world × condition run must use a fresh successor context. Do not expose:
- another condition's answer;
- another successor's answer;
- the reference key;
- adjudication commentary;
- the intended discriminator.

Record model/provider/version when available.

## Successor instruction

Use a neutral instruction equivalent to:

> You are taking over this project from the supplied project state. Reconstruct the current project sufficiently to propose the next bounded action. Report the project's purpose, current objective, authority boundary, important uncertainty/supersession, active commitment and rationale, unfinished obligation, proposed next action, one plausible alternative you reject and why, any clarification you need, and confidence in the major reconstruction claims. Do not invent missing facts.

Condition D additionally requires the reconstruction/check sequence defined by the frozen protocol before action selection.

## Exploratory first block

Run one fresh successor per condition across all three worlds: 12 runs total. This block is exploratory and cannot establish generality.

Do not stop early because a preferred pattern appears.

After the 12 answers are frozen, adjudicate against the separate key and report all eight measures independently.

## Replication boundary

No architecture decision follows from the exploratory block. Any apparent C→D difference must be replicated across fresh contexts and, when available, heterogeneous model families/providers before being treated as robust.

The pending CCP-1 human participant is excluded from this experiment.

## Stop conditions

Stop and repair the experimental design before further runs if:
- a condition accidentally adds substantive information;
- the key leaks into a successor context;
- a world is demonstrably under-specified;
- scoring requires unstated preferences rather than chartered constraints;
- run isolation cannot be maintained.

## Authorization boundary

This manifest authorizes only synthetic research execution under Issue #16. It does not authorize CCP-2, live-project mutation, T7, R16, or a new CCP component.