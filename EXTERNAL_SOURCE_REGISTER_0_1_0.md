# External Source Register 0.1.0

Date: 2026-09-20  
Status: Frozen source register for the first cross-discipline comparison pass.

## Purpose

This register records the external sources used to compare the empirically
derived continuity-failure taxonomy against adjacent disciplines.

The external literature is **not** allowed to rewrite the empirical incident
corpus. It may:

- corroborate an observed failure structure;
- supply an existing formalism or design pattern;
- expose an omitted failure class;
- challenge a proposed requirement;
- reveal where the problem is already substantially solved.

It may not manufacture an incident that did not occur.

## Evidence classes

- **S-A — Standard / official doctrine / primary classic:** stable standard,
  official doctrine, or field-defining primary work.
- **S-B — Peer-reviewed research / review:** peer-reviewed journal or
  conference work.
- **S-C — Recent preprint / emerging research:** useful for current field
  direction, but not treated as settled consensus.

---

## Provenance, event history, and distributed state

### SRC-EXT-001 — W3C PROV-O
- Class: S-A
- Title: *PROV-O: The PROV Ontology*
- Organization: W3C
- Year: 2013
- URL: https://www.w3.org/TR/prov-o/
- Relevant concepts: Entity, Activity, Agent, derivation, attribution,
  association, use, generation.
- Research use: authority/provenance relationships; separation of object,
  activity, and responsible agent.

### SRC-EXT-002 — Event Sourcing
- Class: S-A / practitioner foundational pattern
- Author: Martin Fowler
- Year: 2005
- URL: https://martinfowler.com/eaaDev/EventSourcing.html
- Relevant concepts: application state as a sequence of immutable events;
  reconstruction of past/current state; temporal queries.
- Research use: historical truth versus derived current state.

### SRC-EXT-003 — Azure Event Sourcing Pattern
- Class: S-A / current engineering guidance
- Organization: Microsoft Azure Architecture Center
- Updated: 2026
- URL: https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing
- Relevant concepts: intent-bearing immutable events, compensating events,
  optimistic concurrency, snapshots as derived optimization rather than source
  of truth.
- Research use: event/state separation, conflict handling, snapshot semantics.

### SRC-EXT-004 — Time, Clocks and the Ordering of Events in a Distributed System
- Class: S-A
- Author: Leslie Lamport
- Venue: Communications of the ACM
- Year: 1978
- URL: https://www.microsoft.com/en-us/research/publication/time-clocks-ordering-events-distributed-system/
- Research use: causal/partial ordering; warning that temporal order and
  knowledge about order are distinct from simple wall-clock recency.

---

## Hierarchy, planning, and state transitions

### SRC-EXT-005 — Statecharts
- Class: S-B / field-defining primary
- Author: David Harel
- Title: *Statecharts: A Visual Formalism for Complex Systems*
- Venue: Science of Computer Programming
- Year: 1987
- DOI: 10.1016/0167-6423(87)90035-9
- URL: https://www.sciencedirect.com/science/article/pii/0167642387900359
- Relevant concepts: hierarchy, concurrency, communication, manageable
  descriptions of complex state-transition systems.
- Research use: guarded hierarchical transitions and explicit state structure.

### SRC-EXT-006 — HTN Planning Survey
- Class: S-B
- Authors: Ilche Georgievski, Marco Aiello
- Title: *HTN planning: Overview, comparison, and beyond*
- Venue: Artificial Intelligence
- Year: 2015
- DOI: 10.1016/j.artint.2015.02.002
- URL: https://www.sciencedirect.com/science/article/pii/S0004370215000247
- Relevant concepts: hierarchical task decomposition; rich domain knowledge;
  task networks and planning search.
- Research use: strategic-to-tactical decomposition.

### SRC-EXT-007 — Options Framework
- Class: S-B
- Authors: Richard Sutton, Doina Precup, Satinder Singh
- Title: *Between MDPs and semi-MDPs: A framework for temporal abstraction in reinforcement learning*
- Venue: Artificial Intelligence
- Year: 1999
- DOI: 10.1016/S0004-3702(99)00052-1
- URL: https://www.sciencedirect.com/science/article/pii/S0004370299000521
- Relevant concepts: temporally extended actions / abstraction.
- Research use: actions and plans at multiple time scales.

---

## Safety and control

### SRC-EXT-008 — STPA Handbook
- Class: S-A
- Organization: MIT Partnership for Systems Approaches to Safety and Security
- URL: https://psas.scripts.mit.edu/home/books-and-handbooks/
- Relevant concepts: purpose of analysis, control structures, unsafe control
  actions, scenarios, constraints, requirements, organizational/social factors.
- Research use: unsafe/unauthorized action as a control problem rather than a
  pure memory problem.

