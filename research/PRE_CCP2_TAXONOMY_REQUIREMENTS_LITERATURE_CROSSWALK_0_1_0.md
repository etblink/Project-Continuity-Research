# Pre-CCP-2 Taxonomy × Requirements × Literature Crosswalk 0.1.0

Date: 2026-09-20
Status: **EXPLORATORY SYNTHESIS — DOES NOT AUTHORIZE CCP-2 OR EXPERIMENT EXECUTION**
Governing issue: #4

## Question

Do the horizon concepts introduced in `PRE_CCP2_CONTINUITY_HORIZON_SURVEY_0_1_0.md` expose independent continuity requirements, or do they mostly refine the existing six-class empirical taxonomy and fifteen post-literature requirements?

Classification vocabulary:

- **ALREADY COVERED** — no new requirement warranted.
- **REFINEMENT** — sharpens measurement or semantics of an existing requirement/class.
- **NEW CANDIDATE** — plausible independent gap, but requires a discriminating failure before admission.
- **REJECT** — adds vocabulary without explanatory or experimental value.

## Existing empirical basis

Taxonomy: T1 Orientation Drift; T2 Epistemic-State Drift; T3 Authority Drift; T4 Transition Drift; T5 Negative-Knowledge Loss; T6 Metacognitive Drift.

Requirements: R1–R15 in `POST_LITERATURE_REQUIREMENTS_0_1_0.md`.

## Crosswalk

| Horizon concept | Existing taxonomy pressure | Existing requirements | Literature analogue | Classification | Consequence |
|---|---|---|---|---|---|
| Retention | T1/T2/T5 depending what is lost | R2, R3, R9, R14 | organizational memory; persistent agent memory | ALREADY COVERED | Do not add a retention requirement. Treat as a necessary substrate and measurement dimension. |
| Addressability / location memory | T1 primarily; can induce T3 if wrong source is retrieved | R2, R4, R14, R15 | transactive memory directories; organizational knowledge directories | REFINEMENT | Existing requirements say information must be retrievable/reconstructible, but do not isolate *knowing where authoritative knowledge resides* as a measurable variable. Add no architecture field yet; test by ablation. |
| Grounding / common ground | T1, T2, T3; sometimes T6 | R1, R4, R6, R14 | grounding in communication; shared/task mental models | REFINEMENT | Treat grounding as a success criterion for reconstruction, not a new stored object. A successor can possess records without sharing the distinctions required to interpret them. |
| Legitimacy | T3/T4 directly | R3–R8, R14 | provenance, authorization/control, event/state systems | ALREADY COVERED | The new label is redundant. PCR already has stronger authority and guarded-transition semantics. Retain only as informal umbrella if useful. |
| Trajectory fidelity | T1/T4/T5/T6 across repeated transitions | R1, R7–R13 | mission/intent preservation; long-horizon drift work | NEW CANDIDATE AS DYNAMIC PROPERTY | Do not create R16. First show cumulative failure under repeated handoffs while factual/authority reconstruction remains high. If not separable, collapse into existing classes. |
| Epistemic fidelity | T2 | R3, R4, R6, R10, R14 | provenance and epistemic-state/update work | ALREADY COVERED | No new requirement. Existing PCR semantics are more precise. |
| Purpose/value fidelity | T1 plus Agape cross-cutting axis | R1, R12, R13, R14 | mission intent; goal/constraint preservation | REFINEMENT / POSSIBLE INDEPENDENT MEASURE | R13 already states the normative requirement. What is missing is evidence that purpose can fail independently of factual/authority fidelity. Test before elaborating architecture. |
| Semantic trajectory drift | potentially cross-cutting T1–T6 | no single R; especially R1, R7, R9–R14 | long-horizon agent drift/context degradation | NEW CANDIDATE AS FAILURE DYNAMIC, NOT TAXONOMY CLASS | Reserve term for cumulative semantic divergence across locally plausible steps. It earns status only if controlled repeated-handoff tests distinguish it from omission/context loss. |
| Kernel sufficiency | T1/T3/T5 and stale-kernel risk | R14, R15 plus R1/R2/R4/R9 | materialized views/snapshots; transactive directories; bounded context management | REFINEMENT | Replace vague completeness intuition with reconstruction sufficiency under bounded resources. No kernel expansion is authorized. |
| Compression frontier | T1 and context-swamp positive/negative controls | R1, R2, R11, R14, R15 | context compression and bounded-memory systems | NEW CANDIDATE AS EMPIRICAL OPTIMIZATION QUESTION | Not an architecture requirement. Measure whether both undercompression and overcompression can degrade reconstruction. |
| Heterogeneous-mind invariance | all classes can surface at handoff | R14 strongly; R4/R7/R13 secondarily | distributed cognition; transactive memory; human-machine teams | REFINEMENT / GENERALIZATION TEST | R14 should be tested across successor types rather than assumed from one model. No requirement change yet. |
| Distributed continuity-bearing system | T1/T3/T5 | R2–R5, R9, R12, R14, R15 | distributed cognition; organizational/transactive memory | ALREADY IMPLICIT, USEFUL MODEL | Useful unit of analysis, but not evidence for a new component. PCR already distributes truth across durable artifacts rather than model context. |

## Requirement-by-requirement pressure check

### R1 Preserve hierarchical intent
Strengthened by grounding and trajectory-fidelity framing. No semantic change required.

### R2 Separate working context from durable memory
Strongly supported by current long-horizon memory work. Addressability suggests measuring retrieval topology separately from storage quantity.

### R3 Preserve history without making history current authority
Recent source-grounded trajectory approaches reinforce the value of immutable/evolving histories, but do not eliminate PCR's authority distinction.

