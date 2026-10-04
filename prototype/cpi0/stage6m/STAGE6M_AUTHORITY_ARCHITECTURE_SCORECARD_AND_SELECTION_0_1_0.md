# CPI-0 Stage-6M Authority Architecture Scorecard and Selection 0.1.0

Date: 2026-10-04
Status: FROZEN ARCHITECTURE SELECTION
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #32
Preregistration commit: `a196f5ade1baf21574b6e90ee1825c5572774d15`

## 1. Scoring rule

Scores use the preregistered scale:

- 0 = fails;
- 1 = materially incomplete;
- 2 = workable with important caveats;
- 3 = strong.

Hard-gate criteria are C1, C2, C3, C4 and C13. Any score below 2 on any hard gate makes a candidate ineligible regardless of total score.

## 2. Scorecard

| Criterion | A Free text | B Structured line in ordinary comment | C GitHub-native mutable state | D Structured unsigned append-only record | E Signed Authority Capsule |
|---|---:|---:|---:|---:|---:|
| C1 Semantic unambiguity | 0 | 3 | 3 | 3 | 3 |
| C2 Human / automation separability | 0 | 0 | 0 | 0 | 3 |
| C3 Immutable chronology | 1 | 2 | 0 | 3 | 3 |
| C4 Subject binding | 1 | 3 | 2 | 3 | 3 |
| C5 Withdrawal / revocation | 1 | 3 | 2 | 3 | 3 |
| C6 Conflict handling | 1 | 2 | 1 | 3 | 3 |
| C7 Edit resistance | 0 | 2 | 0 | 3 | 3 |
| C8 Provider neutrality | 2 | 1 | 0 | 3 | 3 |
| C9 Offline verification | 1 | 1 | 0 | 2 | 3 |
| C10 Native-project independence | 2 | 3 | 3 | 3 | 3 |
| C11 Operator burden | 3 | 3 | 3 | 2 | 2 |
| C12 Migration feasibility | 3 | 3 | 3 | 3 | 2 |
| C13 Consequence separation | 2 | 3 | 3 | 3 | 3 |
| **Total / 39** | **17** | **29** | **20** | **34** | **37** |
| **Hard gates passed?** | **NO** | **NO** | **NO** | **NO** | **YES** |

## 3. Candidate A — free-text semantic classifier

### Result

`INELIGIBLE`

Stage 6L directly falsified C1. Open-vocabulary prose creates false PASS, false FAIL, missed withdrawal, quotation/negation problems and ambiguity-driven availability failures.

C2 also fails because the same GitHub OWNER account can carry both human decisions and automation prose.

Chronology can be improved independently, but that does not repair the semantic or principal problem.

### Why it is retained

Free-text prose remains useful contextual evidence. It must cease to be the authority primitive.

## 4. Candidate B — strict structured line in ordinary GitHub comments

### Result

`INELIGIBLE`

A closed machine-readable grammar repairs C1 and can encode sequence, predecessor and subject binding.

However, it fails C2 under the frozen threat model. Automation acting through the owner's GitHub account can emit the same magic line. A social convention that automation "must never emit this string" is not a technical principal boundary.

It is therefore unsuitable as the sole consequential-authority primitive.

### Useful residue

The structured-line idea is still useful as a human-facing serialization of a stronger signed record.

## 5. Candidate C — GitHub-native mutable state

### Result

`INELIGIBLE`

Labels, issue state, PR state/review state and milestones are easy for operators and easy to adopt, but they are provider-specific mutable state.

They fail C2 when automation has equivalent account/API authority and fail C3 because current mutable state does not itself preserve an immutable decision sequence.

They are appropriate as convenience views, not as the authority root.

## 6. Candidate D — structured unsigned append-only authority record

### Result

`INELIGIBLE`

This candidate solves nearly every Stage-6L semantic and chronology problem:

- closed decision enum;
- explicit subject/revision binding;
- monotonic sequence;
- predecessor hash;
- deterministic fork detection;
- append-only replay;
- provider-neutral storage.

But it still fails the hardest remaining Stage-6L problem: C2.

If both the human and automation can write the carrier, an unsigned record cannot prove which principal issued it. Carrier provenance alone merely recreates the `OWNER`-account ambiguity at a better-structured layer.

This is the closest rejected candidate and supplies most of the data model selected below.

## 7. Candidate E — cryptographically attributable Authority Capsule

### Result

`SELECTED_FOR_RESEARCH_PROTOTYPE`

It is the only candidate that passes all five hard gates.

A closed structured payload solves semantic ambiguity. A monotonic sequence plus predecessor digest solves authority ordering without mutable provider timestamps. Exact project/domain/subject/candidate/revision fields solve subject binding.

Most importantly, a signature verifiable against a native-project-pinned owner key creates a principal boundary independent of the GitHub account and independent of automation credentials.

### Selection rationale

Candidate E is not selected merely because it has the largest total score. It is selected because:

1. it is the only candidate that passes every preregistered hard gate;
2. Candidate D demonstrates that structure alone is insufficient under the frozen principal-ambiguity threat;
3. the additional complexity over D is narrowly concentrated in signer attribution;
4. the operator burden can be reduced by a helper/UI without moving private-key custody into CPI;
5. the record remains independently interpretable by the native project.

## 8. Weaknesses of selected architecture

Selection does not imply completeness.

### W1 — key custody

The design moves the strongest principal assumption to possession of the owner private key.

Private-key compromise is explicitly outside the Stage-6M threat model. It must be addressed by operational guidance and later key-rotation/recovery work.

### W2 — bootstrap trust

The owner public key/fingerprint must be pinned by native project governance through an independently authoritative mechanism.

CPI is not allowed to create or silently replace this pin.

### W3 — operator burden

Signing is more work than writing a GitHub comment or changing a label.

A usable adoption path will require a small signing helper or Studio-like UI. The prototype must not solve this by giving automation the private key.

### W4 — key rotation and succession

Initial Stage-6M semantics use one pinned signing key per authority domain.

General key rotation, multi-owner quorum and succession are intentionally deferred rather than improvised into the first prototype.

### W5 — denial of service

An attacker can copy, delete, withhold or reorder carrier artifacts. Verification must fail closed, but cryptographic attribution does not guarantee availability.

### W6 — human intent remains external to key possession

A valid signature proves that the pinned key signed the canonical payload. It does not philosophically prove that the human understood the decision. The architecture is an attribution mechanism, not mind reading.

## 9. Selected architecture principle

The selected design changes CPI's role from:

`INTERPRET PROSE -> INFER AUTHORITY`

to:

`VERIFY NATIVE-PINNED SIGNED RECORD -> PROJECT OBSERVED AUTHORITY`

Ordinary prose, labels, issue state, reviews and comments remain contextual evidence and carriers. They do not independently create consequential authority.

## 10. Consequence boundary

A valid Authority Capsule means only:

`A decision record validly attributable to the project-pinned authority key was observed for this exact subject and revision.`

It does **not** mean:

`CPI authorizes the native project to execute an effect.`

Execution authority remains native-project-local and must be represented separately.

## 11. Selection

`SELECTED_ARCHITECTURE = E__SIGNED_AUTHORITY_CAPSULE`

`FREE_TEXT_AUTHORITY_INFERENCE = RETIRED_AS_CONSEQUENTIAL_AUTHORITY_PRIMITIVE`

`PROTOTYPE_AUTHORIZED = YES__PROJECT_CONTINUITY_RESEARCH_ONLY`

`HIVENUES_ADOPTION = NOT_AUTHORIZED`

`LIVE_FEDERATION = NOT_AUTHORIZED`
