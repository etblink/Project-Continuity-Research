# CCP-1 Reopen-Predicate Brittleness Attack 0.1.0

Date: 2026-09-20  
Status: **PREREGISTERED — NOT YET ADJUDICATED**

## Question

CCP-0 preserved negative knowledge using closures such as:

```text
ROUTE = HELD
BASIS = ...
REOPEN_IF = ...
```

That is substantially stronger than remembering only "we decided not to do X."

But the first implementation represents reopen predicates as literal tokens.
That creates two opposite failure modes:

1. **too permissive** — a weak event carries the expected label and reopens a
   route without actually satisfying the intended burden;
2. **too brittle** — genuinely novel evidence satisfies the underlying reason
   for reopening but uses different vocabulary and remains blocked forever.

The final P1 attack targets both directions.

## Hypothesis under attack

Reopen semantics should be based on **structured evidence properties**, not on a
magic event-name string.

A route may reopen only when all declared requirement predicates are satisfied
by current evidence.

## Structured model under test

A reopen policy will bind:

```text
ROUTE
POLICY VERSION
AUTHORITY SOURCE
REQUIREMENTS
```

Each requirement is satisfied by evidence whose structured attributes meet the
predicate.

The first bounded attributes include concepts such as:

```text
scope
kind
materiality
provenance_verified
status
```

This is deliberately not free-form LLM semantic matching.

## Injected failures

The attack will deliberately attempt to reopen a held route with:

1. a correctly named but **non-material** evidence event;
2. a material event with **unverified provenance**;
3. material evidence for the **wrong scope**;
4. material evidence without the required fresh preregistration;
5. a preregistration without the required material evidence;
6. a route that has already reopened.

All must remain blocked where appropriate.

## Novel-evidence control

A genuinely new evidence kind not named by the old literal vocabulary must be
able to satisfy the reopen burden when its structured properties are right.

Example:

```text
kind = REPLICATION_ANOMALY
materiality = MATERIAL
provenance_verified = true
scope = FCP27
```

should be able to satisfy a requirement for material verified FCP27 evidence
even though the string `REPLICATION_ANOMALY` was never hard-coded into the
closure rule.

This is the primary anti-brittleness control.

## Positive controls

The prototype must also demonstrate:

1. a complete structured evidence packet reopens the route;
2. the matched evidence IDs and requirement IDs are recorded durably;
3. an authorized actor is still required to perform the reopen transition;
4. literal labels alone do not override failed structured predicates.

## Preregistered dispositions

### A — FAIL

Either weak/labeled evidence can reopen a route incorrectly, or genuinely novel
evidence cannot satisfy the burden without changing the policy vocabulary.

### B — PARTIAL

Structured matching prevents trivial false reopening but remains tied to
specific evidence-kind names or cannot explain why the route remains held.

### C — PASS WITH BOUNDED SCOPE

The prototype:

- blocks the deliberately weak/incorrect evidence packets;
- permits genuinely novel evidence based on structured properties;
- requires all declared reopen requirements;
- records which evidence satisfied which requirement;
- requires proper reopen authority;
- prevents repeat reopening;
- preserves all earlier CCP-0/CCP-1 tests.

## Important limitation

Even outcome C would **not** prove that a reopen policy is correctly authored.

A policy can still encode the wrong:

- materiality definition;
- scope;
- provenance requirement;
- number/type of independent evidence items;
- authority source.

The result can establish:

```text
EVIDENCE SATISFIES DECLARED STRUCTURED REOPEN POLICY
```

but not:

```text
DECLARED REOPEN POLICY IS EPISTEMICALLY COMPLETE
```

That higher-order problem remains for policy review, domain-specific
adjudication, and blind trials.

## Boundary

```text
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
NATURAL_LANGUAGE_SEMANTIC_MATCHING = NOT_USED
```
