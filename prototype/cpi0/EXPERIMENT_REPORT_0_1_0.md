# CPI-0 Stage-5 Frozen-Snapshot Semantic Simulation Report 0.1.0

Date: 2026-10-04  
Status: **FROZEN BOUNDED RESULT**

## 1. Objective

Test whether the reduced CPI semantic profile can represent and reject the failure modes frozen in Stages 1–4 without mutating any observed project and without adding infrastructure that could hide semantic defects.

The prototype is intentionally file-backed and local.

## 2. Tested semantic objects

Only four object families are implemented:

1. **Project Projection** — an immutable attestation about project-native state at an observation boundary.
2. **Project Event** — a typed statement that a material project event occurred.
3. **Import Disposition** — the receiving project's local adjudication of a remote object.
4. **Derivation Record** — provenance for an observer-generated or transformed result.

Supporting validation includes:

- purpose-scoped authority mapping;
- exact source identity;
- freshness comparison;
- typed dependency classes;
- negative knowledge with reopen semantics;
- typed transition states and consequence classes;
- fail-closed local canonicalization rules;
- duplicate-event and duplicate-source rejection;
- profile-version rejection;
- derivation auditability.

## 3. Frozen real-world conformance cases

The fixture suite encodes all eight Stage-2 conformance cases:

| Case | Requirement under attack | Result |
| --- | --- | --- |
| A — NFC source routing | Default branch must not override purpose-scoped theorem authority | PASS |
| B — Observatory stale snapshot | Frozen historical validity must coexist with current staleness | PASS |
| C — EBMM HOLD-001 | Hold must preserve reopen conditions and prohibitions | PASS |
| D — PGH external prerequisite | Physical prerequisite must not collapse into generic waiting | PASS |
| E — FCP layer separation | Historical result, prospective result, and routing state must remain distinct | PASS |
| F — HiVenues candidate + owner acceptance | PR candidate must not become canonical; owner acceptance remains a real dependency | PASS |
| G — PCR parallel workstreams | Multiple authorized bounded tracks must not force one global next action | PASS |
| H — false cross-domain bridge | Thematic similarity must remain an explicit non-dependency/held hypothesis | PASS |

## 4. Adversarial controls

Nine fail-closed controls were executed:

1. HARD dependency based only on thematic similarity — REJECTED.
2. Remote event declaring direct local canonical effect — REJECTED.
3. Evidence-only import attempting canonical mutation — REJECTED.
4. Locally accepted import lacking separate local transition identity — REJECTED.
5. Unsupported profile version — REJECTED.
6. Duplicate source identity — REJECTED.
7. Held negative knowledge without reopen semantics — REJECTED.
8. Duplicate event identity — REJECTED.
9. Derivation without auditable inputs/transformation identity — REJECTED.

## 5. Execution result

Command:

```text
python -m unittest -v
```

Result:

```text
Ran 17 tests
OK
```

Python compile validation also passed for the implementation and test modules.

## 6. First-run defect

The first 12-test run produced one failure in the HiVenues owner-acceptance case.

The failure was not a protocol-semantic failure. The fixture basis string said only:

```text
Issue 398 acceptance rule
```

while the test deliberately required the basis to preserve the fact that **owner** acceptance is controlling.

The fixture was corrected to:

```text
Issue 398 owner acceptance rule
```

The strengthened suite was then expanded to 17 tests and passed completely.

This correction is retained because it illustrates the profile's purpose: apparently harmless compression can delete decision-critical authority semantics.

## 7. What this result establishes

At this bounded scope:

```text
PROJECT_PROJECTION_SEMANTIC_FEASIBILITY = PASS
PROJECT_EVENT_SEMANTIC_FEASIBILITY = PASS
LOCAL_IMPORT_CANONICALITY_FIREWALL = PASS
DERIVATION_AUDITABILITY_MINIMUM = PASS
PURPOSE_SCOPED_AUTHORITY = PASS
NEGATIVE_KNOWLEDGE_MINIMUM = PASS
FRESHNESS_SEPARATION = PASS
DEPENDENCY_ANTI_INFERENCE_CONTROL = PASS
```

The four-object reduced profile is therefore **sufficient for the frozen semantic cases tested here**.

No fifth CPI-specific core object has yet been shown necessary.

## 8. What this result does not establish

This prototype does **not** establish:

- cryptographic authenticity of a remote producer;
- secure key distribution or PKI;
- live event delivery;
- completeness of an adapter's extraction from an arbitrary repository;
- resistance to a malicious adapter that intentionally omits negative knowledge;
- automatic semantic mapping for unfamiliar projects;
- multi-writer concurrency;
- large-scale performance;
- live Project Observatory integration;
- automatic local canonical mutation;
- generality beyond the frozen seven-project corpus;
- originality or novelty of the profile;
- a final public protocol.

The fixtures are hand-authored from the Stage-1 audit. This proves bounded semantic representability, not automatic extraction correctness.

## 9. Mutation boundary

```text
OBSERVED_EBMM_MUTATION = NONE
OBSERVED_FCP_MUTATION = NONE
OBSERVED_NFC_MUTATION = NONE
OBSERVED_PGH_MUTATION = NONE
OBSERVED_HIVENUES_MUTATION = NONE
PROJECT_OBSERVATORY_MUTATION = NONE
PROJECT_CONTINUITY_RESEARCH_BRANCH_MUTATION = YES
LIVE_CROSS_PROJECT_EFFECT = NONE
```

All prototype work is confined to the CPI-0 research branch of Project-Continuity-Research.

## 10. Stage-5 disposition

```text
CPI_STAGE5_FROZEN_SNAPSHOT_SEMANTIC_SIMULATION = PASS
REAL_CONFORMANCE_CASES = 8/8 PASS
ADVERSARIAL_CONTROLS = 9/9 PASS
TOTAL_TESTS = 17/17 PASS

CANDIDATE_E_REDUCED_PROFILE = SURVIVES_MINIMUM_SEMANTIC_SIMULATION
FINAL_PROTOCOL = NOT ESTABLISHED
LIVE_FEDERATION = NOT AUTHORIZED
AUTOMATIC_CROSS_PROJECT_WRITE = NOT AUTHORIZED
```

## 11. Next gate

A direct jump to live federation would be unjustified.

The next justified operation is a **read-only Observatory shadow adapter trial** in which the current Project Observatory behavior is reproduced from CPI projections/import semantics while retaining exact source traceability.

Before any live-project participation, that trial must specifically attack the largest remaining gap in this simulation:

> **adapter completeness and omission risk**

The critical question is whether a read-only adapter can generate a sufficiently complete CPI projection from native repositories without hidden conversation knowledge and without silently dropping negative knowledge, authority boundaries, or non-dependencies.

If it cannot, return to architecture/profile research rather than compensating with manual Observatory interpretation.
