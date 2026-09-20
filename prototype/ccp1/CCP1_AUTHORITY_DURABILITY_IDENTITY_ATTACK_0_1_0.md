# CCP-1 Authority Durability / Identity Boundary Attack 0.1.0

Date: 2026-09-20  
Status: **PREREGISTERED — NOT YET ADJUDICATED**

## Question

The first CCP-1 authority layer fixed one semantic flaw:

```text
CALLER-SUPPLIED ROLE LABEL != AUTHORITY
```

But its principal/grant registry is still in-memory state.

That leaves two distinct risks:

1. authority does not survive process restart unless somebody reconstructs it;
2. a caller may present an actor ID without proving that the current session is
   actually bound to that actor.

## Hypothesis under attack

The control plane should distinguish:

```text
DURABLE AUTHORITY STATE
```

from:

```text
CURRENT AUTHENTICATED ACTOR ASSERTION
```

and require both.

## Durable authority model under test

The bounded prototype will represent authority changes as append-only authority
events:

```text
PRINCIPAL_REGISTERED
AUTHORITY_GRANTED
AUTHORITY_REVOKED
```

Replaying those events into a fresh registry must reproduce the same active
principals, grants, revocations, and authority digest.

## Identity-authentication boundary under test

A transition-facing authority check must consume a verified actor assertion,
not a bare actor string.

The first assertion object will bind:

- actor ID;
- external subject identity;
- authenticator ID;
- verification status;
- authentication context / evidence identifier.

The semantic prototype will maintain an explicit allow-list of trusted
authenticator IDs.

This does **not** implement cryptography. The authenticator is an explicit trust
boundary whose result must be independently supplied.

## Injected failures

The attack will deliberately attempt to:

1. authorize with only a bare/self-claimed actor ID;
2. use an assertion marked unverified;
3. use an assertion from an untrusted authenticator;
4. use a verified assertion whose external subject does not match the registered
   principal identity;
5. grant authority to an unknown principal;
6. silently change a principal's bound external subject;
7. replay a durable authority log but accidentally resurrect a revoked grant;
8. use a valid identity assertion after the actor's matching grant was revoked.

All must fail.

## Positive controls

The prototype must demonstrate that:

1. principal registration + grant + revocation events replay deterministically;
2. a grant that was active at shutdown remains active after replay;
3. a revoked grant remains revoked after replay;
4. authority digest is identical before and after replay;
5. a verified assertion from a trusted authenticator for the correct external
   subject may exercise a currently active matching grant;
6. the same authenticated actor loses authority immediately after revocation
   without changing identity.

## Preregistered dispositions

### A — FAIL

Authority cannot be reconstructed after restart or a bare/unverified identity
claim can exercise authority.

### B — PARTIAL

Durable replay works, but the actor-authentication boundary remains implicit or
revocation does not survive replay reliably.

### C — PASS WITH BOUNDED SCOPE

The prototype:

- event-sources principal/grant/revocation state;
- reproduces authority state and digest after replay;
- rejects bare identity claims;
- rejects unverified/untrusted/mismatched actor assertions;
- preserves revocation through replay;
- separates identity verification from authorization;
- preserves all earlier suites.

## Important limitation

Even outcome C would not establish secure authentication.

The prototype does not implement:

- signatures;
- OAuth/OIDC token validation;
- SSH key verification;
- hardware-backed identity;
- certificate chains;
- key rotation;
- credential compromise recovery.

It establishes only the **architectural boundary**:

```text
AUTHENTICATION PROVES WHO IS ACTING
AUTHORIZATION DETERMINES WHAT THAT ACTOR MAY DO
```

and makes both explicit inputs to the control plane.

## Boundary

```text
LIVE_PROJECT_MUTATION = NOT AUTHORIZED
CRYPTOGRAPHIC_AUTHENTICATION = OUT_OF_SCOPE_FOR_THIS_SLICE
```
