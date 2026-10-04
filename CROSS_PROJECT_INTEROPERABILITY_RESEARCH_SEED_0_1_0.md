# Cross-Project Interoperability Research Seed 0.1.0

Date: 2026-10-04
Status: **FROZEN RESEARCH SEED — NO LIVE CROSS-PROJECT CONTROL AUTHORIZED**

Working label: **CPI-0 — Cross-Project Interoperability**

The label is provisional.

## 1. Origin

This research track was opened after an external NotebookLM Deep Dive synthesized multiple active repositories and independently noticed recurring governance structures across them:

- canonical-state discipline;
- exact provenance;
- authority boundaries;
- explicit transition gates;
- negative-result / negative-knowledge retention;
- separation of exploration from qualification;
- succession and drift resistance.

The source audio is preserved by provenance record at:

sources/NOTEBOOKLM_SEVEN_PROJECT_BLUEPRINT_SOURCE_2026_10_04.md

The audio itself is a hypothesis-generating secondary source, not authority.

The immediate human decision was to pursue the possibility that independently governed projects can exchange useful state, evidence, triggers, and dependencies through a minimal common protocol without surrendering their epistemic independence.

## 2. Central research question

> **Can we define a minimal, project-neutral protocol through which independently governed projects can inform one another without surrendering epistemic independence, authority isolation, provenance, or local control over canonical state?**

This is deliberately narrower than building one system that controls all projects.

The research object is **federated continuity**, not project merger.

## 3. Why this belongs in Project Continuity Research

Composite E already defines an Observatory profile with:

- cross-project dependency graphs;
- multiple authority domains;
- portfolio routing;
- external triggers;
- project-level isolation / quarantine.

The current big-picture roadmap also reserves a later phase for multi-project read-only shadow trials.

What is missing between those two ideas is a tested interoperability boundary:

PROJECT-LOCAL TRUTH / AUTHORITY
→ EXPORTABLE OBSERVATION OR EVENT
→ CROSS-PROJECT TRANSPORT
→ LOCAL IMPORT / ADJUDICATION
→ LOCAL CANONICAL STATE — ONLY IF ACCEPTED LOCALLY

Without that boundary, an Observatory risks becoming an oracle whose summaries or inferred dependencies silently acquire authority they did not earn.

## 4. Core distinction

The most important provisional invariant is:

**REMOTE PROJECT STATE != LOCAL PROJECT STATE**

A second project may expose a signed, reproducible, well-provenanced event. That still does not make the event canonical in the receiving project.

The receiving project must decide, under its own authority and policy, whether the imported event is:

- relevant evidence;
- a trigger;
- a dependency update;
- a contradiction;
- a request for review;
- ignorable;
- inadmissible.

Candidate cross-project invariants:

- TRANSPORT != TRUST
- NOTIFICATION != AUTHORIZATION
- DEPENDENCY != CONTROL
- SHARED SCHEMA != SHARED ONTOLOGY
- OBSERVATION != ACCEPTANCE
- INTEROPERABILITY != MERGER
- REMOTE AUTHORITY != LOCAL AUTHORITY

These are hypotheses for adversarial testing, not yet doctrine.

## 5. Meaning of epistemic independence

For this research, a project retains epistemic independence when all of the following remain true:

1. **Local claims remain locally governed.** Another project's conclusion cannot silently become canonical here.
2. **Evidence remains attributable to its source domain.** Imported evidence retains exact source identity and cannot be laundered into source-free known truth.
3. **Authority does not transitively leak.** Authority to govern Project A does not imply authority over Project B.
4. **Local admissibility rules survive integration.** Each project may impose its own evidence burden, transition guards, preregistration, safety rules, or null-subtraction discipline.
5. **Cross-project summaries are challengeable.** Any Observatory-level inference must be traceable to project-local evidence and recomputable or rejectable.
6. **Projects can disagree without corruption.** The protocol must represent unresolved contradictions or incompatible interpretations without forcing premature reconciliation.
7. **A project may disconnect.** Interoperability must not become a hidden requirement for a project to remain intelligible or valid.

## 6. First accepted insight from the NotebookLM synthesis

The strongest accepted insight is not that all repositories are one project.

It is that several repositories have independently developed mechanisms for different aspects of the same meta-problem:

> preserving trustworthy knowledge and coordinated action across complex, long-lived human-AI work.

This makes a common interoperability research track plausible.

The first candidate benefit is a Project Observatory that can observe, translate, compare, route, and alert across projects while preserving each project's local epistemic and authority boundaries.

## 7. Claims explicitly not accepted

### 7.1 HiVenues / Hive as an NFC or PGH sensor array

