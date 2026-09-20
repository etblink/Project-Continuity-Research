# CCP-1 Authority-Spoofing Result 0.1.0

Date: 2026-09-20  
Status: bounded P1 slice complete

## Preregistered question

Can an actor obtain a materially valid phase transition merely by supplying a
plausible authority label?

## Result

```text
AUTHORITY_SPOOFING_SLICE = SURVIVED_INITIAL_BOUNDED_ATTACK
CCP0_REGRESSION = PASS
LIVE_PROJECT_MUTATION = NONE
```

The implementation separates:

```text
ACTOR IDENTITY
ROLE
GRANTED ACTION
GRANTED SCOPE
AUTHORITY SOURCE
GRANTOR
```

Caller-provided role claims are recorded only as metadata. Authorization is
derived from an active grant bound to the actor, action, and scope.

## Attack results

Seven CCP-1 tests pass:

1. spoofed `PROJECT_LEAD` label from an unprivileged worker is rejected;
2. a valid matching grant allows the same transition;
3. a real role used outside its granted scope is rejected;
4. direct public append of a material phase-state event is rejected;
5. an unprivileged actor cannot mint authority;
6. a properly authorized grantor can delegate bounded authority;
7. a revoked grant no longer authorizes the transition.

The delegated-reviewer control also demonstrates that a false claimed role does
not overwrite canonical authority: the accepted event records the actual
`RELEASE_REVIEWER` grant used.

## Regression result

The frozen CCP-0 suite was re-run against the same working tree before
publication:

```text
CCP0_TESTS = 27
CCP0_PASS = 27
CCP0_FAIL = 0

CCP1_AUTHORITY_TESTS = 7
CCP1_PASS = 7
CCP1_FAIL = 0
```

The tested CCP-1 implementation/test blobs are exactly:

```text
prototype/ccp1/authority.py
blob 8068511c6fe947cff6d2057f8355862cfdac4bec

prototype/ccp1/tests/test_authority_spoofing.py
blob da854fd16d7b15ac385505ce1dd990cd0aedd169

prototype/ccp1/README.md
blob cd92141bd61e06e089d7f950f6f3a4db56949180
```

These are the same blobs committed on the CCP-1 branch.

## What this result establishes

Within the semantic prototype boundary:

> **Authority is not a label.**

A materially valid transition now requires a durable relation of the form:

```text
ACTOR
  --holds grant from AUTHORITY SOURCE-->
ROLE
  --permits-->
ACTION
  --within-->
SCOPE
```

This directly attacks the CCP-0 weakness where an `authority=` string could be
asserted by the caller.

## What this result does not establish

This is not a production security model.

Open limitations include:

- principals are semantic identities, not cryptographically authenticated
  identities;
- grants are currently in-memory CCP-1 objects rather than durable accepted
  events;
- `authority_source` is recorded but not yet independently verified;
- bootstrap import remains a trusted boundary;
- the simple scope matcher has not yet been attacked for ambiguity or
  confused-deputy behavior;
- Python callers with arbitrary in-process code execution are outside this
  semantic authorization boundary;
- only material phase transitions are protected in this first slice.

These limits mean the correct disposition is not `AUTHORITY_SOLVED`.

## Disposition

```text
P1_AUTHORITY_SPOOFING = INITIAL_BOUNDED_PASS
NEXT_P1 = BAD_POLICY_ENFORCEMENT
AUTHORITY_DURABILITY_AND_IDENTITY_AUTHENTICATION = OPEN
```
