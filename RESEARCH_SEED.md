# Project Kernel Research Seed

## 1. Origin

The discussion began from two recurring observations about long-term LLM use:

1. LLM behavior is highly sensitive to semantics, framing, suggestion,
   presupposition, context, and inferred intent.
2. During long projects, an LLM can become highly competent at a local task
   while losing orientation to the larger roadmap or purpose.

A useful working distinction emerged:

- **Intelligence**: the ability to reason about the task currently in view.
- **Executive continuity**: the ability to preserve hierarchy, purpose,
  authority, and direction across long periods of work.

The second capability is much weaker than the first unless it is externally
supported.

## 2. Framing / NLP analogy

Hypnosis and NLP were discussed as useful structural analogies, not literal
mechanistic descriptions of transformer inference.

The useful overlap is:

- framing;
- salience;
- presupposition;
- attentional direction;
- semantic association;
- re-anchoring;
- chunking up and down.

A prompt changes which interpretations and actions become salient. However,
LLMs are not literally hypnotized, do not simply mirror a user's subjective
reality, and retain substantial prior structure from training, higher-priority
instructions, tools, and evidence.

## 3. Context failure is more than context length

The recurring problem was characterized as a hierarchy/orientation failure.

A project can begin with:

    Mission
      -> Era / Phase
        -> Milestone
          -> Operation
            -> Working detail

After many turns at the bottom of the hierarchy, the working detail can become
the semantic center of the conversation.

This creates a pattern in which a model may become:

> locally brilliant and globally misoriented.

A larger context window does not necessarily solve this. A large unstructured
context can simply become a larger swamp.

The more important resource may be **salience**, not raw context capacity.

## 4. Memory versus orientation

A key distinction:

- **Memory** asks: what information is retained?
- **Orientation** asks: what matters now, why does it matter, what is
  authoritative, and where should deeper information be retrieved?

The goal should therefore not be to maximize everything an agent remembers.

The goal should be:

> Optimize the agent's ability to recover the correct frame.

## 5. Externalized executive continuity

Long-running AI work needs durable structures outside the conversational
buffer.

Three useful forms of memory were identified:

- **Episodic memory** — what happened.
- **Semantic memory** — what was learned.
- **Teleological memory** — why the project exists and what it is trying to
  accomplish.

Teleological memory is especially fragile in ordinary LLM workflows.

## 6. Two control loops

### Execution loop

    Goal
      -> task contract
        -> implementation
          -> verification
            -> result

### Governance loop

    Result
      -> state update
        -> roadmap reassessment
          -> next-task selection
            -> renewed macro anchor

Many workflows implement the first loop and neglect the second.

## 7. Proposed hierarchy

A possible future hierarchy was discussed:

    PROJECT OBSERVATORY KERNEL
      -> PROJECT KERNEL
        -> ROADMAP / ARCHITECTURE
          -> CURRENT MILESTONE
            -> EXECUTION CONTRACT
              -> CODE / TESTS
                -> RETURN CAPSULE
                  -> PROJECT STATE UPDATE

The hierarchy should close back on itself: lower-level results must update the
higher-level state, rather than allowing the roadmap to become stale prose.

## 8. Candidate Observatory / Project split

The Observatory-level kernel would orient the portfolio as a whole.

Candidate concerns:

- identity and purpose;
- authority model;
- portfolio membership;
- universal operating doctrine;
- compact state vector per project;
- routing and gates;
- global uncertainties;
- canonical evidence pointers;
- succession protocol;
- kernel update protocol;
- next portfolio-level operation.

Each project would have its own project kernel containing only the minimum
durable information a successor should not need to rediscover.

Candidate concerns:

- identity;
- north star;
- doctrine;
- authority and boundaries;
- canonical state;
- current phase;
- phase exit condition;
- architectural invariants;
- frozen / superseded state;
- open questions;
- external dependencies and gates;
- next highest-value operation;
- evidence pointers;
- execution contract rules;
- return contract rules;
- succession bootstrap;
- kernel update rules.

These are hypotheses, not yet frozen requirements.

## 9. Project kernel design principle

> A kernel contains what a successor must not have to rediscover.

The kernel should not duplicate every CI run, issue, conversation, experiment,
or implementation detail.

