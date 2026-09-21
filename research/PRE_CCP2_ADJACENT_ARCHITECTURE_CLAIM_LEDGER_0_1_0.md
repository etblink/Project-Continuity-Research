# Pre-CCP-2 Adjacent Architecture Claim / Nonclaim Ledger 0.1.0

Date: 2026-09-21
Status: **FORWARD-LOOKING RESEARCH — DOES NOT AUTHORIZE CCP-2 OR LIVE-PROJECT MUTATION**
Governing issue: #7

## Purpose

Before extending PCR/CCP, separate what adjacent 2026 systems actually claim from what PCR might be tempted to infer from them.

This ledger is deliberately conservative. `DIRECT CLAIM` means the cited source states the property. `PCR INTERPRETATION` is our crosswalk and is not attributed to the source.

## Sources in this pass

1. He & Yu, *Beyond Memory: A Transactional Continuity Kernel for Long-Lived AI Agents*, arXiv:2608.11632v1 (2026-08-12).
2. Li et al., *MemTX: Transactional Belief Commit for Stateful Agent Memory*, arXiv:2607.23929 (2026-07-27; later metadata shows v2).
3. Fernandez, *From Admission to Invariants: Measuring Deviation in Delegated Agent Systems*, arXiv:2604.17517v2 (2026-04).

All three are preprints / research artifacts; this pass does not treat their formal or empirical claims as independently replicated facts.

---

## A. Transactional Continuity Kernel (CK)

### Direct claims

CK frames persistent-agent continuity as an **authorized activation-lineage** problem rather than storage retention alone.

The abstract states that:

- persistent state does not by itself identify authoritative state;
- unmediated updates can produce stale overwrites, unaudited exposure, and self-authorizing privilege escalation;
- untrusted components propose typed changes against an exact predecessor head or typed absence;
- activation revalidates ownership, pre-state authority, freshness, and effect uniqueness;
- a transition receives one stable disposition: `Commit`, `Reject`, `Quarantine`, or `Defer`;
- only `Commit` advances the branch head and installs the accepted unit including state, authority, lineage, effects, outcome, and receipt;
- a bounded executable model is reported over 2,808,230 reachable states and 5,526,474 state-changing transitions with zero invariant violations.

### Nonclaims / boundaries important to PCR

The paper's continuity notion is infrastructural. Its mechanism can make state activation authorized and auditable without thereby proving that the accepted content is semantically true, that it faithfully represents project purpose, or that a fresh successor understands it correctly.

The bounded-model result verifies the modeled protocol/invariants. It must not be inflated into evidence that arbitrary real deployments, project semantics, or successor reasoning are correct.

### PCR interpretation

CK appears to be a strong candidate substrate or competitor for much of PCR's **authority / transition control plane**, especially R3, R4, R7, and parts of R8/R15.

It does not, from the claims reviewed here, discharge PCR's entire problem. In particular it does not by itself demonstrate R1 hierarchical intent, R9 executable negative knowledge, R10 verified correction, R13 human/project-purpose preservation, or R14 unfamiliar-successor reconstruction.

This is a scope distinction, not a criticism of CK.

---

## B. MemTX

### Direct claims

MemTX argues that **a memory write is not a belief commit**.

Its abstract states that:

- persistent shared memory can propagate one agent's write into another agent's premise and eventually into real side effects;
- each record carries evidence, permissions, provenance, and validity;
- writes are staged under snapshot isolation and admitted through a validate-and-commit pipeline;
- irreversible tool calls are gated on in-flight belief state;
- retracting a belief triggers typed cascading repair of derived records and tool side effects;
- action-safety gating and cascade-repair completeness are checked through property-based testing and bounded exhaustive enumeration;
- the authors report evaluation across five backbones from three model families, including zero downstream harm for MemTX in the reported benchmark.

### Nonclaims / boundaries important to PCR

The reported benchmark result is not evidence that every semantically wrong belief will be rejected, that project purpose survives succession, or that a cold-start successor can reconstruct the project's governing state.

Evidence/provenance/permission metadata improve governability; they do not automatically establish the truth of the evidence or the correctness of the policy admitting it.

### PCR interpretation

MemTX strongly overlaps R2/R4/R6/R7 and provides an especially relevant mechanism for **retraction and cascading repair**, which may be cleaner than bespoke PCR machinery for some future candidates.

It also pressures R5 scoped supersession: PCR should compare its claim-level supersession semantics against dependency-aware retraction rather than assume its own formulation is uniquely necessary.

MemTX does not, from this pass, eliminate the orientation, purpose, negative-knowledge, or heterogeneous-successor questions.

---

## C. Invariant Measurement Layer (IML)

### Direct claims

The paper argues that local enforcement can be structurally blind to global behavioral drift.

The source states that:

- a point-wise enforcement signal can continue to report no violations while behavior leaves the admission-time admissible behavior space;
- the claimed reason is a mismatch between local action evaluation and global trajectory-level properties;
- the paper presents a Non-Identifiability Theorem under its Local Observability Assumption;
- IML retains direct access to a generative model of the admission-time behavior space;
- the authors report tests across multiple drift scenarios plus n8n and LangGraph settings in which local enforcement triggered zero violations while IML detected the tested drift.

### Nonclaims / boundaries important to PCR

The result is formulated around deviation from an admission-time admissible behavior space. That is not automatically equivalent to preservation of a project's evolving meaning, evidence, authority, negative knowledge, or human purpose.

