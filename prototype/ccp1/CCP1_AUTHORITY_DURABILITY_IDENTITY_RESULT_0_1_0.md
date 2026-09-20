# CCP-1 Authority Durability / Identity Boundary Result 0.1.0

Date: 2026-09-20  
Status: **COMPLETE — SECONDARY AUTHORITY-DURABILITY SLICE SURVIVES INITIAL BOUNDED ATTACK**

## Frozen implementation under adjudication

```text
IMPLEMENTATION_COMMIT =
c63372f85bf143d10a6882e0cf6e266ffa0ab2e9

prototype/ccp1/durable_authority.py
blob 3b1aae50d6a969b16e25f1e6c4e19461b11e339f

prototype/ccp1/tests/test_durable_authority.py
blob eb4af52b5fd5978e10536b38d89f5805ea453c27
```

## Preregistered disposition

```text
C — PASS WITH BOUNDED SCOPE
```

## Core result

The prototype now separates:

```text
DURABLE AUTHORITY STATE
```

from:

```text
CURRENT AUTHENTICATED ACTOR ASSERTION
```

Durable authority is represented by append-only events:

```text
PRINCIPAL_REGISTERED
AUTHORITY_GRANTED
AUTHORITY_REVOKED
```

A current action additionally requires a verified assertion from an explicitly
trusted authenticator whose external subject matches the principal binding.

## Injected failures detected

The bounded authority layer rejects:

1. a bare/self-claimed actor ID;
2. an assertion marked unverified;
3. a verified assertion from an untrusted authenticator;
4. a verified assertion whose external subject does not match the principal;
5. a grant to an unknown principal;
6. silent rebinding of a principal to another external subject;
7. use of a valid identity after its matching grant has been revoked.

## Positive controls

The prototype demonstrates:

1. active grants survive authority-log replay;
2. revoked grants remain revoked after replay;
3. authority digest is identical before and after deterministic replay;
4. a verified assertion from a trusted authenticator may exercise a matching
   active grant;
5. the same authenticated identity immediately loses authorization after grant
   revocation.

## CI verification

GitHub Actions run:

```text
RUN_ID = 35537637524
HEAD = c63372f85bf143d10a6882e0cf6e266ffa0ab2e9
JOB = 106149405021
CONCLUSION = success
```

Exact CI result:

```text
CCP0_REGRESSION_SUITE = 27 / 27 PASS
CCP1_ADVERSARIAL_SUITE = 69 / 69 PASS

TOTAL = 96 / 96 PASS
FAIL = 0
ERROR = 0
```

The authority durability / identity slice contributes 9 tests beyond the prior
60-test CCP-1 checkpoint.

## What this establishes

Within the semantic boundary:

```text
AUTHENTICATION = who is acting
AUTHORIZATION = what the authenticated actor may do
```

Those are now explicit and independently evaluated.

Authority is no longer dependent on conversational/in-memory continuity:
principal, grant, and revocation state can be reconstructed from an append-only
authority log.

## What this does not establish

No cryptographic authentication system was implemented.

The trusted authenticator remains an explicit trust boundary.

Still open:

- signature verification;
- OAuth/OIDC/JWT validation;
- SSH or hardware-key authentication;
- key rotation;
- credential compromise recovery;
- authenticator trust governance;
- durable storage transactions around authority events;
- integration of this durable registry into every earlier CCP-1 semantic layer.

## Disposition

```text
SECONDARY_AUTHORITY_DURABILITY_IDENTITY =
C__PASS_WITH_BOUNDED_SCOPE

LIVE_PROJECT_MUTATION = NOT_AUTHORIZED

NEXT_SECONDARY_ATTACK = ORIENTATION_CONTRACT_QUALITY
```