It should combine:

- stable invariants;
- a very small amount of mutable state;
- authoritative pointers to deeper evidence.

## 10. Separation of intent, state, evidence, uncertainty, and history

A robust system should avoid blending desired outcomes with demonstrated facts.

Candidate distinct layers:

- **Intent** — what ought to happen.
- **State** — what has demonstrably happened.
- **Evidence** — why the state claim is justified.
- **Uncertainty** — what remains unknown.
- **History** — how the system arrived here.

This separation is especially important because cooperative AI systems can
otherwise allow desired state to contaminate represented actual state.

## 11. Early failure modes observed across long-running projects

The user's project history suggests at least these recurring classes:

### 11.1 Authority drift
Multiple artifacts describe different realities or imply different sources of
authority.

### 11.2 Apparent continuity without epistemic continuity
A successor can speak fluently about a project before reconstructing the
evidence that justified predecessor beliefs.

### 11.3 Local optimization overriding global purpose
A bounded failure (CI, deployment, browser behavior, implementation detail)
becomes the effective project objective.

### 11.4 Stale state masquerading as current truth
Human-maintained prose or old state labels remain semantically influential
after the real system has moved on.

### 11.5 Loss of negative knowledge
Rejected routes, exhausted searches, falsified assumptions, and known dead
ends are not preserved strongly enough and are rediscovered.

### 11.6 Desired state contaminating demonstrated state
"What should be true" becomes confused with "what has been shown to be true."

### 11.7 Cleanup causing semantic damage
Historical baggage may contain provenance or qualification evidence, while
obsolete historical authority may need to be removed. Retention and authority
are different questions.

### 11.8 Human operator acting as metacognition
The user repeatedly supplies interventions such as:

- What are we actually doing in this Era?
- What is the big picture?
- Is this temporary or architectural?
- Is this document frozen?
- Does this evidence justify promotion?
- Are we solving a superseded problem?
- Is the test stale rather than the product wrong?

This suggests the deeper research question:

> Which executive and metacognitive functions has the human operator
> repeatedly had to supply, and how can those functions be externalized into
> durable architecture?

## 12. Research method proposed

Use the user's project history as the first empirical dataset.

For each incident:

    Observed incident
      -> Cognitive failure
        -> Human correction
          -> Missing executive/metacognitive function
            -> Architectural requirement
              -> Possible mechanical enforcement

Then compare the derived requirements against ideas from:

- agent architectures;
- hierarchical planning;
- distributed systems;
- event sourcing;
- operating systems;
- software governance;
- organizational memory;
- commander's intent / delegation models;
- cognitive science and memory research;
- knowledge management.

Do not begin by assuming that "Project Kernel" is the final answer.

## 13. Competing architecture candidates to explore

Potential designs include:

- document-centric kernel;
- event-sourced state model;
- hierarchical state machine;
- graph-based evidence / authority model;
- hybrid architecture.

They should be compared under identical succession and drift scenarios.

## 14. Adversarial tests

Possible tests:

- fresh successor with no chat history;
- stale but plausible current-state document;
- misleading recent execution context;
- conflicting authority artifacts;
- attractive but out-of-scope task;
- locally sensible change that violates doctrine;
- desire/evidence conflict;
- already-exhausted research path;
- incomplete return handoff;
- obsolete roadmap item with recent implementation chatter.

A successful architecture should guide the agent toward the correct authority,
uncertainty posture, and next operation.

## 15. Cold-start criterion

A completely fresh successor, given only the durable project system, should be
able to answer:

1. What is this project?
2. What is it ultimately trying to accomplish?
3. Where is it now?
4. What evidence establishes that state?
5. What is uncertain?
6. What must not be casually changed?
7. What is historical but no longer authoritative?
8. What operation should occur next, and why?
9. What evidence would permit the project state to advance?

If it cannot, continuity still depends too heavily on chat history.

## 16. Current decision

Do **not** yet create Project Kernel files across repositories.

First preserve this research seed, mine real incidents from project history,
derive requirements, and test candidate architectures.

A dedicated repository is likely appropriate after scope and naming are
settled, but repository creation should follow preservation and research
framing rather than precede them.