The NotebookLM synthesis proposed a more dramatic possibility: authenticated human interaction graphs from Hive / HiVenues might serve as empirical finite relational structures for NFC or PGH.

This is **not accepted as a scientific bridge**.

The existence of a cryptographically authenticated finite relational graph does not establish physical relevance to a theory merely because both can be described with finite relational mathematics.

Before such a bridge could become scientifically meaningful, the theory would need a principled mapping identifying:

- why those observables instantiate theory-relevant quantities;
- what prediction differs from generic graph structure;
- what null model must be subtracted;
- what result would count against the proposed connection.

Current disposition:

- STATUS = SPECULATIVE CROSS-PROJECT HYPOTHESIS
- SCIENTIFIC DEPENDENCY = NOT AUTHORIZED
- EMPIRICAL EVIDENCE = NONE ESTABLISHED

This hold is itself a test case for negative-knowledge preservation.

### 7.2 Observatory as a write-capable global oracle

No current result authorizes Project Observatory, CCP, or a future interoperability layer to mutate multiple live projects.

Any progression beyond read-only observation remains separately gated.

## 8. Minimal interoperability surface — first hypothesis

Do **not** standardize entire repositories.

Instead, test whether each project can expose a small, versioned projection with enough information for safe external interpretation.

A first candidate projection may need fields in these semantic classes:

- project identity;
- protocol version;
- project revision / exact source identity;
- projection revision;
- purpose / domain label;
- current-state summary;
- claims / status;
- evidence references;
- authority domain;
- negative knowledge;
- open uncertainties;
- inbound dependencies;
- outbound events / triggers;
- admissible next transitions;
- reopen predicates;
- freshness / expiry;
- integrity identity.

This is a research vocabulary, **not yet a schema**.

Do not prematurely freeze YAML, JSON, database, graph, or file layout. The protocol must first prove which semantics are actually necessary.

## 9. Candidate event envelope

A cross-project event may eventually require concepts such as:

- event_id
- source_project
- source_revision
- source_event_sequence
- event_type
- scope
- subject
- produced_at
- evidence_refs
- authority_refs
- freshness
- integrity_hash
- protocol_version

The receiving project would record an **import observation** or candidate evidence object.

Critically:

**RECEIVE(event) does not imply ACCEPT_AS_CANONICAL(event).**

Local adjudication remains mandatory unless explicitly and narrowly delegated.

## 10. Observatory boundary

The Observatory should be treated as a **derived observer and router**, not the final judge of project-local truth.

Permissible future functions may include:

- discover a project's declared state surface;
- detect freshness mismatch;
- compare dependency revisions;
- identify cross-project contradictions;
- route source-bound evidence;
- surface reopen triggers;
- flag dependency changes;
- generate portfolio-level orientation projections;
- recommend a project-local review.

A consequential Observatory inference should preserve a chain from inference to source events, source project revisions, source evidence, and transformation/rule version.

The Observatory must be auditable by mechanisms independent of its own conclusion.

Provisional principle:

> **The Observatory must never become an oracle.**

## 11. The auditor problem

If a cross-project system coordinates, reconstructs, routes, and summarizes project state, it becomes capable of introducing its own:

- orientation drift;
- epistemic-state drift;
- authority drift;
- transition drift;
- negative-knowledge loss;
- metacognitive drift.

Therefore the interoperability layer itself must expose:

- exact input identities;
- transformation/version identity;
- deterministic or reproducible derivations where possible;
- explicit inference status;
- unresolved ambiguity;
- local acceptance/rejection outcomes;
- audit trails for routing decisions.

A cross-project protocol that cannot audit its own derived state fails the research objective even if it appears operationally convenient.

## 12. Relationship to CCP

This track does not replace Composite E / CCP.

Instead it asks whether CCP semantics can be safely **federated**.

Candidate relationship:

PROJECT-LOCAL CCP OR EQUIVALENT
→ export projection/event
→ INTEROPERABILITY ENVELOPE
→ OBSERVATORY / ROUTER
→ RECEIVING PROJECT IMPORT
→ LOCAL CCP / LOCAL POLICY ADJUDICATION

A project that does not use CCP should still be able to participate through an adapter if it can expose equivalent semantics.

Project-neutrality therefore requires testing against:

- CCP-backed projects;
- repositories with different governance models;
- projects with weak or partial state machinery;
- projects that deliberately reject some shared concepts.

## 13. Research program

### Stage 0 — Preservation

After this seed is committed:

- RESEARCH QUESTION = PRESERVED
- SOURCE PROVENANCE = PRESERVED
- ACCEPTED / HELD / REJECTED CLAIMS = PRESERVED
- LIVE INTEGRATION = NOT AUTHORIZED

