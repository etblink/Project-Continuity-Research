# CPI-0 Stage-6M Authority Architecture Reconsideration Preregistration 0.1.0

Date: 2026-10-04
Status: FROZEN BEFORE ARCHITECTURE SCORING
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #32

## 1. Controlling evidence

Stage-6L independent evaluator:

`Claude Opus 5.5 (Anthropic)`

Published independent audit commit:

`81cfa0472114f256d0709c58ec9f611518ad62b1`

Exact audit report blob:

`238710fd4e66e2e23e36639d26d879c052c6d4f2`

Final disposition:

`ARCHITECTURE_RECONSIDERATION_REQUIRED`

Stage 6M accepts that disposition as controlling.

It will not attempt another phrase-list repair unless the architecture comparison independently establishes that free-text inference remains preferable.

## 2. Frozen problem statement

CPI must be able to reconstruct consequential human authority without turning a derived observer into an authority source.

The Stage-6L audit establishes three architectural failure classes in the current owner-decision layer:

1. **semantic ambiguity** — open-vocabulary prose cannot be reliably reduced to PASS / FAIL / HOLD / WITHDRAW across negation, questions, quotation, conditionals, edits, and engineering prose;
2. **principal ambiguity** — GitHub `author_association = OWNER` does not distinguish the human owner from automation acting through the owner's account;
3. **chronology ambiguity** — mutable `updated_at` values cannot safely order immutable authority decisions.

Any replacement architecture must address all three.

## 3. Preserved components

Stage 6M treats these as presumptively reusable unless falsified:

- native-source collection;
- content binding;
- repository-bound identity;
- source-set enumeration;
- stabilized observation windows;
- authority-surface preservation;
- project-local authority maps;
- negative knowledge;
- federation optionality;
- no CPI consequence authority.

The architecture-reconsideration target is the authority-recognition / authority-record layer.

## 4. Threat model

Assume:

- arbitrary free-text comments may contain words such as pass, fail, approved, hold, accepted, rejected, merge, ready, blocked, or redesign without being authority decisions;
- automation may post through the same GitHub account as the human owner;
- automation may accidentally emit decision-like prose;
- GitHub comments may be edited;
- issue and PR `updated_at` values may change for reasons unrelated to authority;
- two decisions may occur with the same second-level timestamp;
- provider APIs may be temporarily unavailable;
- CPI may be wrong and must fail closed;
- CPI must not gain the ability to authorize project effects merely by interpreting a record;
- native projects must remain intelligible and operable without CPI.

Out of scope:

- hostile compromise of the human owner's private signing key;
- hostile modification of the CPI verifier code itself;
- GitHub platform compromise.

## 5. Candidate architectures

### A — Free-text semantic classifier

Continue inferring decisions from arbitrary owner prose, with improved grammar / NLP.

### B — Strict structured line in ordinary comments

Recognize only a fixed machine-readable line or fenced record emitted in an ordinary GitHub comment.

Example class:

`CPI-OWNER-DECISION v1 ...`

No cryptographic signer separation beyond the GitHub account.

### C — GitHub-native mutable state

Use labels, issue state, PR review state, milestones, or another GitHub-managed mutable field as the decision primitive.

### D — Structured unsigned append-only authority record

Use a canonical machine-readable record with explicit sequence, subject binding, decision enum, predecessor digest, and immutable append-only semantics, but no independent cryptographic signer.

### E — Structured append-only cryptographically attributable Authority Capsule

Use a canonical decision payload with explicit subject and predecessor binding plus a signature verifiable against a pinned owner-controlled public key that is not available to automation credentials.

## 6. Evaluation criteria

Each candidate will be scored:

- 0 = fails;
- 1 = materially incomplete;
- 2 = workable with important caveats;
- 3 = strong.

### C1 Semantic unambiguity

Can arbitrary contextual prose coexist without affecting authority state?

### C2 Human / automation separability

Can CPI distinguish a human owner's decision from automation using the same GitHub identity?

### C3 Immutable chronology

Can later decisions supersede earlier decisions without relying on mutable timestamps?

### C4 Subject binding

Can the decision bind exactly to project, gate, candidate, and candidate revision?

### C5 Withdrawal / revocation

Can a later explicit withdrawal be represented without semantic inference?

### C6 Conflict handling

Can same-position / conflicting decisions fail closed deterministically?

