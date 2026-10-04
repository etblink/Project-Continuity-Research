# CPI-0 Stage-6A Observatory Shadow Adapter Trial Preregistration 0.1.0

Date: 2026-10-04
Status: FROZEN BEFORE ADAPTER IMPLEMENTATION
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #19
Parent result: prototype/cpi0/EXPERIMENT_REPORT_0_1_0.md

## 1. Objective

Attack the largest unresolved Stage-5 limitation:

> Can a read-only adapter produce a sufficiently complete CPI projection from project-native sources without hidden conversation knowledge and without silently dropping decision-critical authority, negative knowledge, freshness, or non-canonical status?

This is a bounded **source-contract** trial, not a claim that arbitrary repositories can be automatically understood.

## 2. Trial scope

Use the four projects already observed by Project Observatory:

1. Nested Fibrational Cosmology (NFC)
2. Foundational Convergence Program (FCP)
3. Physical Grammar Hypothesis (PGH)
4. HiVenues

Project Observatory itself is the shadow consumer/comparator, not an observed-project mutation target.

## 3. Input identities frozen before implementation

### NFC

Repository:
`etblink/Nested-Fibrational-Cosmology`

Observed main:
`5072d563b0a3dd4a7643be427cd47108216d8793`

Required source:
`PROVENANCE.md`

Blob:
`69cdd64069cd0d24779a344fac0cd309bc54d811`

Theorem-bearing authority expected from native text:

`archive/nfc-canonical-ed3047c2@ed3047c2cbc0abc34d2549dd27754e4d3d05af78`

### FCP

Repository:
`etblink/Foundational-Convergence-Program`

Observed main:
`a41bc6101b63140ee2687e0cf67a47ab6be77215`

Required sources:

- `CURRENT_STATE.md` blob `b5949af93a1855ae1d072fa4aaa4b1c29033579c`
- `FCP_CHARTER.md` blob `579819121d1733e1746868941a3a282de2cf1ac9`

### PGH

Repository:
`etblink/Physical-Grammar-Hypothesis`

Observed main:
`2923875b40ea6901dfafda56a771c36876c4a220`

Required source:
`CURRENT_STATE.md`

Blob:
`32c799bdd42d6c921140bf13bdb988fefa445169`

### HiVenues

Repository:
`etblink/HiVenues`

Observed main:
`4fed1b4bcd65606124579fe8a643e55828655093`

Required repository source:
`README.md`

Blob:
`ad9a0c0b64d0e074e0a315450713ddfb3d9c8f6a`

Required bounded-work sources:

- Issue #398: open; updated `2026-10-04T15:30:48Z`
- PR #397: open / not merged
- PR #397 base `4fed1b4bcd65606124579fe8a643e55828655093`
- PR #397 head `e469282b39d533f1803dcd47b61663dbf05043de`

## 4. Source-contract rule

Each project adapter must declare:

- exact required source identities;
- which semantic facts are expected from each source role;
- extraction/validation rule identity;
- a completeness result.

If a required source is missing, has the wrong identity, or lacks a preregistered required semantic marker, the adapter must return:

`INCOMPLETE`

It must not synthesize the missing fact from conversation memory, a neighboring project, or a plausible default.

## 5. Preregistered must-preserve assertions

### NFC — N1 through N4

N1. Publication `main` is not theorem-bearing authority.

N2. The frozen theorem authority resolves to:
`archive/nfc-canonical-ed3047c2@ed3047c2cbc0abc34d2549dd27754e4d3d05af78`.

N3. Authority is purpose-scoped: publication/provenance and theorem analysis are distinct purposes.

N4. `HUMAN_POLICY_INTENT = UNRESOLVED` is preserved as negative/uncertain knowledge rather than guessed.

### FCP — F1 through F6

F1. `HISTORICAL_RESULT`, `CURRENT_PROSPECTIVE_RESULT`, and `CURRENT_ROUTING_STATE` remain distinct roles.

F2. Method identity `0.2.1_ACTIVE_PROSPECTIVELY` is preserved.

F3. Every substantive future phase requires separate bounded authorization and explicit source/provenance window.

F4. Current routing may name a next recommended operation while the next scientific phase remains unselected/pending separate authorization.

