# Pre-CCP-2 Continuity Horizon Survey 0.1.0

Date: 2026-09-20
Status: **EXPLORATORY RESEARCH — DOES NOT AUTHORIZE CCP-2**
Branch: `research/pre-ccp2-continuity-horizon`

## Purpose

Ask what Project Continuity Research should investigate *if* CCP-1 survives its remaining exit gates, without assuming that it will and without implementing CCP-2.

The motivating problem is broader than memory capacity:

> What information and relations must survive a change of mind for a successor to continue the same project faithfully without merely imitating its predecessor?

Here, a "change of mind" includes succession between sessions, models, providers, humans, agents, or mixed human/agent teams.

## Boundary

This work is literature comparison, hypothesis formation, and future attack design only.

```text
CCP1_COMPLETE = NO
CCP2_AUTHORIZED = NO
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
HUMAN_COLD_START_TRIAL_1 = NOT_YET_RUN
```

Nothing in this survey changes the frozen human-trial target.

---

## First literature horizon

### 1. Grounding and common ground in communication

Clark & Brennan's grounding framework treats successful communication as collaborative work: participants establish sufficient common ground for the purpose at hand rather than assuming that sending information is equivalent to shared understanding.

PCR implication: a successor packet can be factually complete yet continuity can still fail if the successor has not established the distinctions needed to interpret those facts correctly. Continuity therefore may require a **grounding criterion**, not merely information availability.

Candidate attack:

- give two successors the same complete state;
- one receives explicit semantic distinctions/repair opportunities and the other only the records;
- test whether both reconstruct purpose, authority, uncertainty, and next permissible action consistently.

### 2. Transactive memory systems

Wegner's transactive-memory account treats group memory as individual memories plus communication about who knows or stores what.

PCR implication: durable continuity may not require putting everything in one kernel or one context. It may require preserving reliable **location knowledge**: what is known, where authoritative evidence resides, how it can be retrieved, and which source is competent for which question.

This suggests a distinction:

```text
CONTENT_MEMORY != LOCATION_MEMORY
```

Candidate attack:

- hold total information constant;
- vary whether the successor knows where authoritative state, evidence, negative knowledge, and historical rationale reside;
- measure orientation accuracy and retrieval cost.

### 3. Distributed cognition

Hutchins' distributed-cognition program moves the unit of analysis beyond a single person's internal cognition to coordinated systems of people, artifacts, representations, and environment.

PCR implication: the continuity-bearing object may not be an AI context or a human memory at all. It may be the **human + agents + repository + control artifacts + retrieval procedures** as a cognitive system.

That reframes context-window scarcity: the goal is not maximal internalization by one successor, but reliable reconstruction and action across a distributed state system.

Candidate attack:

- compare a monolithic successor packet against a deliberately distributed but navigable state system;
- test accuracy, time, provenance recovery, and resistance to stale-state errors.

### 4. Organizational memory

Organizational-memory research studies how information from an organization's history is acquired, retained, and retrieved for present decisions.

PCR implication: retention alone is insufficient. Retrieval conditions and interpretation matter, and durable project continuity should distinguish retained history from currently authoritative state.

This strongly aligns with existing PCR invariants such as:

```text
HISTORICAL_TRUTH != CURRENT_AUTHORITY
EVIDENCE != STATE
```

The research opportunity is to test whether PCR's supersession and orientation machinery actually improves retrieval of *decision-relevant* history rather than merely preserving it.

### 5. Long-horizon LLM context management

Recent long-horizon agent research explicitly reports context explosion, semantic drift, and degraded reasoning under append-only or passive-compression context strategies. Work such as CAT proposes separating stable task semantics, condensed long-term memory, and high-fidelity short-term interaction while making context maintenance an active operation.

PCR implication: the original incident-derived concern is independently recognizable in contemporary agent research, but PCR's target is broader. Context compression can improve an agent's working trajectory without by itself preserving authority, provenance, negative knowledge, or valid transition semantics.

Candidate comparison:

```text
CONTEXT MANAGEMENT
= what should be in the working context now?

PROJECT CONTINUITY
= what must remain recoverable and correctly interpreted across succession?
```