### C7 Edit resistance

Can editing an old record be detected or made irrelevant to ordering?

### C8 Provider neutrality

Can the authority representation survive migration away from GitHub?

### C9 Offline verification

Can an observer verify validity from preserved records without querying a live provider?

### C10 Native-project independence

Can the project interpret the record without CPI?

### C11 Operator burden

Can an ordinary owner realistically issue a decision?

Scoring is reversed for burden:

- 3 = low burden;
- 0 = impractical.

### C12 Migration feasibility

Can HiVenues adopt the mechanism incrementally without rewriting historical evidence?

### C13 Consequence separation

Does the design clearly distinguish "valid owner decision observed" from "CPI authorizes execution"?

## 7. Hard acceptance gates

A candidate is ineligible for selection if it scores below 2 on any of:

- C1 semantic unambiguity;
- C2 human / automation separability;
- C3 immutable chronology;
- C4 subject binding;
- C13 consequence separation.

No weighted total may override these gates.

## 8. Candidate E provisional payload requirements

These are preregistered requirements, not a declaration that E wins.

If E is selected, the minimum Authority Capsule payload must contain:

- schema/version;
- project identity;
- authority domain;
- subject/gate identity;
- candidate identity;
- candidate revision;
- monotonic sequence number;
- predecessor capsule digest;
- decision enum;
- optional human-readable note digest or reference;
- signer key identifier;
- signature algorithm;
- signature.

Decision enum must be closed, not open prose.

Minimum initial enum:

- PASS;
- HOLD;
- REJECT;
- WITHDRAW.

The signature covers the canonical payload excluding the signature field.

## 9. Ordering rule

Any selected structured design must avoid `updated_at` ordering.

Preferred ordering test:

1. explicit monotonic sequence;
2. predecessor hash-chain continuity;
3. provider timestamp only as descriptive metadata, never as the authority order primitive.

Forked sequence / predecessor conflicts must fail closed.

## 10. Principal rule

A GitHub username or `author_association = OWNER` alone is not sufficient human-principal evidence under the frozen threat model.

Any candidate that depends only on the GitHub account identity fails C2.

For cryptographic designs, the owner public key/fingerprint must be independently pinned by native project governance.

CPI may verify the pin; CPI may not define or silently replace it.

## 11. Provider and storage rule

The decision representation must be logically independent of its transport/storage.

Possible carriers may include:

- repository file;
- issue attachment/comment;
- release artifact;
- provider-neutral object store;
- other project-native durable surface.

Carrier identity is evidence provenance, not decision semantics.

## 12. Prototype boundary

If one architecture survives the hard gates, Stage 6M may create a **research-only prototype** inside Project-Continuity-Research sufficient to test:

- canonicalization;
- signature or identity verification if applicable;
- hash-chain ordering;
- fork detection;
- candidate-revision binding;
- withdrawal;
- invalid signer;
- automation-without-owner-key;
- offline replay.

No prototype may mutate HiVenues or become a live authority source.

## 13. Required falsification cases

The selected design must defeat at least:

1. automation posts "PASS" in prose;
2. automation emits a byte-for-byte structured-looking record without the human authority credential;
3. old decision is edited after a newer decision;
4. valid PASS then valid WITHDRAW;
5. valid PASS for candidate revision A replayed against revision B;
6. two records claim the same sequence with different payloads;
7. predecessor hash does not match;
8. record is copied to another repository/project;
9. signer key differs from pinned owner key;
10. provider is unavailable but preserved records are available;
11. CPI attempts to reinterpret contextual prose;
12. valid observed PASS is present but no project-local execution authorization exists.

## 14. Selection rule

Stage 6M may select an architecture only if:

- it passes every hard acceptance gate;
- its weaknesses are explicitly recorded;
- no simpler surviving architecture provides equivalent guarantees with lower operator burden.

If no candidate qualifies:

`NO_ARCHITECTURE_SELECTED__FURTHER_RESEARCH_REQUIRED`

## 15. Stage boundary

Stage 6M ends with:

- frozen candidate scorecard;
- selected architecture or no-selection result;
- formal semantics;
- prototype evidence if justified;
- migration boundary;
- next audit/implementation gate.

Do not implement the design in HiVenues during Stage 6M.

Do not modify NFC, FCP, PGH, HiVenues, or Project Observatory.
