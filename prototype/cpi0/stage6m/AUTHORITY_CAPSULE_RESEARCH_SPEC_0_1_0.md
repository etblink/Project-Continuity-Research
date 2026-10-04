# CPI-0 Authority Capsule Research Specification 0.1.0

Date: 2026-10-04
Status: FROZEN BEFORE PROTOTYPE IMPLEMENTATION
Program: CPI-0 — Cross-Project Interoperability
Stage: 6M
Selected architecture: E — Signed Authority Capsule

## 1. Purpose

An Authority Capsule is a small, structured, append-only, cryptographically attributable record of a consequential native-project decision.

It exists to let an observer verify:

- which authority domain the decision belongs to;
- which project / gate / candidate / revision it concerns;
- which ordered decision in the chain it is;
- whether it was signed by the native-project-pinned authority key.

It does not grant CPI consequence authority.

## 2. Authority root

The verifier receives a native-project-governed pinned public key.

Stage 6M does not define how a real project initially establishes or rotates that pin.

The prototype rule is:

`CPI MAY VERIFY A PIN; CPI MAY NOT CREATE, REPLACE, OR SILENTLY UPDATE A PROJECT'S PIN.`

The initial prototype supports one Ed25519 key per authority domain.

Key rotation, quorum, succession and recovery are deferred.

## 3. Capsule envelope

The canonical capsule is a JSON object with exactly these fields:

```json
{
  "schema": "cpi.authority-capsule/0.1",
  "project": "etblink/HiVenues",
  "authority_domain": "stage5d.owner_acceptance",
  "subject": "issue:374",
  "candidate": "pr:399",
  "candidate_revision": "0123456789abcdef0123456789abcdef01234567",
  "sequence": 1,
  "predecessor": null,
  "decision": "PASS",
  "note_digest": null,
  "signer_key_id": "ed25519-sha256:<64 lowercase hex>",
  "signature_algorithm": "Ed25519",
  "signature": "<canonical base64 Ed25519 signature>"
}
```

No undeclared fields are accepted in version 0.1.

## 4. Closed decision vocabulary

Version 0.1 accepts exactly:

- `PASS`
- `HOLD`
- `REJECT`
- `WITHDRAW`

No free-text synonym is interpreted.

Human-readable explanation may live anywhere else. If a project wants to cryptographically bind a note, it may place the SHA-256 digest of the note bytes in `note_digest`.

The note text itself has no authority semantics.

## 5. Field semantics

### schema

Exactly:

`cpi.authority-capsule/0.1`

### project

Non-empty, case-sensitive native project identifier.

It is part of the signature and prevents cross-project replay.

### authority_domain

Non-empty, case-sensitive identifier for the native authority domain.

Example:

`stage5d.owner_acceptance`

The native project defines this domain. CPI does not.

### subject

Non-empty exact authority subject / gate identifier.

Example:

`issue:374`

### candidate

Non-empty exact candidate identifier.

Example:

`pr:399`

### candidate_revision

Non-empty exact revision identifier.

For a Git commit this may be a 40-hex commit. The schema itself remains provider-neutral and does not require Git.

The current head capsule must bind the revision being adjudicated.

A PASS for revision A is not a PASS for revision B.

### sequence

Positive integer.

The first capsule is sequence 1.

Each subsequent capsule increments sequence by exactly one.

Boolean values and floating-point values are invalid even though Python may otherwise coerce them to integers.

### predecessor

For sequence 1:

`null`

For sequence >1:

the lowercase SHA-256 hex digest of the complete canonical predecessor envelope, including predecessor signature.

### decision

One of the closed values above.

### note_digest

Either null or exactly 64 lowercase hexadecimal characters representing SHA-256 of human-readable note bytes.

### signer_key_id

Exactly:

`ed25519-sha256:<sha256(raw_32_byte_public_key)>`

The verifier independently derives this from the native-project-pinned public key and requires equality.

### signature_algorithm

Exactly:

`Ed25519`

### signature

Standard RFC 4648 Base64 encoding of the 64-byte Ed25519 signature.

## 6. Canonicalization

Version 0.1 deliberately uses a narrow JSON subset.

Signed payload fields contain only:

- UTF-8 strings;
- positive integers;
- null.

No floats, booleans, arrays or nested objects occur in the signed payload.

Canonical signed bytes are UTF-8 encoding of JSON serialized with:

- object keys sorted lexicographically;
- separators `,` and `:` with no insignificant whitespace;
- `ensure_ascii = false`;
- the `signature` field omitted.

The complete envelope digest uses the same canonicalization with `signature` included.