### Stage 1 — Seven-project state-surface survey

Inspect the participating repositories and record, without changing them:

- what each project treats as canonical state;
- how authority is represented;
- what exact identities are available;
- how evidence is bound;
- how negative knowledge is preserved;
- what can produce an external trigger;
- what dependencies already exist informally;
- what semantics cannot be translated safely.

The goal is to discover the common denominator empirically rather than impose it.

### Stage 2 — Requirements and threat model

Derive requirements from concrete failure modes, especially:

- stale exported state;
- forged project identity;
- semantic collision;
- authority leakage;
- accidental transitive trust;
- circular dependency;
- feedback loops;
- cross-project contradiction;
- version skew;
- replay / duplicate events;
- dropped negative knowledge;
- false reopen triggers;
- Observatory hallucination or overcompression;
- project-specific ontology being mistaken for a universal one.

### Stage 3 — Competing interoperability architectures

At minimum compare:

1. minimal signed state projection;
2. typed event-envelope federation;
3. provenance-graph exchange;
4. query-only federated Observatory;
5. hybrid projection + event model.

Do not choose a winner before adversarial comparison.

### Stage 4 — Null-subtraction pass

For every attractive cross-project connection, ask:

> What part of the apparent relationship is generic to any two structured projects, and what residue is genuinely specific and useful?

This protects against creating a unified architecture from superficial similarities.

### Stage 5 — Read-only simulation

Build or emulate cross-project exchange using frozen snapshots.

No live project mutation.

Required properties:

- exact provenance preserved;
- local authority remains local;
- imported events cannot silently promote state;
- negative knowledge survives routing;
- stale or contradictory inputs are detectable;
- disconnecting one project does not corrupt the others.

### Stage 6 — Observatory shadow trial

If the read-only model survives, allow Project Observatory to consume the protocol in shadow mode.

The Observatory may report and recommend. It may not write canonical project state.

### Stage 7 — Multi-project read-only trial

Only after prior stages survive should this work feed the existing Phase 7 multi-project shadow-trial program.

## 14. First candidate test domains

The initial set should include deliberately different domains:

- a software/product project;
- a scientific/theoretical project;
- a comparison/governance research project;
- a continuity/governance research project;
- Project Observatory itself.

The purpose is not to prove that every project can be flattened into one schema.

The purpose is to discover what **small common interface** remains useful after domain-specific semantics are preserved.

## 15. Success criteria

This track succeeds only if a protocol can demonstrate all of the following:

1. a fresh successor can identify the source and status of imported information;
2. local canonical state remains reproducible without trusting the Observatory;
3. authority cannot leak across project boundaries accidentally;
4. cross-project dependencies can be represented without creating hidden control relationships;
5. stale data and version skew are detectable;
6. negative knowledge and reopen predicates survive transport;
7. contradictory project states can coexist explicitly;
8. a project can reject an imported event without breaking the federation;
9. the protocol remains materially useful across heterogeneous domains;
10. the interoperability layer can itself be audited.

## 16. Failure / stop conditions

Return to research rather than forcing standardization if:

- safe exchange requires project-specific hard-coding for every pair;
- the common schema becomes an encyclopedia of all project ontologies;
- consumers cannot distinguish source claims from local facts;
- authority boundaries become ambiguous;
- the Observatory becomes the only place from which current state is intelligible;
- cross-project routing amplifies stale or incorrect information;
- negative knowledge is lost or reopened spuriously;
- projects become unable to operate independently;
- the interface creates more governance complexity than coordination value;
- a simpler existing interoperability standard solves the problem better.

## 17. Preservation policy

This seed should remain immutable after acceptance.

Corrections or advances should be expressed through new versioned artifacts, issues, experiment reports, or supersession records rather than silently rewriting the origin.

The source audio binary does not need to live in Git history. Its cryptographic identity is preserved separately.

Future public claims must distinguish:

- OBSERVED RECURRENCE
- HYPOTHESIS
- ARCHITECTURAL INFERENCE
- TESTED RESULT
- AUTHORIZED INTEGRATION

## 18. Immediate disposition

- CROSS_PROJECT_INTEROPERABILITY_RESEARCH = AUTHORIZED
- COMMON_SCHEMA = NOT YET AUTHORIZED
- OBSERVATORY_READ_ONLY_INTEROP_RESEARCH = AUTHORIZED
- LIVE_CROSS_PROJECT_WRITES = NOT AUTHORIZED
- HIVENUES_TO_NFC_PGH_SCIENTIFIC_BRIDGE = HELD / UNESTABLISHED

The next legitimate operation is the **Stage 1 seven-project state-surface survey**, followed by a requirements/threat-model artifact.