PCR must therefore not rename this result `semantic trajectory drift` and claim novelty. The relationship requires a discriminator.

### PCR interpretation

IML is strong prior/adjacent art for the proposition:

> local correctness does not imply trajectory fidelity.

The remaining PCR question is narrower and potentially different:

> can repeated succession preserve factual recall, epistemic state, authority, and locally valid transitions while progressively changing the operative meaning or purpose of an evolving project?

If that can be reduced to IML's admission-space deviation, PCR should collapse the terminology and reuse the established framing. If it cannot, the difference must be demonstrated empirically rather than asserted verbally.

---

# Preliminary requirement matrix

Legend:

- `D` = directly addressed by source claims reviewed in this pass
- `P` = partial / useful mechanism but requirement is broader
- `N` = not established by reviewed claims

| PCR requirement | CK | MemTX | IML | Current interpretation |
|---|---:|---:|---:|---|
| R1 hierarchical intent | N | N | P | IML can measure trajectory properties if represented, but none establishes PCR-style intent reconstruction. |
| R2 working vs durable state | P | D | N | MemTX explicitly stages persistent belief state; CK separates candidate evaluation from activation. |
| R3 history vs current authority | D | P | P | CK's accepted branch head is directly relevant; MemTX validity/retraction helps. |
| R4 provenance + authority | D | D | P | Strongest overlap area. |
| R5 scoped supersession | P | D/P | N | MemTX cascading repair is especially relevant; exact equivalence requires deeper dependency-semantics comparison. |
| R6 typed claim states | P | D/P | N | Both transactional systems distinguish candidate/accepted dispositions, but PCR's epistemic vocabulary is broader. |
| R7 guarded transitions | D | D | P | Major convergence. |
| R8 WAIT/HOLD/BLOCKED | P | P | N | CK `Defer` is adjacent but not automatically equivalent to PCR's justified no-action semantics. |
| R9 executable negative knowledge | N/P | P | N | Rejection/retraction is adjacent; PCR's `REOPEN_IF` closure semantics remain unestablished. |
| R10 reflection != correction | N | P | P | MemTX validation and IML external measurement are useful mechanisms, not full solution. |
| R11 safeguard exit conditions | P | P | P | Stable dispositions/detection rules help, but PCR requirement is broader. |
| R12 oversight/execution/context separation | P | P | D/P | All separate some governance function from execution; exact PCR role separation is not established. |
| R13 human agency/project purpose | N | N | P | IML can encode an admission behavior space, but evolving human/project purpose is not established. |
| R14 cold-start reconstruction | N | N | N | Major residual PCR research surface. |
| R15 kernel not sole truth source | P | P | P | All support separation of operational projection/control from deeper state/evidence in different ways. |

This table is provisional and must be revised after full-text claim-level reading. `D` never means "solves PCR universally"; it means the reviewed source directly addresses the core mechanism named in that requirement.

# Preliminary T1–T6 pressure matrix

Legend: `S` strong direct mitigation/mechanism; `P` partial/indirect; `—` not established.

| Failure class | CK | MemTX | IML | Note |
|---|---:|---:|---:|---|
| T1 Orientation Drift | — | — | P | None demonstrates fresh-successor orientation. |
| T2 Epistemic-State Drift | P | S | P | MemTX is strongest here because belief commit/validity/retraction are explicit. |
| T3 Authority Drift | S | S | P | CK is especially direct about pre-state authority and authorized heads. |
| T4 Transition Drift | S | S | P | Transactional admission/activation directly addresses invalid promotions. |
| T5 Negative-Knowledge Loss | P | P | — | Reject/retract helps, but durable closure + reopen conditions remain distinct. |
| T6 Metacognitive Drift | — | P | S/P | IML provides an independent trajectory measurement layer; neither proves semantic self-reframing. |

# What this changes

## 1. PCR should stop treating the control plane as an open greenfield

The 2026 literature already contains serious transactional state-governance mechanisms. Any later architecture competition should include CK-like and MemTX-like designs as baselines/candidates rather than inventing a proprietary control plane first.

## 2. PCR's plausible residual is moving upward

The less-occupied research surface appears to be:

- unfamiliar-successor reconstruction;
- authority-aware addressability;
- durable negative knowledge with explicit reopen conditions;
- preservation of hierarchical/evolving project intent;
- human/project-purpose fidelity;
- independence tests for semantic/trajectory failure despite correct local state mechanics.

This is a hypothesis, not an originality claim.

## 3. `semantic trajectory drift` is now burdened by prior art

The term stays provisional. Issue #5 should not run until its discriminator explicitly distinguishes PCR's proposed phenomenon from admission-time/global behavioral drift measurable by IML.

## 4. R5 deserves a stronger external attack

MemTX's cascading repair may subsume part of PCR's scoped-supersession motivation. A future comparison should construct the same dependency/retraction scenario under both semantics and look for cases where one preserves unaffected claims more correctly or with less machinery.

# Next operation

1. Deep-read CK and MemTX beyond abstracts and replace provisional `D/P/N` cells with claim citations/nonclaims.
2. Add ACP/RAM/Operationalizing-RAM to the ledger because the adjacent governance series now appears broader than the single IML paper.
3. Construct the R5 supersession-vs-cascade-repair comparison.
4. Tighten Issue #5's preregistration around an explicit IML non-equivalence test.
5. Do **not** authorize CCP-2 or implementation from this synthesis.