These overlap but should not be collapsed.

### 6. Agent drift and structured handoffs

Recent work describes semantic, coordination, and behavioral drift across extended multi-agent interactions, while other work reports benefits from structured, traceable handoffs between specialized agents.

PCR implication: succession itself should become an experimental object. A handoff is not successful merely because the next actor can continue producing plausible work. It should preserve reconstructible provenance, authority, unresolved uncertainty, and the ability to detect predecessor error.

Candidate attack:

- chain multiple heterogeneous successors;
- prohibit access to hidden conversation state;
- introduce one plausible but noncanonical predecessor conclusion;
- test whether the chain amplifies, repairs, or correctly quarantines it.

---

## Emerging conceptual decomposition

The literature suggests that "continuity" should provisionally be decomposed into at least five distinct capacities:

1. **Retention** — required information still exists somewhere.
2. **Addressability** — a successor can discover where relevant information resides.
3. **Grounding** — the successor reconstructs the distinctions needed to interpret it for the present task.
4. **Legitimacy** — the successor distinguishes evidence, historical fact, canonical state, and authority.
5. **Trajectory fidelity** — the successor's actions remain connected to project purpose and permissible next operations over repeated handoffs.

This yields a useful provisional inequality:

```text
RETENTION != CONTINUITY
RETRIEVAL != UNDERSTANDING
UNDERSTANDING != AUTHORITY
AUTHORITY != PURPOSE
LOCAL CORRECTNESS != TRAJECTORY FIDELITY
```

## A stronger definition of semantic trajectory drift

PCR should distinguish ordinary forgetting from a more dangerous condition:

> **Semantic trajectory drift**: a process in which locally plausible and individually defensible steps progressively alter the operative meaning, priorities, boundaries, or purpose of a project even though much or all of the underlying factual record remains available.

This matters because increasing a context window attacks missing information but does not necessarily attack incorrect salience, inherited interpretation, authority confusion, or cumulative goal deformation.

### Future measurement idea

Construct a frozen project with known purpose, evidence, negative knowledge, authority, and unresolved questions. Pass it through N heterogeneous successors. At each handoff score separately:

- factual retention;
- purpose reconstruction;
- authority reconstruction;
- uncertainty calibration;
- negative-knowledge preservation;
- next-action legitimacy;
- divergence from the original governing intent.

Do not combine these into one score until empirical covariance is understood.

---

## Kernel sufficiency as a research problem

Existing PCR work correctly treats the Project Kernel as a lossy orientation projection rather than the sole source of truth. The next question is not "how do we put everything in the kernel?" It is:

> What is the minimum orientation state that lets a successor reliably find, interpret, and validate everything else it needs?

A candidate sufficiency contract might require the kernel to make recoverable:

```text
PURPOSE
CURRENT PHASE
CURRENT AUTHORITY BOUNDARY
CANONICAL STATE POINTERS
OPEN UNCERTAINTY
NEGATIVE KNOWLEDGE POINTERS
NEXT-ACTION / WAIT CONDITION
PROVENANCE ROUTES
SUPERSESSION RULES
```

This is a hypothesis, not a specification.

### Compression frontier hypothesis

There may be a measurable frontier between:

- too little orientation state -> successor cannot discover/interpret the project;
- too much orientation state -> context cost, stale duplication, and salience competition degrade performance.

Rather than optimize for the smallest kernel, optimize for the smallest kernel that satisfies a predefined reconstruction task under bounded time/context.

---

## Continuity across different minds

The upcoming human trial and the blind-agent trial motivate a stronger architecture-neutral principle:

```text
A CONTINUITY SYSTEM SHOULD NOT REQUIRE
THE SUCCESSOR TO THINK LIKE THE PREDECESSOR.
```

A robust protocol should tolerate differences in:

- model family/provider;
- context capacity;
- reasoning style;
- domain expertise;
- human versus machine cognition;
- tool access;
- vocabulary.

The invariant target should therefore be externally inspectable relations among claims, evidence, state, authority, constraints, and transitions—not reproduction of a predecessor's internal reasoning trace.

This suggests treating project succession as a **protocol between epistemically heterogeneous participants**.

---

