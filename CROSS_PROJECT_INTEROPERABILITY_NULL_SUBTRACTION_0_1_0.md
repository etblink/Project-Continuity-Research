# Cross-Project Interoperability Null-Subtraction Pass 0.1.0

Date: 2026-10-04
Status: FROZEN STAGE-4 NULL-SUBTRACTION RESULT
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #19

Upstream artifacts:

- CROSS_PROJECT_STATE_SURFACE_SURVEY_0_1_0.md
- CROSS_PROJECT_INTEROPERABILITY_REQUIREMENTS_THREAT_MODEL_0_1_0.md
- CROSS_PROJECT_INTEROPERABILITY_ARCHITECTURE_COMPETITION_0_1_0.md

## 1. Purpose

The architecture competition selected a hybrid attested projection plus typed event federation for read-only simulation.

This pass asks a stricter question:

What part of that design is actually specific to the cross-project continuity problem after generic interoperability, event, attestation, provenance, and integrity mechanisms are subtracted?

The purpose is to prevent a generic distributed-systems stack from being redescribed as a new project-continuity protocol.

## 2. Null hypothesis

The null is:

EXISTING_INTEROPERABILITY_AND_PROVENANCE_MECHANISMS
+
PROJECT_SPECIFIC_PREDICATES
=
SUFFICIENT

If the null is adequate, CPI should become a profile/convention over existing standards rather than a new foundational wire protocol.

A new mechanism is justified only where the frozen requirements cannot be satisfied by composition of mature generic mechanisms plus a bounded semantic profile.

## 3. Generic machinery to subtract

### G1 — Event envelope

Generic event identity, source, type, time, version, and data fields are not CPI-specific.

CloudEvents already standardizes this class of problem.

Disposition:

SUBTRACT_FROM_NOVELTY

### G2 — Subject-bound attestation

Binding metadata to an exact subject with a typed predicate is not CPI-specific.

The in-toto Attestation Framework already supplies the general Statement / Predicate / Envelope / Bundle decomposition.

Disposition:

SUBTRACT_FROM_NOVELTY

### G3 — Digital-signature envelope

Authenticated serialization and multi-signature envelope design are established security problems.

CPI should not invent its own signature envelope.

Disposition:

SUBTRACT_FROM_NOVELTY

### G4 — Content digests and immutable identifiers

Commit hashes, tree hashes, blob digests, object IDs, and cryptographic digests are generic integrity mechanisms.

Disposition:

SUBTRACT_FROM_NOVELTY

### G5 — Provenance graph primitives

Entity/activity/agent provenance, derivation, attribution, generation, and usage relations are established provenance concepts.

W3C PROV provides mature vocabulary.

Disposition:

SUBTRACT_FROM_NOVELTY

### G6 — Append-only event history

Immutable event logging and replay are established architecture patterns.

Disposition:

SUBTRACT_FROM_NOVELTY

### G7 — Idempotent delivery / duplicate detection

Stable event identity and duplicate-safe consumption are standard distributed-systems requirements.

Disposition:

SUBTRACT_FROM_NOVELTY

### G8 — Schema and protocol versioning

Versioned schemas and compatibility negotiation are generic interoperability requirements.

Disposition:

SUBTRACT_FROM_NOVELTY

### G9 — Checkpoints / snapshots

Point-in-time state checkpoints are generic event-sourcing and distributed-state mechanisms.

Disposition:

SUBTRACT_FROM_NOVELTY

### G10 — Authentication versus payload semantics

The distinction between proving who signed a statement and deciding whether the statement is true or authorized is not unique to CPI.

Disposition:

SUBTRACT_FROM_NOVELTY

## 4. Residual semantics after subtraction

The following requirements remain materially specific to the observed cross-project continuity problem.

They may still have analogues elsewhere, but they are not supplied merely by generic event/attestation/provenance machinery.

### R1 — Remote/local canonicality firewall

Core rule:

REMOTE ATTESTATION
!=
LOCAL ACCEPTANCE
!=
LOCAL AUTHORIZATION
!=
LOCAL CANONICAL STATE

Existing attestation systems can prove provenance of a remote statement.

They do not automatically define the receiving project's epistemic admission semantics.

CPI-specific need:

A mandatory local import disposition boundary.

### R2 — Purpose-scoped authority resolver

A repository may have multiple authoritative sources for different purposes.

NFC proves that:

