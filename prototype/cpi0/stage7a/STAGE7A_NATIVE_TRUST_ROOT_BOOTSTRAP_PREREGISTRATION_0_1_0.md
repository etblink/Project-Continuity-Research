# CPI-0 Stage-7A Native Trust-Root Bootstrap Architecture Preregistration 0.1.0

Date: 2026-10-04
Status: FROZEN BEFORE ARCHITECTURE SCORING
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #41

## 1. Controlling prior boundary

Stage-6 research closure:

`879005a6bbd40d123c24a1d87d77a8ad6b74f53b`

Independent Stage-6 endpoint:

- Stage-6T audit commit `8b6c872cf7a2dd84c618aa2b92c64c02ed9d1014`
- report blob `00f856c9088b3ec24f5e350e124d977ff651b085`
- disposition `PASS_WITH_NONMATERIAL_FINDINGS`
- S3=0 / S2=0 / S1=0
- Signed Authority Capsule architecture qualified at research / observed-history scope only.

Open primary adoption prerequisites:

1. native public-key bootstrap / trust-root establishment;
2. authenticated completeness/currentness.

Stage 7A addresses prerequisite 1 only.

## 2. Research question

What is the smallest project-neutral architecture that lets a native project establish the initial trusted Authority Capsule public key while preserving:

- native-project sovereignty;
- separation from ordinary automation using the same provider account;
- explicit trust assumptions;
- exact project/domain/key binding;
- substitution and replay resistance;
- durable replayable evidence;
- no CPI authority to appoint a key or cause project effects?

## 3. Bootstrap axiom under test

Stage 7A preregisters the following proposition for adversarial testing:

`NO TRUST FROM NOTHING`

A first cryptographic authority key cannot authenticate the fact that it should be trusted merely by:

- signing itself;
- being first observed;
- being published by an account whose credentials are also available to ordinary automation.

Self-signature proves possession of the candidate key.

It does not prove native-project authorization of that key.

If this proposition survives the candidate comparison, every qualifying bootstrap architecture must expose at least one independent trust assumption rather than hiding it.

## 4. Threat model

Assume:

1. no previously trusted Authority Capsule project key exists;
2. ordinary automation may act through the same GitHub/project-provider account as the human owner;
3. ordinary automation may create commits, comments, issues, workflow output and repository files where its provider credentials permit;
4. ordinary automation can read all public bootstrap artifacts;
5. repository/provider state may be mutable;
6. bootstrap artifacts may be copied or replayed;
7. provider APIs may later be unavailable;
8. CPI can be wrong and must fail closed;
9. the native owner can perform a bounded one-time manual bootstrap ceremony if the architecture requires it;
10. a project may or may not have an existing domain, signing identity, hardware authenticator or other external trust anchor;
11. any trust placed in an external anchor must be explicit and attributable to native project governance;
12. possession of the candidate Authority Capsule private key is not itself sufficient bootstrap evidence.

### Out of scope for Stage 7A

- hostile compromise of every independently declared bootstrap anchor;
- coercion of the human owner;
- malicious hardware/identity provider after the native project explicitly chooses to trust it;
- project owner intentionally approving an unintended key;
- post-bootstrap key rotation / recovery / succession;
- authenticated global currentness/completeness;
- native execution semantics.

## 5. Candidate architectures

### Candidate A — self-signed genesis root

The new Authority Capsule key signs a root declaration naming itself.

No independent anchor.

Purpose: negative control for circular bootstrap.

### Candidate B — provider-owner declaration

A native provider account, for example the GitHub repository owner, publishes a structured initial key declaration.

Variants may include:

- ordinary commit;
- provider-verified commit/tag;
- issue/comment;
- provider account signature.

The provider identity is the sole bootstrap authority.

### Candidate C — trust on first use (TOFU)

The first observed candidate authority key becomes pinned.

Later substitutions are rejected.

No separate proof of initial native authorization.

### Candidate D — single pre-existing independent anchor

A pre-existing trust anchor independently recognized by the native project authenticates the exact initial Authority Capsule key binding.

Possible anchor classes include, without presuming equivalence:

- pre-existing offline signing key;
- pre-existing hardware/user-verifying credential;
- project-controlled DNS/DNSSEC or equivalent domain root;
- independently trusted identity/certificate system;
- another already-authoritative native governance key.

The candidate Authority Capsule key may prove possession, but the independent anchor establishes why the project trusts it.

### Candidate E — threshold multi-anchor bootstrap

A root manifest is accepted only when a threshold of independently controlled bootstrap anchors authenticate the same exact binding.

At least one required anchor must be unavailable to ordinary project automation.

Example profiles might combine:

- native provider publication;
- independently controlled domain proof;
- human-held hardware/offline credential;
- independent governance witness.

The candidate is architectural; Stage 7A does not assume any specific pair is universally available.

### Candidate F — Native Bootstrap Manifest with explicit anchor policy

A project-neutral structured bootstrap manifest binds:

- project identity;
- authority domain;
- initial Authority Capsule public key / key ID;
- bootstrap policy identity;
- exact trust anchors / proof references;
- anti-replay generation/challenge material;
- optional human-readable note digest.

The manifest itself is not self-authenticating.

It is accepted only if a predeclared/native bootstrap policy verifies one of the qualifying anchor profiles.

A valid policy must require at least one proof unavailable to ordinary project automation.

This candidate is intended to test whether the architecture should standardize the **representation and verification boundary** while leaving the concrete native trust anchor to the project.

It must not be scored as passing merely because the manifest is structured.

## 6. Scoring

Each criterion is scored:

- 0 = fails;
- 1 = materially incomplete;
- 2 = workable with important caveats;
- 3 = strong.

### C1 — non-circular trust foundation

