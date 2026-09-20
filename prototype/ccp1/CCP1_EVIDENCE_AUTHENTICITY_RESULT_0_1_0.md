# CCP-1 Evidence-Authenticity Result 0.1.0

Date: 2026-09-20  
Status: **COMPLETE — SECONDARY CCP-1 EVIDENCE-AUTHENTICITY SLICE SURVIVES INITIAL BOUNDED ATTACK**

## Frozen implementation under adjudication

```text
IMPLEMENTATION_COMMIT =
c670f8f1ad3c5d1b0471b098978826a69a5d943a

prototype/ccp1/evidence.py
blob 1105dc528eaccf60e759f0d8578df078dcba3b1f

prototype/ccp1/tests/test_evidence.py
blob 7fab2ebe337c90de7f810de8c28ec31852ff57b1
```

## Preregistered disposition

```text
C — PASS WITH BOUNDED SCOPE
```

## Core result

The control plane now distinguishes:

```text
EVIDENCE REFERENCE EXISTS
```

from:

```text
EVIDENCE OBJECT VERIFIED
```

for a bounded Git-object evidence class.

A Git evidence binding records:

- repository;
- exact revision / commit SHA;
- optional path;
- optional expected blob SHA;
- immutable evidence ID.

A verification adapter compares that expected binding with the resolved object
identity and produces a deterministic verification record.

## Injected failures detected

The verifier rejected:

1. wrong repository;
2. wrong resolved commit;
3. wrong blob SHA;
4. unavailable object;
5. failed verification used for material claim qualification;
6. never-verified evidence used for qualification;
7. direct material-claim qualification bypass;
8. silent rebinding of an existing evidence ID.

A verified object still could not qualify a claim when the actor lacked the
required claim-qualification authority.

## Positive controls

The prototype demonstrated:

1. exact repository/commit/path/blob identity verifies;
2. identical expected/observed identity reproduces the same verification digest;
3. verified evidence may support a material claim under proper authority;
4. the accepted claim records the exact verification digest and binding digest;
5. the evidence reference recorded on the accepted claim is the same immutable
   evidence ID that was verified.

## CI verification

GitHub Actions run:

```text
RUN_ID = 35536525828
HEAD = c670f8f1ad3c5d1b0471b098978826a69a5d943a
CONCLUSION = success
```

Exact CI result:

```text
CCP0_REGRESSION_SUITE = 27 / 27 PASS
CCP1_ADVERSARIAL_SUITE = 51 / 51 PASS

TOTAL = 78 / 78 PASS
FAIL = 0
ERROR = 0
```

The evidence-authenticity slice contributes 10 tests beyond the prior 41-test
CCP-1 P1 family.

## What this establishes

Within the bounded adapter model:

> A material claim can now be gated on reproducible evidence-object identity
> rather than merely on the existence of a reference label.

The accepted claim can later answer:

```text
WHICH OBJECT IDENTITY WAS VERIFIED?
WHICH VERIFICATION RECORD WAS USED?
```

## What this does not establish

The verifier does **not** establish that the evidence entails the claim.

```text
OBJECT_IDENTITY_VERIFIED
!=
CLAIM_ENTAILMENT_VERIFIED
```

Open trust boundaries remain:

- resolver authenticity;
- remote Git hosting trust;
- cryptographic signature validation;
- local object/database corruption;
- domain-specific entailment;
- evidence freshness after verification;
- non-Git evidence classes;
- multiple independent evidence-source requirements.

## Disposition

```text
SECONDARY_EVIDENCE_AUTHENTICITY = C__PASS_WITH_BOUNDED_SCOPE
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED

NEXT_SECONDARY_ATTACK = INVALID_ACCEPTED_EVENT_CORRECTION
```