- publication main can be authoritative for publication/provenance routing;
- another immutable ref can be theorem-bearing authority.

Generic subject identity does not answer which subject is authoritative for which purpose.

CPI-specific need:

Authority must be mapped to purpose/scope rather than inferred from source location.

### R3 — Project-native state preservation

The common layer must not require the source project to replace its native state model.

Observed native models range from:

- sole mutable state file;
- live state plus ledgers;
- frozen canon;
- machine-readable capsule;
- issue/PR/test/human-acceptance product governance;
- derived snapshots.

CPI-specific need:

Interoperability object is explicitly a projection/attestation about native state, not a replacement state model.

### R4 — Negative-knowledge transport

Generic event and provenance systems can encode negative records, but they do not require preservation of:

- held routes;
- failed derivations;
- do-not-assume constraints;
- checked non-dependencies;
- prohibited actions;
- reopen predicates;
- stop conditions.

The seven-project survey shows these objects are decision-critical.

CPI-specific need:

Negative knowledge is mandatory semantic content rather than optional annotation.

### R5 — Reopen semantics

A route can be closed or held yet legitimately reopen under a named condition.

The system must preserve:

- closure basis;
- reopen predicate;
- trigger source;
- local adjudication.

Generic event models do not define this epistemic lifecycle.

### R6 — Dependency anti-inference rule

CPI requires an explicit distinction between:

- demonstrated dependency;
- contextual relation;
- checked non-dependency;
- unknown relation.

The protocol must prohibit dependency inference from thematic or mathematical similarity alone.

This is central because cross-project synthesis systems are especially prone to generating attractive false bridges.

### R7 — Stale-but-valid state

A frozen historical snapshot can remain correct at its observation boundary while being stale relative to the source project.

CPI-specific need:

Freshness is not truth/falsity.

The state model must permit:

VALID_AT_BOUNDARY = YES
CURRENT = NO

without rewriting history.

### R8 — Trigger versus authorization versus prerequisite

Observed projects distinguish:

- evidence trigger;
- physical prerequisite;
- owner choice;
- qualification result;
- separate authorization;
- prohibition.

CPI-specific need:

These are different control semantics and may not collapse into one blocked or ready field.

### R9 — Human acceptance as first-class authority

Some gates are intentionally controlled by a human owner.

Generic CI/attestation systems tend to privilege machine-verifiable state.

CPI-specific need:

Human acceptance can be a legitimate typed authority event without being replaced by machine pass status.

### R10 — Consequence-class boundary

The same project can authorize:

- read-only observation;
- repository-local work;
- external infrastructure change;
- physical experiment;
- financial/value action;
- publication;
- public deployment

under different burdens.

CPI-specific need:

Authorization must name consequence class.

### R11 — Observer non-oracle rule

A cross-project observer is derived state.

Its convenience must not make it the only intelligible or authoritative source.

CPI-specific need:

Every consequential observer inference remains source-traceable, challengeable, and independently recomputable where feasible.

### R12 — Federation optionality

A project must be able to disconnect without losing its own truth, authority, or continuity.

This is stronger than ordinary service availability.

It is an epistemic independence property.

## 5. Residual architecture

After null subtraction, the selected design becomes smaller.

The likely CPI-specific object set is not a new transport stack.

It is a semantic profile consisting of four predicate families:

### A. Project Projection

A typed attestation about project-native state at an exact observation boundary.

### B. Project Event

A typed statement that a material project event occurred.

Transport may reuse a generic event envelope.

### C. Import Disposition

A receiving project's local decision about a remote projection/event.

This is the canonicality firewall.

### D. Derivation / Observer Record

A statement binding a derived Observatory inference to exact inputs and transformation identity.

Generic provenance relations may be reused underneath.

## 6. Strong correction to Stage-3 language

Stage 3 used the phrase:

HYBRID_ATTESTED_PROJECTION_PLUS_TYPED_EVENT_FEDERATION

That architecture remains selected for simulation.

However the null-subtraction result changes the likely public form.

The current best formulation is:

CPI = SEMANTIC INTEROPERABILITY PROFILE

not:

CPI = NEW GENERAL-PURPOSE WIRE PROTOCOL

The profile may define:

- predicate semantics;
- required fields;
- validation rules;
- local-admission rules;
- negative-knowledge requirements;
- conformance tests.

It should reuse existing generic envelopes and provenance concepts where practical.