Does the candidate rely on something independently trusted rather than the key being bootstrapped authenticating itself?

### C2 — same-account automation separation

Can ordinary automation using the same provider account bootstrap/substitute a root without access to an independent owner-controlled anchor?

### C3 — native-project sovereignty

Does the native project, rather than CPI, define/approve the bootstrap trust basis and root?

### C4 — exact binding / substitution resistance

Can evidence bind the exact:

`project + authority_domain + candidate public key/key-id + bootstrap policy`

so substitution/rebinding fails?

### C5 — explicit trust basis

Can an auditor state exactly what external/native assumption caused the candidate root to be trusted?

### C6 — durable replayable evidence

Can the bootstrap evidence be preserved and independently replayed after the original provider/session is unavailable?

### C7 — anti-replay / generation safety

Can an old otherwise-valid bootstrap declaration be distinguished from the intended bootstrap generation/context?

### C8 — provider neutrality

Can the architecture work without making one provider identity system universally authoritative?

### C9 — human-control evidence

Can the architecture include evidence unavailable to ordinary automation and meaningfully tied to a human-controlled trust anchor?

User-presence alone does not automatically establish native owner identity unless the credential itself is independently bound.

### C10 — anchor compromise isolation

Does compromise of one ordinary provider credential avoid silently compromising the trust root?

### C11 — offline verifiability

Can core proof validity be checked offline given preserved evidence and the declared trust anchor material?

### C12 — future key-lifecycle extensibility

Can later rotation/recovery/succession be added without changing the genesis trust semantics?

### C13 — operator burden

3 = low burden; 0 = impractical burden.

### C14 — project adoption feasibility

Can materially different project types adopt the architecture without inheriting another project's provider or governance model?

### C15 — CPI consequence separation

Does successful bootstrap verification establish only a trust-root fact, never CPI authorization to execute project effects?

## 7. Hard gates

A candidate is ineligible if it scores below 2 on any of:

- C1 non-circular trust;
- C2 same-account automation separation;
- C3 native sovereignty;
- C4 exact binding/substitution resistance;
- C5 explicit trust basis;
- C6 durable replayable evidence;
- C15 consequence separation.

Weighted totals cannot override a failed hard gate.

## 8. Selection rule

An architecture may be selected only if:

1. every hard gate passes;
2. its trust assumptions are explicit;
3. it does not claim to prove native owner identity from self-signature or provider identity alone;
4. it does not make CPI the bootstrap authority;
5. no simpler surviving candidate offers equivalent guarantees with lower trust/burden.

If no candidate survives:

`NO_BOOTSTRAP_ARCHITECTURE_SELECTED__FURTHER_RESEARCH_REQUIRED`

If a framework candidate survives but no concrete native anchor exists:

`ARCHITECTURE_SELECTED_FOR_RESEARCH__NATIVE_ROOT_NOT_ESTABLISHED`

## 9. Required falsification cases

Any selected architecture must be able to address at least:

1. candidate Authority key self-signs its own genesis declaration;
2. same-account automation publishes a replacement key;
3. automation creates a provider-verified commit naming its key;
4. attacker key is first in a TOFU race;
5. valid root evidence is copied to another project;
6. valid root evidence is copied to another authority domain;
7. candidate key is substituted after an anchor signed the intended key;
8. bootstrap policy is altered after proofs were generated;
9. old bootstrap generation is replayed;
10. threshold profile is missing a required anchor;
11. two contradictory fully valid root manifests appear;
12. provider becomes unavailable after bootstrap;
13. CPI supplies a key without native anchor evidence;
14. same-account automation controls the native carrier but not the independent anchor;
15. valid bootstrap proof is observed but `execution_authorized_by_cpi` remains false;
16. anchor provenance is ambiguous or omitted;
17. a human-presence credential is created and used in the same ceremony without an independent native binding;
18. OIDC/workflow identity is confused with human owner identity;
19. candidate private-key possession is confused with authorization;
20. a bootstrap verifier silently substitutes its own trust anchor.

## 10. Standards/reference sanity checks

Stage 7A may use existing systems as comparative evidence, not as automatic solutions.

Relevant patterns include:

- TUF: trusted root metadata identifies trusted role keys and thresholds; initial trust still requires a trusted root distribution assumption;
- Sigstore: signing identity chains to OIDC identity plus a separately distributed trust root/transparency infrastructure;
- WebAuthn/FIDO: user presence/verification can strongly authenticate use of a credential, but the relying party must still establish which credential/identity it trusts.

No external standard is presumed to satisfy native-project sovereignty by itself.

## 11. Optional prototype boundary

Only after the scorecard/selection is frozen may Stage 7A create a research-only prototype in Project-Continuity-Research.

No prototype may:

- generate or request a real owner credential;
- mutate a native project;
- register a real WebAuthn/passkey;
- alter DNS;
- establish a real trust root;
- deploy currentness/federation.

Ephemeral test keys / synthetic anchor proofs are permitted.

## 12. Required Stage-7A output

Stage 7A must freeze:

1. architecture scorecard;
2. selected architecture or explicit no-selection;
3. formal bootstrap trust semantics;
4. explicit distinction between:
   - proof of key possession;
   - proof of anchor control;
   - native authorization to trust the key;
5. optional research prototype evidence;
6. native-adoption boundary;
7. next independent audit gate.

## 13. Preserved controls

No mutation to:

- HiVenues;
- NFC;
- FCP;
- PGH;
- Evidence-Based-Market-Methods;
- Project Observatory.

No real owner key.
No real bootstrap anchor.
No currentness/completeness mechanism.
No native adoption.
No live federation.

False bridge remains:

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

`FEDERATION_OPTIONALITY = PASS`
