# Adjacent-Fields Comparative Review 0.1.0

Date: 2026-09-20  
Status: First external comparison pass. No final architecture selected.

## Research question

Which parts of our six empirical failure classes already have mature analogues
in adjacent disciplines, and which parts remain poorly covered by existing
memory/agent designs?

Current empirical taxonomy:

1. Orientation Drift
2. Epistemic-State Drift
3. Authority Drift
4. Transition Drift
5. Negative-Knowledge Loss
6. Metacognitive Drift

---

# 1. Hierarchical planning and mission intent

## What already exists

HTN planning explicitly represents hierarchical task decomposition. The
options framework similarly formalizes temporally extended action at multiple
levels of abstraction.

Mission-command doctrine adds something planning formalisms often do not:
subordinate action is oriented by a concise statement of **purpose, key tasks,
and desired end state**, and higher-level intent nests across echelons.

Cognitive-control research also gives a useful non-software analogy: Koechlin
et al. report a cascade of executive control tied to immediate stimuli,
present context, and temporal episode rather than one flat control process.

Recent agent work independently converges on this split. COMPASS separates:

```text
TACTICAL EXECUTION
STRATEGIC OVERSIGHT
CONTEXT ORGANIZATION
```

into a Main Agent, Meta-Thinker, and Context Manager.

## What transfers well

- Mission / phase / task hierarchy should be explicit.
- Strategic intent should be compact enough to remain active during tactical
  work.
- High-level and low-level cognition do not need to occupy one undifferentiated
  context.
- Decomposition should preserve why a subtask exists, not only what it does.

## What does not transfer automatically

Classical HTN planning assumes an authored task hierarchy and domain model. It
does not solve:

- stale authority;
- uncertain evidence;
- conflicting artifacts;
- changing human purpose;
- successive model instances;
- historical supersession;
- whether a task should remain closed.

Mission command preserves purpose but relies on trained humans with shared
institutional understanding. Our problem must make enough of that orientation
explicit that a cold-start agent can recover it.

## Empirical taxonomy impact

**Orientation Drift is strongly corroborated as a real structural problem, not
just a prompting quirk.**

---

# 2. Event sourcing and materialized current state

## What already exists

Event sourcing separates:

```text
IMMUTABLE EVENT HISTORY
```

from:

```text
DERIVED CURRENT STATE / PROJECTION
```

Fowler emphasizes that state can be reconstructed from the event history.
Current Azure guidance further stresses intent-bearing events, immutable
history, compensating events, optimistic concurrency, and snapshots that are
derived optimizations rather than replacements for the event stream.

This maps strikingly well onto our historical-versus-current-state incidents.

## What transfers well

- Historical evidence should not be rewritten just because current
  interpretation changes.
- Current state should be a projection of authoritative history rather than an
  untraceable prose replacement.
- Corrections should often be additive/compensating rather than destructive.
- A snapshot is useful for orientation but is not the complete history.
- Concurrency/staleness is a first-class state problem.

## What does not transfer automatically

A project is not merely an event-sourced database.

Event sourcing records **what changed**. It does not by itself determine:

- whether a scientific claim is justified;
- which artifact has governance authority;
- whether one claim partially supersedes another;
- whether an agent is allowed to promote a result;
- why a route should remain closed;
- what human purpose the state is serving.

## Important implication

The future **Project Kernel should probably not be the event store**.

A stronger analogy is:

> **Kernel = compact materialized orientation view derived from deeper durable
> state/evidence/provenance structures.**

That is a significant refinement of our earlier thinking.

---

# 3. Provenance and distributed systems

## What already exists

W3C PROV cleanly distinguishes:

- entities;
- activities;
- agents;
- generation;
- use;
- derivation;
- attribution;
- association.

Lamport's work on event ordering shows another important distinction: in a
distributed system, ordering and causality cannot simply be inferred from
naive wall-clock sequence.

## What transfers well

- Facts need source identity.
- Derived artifacts should preserve lineage.
- Who/what generated or authorized an object matters.
- Temporal order should not be confused with causal or governing order.
- A later artifact is not automatically authoritative merely because it is
  later.

## Where our problem goes further

PROV answers questions like:

```text
Where did this come from?
What activity produced it?
Who was associated with it?
```

Our corpus additionally asks:

```text
Does this source govern this claim?
At what scope?
Is it current, frozen, historical, candidate, or superseded?
What exactly did it supersede?
May this evidence cause a state transition?
```

This suggests that **provenance and authority are related but not identical**.

## Empirical taxonomy impact

Authority Drift survives external comparison as a distinct category.

---

# 4. Statecharts and safety engineering

## What already exists

