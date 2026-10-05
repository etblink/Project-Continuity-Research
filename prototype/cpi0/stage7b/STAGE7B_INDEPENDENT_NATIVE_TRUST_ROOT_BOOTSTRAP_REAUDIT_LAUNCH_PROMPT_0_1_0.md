# CPI-0 Stage-7B Independent Native Trust-Root Bootstrap Re-Audit Launch Prompt 0.1.0

You are the independent evaluator for CPI-0 Stage 7B.

## Independence

Do not use prior conversation memory as audit evidence.

Treat Stage-7A preregistration, scorecard, Hive profile note, specification, prototype, tests, CI and report as claims to independently verify.

Do not repair findings.
Do not merge.
Do not implement Hive/Keychain support.
Do not request any real user signature.
Do not modify observed projects or Project Observatory.
Do not implement currentness/completeness or federation.

## Repository / branch

Repository:

`etblink/Project-Continuity-Research`

Audit branch:

`audit/cpi0-stage7b-independent-native-trust-root-bootstrap`

Start from the exact launch-control commit containing this prompt.

## Controlling prior boundary

Stage-6 closure:

- closure commit `879005a6bbd40d123c24a1d87d77a8ad6b74f53b`
- independent Stage-6T audit commit `8b6c872cf7a2dd84c618aa2b92c64c02ed9d1014`
- Stage-6T report blob `00f856c9088b3ec24f5e350e124d977ff651b085`
- S3=0 / S2=0 / S1=0 at Stage-6 research scope

Stage 7A addresses only native public-key bootstrap/trust-root establishment.

Authenticated completeness/currentness remains out of scope.

## Stage-7A artifacts under audit

Preregistration:

`prototype/cpi0/stage7a/STAGE7A_NATIVE_TRUST_ROOT_BOOTSTRAP_PREREGISTRATION_0_1_0.md`

Hive profile note:

`prototype/cpi0/stage7a/STAGE7A_HIVE_ACTIVE_AUTHORITY_ANCHOR_PROFILE_NOTE_0_1_0.md`

Architecture scorecard:

`prototype/cpi0/stage7a/STAGE7A_NATIVE_TRUST_ROOT_SCORECARD_AND_SELECTION_0_1_0.md`

Formal specification:

`prototype/cpi0/stage7a/NATIVE_BOOTSTRAP_MANIFEST_RESEARCH_SPEC_0_1_0.md`

Prototype:

`prototype/cpi0/stage7a/native_bootstrap_manifest.py`

Tests:

`prototype/cpi0/stage7a/test_native_bootstrap_manifest.py`

Report:

`prototype/cpi0/stage7a/EXPERIMENT_REPORT_0_1_0.md`

Qualified implementation/workflow commit:

`d134bdf5a7d487a2052db0466368552bdf1ef05a`

Qualification run:

`37256735898` — claimed SUCCESS, 30/30 tests

Report-bearing commit:

`f7d23c49d47894dad8dae7073e2ccd8cdbc478a6`

Report-bearing run:

`37256828304` — claimed SUCCESS

Treat every CI result as a claim, not proof.

## Stage-7A selected result under audit

Stage 7A claims:

```text
NO_TRUST_FROM_NOTHING = PASS

SELECTED_BOOTSTRAP_ARCHITECTURE =
F__NATIVE_BOOTSTRAP_MANIFEST_WITH_EXPLICIT_ANCHOR_POLICY

MINIMUM_QUALIFYING_TRUST_PROFILE =
D__SINGLE_PREEXISTING_INDEPENDENT_ANCHOR

OPTIONAL_HIGHER_ASSURANCE_PROFILE =
E__THRESHOLD_MULTI_ANCHOR

HIVE_ACTIVE_PROFILE =
SPECIFIED__NOT_IMPLEMENTED

NATIVE_ROOT =
NOT ESTABLISHED
```

## A. Independently re-score Candidates A-F

Re-apply the frozen 15 criteria and hard gates.

Specifically challenge:

### Candidate A — self-signed root

Could any interpretation make self-signature establish native authorization, rather than merely key possession?

### Candidate B — provider-owner declaration

Under the frozen threat model, ordinary automation may act through the same provider account.