## 7. Candidate reuse mapping

### Generic event context

Prefer CloudEvents-compatible semantics for event identity/source/type/time where events are transported.

### Attestation structure

Prefer in-toto-like subject + typed predicate + authenticated envelope layering.

Do not automatically adopt software-supply-chain predicate semantics.

### Provenance

Prefer W3C-PROV-compatible conceptual relations where useful.

Do not require RDF/OWL or a graph database for the minimum profile.

### Repository identity

Use native Git identities directly when they are already the authoritative immutable identifiers.

## 8. What may still require original specification work

The following likely require CPI-specific normative definitions:

1. authority-purpose mapping;
2. canonicality firewall and import dispositions;
3. negative-knowledge object requirements;
4. reopen predicate semantics;
5. dependency class plus basis/counterfactual rule;
6. stale-but-valid projection semantics;
7. trigger/prerequisite/authorization distinction;
8. consequence-class declaration;
9. observer derivation obligations;
10. federation/disconnection invariant.

These may be profile semantics rather than new transport primitives.

## 9. Novelty caution

No novelty claim is authorized.

The fact that this exact combination was not found in the initial continuity literature review or standards reconnaissance does not establish originality.

A later prior-art search should specifically test:

- federated policy decision systems;
- scientific workflow provenance exchange;
- multi-agent governance attestations;
- cross-repository project-state protocols;
- federated knowledge-graph admission semantics;
- evidence exchange with local trust policy;
- distributed issue/decision record standards.

Current permitted claim:

The seven-project corpus creates a concrete need for a combined semantic profile whose full requirements are not supplied merely by generic event, attestation, or provenance envelopes.

## 10. Null controls

### Null control A — Generic event only

If ProjectEvent alone can preserve all eight adversarial cases without a projection or local import disposition, Candidate E is overbuilt.

Current result:

NOT SUPPORTED

Cold start, negative-knowledge completeness, and remote/local canonicality remain weak.

### Null control B — Generic attestation only

If subject + predicate + signature alone determines safe cross-project admission, CPI-specific semantics are unnecessary.

Current result:

NOT SUPPORTED

Authentication and subject binding do not define receiving-project canonicalization or authority.

### Null control C — Full provenance graph only

If generic provenance relations alone determine safe state/routing, CPI-specific semantics are unnecessary.

Current result:

NOT SUPPORTED

Provenance can say where a statement came from without defining whether it is locally admitted, reopened, prohibited, or authorized.

### Null control D — Query-only observer

If a sophisticated observer can infer all semantics safely without an explicit profile, a common profile is unnecessary.

Current result:

NOT SUPPORTED_AS_GENERAL_SOLUTION

The adapter becomes hidden governance and increases oracle risk.

## 11. Stage-4 disposition

GENERIC_EVENT_MACHINERY = SUBTRACTED

GENERIC_ATTESTATION_MACHINERY = SUBTRACTED

GENERIC_SIGNATURE_ENVELOPE = SUBTRACTED

GENERIC_PROVENANCE_PRIMITIVES = SUBTRACTED

GENERIC_VERSIONING_AND_IDEMPOTENCE = SUBTRACTED

CPI_SPECIFIC_RESIDUAL = NONEMPTY

NEW_GENERAL_PURPOSE_WIRE_PROTOCOL = NOT_JUSTIFIED

SEMANTIC_INTEROPERABILITY_PROFILE = JUSTIFIED_FOR_SIMULATION

CANDIDATE_E_RETAINED = YES__REDUCED_TO_PROFILE_PLUS_REUSED_GENERIC_LAYERS

NOVELTY_CLAIM = NOT_AUTHORIZED

LIVE_FEDERATION = NOT_AUTHORIZED

## 12. Next legitimate operation

Stage 5 is now justified:

READ_ONLY FROZEN-SNAPSHOT SIMULATION

The simulation should implement only enough machinery to prove or break:

- Project Projection;
- Project Event;
- Import Disposition;
- Derivation Record;
- authority-purpose mapping;
- negative knowledge;
- freshness;
- dependency/trigger semantics.

It should use frozen repository snapshots and must perform no writes to observed projects.

The simulation should test all eight Stage-2 adversarial conformance cases and include deliberately malformed or misleading inputs.

If those semantics cannot survive in a small file-backed prototype, return to architecture research rather than adding infrastructure.