Statecharts extend flat state machines using hierarchy, concurrency, and
communication. They provide a mature formal intuition for nested states and
guarded transitions.

STPA is even closer to our transition/authority findings. It treats safety as
a control problem and examines unsafe control actions, including actions that
are:

- not provided when needed;
- provided when unsafe;
- provided at the wrong time/order;
- applied too long or stopped too soon.

## What transfers well

A project transition should be representable as:

```text
CURRENT_STATE
+ REQUESTED_ACTION
+ CONTEXT
+ GUARD / PRECONDITION
→ ALLOWED_NEXT_STATE
```

This matches many incidents better than prose memory does.

Examples:

```text
FUNCTIONAL_ACCEPTED
does not imply
ASTRA_AUTHORIZED

TARGET_SELECTED
does not imply
AUDIT_EXECUTION_AUTHORIZED

EVIDENCE_FOUND
does not imply
CANONICAL_PROMOTION
```

STPA also validates our intuition that **inaction can be unsafe and action can
be unsafe** depending on context. That is highly relevant to:

```text
CONTINUE CORRECTLY
WAIT CORRECTLY
STOP CORRECTLY
```

## What does not transfer automatically

Safety constraints usually protect against specified losses/hazards.

Our system also needs to reason about:

- epistemic overclaim;
- scope and authority;
- scientific underdetermination;
- value/purpose drift;
- beneficial but unauthorized action.

## Empirical taxonomy impact

Transition Drift is strongly supported as a control problem, not merely a
memory problem.

---

# 5. Organizational memory and routines

## What already exists

Walsh and Ungson treat organizational memory in terms of acquisition,
retention, and retrieval, while explicitly discussing use, misuse, and abuse.

Cohen and Bacdayan show that procedural routines can improve reliability and
speed while becoming suboptimal when automatically transferred to
inappropriate situations.

This is a close match for our finding that safeguards can themselves become
failure modes.

## What transfers well

- Memory quality depends on retrieval context, not just retention.
- Institutionalized routines can preserve continuity across individuals.
- A formerly useful procedure can become harmful when context changes.
- The organization/project can remember things no individual currently holds
  in working memory.

## Crucial extension from our corpus

Our negative knowledge is more operationally specific than ordinary
organizational memory:

```text
ROUTE = CLOSED
BASIS = ...
AUTHORITY = ...
REOPEN_IF = ...
```

This is not merely remembering a past rejection. It is remembering the
**decision boundary**.

## Empirical taxonomy impact

Negative-Knowledge Loss appears to be more than generic forgetting.

---

# 6. Cognitive science: working memory versus executive orientation

## What already exists

Baddeley's working-memory model treats short-term active cognition as
limited-capacity and includes a central-executive component.

Koechlin et al. provide evidence for hierarchical cognitive control tied to
different contextual levels.

These analogies reinforce a distinction we reached independently:

```text
MEMORY CAPACITY
!=
EXECUTIVE ORIENTATION
```

A system can possess the relevant information yet fail to keep the right
level of control active.

## Transfer caution

Human cognitive architecture is not a mechanistic explanation of transformers.
The value here is conceptual decomposition, not biological analogy.

## Empirical taxonomy impact

Our original intuition that "bigger context" is not equivalent to better
orientation receives cross-domain support.

---

# 7. LLM memory systems

## What current work is good at

Generative Agents, MemGPT, A-MEM, Mem0, and recent memory surveys address
important parts of persistent-agent memory:

- long-term storage;
- retrieval;
- reflection;
- compression;
- hierarchical memory;
- dynamic linking;
- consolidation;
- graph relations;
- forgetting;
- contradiction handling.

LongMemEval evaluates extraction, multi-session reasoning, temporal reasoning,
knowledge updates, and abstention.

These are real advances and directly address part of the continuity problem.

## Where the fit is incomplete

Most memory architectures are primarily organized around:

```text
WHAT SHOULD BE STORED?
WHAT SHOULD BE RETRIEVED?
HOW SHOULD MEMORY BE SUMMARIZED / LINKED?
```

Our corpus repeatedly requires additional questions:

```text
WHAT GOVERNS?
WHAT IS ONLY HISTORICAL?
WHAT STATE HAS BEEN EARNED?
WHAT TRANSITION IS AUTHORIZED?
WHAT MUST REMAIN CLOSED?
WHAT WOULD REOPEN IT?
WHAT PURPOSE MUST SURVIVE LOCAL OPTIMIZATION?
```

Those are not ordinary retrieval questions.

## Important distinction

A memory system can retrieve the correct historical fact and still fail if the
agent applies it with the wrong authority.

Therefore:

> **Retrieval correctness is necessary but not sufficient for continuity
> correctness.**

---

# 8. LLM planning and long-horizon context management