Determine whether provider publication alone can satisfy C2.

If a provider-verified commit uses a separate owner-controlled signing key, determine whether that is genuinely Candidate B or actually Candidate D.

### Candidate C — TOFU

Determine whether first observation plus later pinning provides any independent evidence that the first root was the intended native root.

### Candidate D — one independent pre-existing anchor

Determine whether a single independently trusted native anchor is actually enough to pass all frozen hard gates when exact binding/replay/provenance are present.

### Candidate E — threshold multi-anchor

Determine whether threshold evidence materially improves the hard-gate result or only compromise resilience, and whether the burden justifies making it mandatory.

### Candidate F — Native Bootstrap Manifest

Determine whether F adds a genuinely useful project-neutral binding/policy representation beyond D or merely relabels D.

The selection rule says F may win only if the simpler D candidate is not equivalent at lower burden.

If F's added representation does not provide a material common interoperability boundary, say so.

## B. Attack the NO TRUST FROM NOTHING conclusion

Try to falsify:

`A FIRST CRYPTOGRAPHIC TRUST ROOT CANNOT AUTHENTICATE ITS OWN AUTHORITY WITHOUT AN INDEPENDENT TRUST ASSUMPTION.`

Distinguish:

- proof of candidate-key possession;
- proof of external-anchor control;
- native authorization to trust that anchor/root.

Look for any hidden way Stage 7A derives the third from either of the first two.

If the architecture merely moves the unresolved trust question into the native policy, determine whether that is:

- an honest explicit boundary consistent with the research question; or
- a failure of C1/C3/C5 that invalidates selection.

This is a central audit question.

## C. Native policy provenance / circularity audit

The prototype accepts `NativeBootstrapPolicy` as an independent verifier input.

Adversarially test:

1. caller supplies an invented policy that pins an attacker key;
2. caller labels invented provenance as "native";
3. CPI/tooling substitutes another account/anchor/policy;
4. policy object is modified while manifest/proof remain valid;
5. two observers use different policies for the same project/domain;
6. policy provenance is absent, ambiguous or misleading.

Determine exactly what the verifier proves in these cases.

The expected Stage-7A claim is conditional:

`GIVEN AN INDEPENDENTLY SUPPLIED NATIVE POLICY, THE QUALIFYING ANCHOR AUTHENTICATED THIS EXACT ROOT BINDING.`

It does NOT claim to cryptographically prove that the policy itself is native.

If the implementation/report overclaims beyond that conditional statement, classify it materially.

## D. Execute and independently attack the prototype

From a fresh checkout:

1. install exactly Stage-7A requirements;
2. py_compile implementation/tests;
3. run the committed 30-test suite;
4. write independent probes, not just test wrappers.

At minimum reproduce:

1. valid independent anchor bootstrap;
2. candidate self-signature cannot substitute for anchor proof;
3. provider prose/OWNER state is not a proof;
4. wrong anchor key;
5. project rebinding;
6. authority-domain rebinding;
7. candidate root-key substitution;
8. policy substitution;
9. generation replay;
10. challenge substitution;
11. anchor-profile substitution;
12. anchor-subject substitution;
13. missing proof;
14. duplicate proof;
15. two contradictory valid genesis manifests;
16. duplicate same genesis;
17. offline replay;
18. CPI consequence separation;
19. duplicate-key JSON;
20. noncanonical JSON.

Also search for new defects.

## E. Raw/canonical manifest audit

Independently inspect the Native Bootstrap Manifest canonicalization.

Test:

- duplicate keys;
- leading/trailing whitespace;
- BOM;
- malformed UTF-8;
- non-object root;
- extra/missing fields;
- alternate JSON escapes;
- Unicode scalar edge cases;
- numeric JSON injection;
- candidate key-id syntax;
- challenge syntax;
- note digest syntax.

Determine whether Python's implementation is actually consistent with the specification's RFC-8785/JCS claim for the restricted strings/null schema.

## F. Conflict / replay semantics

Test:

- two distinct manifests, both legitimately signed by the same independent anchor under the same expected genesis policy;
- same manifest duplicated across carriers;
- old generation replay;
- same generation but changed challenge;
- changed candidate key;
- changed native policy ID.

