# CCP-1 Evidence-Authenticity Attack 0.1.0

Date: 2026-09-20  
Status: **PREREGISTERED — NOT YET ADJUDICATED**

## Question

CCP-0 requires evidence references to exist in the source registry.

That prevents unknown references, but it does not establish that a reference
actually resolves to the repository/revision/artifact the project believes it
does.

The attack is:

> Can a materially qualified claim become canonical using an evidence identifier
> whose external object is stale, mismatched, unavailable, or otherwise
> unverified?

## Hypothesis under attack

For evidence classes that support reproducible identity, the control plane
should distinguish:

```text
EVIDENCE REFERENCE EXISTS
```

from:

```text
EVIDENCE OBJECT VERIFIED
```

and a material evidence-backed promotion should depend on the latter.

## Bounded adapter model

The first adapter targets Git object identity.

A binding may name:

```text
repository
revision / commit SHA
path
expected blob SHA
```

A trusted resolver returns the actually observed object identity.

The adapter records:

- adapter ID/version;
- expected binding;
- observed identity;
- individual verification checks;
- overall PASS/FAIL;
- deterministic verification digest.

The resolver is an explicit trust boundary. This slice tests the semantics
around it; it does not claim that every resolver is trustworthy.

## Injected failures

The attack will deliberately attempt to use:

1. the wrong repository;
2. the wrong resolved commit;
3. the wrong file/blob SHA;
4. an unavailable object;
5. a failed verification record to qualify a material claim;
6. direct material claim qualification that bypasses evidence verification.

All must fail.

## Positive controls

The prototype must demonstrate that:

1. an exact repository/commit/path/blob identity verifies;
2. the same expected/observed identity reproduces the same verification digest;
3. a verified evidence object can support material claim qualification under
   proper authority;
4. the accepted claim records the exact verification digest(s) used;
5. changing a binding under the same evidence ID is rejected rather than
   silently rebinding history.

## Preregistered dispositions

### A — FAIL

A failed or unverified object can still qualify a material claim, or evidence
identity can silently rebind.

### B — PARTIAL

Object mismatches are detected, but claim promotion is not actually gated on
verification records or the result is not reproducibly bound.

### C — PASS WITH BOUNDED SCOPE

The prototype:

- detects the deliberately mismatched/unavailable Git objects;
- binds evidence ID to immutable expected identity;
- records deterministic verification results;
- prevents failed/unverified evidence from qualifying a material claim;
- records verification identity on an accepted claim;
- preserves all earlier suites.

## Important limitation

Even outcome C would **not** prove that the evidence entails the claim.

It establishes:

```text
THIS IS THE OBJECT WE SAID WE WERE USING
```

not:

```text
THIS OBJECT JUSTIFIES THE SCIENTIFIC / PRODUCT CONCLUSION
```

Entailment remains a domain-specific adjudication problem.

Likewise, the resolver is a trust boundary. Real deployment would require
reproducible remote reads, local Git verification, cryptographic hashes,
signatures where available, or other domain-appropriate mechanisms.

## Boundary

```text
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
EVIDENCE_ENTAILMENT = OUT_OF_SCOPE_FOR_THIS_SLICE
```