### R4 Bind claims to provenance and authority
Remains central. Addressability adds the practical question of whether a successor can locate the authoritative source, not merely whether provenance exists.

### R5 Make supersession scoped
No horizon concept independently changes this requirement. Recent trajectory/deprecation approaches are adjacent corroboration.

### R6 Typed claim states
Epistemic fidelity is already represented here. No expansion justified.

### R7 Explicit guarded transitions
Trajectory fidelity may eventually require repeated-transition evaluation, but not a new transition primitive.

### R8 WAIT/HOLD/BLOCKED
Purpose and trajectory tests must include justified non-action so that continued activity is not mistaken for continuity.

### R9 Executable negative knowledge
Repeated handoffs provide a stronger stress test: reopen conditions should survive succession without becoming inert prose.

### R10 Reflection != verified correction
Grounding repair must not allow conversational agreement to silently become canonical correction.

### R11 Safeguard exit conditions
Compression/reconstruction experiments must be bounded; otherwise orientation quality can be confounded with unlimited search.

### R12 Separate oversight/execution/context management
Distributed-cognition literature makes this separation conceptually plausible, but the empirical corpus remains the actual basis for the requirement.

### R13 Preserve human agency and project purpose
This is the main home for the `agape` intuition. No R16 should be created unless a purpose-fidelity failure survives controls showing correct facts, authority, and transition mechanics.

### R14 Reconstructible durable orientation
This becomes the principal experimental surface for addressability, grounding, heterogeneous successors, and kernel sufficiency.

### R15 Kernel not sole source of truth
The horizon survey strengthens rather than changes it. A compact orientation artifact should be evaluated by its ability to route reconstruction to deeper evidence.

## Literature comparison — important non-equivalences

### Transactive memory
Transactive-memory work makes location/expertise directories first-class: effective collective memory includes knowledge of *who/where knows what*. PCR's likely contribution is not this idea itself. The research opportunity is to test whether authority-aware project continuity requires a specialized version: not merely `WHERE IS INFORMATION?`, but `WHERE IS THE CURRENTLY AUTHORITATIVE EVIDENCE FOR THIS CLAIM/SCOPE?`.

### Grounding/common ground
Grounding theory warns against equating message delivery with mutual understanding. PCR should not convert this into a `GROUNDING` database field. Instead, successor tests should score whether key distinctions were actually reconstructed.

### Distributed cognition / organizational memory
These perspectives weaken any model in which continuity lives inside one LLM. They support treating repository, humans, agents, indexes, provenance and procedures as a coupled system. This is conceptual support for R2/R12/R14/R15, not proof of PCR architecture.

### Long-horizon agent memory
Recent work increasingly separates persistent memory, temporal evolution, execution state, and retrieval. This narrows PCR's plausible novelty: generic persistence, hierarchy, summarization, and temporal memory cannot be claimed as distinctive. PCR should focus its tests on authority, scoped supersession, negative knowledge, guarded state promotion, and purpose-preserving succession where existing memory benchmarks may be weak.

### Recent continuity/control-plane convergence
A 2026 preprint titled *Beyond Memory: A Transactional Continuity Kernel for Long-Lived AI Agents* independently frames continuity around authorized lineage, freshness, atomic activation, and non-self-authorizing updates. This is unusually close to CCP-1's authority/concurrency direction. It must be treated as a serious adjacent architecture, not merely corroboration. Before any originality claim or CCP-2 design, perform a dedicated comparison for overlap, differences, priority, and whether PCR machinery can be simplified or replaced.

## Main synthesis

The five-part horizon decomposition should **not** become five architecture modules.

Current disposition:

```text
RETENTION          = ALREADY COVERED
ADDRESSABILITY     = REFINEMENT / ABLATION VARIABLE
GROUNDING          = REFINEMENT / OUTCOME CRITERION
LEGITIMACY         = ALREADY COVERED, LABEL REDUNDANT
TRAJECTORY FIDELITY= NEW CANDIDATE DYNAMIC PROPERTY
```

Likewise:

```text
EPISTEMIC FIDELITY = ALREADY COVERED
PURPOSE FIDELITY   = R13 REFINEMENT + INDEPENDENCE TEST
SEMANTIC TRAJECTORY DRIFT = CANDIDATE CROSS-CUTTING DYNAMIC
KERNEL SUFFICIENCY = R14/R15 REFINEMENT
COMPRESSION FRONTIER = EMPIRICAL QUESTION, NOT REQUIREMENT
```

## Highest-value discriminators

1. **Repeated-handoff independence test** — can purpose/trajectory fail while factual recall, epistemic state, and authority remain correct?
2. **Addressability ablation** — with identical complete corpus, does removing reliable source-location knowledge impair correct reconstruction beyond raw retrieval cost?
3. **Kernel sufficiency ablation** — which orientation functions cause decision-critical reconstruction failure when removed?
4. **Adjacent-architecture comparison** — compare CCP semantics directly against the 2026 Transactional Continuity Kernel and other state-management systems before extending PCR.

## Anti-proliferation decision

No new requirement is admitted by this crosswalk.

No seventh taxonomy class is admitted.

No new CCP component is admitted.

The horizon work has produced **measurement refinements and two candidate dynamic phenomena**, not an architecture expansion.

## Next operation

Before authorizing Issues #5 or #6 to run:

1. perform a focused adjacent-architecture comparison, especially the independently published Transactional Continuity Kernel;
2. tighten the repeated-handoff discriminator so `trajectory fidelity` cannot pass merely by restating R1/R13;
3. define bounded reconstruction outcomes for addressability/kernel ablations;
4. preregister evaluator independence and anti-circularity controls.

CCP-1 and the frozen human cold-start remain untouched.