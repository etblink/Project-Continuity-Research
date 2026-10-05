# CPI-0 Stage-7A Native Trust-Root Bootstrap Architecture Scorecard and Selection 0.1.0

Date: 2026-10-04
Status: FROZEN ARCHITECTURE SELECTION
Program: CPI-0 — Cross-Project Interoperability
Governing issue: #41
Preregistration commit: `97e61e35187e1235d793aec24aad94d39633921a`
Hive profile note commit: `c82c9b5b9ba7ec78c9b670840d132e0c8d26fecf`

## 1. Scoring rule

Scores:

- 0 = fails;
- 1 = materially incomplete;
- 2 = workable with important caveats;
- 3 = strong.

Hard gates:

- C1 non-circular trust;
- C2 same-account automation separation;
- C3 native-project sovereignty;
- C4 exact binding/substitution resistance;
- C5 explicit trust basis;
- C6 durable replayable evidence;
- C15 CPI consequence separation.

Any score below 2 on a hard gate makes the candidate ineligible regardless of total score.

## 2. Scorecard

| Criterion | A Self-signed root | B Provider-owner declaration | C TOFU | D Single independent anchor | E Threshold multi-anchor | F Native Bootstrap Manifest + explicit anchor policy |
|---|---:|---:|---:|---:|---:|---:|
| C1 Non-circular trust | 0 | 1 | 0 | 3 | 3 | 3 |
| C2 Same-account automation separation | 0 | 0 | 0 | 3 | 3 | 3 |
| C3 Native-project sovereignty | 1 | 2 | 1 | 3 | 3 | 3 |
| C4 Exact binding / substitution resistance | 2 | 3 | 2 | 3 | 3 | 3 |
| C5 Explicit trust basis | 0 | 2 | 1 | 3 | 3 | 3 |
| C6 Durable replayable evidence | 3 | 2 | 3 | 3 | 3 | 3 |
| C7 Anti-replay / generation safety | 1 | 2 | 1 | 3 | 3 | 3 |
| C8 Provider neutrality | 3 | 0 | 3 | 2 | 3 | 3 |
| C9 Human-control evidence | 0 | 0 | 0 | 3 | 3 | 3 |
| C10 Ordinary-provider compromise isolation | 0 | 0 | 0 | 3 | 3 | 3 |
| C11 Offline verifiability | 3 | 2 | 3 | 3 | 3 | 3 |
| C12 Future key-lifecycle extensibility | 3 | 2 | 2 | 2 | 3 | 3 |
| C13 Operator burden | 3 | 3 | 3 | 2 | 1 | 2 |
| C14 Project adoption feasibility | 3 | 1 | 3 | 2 | 1 | 3 |
| C15 CPI consequence separation | 3 | 3 | 3 | 3 | 3 | 3 |
| **Total / 45** | **25** | **23** | **25** | **41** | **42** | **44** |
| **Hard gates passed?** | **NO** | **NO** | **NO** | **YES** | **YES** | **YES** |

## 3. Candidate A — self-signed genesis root

### Result

`INELIGIBLE`

A self-signature proves possession of the candidate root key.

It does not prove that the native project authorized that key to become its root.

Same-account automation can generate a new candidate key and self-sign the same declaration.

The candidate therefore fails C1, C2 and C5.

## 4. Candidate B — provider-owner declaration

### Result

`INELIGIBLE UNDER THE FROZEN THREAT MODEL`

A structured declaration through GitHub or another provider can strongly bind a key to a repository artifact.

But Stage 7A explicitly assumes ordinary automation may act through the same provider account.

Therefore provider-owner status, provider publication and ordinary provider credentials cannot by themselves separate the human owner from automation.

A provider-verified commit would become a different case only when its signing credential is itself independently controlled and natively trusted. At that point it is an instance of Candidate D rather than Candidate B.

## 5. Candidate C — trust on first use

### Result

`INELIGIBLE`

TOFU can make later substitution visible.

It does not prove the first key was the intended native root.

A race won by automation or an attacker becomes permanently pinned.

It fails C1 and C2.

## 6. Candidate D — single pre-existing independent anchor

### Result

`QUALIFYING MINIMUM TRUST PROFILE`

Candidate D passes every hard gate when all of the following are true:

1. the native project explicitly chooses the anchor;
2. the anchor exists independently of the candidate Authority Capsule key;
3. ordinary project automation does not control the anchor;
4. the anchor authenticates the exact project/domain/candidate-key/policy/generation binding;
5. preserved evidence can be replayed later;
6. the verifier does not infer CPI consequence authority.

Candidate D is the smallest trust model that survives the frozen bootstrap threat model.

It remains anchor-specific: every concrete anchor needs a defined proof format and verification method.

## 7. Candidate E — threshold multi-anchor bootstrap

### Result

`QUALIFYING OPTIONAL HIGHER-ASSURANCE PROFILE`

Threshold multi-anchor bootstrap provides strong compromise isolation and explicit corroboration.

It is not selected as the default minimum because:

- many projects do not possess multiple independent anchors;
- operator burden is substantially higher;
- Candidate D already passes the frozen hard gates.