## Logos / agape as exploratory prompts

The terms `logos` and `agape` are not adopted as technical architecture terms here. They are retained only as prompts for a possible missing distinction.

A secular, testable translation is:

- **epistemic fidelity**: preserve what the project has reason to regard as true, false, uncertain, superseded, or unsupported;
- **teleological / value fidelity**: preserve what the project is for, whom it serves, what boundaries constrain it, and which goals must not be silently optimized away.

Existing PCR work is comparatively strong on epistemic and authority state. A future audit should ask whether **purpose/value constraints are represented with comparable rigor**, or whether they currently survive mainly as prose and tacit human interpretation.

This is especially important because an agent can remain factually accurate while optimizing the wrong objective.

Candidate attack:

- construct two actions equally consistent with factual state;
- make one violate an explicit project purpose or human-agency constraint;
- test whether the continuity representation distinguishes them without relying on hidden conversational intent.

---

## Initial research hypotheses

H1. Larger context windows reduce some omission failures but do not by themselves solve semantic trajectory drift.

H2. Successor orientation depends on location/addressability memory as well as content retention.

H3. Project continuity is better modeled as a distributed cognitive/provenance system than as a single-agent memory subsystem.

H4. Kernel quality should be measured by reconstruction sufficiency under bounded resources, not by completeness or compression ratio alone.

H5. Cross-mind continuity requires externally inspectable semantic and authority relations rather than preservation of predecessor reasoning style.

H6. Purpose/value fidelity is a distinct continuity dimension that can fail while factual and epistemic fidelity remain intact.

H7. Repeated handoffs can reveal cumulative trajectory failures that single cold-start trials cannot detect.

---

## Proposed future experiment families

These are preregistration candidates only; none are authorized by this document.

### HF-1 — Repeated heterogeneous handoff

Measure degradation across a chain of different successor types.

### KF-1 — Kernel ablation / compression frontier

Systematically remove or compress orientation fields and measure reconstruction failure.

### LM-1 — Location-memory ablation

Preserve all underlying documents but vary the successor's ability to discover authoritative locations.

### GF-1 — Grounding repair

Compare static handoff against a protocol that permits explicit clarification/grounding while preserving an audit trail.

### PF-1 — Purpose-fidelity conflict

Present factually valid candidate actions that differ in consistency with frozen project purpose and human-agency constraints.

### CF-1 — Context-size control

Hold project semantics constant while varying available context size and retrieval architecture, separating raw capacity effects from continuity-architecture effects.

---

## What would change our mind

This line of research should be weakened or abandoned if controlled tests show that:

- ordinary long-context retrieval reliably eliminates the observed continuity failures;
- kernel sufficiency does not predict successor performance beyond simple document availability;
- heterogeneous handoffs perform no worse than same-model continuation after controlling for information access;
- purpose fidelity is empirically reducible to existing authority/policy semantics with no independent failure cases;
- an established adjacent-field architecture already provides the full required semantics more simply.

## Next research step

Before implementing any experiment above:

1. deepen the literature survey with primary sources and competing terminology;
2. map each proposed concept against the existing six-class incident taxonomy and 15 post-literature requirements;
3. identify which hypotheses are genuinely new versus rediscoveries or renamings;
4. preregister the smallest discriminating experiment only after that comparison.

That sequence protects the project from turning an interesting vocabulary into architecture by suggestion alone.

## Sources consulted in first pass

- Clark, H. H. & Brennan, S. E. (1991), *Grounding in Communication*.
- Wegner, D. M. (1987), *Transactive Memory: A Contemporary Analysis of the Group Mind*.
- Hutchins, E. (1995), *Cognition in the Wild*.
- Walsh, J. P. & Ungson, G. R. (1991), *Organizational Memory*.
- Liu et al. (2025), *Context as a Tool: Context Management for Long-Horizon SWE-Agents*.
- Rath (2026), *Agent Drift: Quantifying Behavioral Degradation in Multi-Agent LLM Systems Over Extended Interactions*.
- Barrak (2025), *Traceability and Accountability in Role-Specialized Multi-Agent LLM Pipelines*.

Source claims should be checked against primary publications before any later formal literature freeze.