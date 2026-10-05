# CPI-0 Stage-7A Native Trust-Root Bootstrap Architecture Report 0.1.0

Date: 2026-10-04
Status: FROZEN STAGE REPORT
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #41

## 1. Prior controlling boundary

Stage-6 authority-architecture research closure:

`879005a6bbd40d123c24a1d87d77a8ad6b74f53b`

Stage-6 independent endpoint:

- Stage-6T audit commit `8b6c872cf7a2dd84c618aa2b92c64c02ed9d1014`
- exact report blob `00f856c9088b3ec24f5e350e124d977ff651b085`
- S3=0 / S2=0 / S1=0
- Signed Authority Capsule architecture qualified for research-reference observed-history scope.

Stage 7A addresses only the first open adoption prerequisite:

`NATIVE PUBLIC-KEY BOOTSTRAP / TRUST-ROOT ESTABLISHMENT`

Authenticated completeness/currentness remains outside scope.

## 2. Preregistration

Frozen before architecture scoring:

`prototype/cpi0/stage7a/STAGE7A_NATIVE_TRUST_ROOT_BOOTSTRAP_PREREGISTRATION_0_1_0.md`

Commit:

`97e61e35187e1235d793aec24aad94d39633921a`

Blob:

`1ef9ead177da7af3f3025a1993694730fbad01f5`

The preregistration froze:

- threat model;
- bootstrap axiom under test;
- Candidates A-F;
- 15 scoring criteria;
- seven hard gates;
- 20 falsification cases;
- mutation boundary;
- selection rule.

## 3. No-trust-from-nothing result

The preregistered proposition survived scoring:

`NO TRUST FROM NOTHING = PASS`

A first Authority Capsule root cannot establish its own native authority merely through:

- self-signature;
- first observation;
- same-account provider publication.

A bootstrap architecture must expose at least one independent trust assumption.

## 4. Architecture selection

Frozen scorecard:

`prototype/cpi0/stage7a/STAGE7A_NATIVE_TRUST_ROOT_SCORECARD_AND_SELECTION_0_1_0.md`

Commit:

`ffe33046533bd0fd21e08e9256f98420e701f438`

Blob:

`8002b0bdcd03dc0f4c10930ff36cb0ed19b13456`

Selection:

```text
SELECTED_BOOTSTRAP_ARCHITECTURE =
F__NATIVE_BOOTSTRAP_MANIFEST_WITH_EXPLICIT_ANCHOR_POLICY

MINIMUM_QUALIFYING_TRUST_PROFILE =
D__SINGLE_PREEXISTING_INDEPENDENT_ANCHOR

OPTIONAL_HIGHER_ASSURANCE_PROFILE =
E__THRESHOLD_MULTI_ANCHOR
```

Candidates A/B/C fail hard gates.

Candidate D is the minimum qualifying trust model.

Candidate E qualifies but is not required as the default because of substantially higher burden.

Candidate F is selected as the project-neutral representation and verification boundary and requires at least one Candidate-D-style independent anchor.

## 5. Hive Active-authority profile

User-proposed concrete profile:

`HIVE_ACTIVE_AUTHORITY_ANCHOR`

Profile note:

`prototype/cpi0/stage7a/STAGE7A_HIVE_ACTIVE_AUTHORITY_ANCHOR_PROFILE_NOTE_0_1_0.md`

Commit:

`c82c9b5b9ba7ec78c9b670840d132e0c8d26fecf`

Blob:

`19e5604202994ef84806f77c8b1dc526dd6b28f9`

Research interpretation:

```text
signing interface = Hive Keychain
bootstrap anchor = pre-existing Hive account Active authority
example native account = @etblink
profile = HIVE_ACTIVE_AUTHORITY_V1
```

Hive Keychain is not itself the trust root.

A successful Keychain callback is not authority evidence.

A qualifying verifier must establish both:

1. the exact bootstrap statement signature;
2. that the signer set satisfies the declared Hive account's Active authority.

A Hive signature proves control of the Hive authority only after the account-authority relationship is established.

The native project must independently choose that exact Hive account/authority as its bootstrap anchor.

## 6. External reference sanity check

Stage 7A checked current official Hive documentation.

Observed relevant facts:

- Hive Keychain exposes `requestSignBuffer` with Posting, Active or Memo key roles;
- Hive APIs expose `verify_account_authority`, which checks whether supplied public keys satisfy an account authority level;
- Hive account authorities include thresholds, key authorities and account authorities.

These facts support the plausibility of `HIVE_ACTIVE_AUTHORITY_V1`.

They do not establish historical/offline authority-state proof and do not constitute native adoption.

## 7. Formal manifest semantics

Specification:

`prototype/cpi0/stage7a/NATIVE_BOOTSTRAP_MANIFEST_RESEARCH_SPEC_0_1_0.md`

Commit:

`7902b49aedb94b70005adeab6e395330cb31e638`

Blob:

`77d1e925ab48d82e82a45fd5d63f978509be6b03`

The manifest binds exactly:

- project;
- authority domain;
- candidate Authority Capsule key ID;
- bootstrap policy;
- generation;
- challenge;
- anchor profile;
- anchor subject;
- optional note digest.

Canonical artifact semantics use RFC 8785 / JCS over strings/null only.

The common anchor statement is domain-separated and signs the exact manifest SHA-256.

## 8. Trust semantics

Stage 7A formally separates:

```text
CANDIDATE KEY POSSESSION
!=
INDEPENDENT ANCHOR CONTROL
!=
NATIVE AUTHORIZATION TO TRUST THE KEY
```

Successful bootstrap verification means only:

`GIVEN THE INDEPENDENTLY SUPPLIED NATIVE POLICY, A QUALIFYING INDEPENDENT ANCHOR AUTHENTICATED THIS EXACT INITIAL ROOT BINDING.`

The verifier does not prove the native policy from nothing.

The verifier must not silently substitute its own anchor or policy.

## 9. Research prototype

Implementation:

`prototype/cpi0/stage7a/native_bootstrap_manifest.py`

Blob:

`e81cfa911d024c5bd8bc2db6d20656b6ca40a2e5`

Adversarial tests:

`prototype/cpi0/stage7a/test_native_bootstrap_manifest.py`

Blob:

`4d8243819b38e71be2096e539886c0fcec685d89`

Requirements:

`prototype/cpi0/stage7a/requirements.txt`

Blob:

`c011dd5d074245a5d49692b0d7044fd80d8a855f`

Workflow:

`.github/workflows/cpi0-stage7a.yml`

Blob:

`489088eafaf93c962f76a12d54b4db193534e164`

## 10. Prototype scope

Implemented:

- canonical Native Bootstrap Manifest;
- independently supplied native policy;
- exact policy/manifest matching;
- synthetic `OFFLINE_ED25519_V1` independent anchor;
- domain-separated anchor proof;
- root substitution/replay checks;
- duplicate canonical proof deduplication;
- conflicting independently valid genesis roots fail closed;
- offline replay;
- CPI consequence separation.

Intentionally not implemented:

`HIVE_ACTIVE_AUTHORITY_V1`

The Hive profile fails closed with `UnsupportedAnchorProfileError`.

This prevents Stage 7A from claiming Hive/Keychain qualification before Hive-specific cryptographic and authority-state verification is implemented and independently audited.

## 11. Exact qualification

Qualified head:

`d134bdf5a7d487a2052db0466368552bdf1ef05a`

GitHub Actions run:

`37256735898`

Result:

`SUCCESS`

Observed:

```text
CRYPTOGRAPHY_VERSION = 46.0.4
Ran 30 tests in 0.020s
OK

STAGE7A_BOOTSTRAP_FRAMEWORK = PASS
TRUST_ROOT_ESTABLISHED_FOR_OBSERVED_POLICY = True
EXECUTION_AUTHORIZED_BY_CPI = False
HIVE_PROFILE_IMPLEMENTED = False
MANIFEST_DIGEST =
6b15a0f2037a201ee1de1a47c11b26ed14b2bf5da7ce3bfbaf4b635b56853a0c
```

## 12. Required falsification evidence

The committed suite demonstrates at prototype scope:

- candidate self-signature has no bootstrap path;
- provider prose has no bootstrap path;
- wrong independent anchor fails;
- project/domain/candidate/policy/generation/challenge/anchor substitution fails;
- missing proof fails;
- duplicate identical proofs deduplicate;
- two distinct independently valid genesis manifests conflict and fail closed;
- offline replay succeeds;
- CPI execution authorization remains false;
- duplicate-key / noncanonical manifest forms fail;
- Hive profile is fail-closed while unimplemented;
- Keychain callback state is not an authority input;
- native policy is a distinct independent input;
- manifest digest binds every authority field;
- candidate private key is not required to authorize its public root identity.

## 13. Open issue exposed by the prototype

A verifier can only evaluate trust relative to the independently supplied native policy.

Therefore:

`NATIVE POLICY DISTRIBUTION / PROVENANCE REMAINS AN EXPLICIT TRUST ASSUMPTION`

This is not hidden.

A real adoption must define how a human/native project establishes and preserves the policy that says, for example:

`HIVE MAINNET @etblink ACTIVE AUTHORITY IS THE BOOTSTRAP ANCHOR FOR THIS PROJECT/DOMAIN`.

## 14. Hive-specific next research

The selected Hive profile requires a later bounded implementation/audit of:

- exact Keychain `requestSignBuffer` message bytes;
- Hive compact secp256k1 signature recovery/verification;
- exact public key encoding;
- Active authority threshold evaluation;
- nested account-authority behavior;
- authority-state snapshot/binding;
- historical/offline replay claims;
- profile-specific contradiction/conflict handling.

A live @etblink signature is not required for that research and must not be requested before synthetic verification is independently qualified.

## 15. Mutation / adoption boundary

Stage 7A changed only Project-Continuity-Research.

```text
HIVENUES = NONE
NFC = NONE
FCP = NONE
PGH = NONE
EVIDENCE_BASED_MARKET_METHODS = NONE
PROJECT_OBSERVATORY = NONE
REAL_OWNER_KEY = NONE
REAL_HIVE_SIGNATURE = NONE
HIVE_BROADCAST = NONE
NATIVE_TRUST_ROOT = NONE
NATIVE_ADOPTION = NONE
CURRENTNESS_PROTOCOL = NONE
LIVE_FEDERATION = NONE
```

## 16. False bridge / optionality

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

`FEDERATION_OPTIONALITY = PASS`

## 17. Stage disposition

Self-evidence only:

```text
NO_TRUST_FROM_NOTHING = PASS
ARCHITECTURE_SELECTION =
F__NATIVE_BOOTSTRAP_MANIFEST_WITH_EXPLICIT_ANCHOR_POLICY
MINIMUM_TRUST_PROFILE =
D__SINGLE_PREEXISTING_INDEPENDENT_ANCHOR
COMMON_FRAMEWORK_PROTOTYPE = PASS
HIVE_ACTIVE_PROFILE = SPECIFIED__NOT_IMPLEMENTED
INDEPENDENT_CLOSURE = NOT CLAIMED
```

Final Stage-7A disposition:

`BOOTSTRAP_ARCHITECTURE_SELECTION_PASS__INDEPENDENT_REAUDIT_REQUIRED`

A fresh independent evaluator must re-score the bootstrap candidates, challenge the no-trust-from-nothing conclusion, execute/attack the common prototype, and determine whether Candidate F/D is actually justified before any Hive-profile implementation or native adoption proceeds.