### SRC-EXT-009 — Basic STPA examples
- Class: S-A / training material from MIT STPA program
- URL: https://psas.scripts.mit.edu/home/wp-content/uploads/2017/04/Thomas-Basic-STPA-exercises.pdf
- Relevant concepts: unsafe control action can arise from non-provision,
  improper provision, wrong timing/order, or excessive/insufficient duration.
- Research use: transition drift and timing-sensitive authority.

---

## Organizational memory and intent

### SRC-EXT-010 — Organizational Memory
- Class: S-B
- Authors: James P. Walsh, Gerardo Rivera Ungson
- Venue: Academy of Management Review
- Year: 1991
- DOI: 10.5465/amr.1991.4278992
- URL: https://journals.aom.org/doi/10.5465/amr.1991.4278992
- Relevant concepts: acquisition, retention, retrieval; organizational memory
  may be used, misused, or abused.
- Research use: memory quality is not only storage quantity; retained knowledge
  can constrain later action well or badly.

### SRC-EXT-011 — Organizational routines as procedural memory
- Class: S-B
- Authors: Michael D. Cohen, Paul Bacdayan
- Venue: Organization Science
- Year: 1994
- DOI: 10.1287/orsc.5.4.554
- URL: https://pubsonline.informs.org/doi/pdf/10.1287/orsc.5.4.554
- Relevant concepts: routines improve reliability/speed but can become
  suboptimal when transferred to inappropriate situations.
- Research use: safeguards/routines can themselves become drift mechanisms.

### SRC-EXT-012 — Mission Command / Commander's Intent
- Class: S-A / official doctrine, accessed via public PDF mirror and Army
  summary
- Title: ADP 6-0, *Mission Command: Command and Control of Army Forces*
- Public PDF mirror:
  https://irp.fas.org/doddir/army/adp6_0.pdf
- Army summary:
  https://www.army.mil/article/225414/combined_arms_center_launches_new_mission_command_doctrine
- Relevant concepts: purpose, key tasks, desired end state, nested intent,
  disciplined initiative, limits for subordinate action.
- Research use: preserving purpose without prescribing every tactical action.

---

## Cognitive science

### SRC-EXT-013 — Working Memory
- Class: S-B
- Author: Alan Baddeley
- Title: *Working memory: looking back and looking forward*
- Venue: Nature Reviews Neuroscience
- Year: 2003
- DOI: 10.1038/nrn1201
- URL: https://www.nature.com/articles/nrn1201
- Relevant concepts: limited-capacity working memory and central executive.
- Research use: distinction between temporary active state and larger memory.

### SRC-EXT-014 — Architecture of Cognitive Control
- Class: S-B
- Authors: Etienne Koechlin, Chrystèle Ody, Frédérique Kouneiher
- Venue: Science
- Year: 2003
- DOI: 10.1126/science.1088545
- URL: https://pubmed.ncbi.nlm.nih.gov/14615530/
- Relevant concepts: cascade of executive processes controlled by stimulus,
  present context, and temporal episode.
- Research use: hierarchical/context-sensitive executive control.

---

## LLM agent memory, planning, and reflection

### SRC-EXT-015 — ReAct
- Class: S-B
- Authors: Shunyu Yao et al.
- Venue: ICLR 2023
- Title: *ReAct: Synergizing Reasoning and Acting in Language Models*
- URL: https://arxiv.org/abs/2210.03629
- Relevant concepts: interleaving reasoning traces and environment actions.
- Research use: external observation can update plans and reduce purely
  internal error propagation.

### SRC-EXT-016 — Reflexion
- Class: S-B
- Authors: Noah Shinn et al.
- Venue: NeurIPS 2023
- Title: *Reflexion: Language Agents with Verbal Reinforcement Learning*
- URL: https://arxiv.org/abs/2303.11366
- Relevant concepts: episodic reflection memory based on feedback.
- Research use: persistent lessons from failure; comparison to our
  metacognitive-drift cases.

### SRC-EXT-017 — Critical self-correction survey
- Class: S-B
- Authors: Ryo Kamoi et al.
- Venue: Transactions of the Association for Computational Linguistics
- Year: 2024
- DOI: 10.1162/tacl_a_00713
- URL: https://aclanthology.org/2024.tacl-1.78/
- Relevant finding: prompted intrinsic self-correction is unreliable in many
  reasoning settings; reliable external feedback is an important enabling
  condition.
- Research use: external reorientation surfaces versus ungrounded reflection.

### SRC-EXT-018 — Large Language Models Cannot Self-Correct Reasoning Yet
- Class: S-B
- Authors: Jie Huang et al.
- Venue: ICLR 2024
- URL: https://proceedings.iclr.cc/paper_files/paper/2024/hash/8b4add8b0aa8749d80a34ca5d941c355-Abstract-Conference.html
- Relevant finding: intrinsic self-correction can fail or degrade reasoning
  without external feedback.
- Research use: failed self-correction / frame-preserving correction.