Threshold profiles remain a valid future policy option for projects whose risk warrants them.

## 8. Candidate F — Native Bootstrap Manifest with explicit anchor policy

### Result

`SELECTED_FOR_RESEARCH`

Candidate F is selected as the project-neutral architecture.

It does **not** create trust by itself.

Instead it standardizes the exact object being authorized and the verification boundary around one or more native anchors.

A conforming Candidate-F policy must require at least one qualifying Candidate-D-style independent anchor.

It may optionally require Candidate-E threshold evidence.

### Why F is not defeated by the simpler D candidate

Candidate D answers:

`WHAT PRE-EXISTING THING DO WE TRUST?`

Candidate F answers:

`WHAT EXACT ROOT BINDING IS THAT THING AUTHORIZING, UNDER WHAT POLICY AND GENERATION?`

D alone requires each anchor integration to invent its own binding, anti-replay and provenance representation.

F adds the smallest common project-neutral representation needed for:

- exact project/domain/root-key binding;
- policy identity;
- generation/replay separation;
- anchor proof references;
- common audit/replay behavior.

Therefore D and F are complementary rather than competing equivalents:

```text
F = COMMON BOOTSTRAP MANIFEST / VERIFICATION BOUNDARY
D = MINIMUM QUALIFYING ANCHOR POLICY
E = OPTIONAL THRESHOLD ANCHOR POLICY
```

## 9. Selected architecture

```text
SELECTED_BOOTSTRAP_ARCHITECTURE =
F__NATIVE_BOOTSTRAP_MANIFEST_WITH_EXPLICIT_ANCHOR_POLICY

MINIMUM_QUALIFYING_TRUST_PROFILE =
D__SINGLE_PREEXISTING_INDEPENDENT_ANCHOR

OPTIONAL_HIGHER_ASSURANCE_PROFILE =
E__THRESHOLD_MULTI_ANCHOR
```

## 10. No-trust-from-nothing result

The preregistered proposition survives:

`NO TRUST FROM NOTHING = PASS`

Stage 7A finds no architecture that can derive the first native root purely from:

- the candidate key;
- first observation;
- same-account provider identity.

A bootstrap architecture must expose at least one independent native trust assumption.

This is not a defect in Candidate F.

It is the thing Candidate F is designed to make explicit.

## 11. Hive Active profile adjudication

The profile:

`HIVE_ACTIVE_AUTHORITY_ANCHOR`

is retained as a plausible Candidate-D instance within Candidate F.

For that profile:

```text
candidate native anchor:
Hive mainnet account @etblink
required authority:
ACTIVE
human signing interface:
Hive Keychain requestSignBuffer
```

The architecture-level trust assumption would be:

`THE NATIVE PROJECT CHOOSES THE DECLARED HIVE ACCOUNT'S ACTIVE AUTHORITY AS A BOOTSTRAP ANCHOR`

Hive Keychain is not itself the anchor.

It is the signing/key-custody interface.

The profile is qualifying only if ordinary project automation lacks sufficient Hive Active authority.

A posting-key signature is not interchangeable with the Active-anchor profile.

## 12. Critical Hive profile caveat

A Hive signature proves control of a Hive key.

A verifier must additionally establish that the signer satisfies the declared account's Active authority under the relevant preserved Hive authority state.

The profile must not reduce:

`SIGNATURE FROM SOME KEY ASSOCIATED WITH @etblink`

to:

`SATISFIES @etblink ACTIVE AUTHORITY`

without threshold/account-authority evaluation.

How the relevant Hive authority state is durably bound/replayed is a prototype/audit question, not assumed solved here.

## 13. Human ceremony boundary

Candidate F does not automate away the genesis trust decision.

For a one-time bootstrap ceremony, the native owner/operator must explicitly choose the anchor policy.

For a Hive profile this means consciously selecting:

```text
network = hive-mainnet
anchor account = <native project chosen account>
authority = active
policy = HIVE_ACTIVE_SIGNATURE_V1
```

The signed manifest then makes that choice durable and machine-verifiable.

The verifier must not choose the account on the project's behalf.

## 14. Selection status

`ARCHITECTURE_SELECTED_FOR_RESEARCH__NATIVE_ROOT_NOT_ESTABLISHED`

No real project root has been created.

No Hive signature has been requested.

No native project has adopted the selected architecture.

## 15. Prototype authorization

A research-only prototype inside Project-Continuity-Research is authorized after this frozen selection.

It may use:

- synthetic Native Bootstrap Manifests;
- ephemeral candidate Authority Capsule keys;
- synthetic independent anchor keys;
- synthetic Hive-account authority fixtures;
- offline signature/threshold verification;
- deterministic test vectors.

It may not:

- invoke a real user's Hive Keychain;
- request a real @etblink signature;
- broadcast to Hive;
- mutate DNS;
- alter HiVenues or another native project;
- establish a live trust root;
- create currentness/federation.

## 16. Next research objective

Prototype and adversarially test the common Candidate-F manifest and the minimum Candidate-D anchor boundary.

The Hive Active profile should be represented as a first concrete external-anchor adapter, but any incomplete Hive-specific verification must be labeled as such rather than treated as a qualified native root.
