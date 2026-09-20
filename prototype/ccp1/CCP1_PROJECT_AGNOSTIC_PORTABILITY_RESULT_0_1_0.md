# CCP-1 Project-Agnostic Portability Result 0.1.0

Date: 2026-09-20  
Status: **COMPLETE — SECONDARY PORTABILITY SLICE SURVIVES INITIAL BOUNDED ATTACK**

## Frozen implementation under adjudication

```text
IMPLEMENTATION_COMMIT =
b76a6fc3fc0e6e117bb914531a657cd112643482

prototype/ccp1/portability.py
blob a7647b127f835d5c5e55b2ce6959477a8bc40f3e

prototype/ccp1/tests/test_portability.py
blob d7129ae314571bfdce7eae8df3986adff9842f60
```

## Preregistered disposition

```text
C — PASS WITH BOUNDED SCOPE
```

## Core result

The same unchanged semantic engine was instantiated from configuration for four
materially different project vocabularies:

1. software/product release;
2. scientific/research adjudication;
3. creative/editorial publication;
4. an opaque synthetic domain using intentionally meaningless identifiers.

Each profile supplied domain vocabulary only as data:

```text
PURPOSE
PHASE SUBJECT
FROM STATE
TO STATE
TRANSITION NAME
REQUIRED ACTION
AUTHORITY SCOPE
HELD ROUTE
HOLD BASIS
```

No domain-specific branch was added to the core transition/orientation engine.

## Injected failures detected

The bounded portability layer rejected or safely handled:

1. missing required profile semantics;
2. unauthorized actor transitions in every domain;
3. operation kernels omitting the domain's held route;
4. cross-profile state leakage.

The opaque profile also succeeded despite identifiers carrying no useful human
semantic cues.

## Positive controls

All four profiles demonstrated the same semantics for:

- authority/action/scope;
- active policy identity;
- phase state;
- held negative knowledge;
- operation-scoped orientation;
- kernel freshness and sufficiency;
- authorized transition execution;
- unauthorized transition rejection.

Profile identity is deterministic and digest-bound.

## CI verification

GitHub Actions run:

```text
RUN_ID = 35542032351
HEAD = b76a6fc3fc0e6e117bb914531a657cd112643482
JOB = 106161303490
CONCLUSION = success
```

Exact CI result:

```text
CCP0_REGRESSION_SUITE = 27 / 27 PASS
CCP1_ADVERSARIAL_SUITE = 97 / 97 PASS

TOTAL = 124 / 124 PASS
FAIL = 0
ERROR = 0
```

The portability slice contributes 9 tests beyond the prior 88-test CCP-1
checkpoint.

## What this establishes

Within the bounded profile surface:

> The current semantic engine is not trivially dependent on HiVenues/FCP/NFC
> vocabulary.

The opaque control is particularly useful because successful behavior cannot be
explained by semantic recognition of familiar project nouns.

## What this does not establish

This is not universal portability.

The profiles were still designed inside this research program.

Still required:

- genuinely independent projects;
- unfamiliar users;
- non-Git evidence adapters;
- authority systems unlike the current grant model;
- blind successor trials;
- human usability testing.

## Disposition

```text
SECONDARY_PROJECT_AGNOSTIC_PORTABILITY =
C__PASS_WITH_BOUNDED_SCOPE

AUTONOMOUS_SECONDARY_ATTACK_SET = COMPLETE

LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
CCP2 = NOT YET AUTHORIZED

NEXT_GATE =
BLIND_AGENT_COLD_START
AND
HUMAN_COLD_START_USABILITY
```