Because the schema is narrow, Stage 6M does not claim general RFC-8785/JCS compatibility.

## 7. Signature rule

Ed25519 signs the canonical signed payload bytes.

Verification requires:

1. strict schema validation;
2. derived key ID equals `signer_key_id`;
3. Ed25519 signature verification succeeds.

Carrier account identity is irrelevant to cryptographic validity.

A GitHub comment posted by `OWNER` but lacking a valid capsule signature is contextual prose only.

## 8. Chain rule

Given a set of capsules for one authority chain:

1. verify each capsule schema and signature;
2. require one and only one capsule at every sequence position;
3. require sequence numbers to be contiguous beginning at 1;
4. require sequence 1 predecessor = null;
5. for every later capsule, require `predecessor` = digest of the exact prior complete envelope;
6. require the same project, authority_domain, subject and candidate across the chain;
7. do not use provider timestamps to order authority.

A duplicate sequence with distinct capsule digests is a fork and fails closed.

A missing sequence fails closed.

A predecessor mismatch fails closed.

## 9. Revision rule

Historical capsules may refer to earlier candidate revisions.

For a current adjudication request, the head capsule's `candidate_revision` must exactly equal the requested current revision.

This permits an explicit later decision about a revised candidate while preventing replay of a PASS from revision A as authority for revision B.

## 10. Decision-state rule

The current observed owner decision is exactly the head capsule's closed `decision`.

Examples:

- PASS -> current observed decision PASS;
- PASS -> WITHDRAW -> current observed decision WITHDRAW;
- PASS -> HOLD -> current observed decision HOLD;
- REJECT -> PASS on later revision -> current observed decision PASS for that later revision.

No linguistic interpretation is performed.

## 11. Edit semantics

Authority order is determined only by sequence and predecessor linkage.

Carrier edits do not re-date decisions.

If an old capsule is edited without re-signing:

signature verification fails.

If an old capsule is changed and re-signed while a later capsule remains:

the later capsule's predecessor digest no longer matches and verification fails.

If two different valid owner-signed capsules exist at the same sequence:

fork -> fail closed.

## 12. Same-time semantics

Wall-clock timestamps are not authority-order inputs.

Two provider events occurring in the same second cannot change ordering.

Ordering comes only from sequence and predecessor linkage.

## 13. Human / automation separation

The frozen threat model permits automation to use the same GitHub account as the human owner.

Therefore:

- GitHub username is not authority;
- OWNER association is not authority;
- ordinary comments are not authority;
- labels/review states are not authority;
- a structured-looking unsigned capsule is not authority.

Only possession of the pinned private signing key can produce a valid capsule under version 0.1.

The private key must not be made available to ordinary automation credentials.

## 14. Carrier neutrality

A valid capsule may be carried by:

- a repository file;
- a GitHub comment;
- a release artifact;
- an attachment;
- another durable native-project-approved surface.

Carrier location contributes provenance but not authority semantics.

A preserved capsule set plus the pinned public key must be sufficient for offline cryptographic replay.

## 15. CPI consequence boundary

Successful verification produces only an observed authority fact.

Prototype verifier output must always distinguish:

```text
capsule_chain_valid = true
observed_decision = <closed enum>
execution_authorized_by_cpi = false
```

A native project may separately define what a valid PASS permits.

CPI does not.

## 16. Required Stage-6M falsification cases

The prototype must demonstrate:

1. automation prose containing PASS is ignored;
2. structured-looking record without valid signature is rejected;
3. old capsule edit invalidates signature or chain;
4. PASS -> WITHDRAW yields WITHDRAW;
5. PASS revision A replayed for revision B is rejected;
6. two distinct valid capsules at same sequence fail as fork;
7. predecessor mismatch fails;
8. cross-project copy fails expected-project binding;
9. wrong pinned key fails;
10. provider-offline replay succeeds from preserved capsules/key;
11. contextual prose is never interpreted;
12. valid PASS still reports `execution_authorized_by_cpi = false`.

Additional tests should cover malformed Base64, extra fields, booleans/floats as sequence values, unknown decision enum, noncanonical predecessor identifiers and signature tampering.

## 17. Prototype boundary

The Stage-6M implementation is research-only.

It may generate ephemeral test keys inside tests.

It must not contain or generate a real HiVenues owner private key.

It must not mutate HiVenues or establish a live authority surface.

## 18. Version-0.1 non-goals

Deferred:

- key rotation;
- key recovery;
- multi-owner quorum;
- delegated authority;
- threshold signatures;
- hardware-key UX;
- carrier discovery protocol;
- native-project adoption;
- live Project Observatory ingestion.

These omissions must not be silently filled in by CPI.