Any two distinct independently valid genesis roots under a single-genesis policy must fail closed.

CPI must not choose a winner.

## G. Consequence separation

Verify that successful bootstrap never produces:

- current owner decision;
- merge/deploy permission;
- external-effect authorization;
- federation authority.

`execution_authorized_by_cpi` must remain false.

## H. Hive Active / Keychain profile audit

Stage 7A does not implement Hive support.

Verify that:

- `HIVE_ACTIVE_AUTHORITY_V1` fails closed as unsupported;
- Keychain callback/success state is not an authority input;
- no real @etblink signature exists;
- no Hive broadcast exists;
- no live root is established.

Independently assess the **plausibility** of the proposed profile from current public Hive/Keychain semantics:

- Keychain `requestSignBuffer` can request an Active-role message signature;
- Hive account authority is threshold-based and may include key/account authorities;
- a valid profile must establish that signer keys satisfy the declared account Active authority, not merely appear in account data;
- live account-authority RPC alone may be insufficient for historical/offline replay claims.

Do not mark the Hive profile qualified.

Classify only whether it is a plausible next research target.

## I. Hard-gate attack on same-account automation

Assume GitHub/provider automation can:

- create files;
- create commits;
- edit issues/comments;
- alter ordinary provider metadata within its permissions.

But it cannot access the independent anchor private key.

Determine whether it can nevertheless cause the Stage-7A verifier to trust an attacker Authority Capsule key **without also substituting the independently supplied native policy**.

If policy substitution is the only path, say so explicitly and connect that to the policy trust boundary.

## J. Project-neutrality audit

Determine whether Candidate F can support materially different native anchors without making:

- Hive;
- GitHub;
- WebAuthn;
- DNS;
- CPI

universally authoritative.

The architecture should standardize the manifest/binding boundary, not the native identity system.

## K. Mutation / adoption boundary

Confirm Stage 7A did not modify:

- HiVenues;
- NFC;
- FCP;
- PGH;
- Evidence-Based-Market-Methods;
- Project Observatory.

Confirm no:

- real owner key;
- real Hive signature;
- Hive broadcast;
- native trust-root deployment;
- native adoption;
- currentness/completeness mechanism;
- live federation.

## L. False bridge / federation optionality

Reconfirm unless native evidence falsifies:

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
FEDERATION_OPTIONALITY = PASS
```

## Severity / final disposition

Use the existing CPI severity scale.

Use exactly one:

- `PASS__BOOTSTRAP_ARCHITECTURE_AND_COMMON_PROTOTYPE_QUALIFIED`
- `PASS_WITH_NONMATERIAL_FINDINGS`
- `REPAIR_REQUIRED`
- `ARCHITECTURE_RECONSIDERATION_REQUIRED`
- `INSUFFICIENT_AUDIT`

Any unresolved S2 requires at least `REPAIR_REQUIRED`.

Use `ARCHITECTURE_RECONSIDERATION_REQUIRED` if a frozen hard-gate premise underlying F/D fails.

A finding that the native policy itself requires an independent trust assumption is not automatically a defect because Stage 7A explicitly claims that boundary. It becomes material if Stage 7A hides it, lets CPI silently supply it, or overclaims unconditional native authorization.

## Required output

Write exactly one report:

`prototype/cpi0/stage7b/STAGE7B_INDEPENDENT_NATIVE_TRUST_ROOT_BOOTSTRAP_REAUDIT_REPORT_0_1_0.md`

Include:

- evaluator identity / independence;
- exact launch-control identity;
- exact audited blobs;
- independent execution;
- independent A-F scorecard;
- no-trust-from-nothing adjudication;
- native-policy/circularity analysis;
- common-prototype attack results;
- conflict/replay results;
- Hive-profile plausibility/boundary result;
- new findings by severity;
- architecture status;
- mutation/adoption audit;
- false bridge / federation optionality;
- final disposition.

If push access is unavailable, create the exact raw Markdown report locally and provide:

- local audit commit;
- parent launch-control;
- exact report Git blob;
- raw .md attachment;
- optional format-patch.

Then stop.

Do not repair.
Do not merge.
Do not implement Hive support.
Do not request a real user signature.
Do not implement native adoption/currentness/federation.
