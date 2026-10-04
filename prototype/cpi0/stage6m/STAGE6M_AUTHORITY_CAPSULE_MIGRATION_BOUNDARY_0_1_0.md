# CPI-0 Stage-6M Authority Capsule Migration and Adoption Boundary 0.1.0

Date: 2026-10-04
Status: FROZEN RESEARCH BOUNDARY
Program: CPI-0 — Cross-Project Interoperability
Stage: 6M
Governing issue: #32

## 1. Result scope

Stage 6M selects the Signed Authority Capsule architecture for **research prototype purposes**.

This is not an adoption decision for HiVenues or any other native project.

`ARCHITECTURE_SELECTED_FOR_RESEARCH = YES`

`NATIVE_PROJECT_ADOPTION = NO`

`LIVE_AUTHORITY_SURFACE = NONE`

`LIVE_FEDERATION = NONE`

## 2. No retroactive rewriting

Existing native history must not be rewritten into synthetic Authority Capsules.

In particular, HiVenues Issue #374, Issue #398, PR #399 and their existing comments/reviews remain historical/native evidence exactly as they occurred.

If HiVenues later adopts capsules, the first native capsule must be a **new contemporaneous owner decision** created after explicit native-project adoption.

CPI must not manufacture a genesis capsule from old prose.

## 3. Adoption is project-local

A native project that chooses to adopt Authority Capsules must itself define at minimum:

- whether capsules are authoritative for that project;
- the authority domain(s);
- the native subject/gate identifiers;
- candidate/revision semantics;
- the pinned owner public key/fingerprint;
- the approved carrier/discovery surface;
- what each decision enum means locally;
- what, if any, native execution transition a valid PASS permits.

CPI may observe and verify those declarations.

CPI may not create them on the project's behalf.

## 4. Optionality

Authority Capsules are **not** a universal mandatory governance format.

They are a candidate interoperable authority primitive for cases where a project needs an externally reconstructable consequential human decision and ordinary provider identity is insufficient.

Projects whose native governance already supplies content-addressed, machine-readable, non-ambiguous authority may continue using their native mechanism.

`FEDERATION_OPTIONALITY = PRESERVED`

## 5. HiVenues-specific prospective path

A later, separately authorized HiVenues adoption stage would need to:

1. define the native owner-acceptance authority domain;
2. establish and publish a native owner public-key pin;
3. establish a human signing workflow in which ordinary automation cannot access the private key;
4. define the capsule carrier/discovery rule;
5. issue a first contemporaneous capsule for the then-current candidate/revision;
6. independently test verification, withdrawal, revision changes, fork handling and loss/recovery behavior;
7. preserve existing #374/#398/#399 prose as context/history rather than converting it to signed authority.

Stage 6M performs none of these operations.

## 6. Key custody boundary

The Stage-6M prototype generates only ephemeral or deterministic test keys.

No real owner private key is generated, stored, uploaded or requested.

Any future private key:

- must remain outside CPI automation;
- must not be stored in repository plaintext;
- must not be placed in ordinary CI secrets if CI can autonomously emit authority;
- should ideally be protected by an owner-controlled signing device or equivalent human-mediated boundary.

Operational key-custody design is deferred to a later adoption study.

## 7. Pin bootstrap boundary

A signature is only as meaningful as the native authority of the public-key pin.

Stage 6M therefore does not solve bootstrap by declaring a CPI file authoritative.

A future project's pin must be established through that project's native governance before CPI can rely on it.

## 8. Key rotation / succession boundary

Version 0.1 supports one pinned Ed25519 key per authority domain.

Not yet specified:

- key rotation;
- lost-key recovery;
- successor owner;
- multiple owners;
- quorum;
- delegated signer;
- emergency revocation.

These must be solved prospectively before any use case requires them.

## 9. Carrier boundary

Stage 6M does not select a single transport.

A capsule may eventually be carried in a repository file, issue/comment, release artifact or other durable native surface.

The carrier may provide provenance and discovery.

It does not substitute for the capsule signature.

## 10. CPI projection rule after hypothetical adoption

If a future native project adopts capsules, CPI may project:

- chain validity;
- signer-key match;
- exact project/domain/subject/candidate/revision binding;
- current closed decision enum;
- capsule digest/sequence;
- observation provenance.

CPI must continue to project:

`execution_authorized_by_cpi = false`

The native project remains the only source of consequences.

## 11. Other projects

No change is made to:

- NFC;
- FCP;
- PGH;
- Evidence-Based-Market-Methods;
- HiVenues;
- Project Observatory;
- future planned projects.

Stage 6M does not assert that each project should adopt capsules.

## 12. Historical false-bridge control

No Authority Capsule result establishes a HiVenues/Hive -> NFC/PGH scientific dependency.

`DEPENDENCY = NONE / NOT ESTABLISHED`

`STATUS = HELD SPECULATION`

## 13. Exit condition

Stage 6M may close only as a research architecture result after independent re-audit.

Any native adoption requires a later stage with its own prospective authorization and tests.