## Current convergence

Recent work is directly encountering the same broad problem.

COMPASS identifies long histories as a source of overlooked evidence and
irrelevant distraction and separates strategic oversight from execution and
context management.

A 2026 long-horizon survey, *The Horizon Gap*, explicitly distinguishes:

- long-horizon task requirements;
- long-context model capacity;
- long-term memory system persistence;

and highlights failures such as lost earlier decisions, premature completion,
and goal drift.

Recent context-rot work reports that accumulated context in long-horizon search
can induce premature uncertain answers or abandonment.

Agent Planning Benchmark separately evaluates planning and execution-oriented
capabilities, including infeasible-task handling and calibrated refusal.

## What this changes for our research

The premise of our project is **not unique**.

The broader agent field is independently converging on:

- context management;
- strategic/tactical separation;
- long-horizon planning diagnostics;
- explicit stopping/infeasibility;
- persistent memory;
- reflection.

That is good news: our observations are not merely idiosyncratic to one user's
workflow.

## What still appears distinctive

Our corpus is unusually rich in:

- exact canonical identity;
- partial supersession;
- scientific claim/evidence promotion;
- negative knowledge with reopen conditions;
- cross-session successor authority;
- frozen/historical/current distinctions;
- human agency as a governing constraint.

Those are not yet the center of most agent-memory systems.

---

# 9. Self-correction and metacognition

## Current evidence

Reflexion shows that stored verbal reflections can improve later attempts when
useful feedback exists.

But the self-correction literature is cautionary. ICLR 2024 work found that
intrinsic reasoning self-correction without external feedback can fail or even
degrade performance. A 2024 TACL critical survey concludes that reliable
external feedback is an important condition for successful self-correction in
many settings.

The newer REFLECT work takes a particularly relevant step: a suspected error
is not merely "reflected on"; it is patched and replayed, and the outcome
change becomes evidence about whether the diagnosis was correct.

## Strong convergence with our corpus

This maps closely to our distinction:

```text
FREE-FORM REFLECTION
```

versus:

```text
REORIENTATION SURFACE
+ EXTERNAL EVIDENCE
+ TESTED CORRECTION
```

Our failed self-correction cases therefore have strong external support.

## Empirical taxonomy impact

Metacognitive Drift remains distinct.

The problem is not absence of reflection. It is **unverified or wrong-level
reflection**.

---

# 10. What appears already solved versus still open

## Relatively mature building blocks

We should not reinvent:

- immutable historical logs;
- provenance graphs;
- hierarchical state machines;
- guarded transitions;
- hierarchical task decomposition;
- strategic intent / end-state statements;
- read/write projections and snapshots;
- external feedback loops;
- safety constraints and preconditions.

## Partly solved in current agent systems

- persistent memory;
- context compression;
- dynamic retrieval;
- episodic reflection;
- strategic/tactical role separation;
- long-horizon planning diagnostics.

## Still weakly covered as an integrated problem

The combination:

```text
PURPOSE
+ EVIDENCE
+ AUTHORITY
+ CURRENT STATE
+ SCOPED SUPERSESSION
+ GUARDED TRANSITIONS
+ NEGATIVE KNOWLEDGE
+ REORIENTATION
+ HUMAN AGENCY
+ SUCCESSION
```

does not appear in this review as one mature, portable architecture for
long-running human–AI projects.

That is the current candidate novelty boundary.

It must still be tested further before we claim originality.

---

# 11. Logos, Agape, and the unnamed authority/action dimension

## Logos

External fields strongly support the Logos side:

- provenance;
- evidence lineage;
- event history;
- state reconstruction;
- external verification;
- contradiction handling.

## Agape

Adjacent engineering disciplines preserve **purpose**, but they do not fully
capture our normative interpretation of Agape.

Mission command is useful because it preserves mission purpose while allowing
local initiative. Safety engineering protects valued outcomes. Neither is a
complete theory of human-centered service or human agency.

Therefore Agape remains more of a **design philosophy hypothesis** than an
engineering primitive.

## The third concern

External comparison strengthens the idea that another axis exists around:

```text
AUTHORITY
PERMISSION
ACTION
TIMING
STEWARDSHIP OF TRANSITIONS
```

Statecharts, STPA, provenance, and mission command all treat this as distinct
from merely knowing what is true.

We should still not name it philosophically yet.

---

# 12. Major conclusion

The research question has sharpened.

We are no longer primarily asking:

> How should an AI remember a long project?

We are asking:

> **How can a durable external control architecture keep successive intelligent
> agents correctly oriented to purpose, evidence, authority, state, and
> permissible action across arbitrarily long horizons?**

Memory is one subsystem of that problem.

It is not the whole problem.
