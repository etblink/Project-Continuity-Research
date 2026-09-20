# CCP-1 — Adversarial Hardening Prototype

CCP-1 attacks the assumptions that survived CCP-0.

It remains read-only / shadow mode with respect to real projects.

## P1 attack sequence

1. authority spoofing — **complete: bounded pass**
2. bad-policy enforcement — **complete: disposition C**
3. stale / concurrent transitions — **complete: disposition C**
4. kernel omission — **complete: disposition C**
5. reopen-predicate brittleness — **complete: disposition C**

```text
P1_ATTACK_FAMILY = COMPLETE
```

## Verified P1 checkpoint

GitHub Actions run `35535927777`:

```text
CCP0_REGRESSION_SUITE  = 27 / 27 PASS
CCP1_ADVERSARIAL_SUITE = 41 / 41 PASS
TOTAL                  = 68 / 68 PASS
```

The CCP-0 prototype and its frozen 27-test suite remain unchanged under
`prototype/ccp0/` and serve as the regression baseline.

## Secondary CCP-1 program

Next bounded work:

1. evidence authenticity / reproducible evidence adapters;
2. disputed/invalid accepted-event correction;
3. authority durability / identity-authentication boundary;
4. orientation-contract quality;
5. supersession / graph scale;
6. project-agnostic portability;
7. blind cold-start and human usability when independent participants are
   available.

```text
LIVE_PROJECT_MUTATION = NOT_AUTHORIZED
CCP2 = NOT YET AUTHORIZED
```

Frozen result artifacts:

- `CCP1_AUTHORITY_SPOOFING_RESULT_0_1_0.md`
- `CCP1_BAD_POLICY_RESULT_0_1_0.md`
- `CCP1_STALE_CONCURRENT_TRANSITION_RESULT_0_1_0.md`
- `CCP1_KERNEL_OMISSION_RESULT_0_1_0.md`
- `CCP1_REOPEN_PREDICATE_RESULT_0_1_0.md`
- `CCP1_P1_ATTACK_FAMILY_RESULT_0_1_0.md`


## Secondary CCP-1 results

- Evidence authenticity / reproducible Git-object identity — **complete: disposition C, bounded pass**

Verified checkpoint:

```text
CCP0 = 27 / 27 PASS
CCP1 = 51 / 51 PASS
TOTAL = 78 / 78 PASS

NEXT_SECONDARY_ATTACK = INVALID_ACCEPTED_EVENT_CORRECTION
```

Frozen secondary result artifacts:

- `CCP1_EVIDENCE_AUTHENTICITY_RESULT_0_1_0.md`


- Accepted-event correction — **complete: disposition C, claim-level bounded pass**

Current verified checkpoint:

```text
CCP0 = 27 / 27 PASS
CCP1 = 60 / 60 PASS
TOTAL = 87 / 87 PASS

NEXT_SECONDARY_ATTACK = AUTHORITY_DURABILITY_AND_IDENTITY_BOUNDARY
```

Additional frozen result:

- `CCP1_ACCEPTED_EVENT_CORRECTION_RESULT_0_1_0.md`


- Authority durability / identity-authentication boundary — **complete: disposition C, bounded pass**

Current verified checkpoint:

```text
CCP0 = 27 / 27 PASS
CCP1 = 69 / 69 PASS
TOTAL = 96 / 96 PASS

NEXT_SECONDARY_ATTACK = ORIENTATION_CONTRACT_QUALITY
```

Additional frozen result:

- `CCP1_AUTHORITY_DURABILITY_IDENTITY_RESULT_0_1_0.md`


- Orientation-contract quality / external review — **complete: disposition C, bounded pass**

Current verified checkpoint:

```text
CCP0 = 27 / 27 PASS
CCP1 = 78 / 78 PASS
TOTAL = 105 / 105 PASS

NEXT_SECONDARY_ATTACK = SUPERSESSION_GRAPH_SCALE
```

Additional frozen result:

- `CCP1_ORIENTATION_CONTRACT_QUALITY_RESULT_0_1_0.md`


- Supersession graph scale / scoped chain resolution — **complete: disposition C, bounded pass**

Current verified checkpoint:

```text
CCP0 = 27 / 27 PASS
CCP1 = 88 / 88 PASS
TOTAL = 115 / 115 PASS

NEXT_SECONDARY_ATTACK = PROJECT_AGNOSTIC_PORTABILITY
```

Additional frozen result:

- `CCP1_SUPERSESSION_GRAPH_SCALE_RESULT_0_1_0.md`
