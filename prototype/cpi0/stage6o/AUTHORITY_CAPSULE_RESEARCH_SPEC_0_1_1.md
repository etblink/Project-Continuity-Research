# CPI-0 Authority Capsule Research Specification 0.1.1

Date: 2026-10-04
Status: FROZEN CORRECTIVE RESEARCH SPECIFICATION
Program: CPI-0 — Cross-Project Interoperability
Stage: 6O
Supersedes for prospective prototype use: Authority Capsule Research Specification 0.1.0
Signed payload schema remains: `cpi.authority-capsule/0.1`

## 1. Purpose

Version 0.1.1 preserves the Stage-6M signed capsule data model while correcting two overclaims identified by the independent Stage-6N audit:

1. a supplied signed chain does not establish that no later capsule exists;
2. canonical signing bytes are insufficient unless raw carrier parsing is also unambiguous.

The verifier therefore establishes **observed cryptographic history**, not current authority, unless a separately authenticated completeness mechanism exists.

## 2. Preserved signed envelope

The exact signed/envelope fields and decision enum from 0.1.0 are unchanged.

Decision values remain exactly:

- `PASS`
- `HOLD`
- `REJECT`
- `WITHDRAW`

The Stage-6M deterministic vector must remain byte-for-byte compatible.

## 3. Canonical capsule artifact

A capsule artifact is the exact canonical complete-envelope JSON byte sequence.

Canonicalization remains:

- UTF-8;
- keys sorted lexicographically;
- separators `,` and `:` with no insignificant whitespace;
- `ensure_ascii = false`;
- no NaN/Infinity;
- signature included for the complete envelope.

No leading/trailing whitespace or newline is part of a valid artifact.

Equivalent but differently serialized JSON is not a valid version-0.1.1 artifact.

## 4. Raw parsing rule

Authority verification begins from raw bytes.

The parser must:

- accept bytes, not a pre-parsed mapping, at the public carrier boundary;
- reject UTF-8 BOM;
- decode UTF-8 strictly;
- parse exactly one JSON value;
- require an object root;
- reject duplicate keys;
- reject floating-point numbers;
- reject NaN, Infinity and non-standard constants;
- reject malformed JSON;
- validate exact schema fields and types;
- reserialize the parsed envelope canonically;
- require exact byte equality between the raw artifact and canonical reserialization.

Duplicate-key first-wins/last-wins behavior is therefore outside the valid input language.

## 5. Identifier semantics

Project, authority-domain, subject, candidate and revision identifiers are exact Unicode code-point sequences represented by valid UTF-8.

The capsule layer performs:

- no Unicode normalization;
- no case folding;
- no provider-specific aliasing.

Native projects must define canonical identifiers before signing when such normalization is needed.

## 6. Sequence domain

`sequence` is an integer satisfying:

`1 <= sequence <= 2^63 - 1`

Booleans and floats are invalid.

A verifier must check continuity incrementally and must not allocate a range proportional to the largest observed sequence.

## 7. Pinned authority key

The verification input is a structured pinned-authority record containing:

- raw 32-byte Ed25519 public key;
- project;
- authority domain;
- native provenance identifier;
- native provenance revision.

The public key must decode canonically to a non-identity Ed25519 point in the prime-order subgroup.

The verifier derives the key ID from the validated pin.

A capsule-provided key ID is never a substitute for the pin.

## 8. Pin provenance

Version 0.1.1 makes pin provenance explicit in verification output.

It does not authenticate the provenance source by itself.

Native pin bootstrap remains a future adoption prerequisite and must be outside every credential available to ordinary automation.

CPI may verify a native pin.

CPI may not originate, replace or silently upgrade native pin authority.

## 9. Binding partition

Raw artifacts are parsed before chain reduction.

For a requested target chain, exact binding is:

`(project, authority_domain, subject, candidate)`

Artifacts with another exact binding are foreign to the target chain and do not participate in its fork/sequence reduction.

Target-binding artifacts must satisfy the pinned-key signature.

This prevents a copied capsule from another valid owner-signed chain from manufacturing a target-chain fork.

## 10. Observed-chain verification

