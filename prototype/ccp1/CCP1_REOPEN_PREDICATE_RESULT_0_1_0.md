# CCP-1 Reopen-Predicate Brittleness Result 0.1.0

Date: 2026-09-20  
Status: **COMPLETE — FINAL P1 SLICE SURVIVES INITIAL BOUNDED ATTACK**

## Frozen implementation under adjudication

```text
IMPLEMENTATION_COMMIT =
706e97f40b20991f217513890e870e9146f4b177

prototype/ccp1/reopen.py
blob d2491b093670b8495f7ae4f056fd1fc182324ffa

prototype/ccp1/tests/test_reopen.py
blob 0e156b01a6d1a5427aec181c5fc3b7fbd4c73062
```

The implementation also introduced the first repository-native semantic test
workflow:

```text
.github/workflows/ccp-tests.yml
blob 45fd6ec64c59346bb6c4c13c38a770bc9aca55f3
```

## Preregistered disposition

```text
C — PASS WITH BOUNDED SCOPE
```

## Core result

The first negative-knowledge model used literal reopen tokens.

The hardened model instead evaluates structured evidence attributes against
explicit requirements.

The route no longer asks:

```text
DID EVENT NAMED "MATERIAL_EVIDENCE_EVENT" OCCUR?
```

It asks whether evidence satisfies properties such as:

```text
scope = FCP27
materiality = MATERIAL
provenance_verified = true
```

together with the independently required preregistration condition.

## Injected failures detected

The route remained held when presented with:

1. a correctly named but non-material evidence event;
2. material evidence with unverified provenance;
3. material evidence for the wrong scope;
4. material evidence without fresh preregistration;
5. preregistration without material evidence;
6. an attempt to reopen a route that was already open.

An unprivileged actor with an otherwise complete evidence packet also remained
unable to reopen the route.

## Anti-brittleness control

A genuinely novel evidence kind:

```text
kind = REPLICATION_ANOMALY
materiality = MATERIAL
provenance_verified = true
scope = FCP27
```

successfully satisfied the material-evidence burden even though the string
`REPLICATION_ANOMALY` was never hard-coded into that requirement.

This is the key distinction:

```text
EVIDENCE VOCABULARY
!=
EVIDENCE BURDEN
```

## Durable reopening record

A successful structured reopen records:

- reopen-policy version;
- reopen-policy digest;
- policy authority source;
- requirement IDs;
- evidence fact IDs satisfying each requirement;
- authority grant used for the reopen action.

Therefore the system can later answer not only:

```text
WHY DID THIS ROUTE REOPEN?
```

but:

```text
WHICH DECLARED BURDEN DID EACH EVIDENCE ITEM SATISFY?
```

## CI verification

GitHub Actions run:

```text
RUN_ID = 35535927777
HEAD = 706e97f40b20991f217513890e870e9146f4b177
CONCLUSION = success
```

Exact CI result:

```text
CCP0_REGRESSION_SUITE = 27 / 27 PASS
CCP1_ADVERSARIAL_SUITE = 41 / 41 PASS

TOTAL = 68 / 68 PASS
FAIL = 0
ERROR = 0
```

The CCP-1 suite contains:

```text
authority spoofing       7
bad-policy enforcement   9
stale/concurrent         9
kernel omission          7
reopen predicates        9
--------------------------
total                    41
```

## What this establishes

Within the semantic prototype boundary:

> **Negative knowledge can be durable without requiring the future to use the
> exact vocabulary of the past.**

The route remains closed against weak or mislabeled evidence while allowing
genuinely novel evidence to satisfy the underlying structured burden.

## What this does not establish

The structured policy can still be wrong.

Open questions include:

- whether materiality is defined correctly;
- whether provenance verification is trustworthy;
- whether multiple independent evidence items should be required;
- whether the scope ontology is correct;
- whether new evidence attributes require policy migration;
- whether humans/agents can author good reopen policies consistently;
- whether structured fields become a hidden rigid ontology over time.

This result establishes better **predicate semantics**, not epistemic
infallibility.

## Disposition

```text
P1_REOPEN_PREDICATE_BRITTLENESS = C__PASS_WITH_BOUNDED_SCOPE

P1_ATTACK_FAMILY = COMPLETE
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED

NEXT_GATE =
FREEZE_P1_FAMILY_RESULT
THEN_BEGIN_SECONDARY_CCP1_ATTACKS
```