### SRC-EXT-019 — Generative Agents
- Class: S-B
- Authors: Joon Sung Park et al.
- Year: 2023
- Title: *Generative Agents: Interactive Simulacra of Human Behavior*
- URL: https://arxiv.org/abs/2304.03442
- Relevant concepts: memory stream, retrieval, reflection, planning.
- Research use: episodic-to-reflective memory pipeline.

### SRC-EXT-020 — MemGPT
- Class: S-C / influential preprint-system paper
- Authors: Charles Packer et al.
- Year: 2023
- Title: *MemGPT: Towards LLMs as Operating Systems*
- URL: https://arxiv.org/abs/2310.08560
- Relevant concepts: hierarchical memory tiers, virtual context management,
  interrupts.
- Research use: context capacity versus memory hierarchy.

### SRC-EXT-021 — LongMemEval
- Class: S-C
- Authors: Di Wu et al.
- Year: 2024
- Title: *LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory*
- URL: https://arxiv.org/abs/2410.10813
- Relevant concepts: extraction, multi-session reasoning, temporal reasoning,
  knowledge updates, abstention.
- Research use: memory evaluation dimensions and their limits.

### SRC-EXT-022 — A-MEM
- Class: S-C
- Authors: Wujiang Xu et al.
- Year: 2025
- Title: *A-MEM: Agentic Memory for LLM Agents*
- URL: https://arxiv.org/abs/2502.12110
- Relevant concepts: dynamically linked and evolving memory notes.
- Research use: adaptive organization of memory rather than fixed chunks.

### SRC-EXT-023 — Mem0
- Class: S-C
- Authors: Prateek Chhikara et al.
- Year: 2025
- Title: *Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory*
- URL: https://arxiv.org/abs/2504.19413
- Relevant concepts: extraction, consolidation, retrieval, graph memory,
  efficiency.
- Research use: scalable persistent memory engineering.

### SRC-EXT-024 — COMPASS
- Class: S-C
- Authors: Guangya Wan et al.
- Year: 2025
- Title: *COMPASS: Enhancing Agent Long-Horizon Reasoning with Evolving Context*
- URL: https://arxiv.org/abs/2510.08790
- Relevant concepts: tactical Main Agent, strategic Meta-Thinker, Context
  Manager with concise progress briefs.
- Research use: strong independent convergence with Project Lead /
  executor / context-manager separation.

### SRC-EXT-025 — Memory for Autonomous LLM Agents
- Class: S-C
- Author: Pengfei Du
- Year: 2026
- Title: *Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers*
- URL: https://arxiv.org/abs/2603.07670
- Relevant concepts: write-manage-read loop; consolidation, retrieval,
  reflection, forgetting, contradiction handling.
- Research use: current memory-system design space.

### SRC-EXT-026 — Context Rot in Long-Horizon Search
- Class: S-C
- Authors: Shijie Xia et al.
- Year: 2026
- Title: *Diagnosing and Mitigating Context Rot in Long-horizon Search*
- URL: https://arxiv.org/abs/2606.29718
- Relevant concepts: large accumulated context can cause premature uncertain
  answers or giving up; context management mitigations.
- Research use: direct comparison with orientation paralysis/context swamp.

### SRC-EXT-027 — REFLECT
- Class: S-C
- Authors: Xiaofeng Lin et al.
- Year: 2026
- Title: *REFLECT: Intervention-Supported Error Attribution for Silent Failures in LLM Agent Traces*
- URL: https://arxiv.org/abs/2606.09071
- Relevant concepts: diagnose a candidate failure, replay with a targeted patch,
  use outcome change as evidence to refine attribution.
- Research use: tested metacognition rather than free-form introspection.

### SRC-EXT-028 — Agent Planning Benchmark
- Class: S-C
- Authors: Haoyu Sun et al.
- Year: 2026
- Title: *Agent Planning Benchmark: A Diagnostic Framework for Planning Capabilities in LLM Agents*
- URL: https://arxiv.org/abs/2606.04874
- Relevant concepts: planning-specific diagnosis, long-horizon planning,
  extraneous/broken tools, infeasible tasks, calibrated refusal.
- Research use: planning versus execution distinction; stopping/infeasibility.

### SRC-EXT-029 — The Horizon Gap
- Class: S-C
- Authors: Mingguang Chen, Licheng Wang, Bo Qu
- Year: 2026
- Title: *The Horizon Gap: Planning, Memory, Execution, Training, and Evaluation for Long-Horizon LLM Agents*
- URL: https://arxiv.org/abs/2608.06663
- Relevant concepts: distinguishes long-horizon, long-context, and long-term
  memory; surveys goal drift, premature completion, and lost earlier decisions.
- Research use: current field-level comparison to our independently derived
  problem statement.

## Register rule

Recent S-C work may motivate experiments or architecture candidates. It does
not outrank the empirical corpus or stable S-A/S-B concepts merely because it
is newer.
