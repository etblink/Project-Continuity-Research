# CPI-0 Stage-7A Hive Active-Authority Bootstrap Anchor Profile Note 0.1.0

Date: 2026-10-04
Status: RESEARCH PROFILE — NOT NATIVE ADOPTION
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #41
Preregistration: `97e61e35187e1235d793aec24aad94d39633921a`

## 1. Purpose

Record a concrete candidate-D / candidate-F anchor profile proposed after preregistration and before architecture scoring:

`HIVE_ACTIVE_AUTHORITY_ANCHOR`

This does not add or replace a preregistered architecture candidate.

It instantiates the already-frozen:

- Candidate D — single pre-existing independent anchor;
- Candidate F — Native Bootstrap Manifest with explicit anchor policy.

## 2. Proposed native anchor

For a project that explicitly chooses Hive identity as a bootstrap trust basis:

```text
network = HIVE_MAINNET
account = @etblink
authority_level = ACTIVE
signing_interface = HIVE_KEYCHAIN
```

For project-neutral architecture, the account is a policy parameter rather than hard-coded globally.

## 3. Architectural distinction

Hive Keychain is not itself the trust root.

Keychain is:

- a private-key custody/signing interface;
- a human-facing confirmation boundary;
- a mechanism for requesting a buffer signature.

The trust claim is instead:

`THE NATIVE PROJECT ACCEPTS THE HIVE ACCOUNT'S ACTIVE AUTHORITY AS A BOOTSTRAP ANCHOR`

The cryptographic proof then demonstrates control of a key satisfying that Hive account authority.

## 4. Why Active rather than Posting

The Stage-7A threat model permits ordinary automation to hold routine provider credentials.

A Hive posting authority is commonly suitable for routine social/application operations.

For trust-root bootstrap, the stronger intended profile is therefore Active authority, with the operational assumption:

`ORDINARY PROJECT AUTOMATION DOES NOT POSSESS THE @etblink ACTIVE PRIVATE AUTHORITY`

This assumption must be tested and stated explicitly.

Owner authority is not required for the research profile and should remain outside routine signing flows.

## 5. Proposed signed bootstrap statement

A future synthetic prototype may ask Keychain to sign a domain-separated message derived from the exact canonical Native Bootstrap Manifest.

Conceptual message:

```text
CPI-NATIVE-BOOTSTRAP/0.1
network=hive-mainnet
anchor_account=etblink
anchor_authority=active
project=<exact native project id>
authority_domain=<exact Authority Capsule domain>
bootstrap_policy=<exact policy id>
candidate_authority_key_id=<exact Ed25519 key id>
generation=<anti-replay generation/challenge>
manifest_digest=<sha256 canonical manifest>
```

The exact serialization must be frozen before any prototype.

## 6. Verification model

A research verifier would need to establish separately:

### A. Manifest binding

The signed message binds the exact:

- project;
- authority domain;
- candidate Authority Capsule key;
- bootstrap policy;
- generation/challenge;
- manifest digest.

### B. Hive signature validity

The signature is cryptographically valid for a recovered/provided Hive public key.

### C. Hive account authority

The signer key or authority path satisfies the required Active authority for the declared Hive account.

Verification must respect Hive authority thresholds and account/key authorities rather than merely checking that a public key appears somewhere in the account object.

### D. Native policy

The native project's bootstrap policy explicitly names the Hive account / authority level as an accepted bootstrap anchor.

Without this policy fact, a valid @etblink signature proves control of @etblink but does not by itself prove that an arbitrary project intended to trust @etblink.

## 7. Same-account automation separation

This profile can satisfy the Stage-7A same-account-automation gate only if ordinary automation:

- may control GitHub/repository provider credentials;
- does NOT control a Hive key set sufficient to satisfy the declared @etblink Active authority.

Therefore a GitHub automation compromise alone cannot substitute a different bootstrap key.

Keychain UI presence is useful operationally but is not itself a cryptographic proof that a human clicked the confirmation.

The cryptographic boundary is possession/control of the independently trusted Hive Active authority.

## 8. Proof of possession versus authorization

The profile keeps three facts separate:

```text
KEYCHAIN SIGNATURE
= proof that a Hive authority key signed the bound statement

HIVE ACTIVE AUTHORITY VERIFICATION
= proof that the signer satisfies @etblink Active authority

NATIVE BOOTSTRAP POLICY
= reason this project accepts @etblink Active authority as a trust anchor
```

None may substitute for another.

## 9. Replay / replacement controls

The signed bootstrap object must bind:

- exact project;
- exact authority domain;
- exact candidate key;
- exact policy identity;
- exact generation/challenge.

A signature for another project/domain/key/generation must fail.

A new root must not silently replace the frozen bootstrap generation.

Post-bootstrap rotation remains outside Stage 7A.

## 10. On-chain carrier variant

A future adoption study may compare:

### Off-chain Keychain buffer signature

Advantages:

- no blockchain write;
- simple bounded signing ceremony;
- exact signed message can be preserved.

Caveat:

- verifier must reconstruct/validate the relevant Hive account authority independently.

### Hive on-chain declaration

A future native project might publish the manifest digest through a Hive operation signed with the required authority.

Advantages:

- durable public carrier;
- blockchain ordering/timestamp context.

Caveat:

- this is an external effect and is NOT authorized in Stage 7A;
- it is not an independent second trust anchor if it uses the same Hive authority;
- it does not eliminate the need for native policy saying why the Hive identity is trusted.

Stage 7A performs neither.

## 11. Authority-state replay caveat

A signature is only meaningful relative to the Hive authority state used to evaluate it.

A future specification must define how the bootstrap verifier binds or reconstructs:

- Hive account;
- required authority level;
- authority state / chain context;
- signer key(s);
- threshold satisfaction.

Live RPC response alone should not be silently treated as immutable historical proof.

This is a research item for the prototype/audit, not assumed solved by Keychain.

## 12. Current hypothesis

`HIVE_ACTIVE_AUTHORITY_ANCHOR = PLAUSIBLE QUALIFYING CANDIDATE-D PROFILE`

provided:

1. the native project explicitly chooses the exact Hive account and Active authority as its bootstrap anchor;
2. ordinary project automation lacks that Active authority;
3. exact manifest binding and replay protection are present;
4. Hive authority satisfaction is verified rather than inferred from username;
5. preserved evidence is sufficient for the claimed replay model.

Within Candidate F, this could become a concrete policy profile such as:

`HIVE_ACTIVE_SIGNATURE_V1`

No selection or adoption is claimed by this note.