Given target-chain artifacts:

1. strictly parse canonical raw artifacts;
2. partition by exact binding;
3. verify target signatures against the pinned authority key;
4. deduplicate identical canonical artifacts by SHA-256;
5. require at most one distinct target capsule at each sequence;
6. require contiguous observed sequence beginning at 1;
7. require sequence 1 predecessor = null;
8. require each later predecessor to equal SHA-256 of the exact prior canonical envelope;
9. require the observed head revision to equal the requested revision.

A successful result establishes only the verified observed chain.

## 11. Required result semantics

Successful observed-chain verification returns at minimum:

```text
capsule_chain_valid = true
authority_state = OBSERVED_CHAIN_ONLY
completeness_status = NOT_ESTABLISHED
latest_observed_decision = <closed enum>
verified_through_sequence = <n>
verified_through_capsule_digest = <sha256>
current_decision = null
execution_authorized_by_cpi = false
```

It must also report the pinned key identity/provenance used for verification.

## 12. Currentness rule

Version 0.1.1 defines **no authenticated completeness protocol**.

Therefore an Authority Capsule chain alone cannot establish:

- that no later signed capsule exists;
- that an observed fork branch was not withheld;
- that the observed head is globally current.

Any API request for a current decision under version 0.1.1 must fail closed.

Suppression of a later capsule may change `latest_observed_decision`, because it changes the observed evidence set.

It must never change `current_decision` from null to an affirmative value.

## 13. Future completeness mechanisms

A later specification may define a currentness/completeness basis, such as:

- authenticated append-only authority journal;
- independently protected monotonic witness/checkpoint;
- project-native rollback-resistant source with qualified discovery.

No such mechanism is selected or implied by version 0.1.1.

Any future mechanism requires separate prospective specification and independent audit.

## 14. Fork rule

Two distinct valid target-chain capsules at the same sequence are an observed fork and fail closed.

If one fork branch is withheld, the verifier cannot infer the hidden branch.

It reports only the surviving observed chain and `completeness_status = NOT_ESTABLISHED`.

## 15. Withdrawal / revision semantics

Within the observed chain, the latest observed closed decision is the head decision.

Examples:

- PASS -> WITHDRAW => latest observed WITHDRAW;
- HOLD(A) -> PASS(B) => latest observed PASS for revision B;
- PASS(A) cannot be replayed as observed authority for revision B.

These are observed-history statements, not global-currentness statements.

## 16. Carrier edits

Any change to canonical artifact bytes changes the artifact digest.

An unsigned edit invalidates the signature.

A re-signed historical edit changes its canonical envelope digest and therefore breaks any existing successor predecessor link.

Noncanonical reserialization is rejected even if it parses to an otherwise identical mapping.

## 17. Consequence separation

A successful observed-chain result remains evidence only.

`execution_authorized_by_cpi = false`

is mandatory.

No version-0.1.1 verifier may infer native execution authority from PASS.

## 18. Public API boundary

The public authority verification entry point consumes raw artifacts plus a structured native pin and exact expected binding/revision.

Pre-parsed mappings are not an authority-bearing public input path.

Ordinary GitHub author, OWNER, comment, review, label or issue-state fields are not authority inputs.

## 19. Error contract

Malformed public inputs fail through the `CapsuleError` hierarchy.

Fail-closed availability degradation is preferable to interpreting malformed authority evidence.

## 20. Adoption boundary

Version 0.1.1 remains a research prototype.

It does not:

- create a native owner key;
- define a native key pin;
- define capsule discovery/currentness;
- convert historical HiVenues prose into capsules;
- authorize HiVenues adoption;
- alter NFC/FCP/PGH/EBMM;
- alter Project Observatory;
- enter federation.

## 21. False bridge

No result establishes a HiVenues/Hive -> NFC/PGH dependency.

```text
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

## 22. Independent closure

Version 0.1.1 remains unqualified until a fresh independent audit re-tests:

- suppression/truncation semantics;
- canonical raw parsing;
- duplicate-key rejection;
- pin validation/provenance;
- binding partition;
- error normalization;
- deterministic compatibility;
- consequence separation.