F5. The adapter must not reinterpret a historical occurrence of `EVIDENCE_TRIGGERED_HOLD` as the current universal routing state merely because that phrase exists in the file.

F6. `FCP27_SELECTED = NO` remains distinguishable from ordinary task readiness.

### PGH — P1 through P7

P1. Active candidate package is `PGH-OBJ-0052`.

P2. Actual apparatus remains unbound.

P3. The next scientific operation is `APPARATUS_REALIZATION_AND_TARGET_FREEZE`.

P4. That operation requires external physical action.

P5. Physical trials are not authorized.

P6. Web/registry target search remains forbidden without a new independent trigger.

P7. The machine-readable `do_not_assume` list is transported as negative knowledge.

### HiVenues — H1 through H7

H1. Current merged main and PR #397 candidate head remain distinct identities.

H2. PR #397 is not merged and must not be presented as canonical main.

H3. Issue #398 is the active bounded redesign charter.

H4. Owner acceptance governs the usability gate; machine qualification is not substituted for it.

H5. Repository doctrine/roadmap/issue/test authority roles remain distinct.

H6. The adapter must identify that the issue/PR state is newer bounded-work context layered over merged main, not proof that main already contains the redesign.

H7. No live external effect is authorized merely by this shadow reconstruction.

## 6. Shadow comparison assertions

The trial must additionally compare against frozen Project Observatory Snapshot v0.2.

Snapshot source:

`snapshots/PROJECT_OBSERVATORY_SNAPSHOT_V0_2.md`

Blob:
`e62a0b86e2317d7b441eb3d5ecf8ee71cc49460a`

Required comparison:

- preserve v0.2 as valid historical observer state;
- detect that its HiVenues observed commit `bf9a0b4e...` is stale relative to current `4fed1b4b...`;
- do not rewrite v0.2;
- do not treat current divergence as proof that the historical snapshot was false.

## 7. Adversarial source-removal controls

At minimum execute:

A. Remove NFC PROVENANCE source -> adapter must return INCOMPLETE rather than use main as theorem authority.

B. Remove FCP charter -> adapter must refuse to claim future-phase authorization semantics are complete.

C. Remove PGH current-state capsule -> adapter must refuse to reconstruct the do-not-assume set.

D. Remove HiVenues Issue #398 -> adapter must refuse to claim usability acceptance authority is known.

E. Mark PR #397 merged=true without changing canonical main input -> adapter must flag an inconsistent source packet.

F. Replace Observatory historical commit with current HiVenues commit while keeping snapshot identity unchanged -> adapter must flag snapshot tampering/inconsistency.

## 8. Implementation boundary

Allowed:

- file-backed fixture/source packets;
- deterministic parsers;
- explicit per-project source contracts;
- CPI projection generation;
- diagnostic completeness reports;
- comparison against frozen Observatory snapshot.

Not allowed:

- observed-project writes;
- Project Observatory writes;
- live cross-project imports;
- LLM inference inside the adapter;
- conversation-memory fallback;
- network mutation;
- automatic GitHub actions;
- graph database/message broker/PKI.

## 9. Acceptance gate

PASS requires:

1. all 24 must-preserve assertions N1-N4, F1-F6, P1-P7, H1-H7 pass;
2. all six source-removal/inconsistency controls fail closed;
3. stale-but-valid Observatory comparison passes;
4. every generated projection records its adapter/source-contract version;
5. no observed project is mutated;
6. no missing semantic fact is filled from a default or conversation context.

Any false PASS is a Stage-6A failure.

## 10. Interpretation boundary

A PASS would establish only:

> Explicit, auditable, project-specific read-only source contracts can generate CPI projections for these four projects while failing closed on preregistered omission/inconsistency attacks.

It would **not** establish:

- universal automatic repository understanding;
- elimination of project-specific adapters;
- cryptographic authenticity;
- safe live federation;
- write authority;
- protocol finality.

## 11. Stop condition

If completeness depends on hidden ad hoc logic that cannot be stated in the source contract, or if source removal causes plausible-but-wrong projections rather than INCOMPLETE, return to profile/adapter architecture research.

Truth over integration.
