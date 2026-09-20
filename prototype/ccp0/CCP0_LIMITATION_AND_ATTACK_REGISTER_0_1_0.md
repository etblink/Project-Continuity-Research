# CCP-0 Limitation and Attack Register 0.1.0

Date: 2026-09-20  
Status: Open limitation register following CCP-0.

## Purpose

A passing semantic prototype is dangerous if its omissions are mistaken for
solved problems.

This register records the assumptions and attack surfaces that remain open.

## L-01 — Authority is asserted, not independently authenticated

CCP-0 records authority labels such as:

```text
PROJECT_LEAD
CANONICAL_FCP
SNAPSHOT
INDEPENDENT_ADJUDICATION
```

but does not cryptographically or institutionally prove that the actor actually
possesses that authority.

### Consequence

A dishonest or mistaken caller can submit a correctly shaped event under an
incorrect authority label.

### Required CCP-1 work

Separate:

```text
ACTOR IDENTITY
ROLE
GRANTED AUTHORITY
SCOPE
AUTHORITY SOURCE
```

and test unauthorized transitions.

---

## L-02 — Policy correctness remains an upstream assumption

A typed transition system can perfectly enforce a bad policy.

CCP-0 tests:

```text
does the guard fire?
```

It does not prove:

```text
is this the right guard?
```

### Required CCP-1 work

Add policy provenance, version migration, independent policy review, and
regression tests against the incident corpus.

---

## L-03 — Evidence authenticity is not verified

Evidence references must exist in the source registry, but CCP-0 does not
verify:

- file hashes;
- Git ancestry;
- repository ownership;
- signatures;
- remote authenticity;
- whether the evidence actually entails the claim.

### Required CCP-1 work

Introduce evidence adapters with reproducible identifiers and verification
results.

---

## L-04 — Evidence-to-claim entailment remains domain-specific

CCP-0's outcome burden model is intentionally simple.

Real scientific/product adjudication may require:

- logical entailment;
- quantitative thresholds;
- multiple independent sources;
- human review;
- uncertainty intervals;
- contradiction resolution.

### Required CCP-1 work

Keep the control-plane semantics generic while allowing domain-specific
adjudicators.

---

## L-05 — No concurrency model

The prototype is single-process.

It does not test two agents simultaneously attempting:

- conflicting state transitions;
- duplicate acceptance;
- stale writes;
- authority races;
- independent supersession.

### Required CCP-1 work

Add expected-version / compare-and-swap semantics and adversarial concurrency
tests.

---

## L-06 — Event append is not externally durable

The append-only ledger is in memory during the experiment.

### Required CCP-1 work

Use a durable append format or lightweight database while preserving:

- deterministic replay;
- portable export;
- human inspectability;
- cryptographic integrity where appropriate.

---

## L-07 — External freshness is observation freshness, not truth freshness

If a repository ref still points at the same SHA, CCP-0 can say it matches the
frozen boundary.

That does not establish that the underlying claim remains scientifically or
product-wise adequate.

### Required CCP-1 work

Keep:

```text
SOURCE REVISION FRESHNESS
```

separate from:

```text
CLAIM / WORLD FRESHNESS
```

---

## L-08 — Project intent can still be underspecified

The prototype version-tracks purpose, but a short purpose statement may fail to
capture the actual good the project exists to serve.

This is where the Agape hypothesis remains only partly operationalized.

### Required CCP-1 work

Experiment with a compact intent object containing:

- beneficiary / stakeholder;
- purpose;
- unacceptable tradeoffs;
- human-agency boundary;
- end-state / success criteria.

Avoid turning this into an enormous manifesto.

---

## L-09 — The third authority/action dimension remains unnamed and underspecified

The architecture clearly needs a distinction between:

```text
what is true
what is good / intended
what is permitted / warranted now
```

but the philosophical and formal relationship among these is still open.

### Required research

Do not force a name yet. Test whether authority/action semantics decompose into
existing concepts such as authorization, stewardship, prudence, or practical
reason.

---

## L-10 — Human cold-start usability is untested

CCP-0 was written and interpreted by the researchers who designed it.

### Required CCP-1 / later work

A person who did not invent the protocol must be able to:

- understand the kernel;
- inspect why a route is held;
- determine what would reopen it;
- understand why a transition was rejected;
- distinguish historical from current state.

---

## L-11 — Agent cold-start usability is only indirectly tested

Historical replay shows the semantics can encode the right answer.

It does not yet prove that a fresh model can consume the generated kernel and
control-plane views and orient correctly without hidden conversation history.

### Required CCP-1 work

Blind successor trial with only generated artifacts.

---

## L-12 — Negative knowledge may overconstrain discovery

A route with strong closure semantics can prevent pointless repetition.

It can also become institutionalized blindness if the reopen predicate is too
narrow.

### Required CCP-1 attack

Construct cases where genuinely novel evidence should reopen a route but does
not match the old vocabulary exactly.

Test semantic rather than merely literal reopen criteria.

---

## L-13 — Scoped supersession can become excessively granular

Claim-level supersession is powerful but may create a graph too complex for
humans to audit.

### Required CCP-1 work

Measure:

- graph size;
- kernel compression;
- number of active supersession edges;
- human comprehension.

---

## L-14 — Kernel generation can still omit something important

Freshness proves that a kernel corresponds to the current projection.

It does **not** prove that the projection selected the right things to show.

### Required CCP-1 work

Treat kernel generation as a lossy orientation function and test omission
failures explicitly.

This may become one of the most important future adversarial classes.

---

## L-15 — No recovery from a corrupted accepted ledger

CCP-0 assumes accepted events are durable truth once appended.

### Required CCP-1 work

Define:

- invalid-event discovery;
- compensating correction;
- disputed-event state;
- forensic preservation;
- no silent deletion.

---

# Attack priority

Highest-value next attacks:

```text
P1 authority spoofing
P1 bad-policy enforcement
P1 stale/concurrent transition
P1 kernel omission
P1 reopen-predicate brittleness

P2 evidence-authenticity failure
P2 ledger correction / disputed event
P2 cold-start successor confusion
P2 human usability

P3 scaling / performance
P3 UI
```

The prototype should not advance to live mutation of real projects until the P1
attack family has been exercised.
