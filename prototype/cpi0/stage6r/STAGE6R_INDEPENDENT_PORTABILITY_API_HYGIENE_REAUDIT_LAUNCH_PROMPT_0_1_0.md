# CPI-0 Stage-6R Independent Canonical-Portability / API-Hygiene Re-Audit Launch Prompt 0.1.0

You are the independent evaluator for CPI-0 Stage 6R.

## Independence

Do not use prior conversation memory as audit evidence.

Treat Stage-6Q specification, code, tests, CI and report as claims to independently verify.

Do not repair findings.
Do not merge.
Do not modify observed projects or Project Observatory.
Do not implement native adoption, completeness/currentness, or federation.

## Repository / branch

Repository:

`etblink/Project-Continuity-Research`

Audit branch:

`audit/cpi0-stage6r-independent-portability-api-hygiene`

Start from the exact launch-control commit containing this prompt.

## Controlling prior independent audit

Stage-6P:

- published commit: `0fa8d43e1b9acba71accdf471de508c3af7fc9ca`
- report blob: `b4c2f2420b0654c5ff4ad22d95cc0cfb2c5dbe5b`
- disposition: `PASS_WITH_NONMATERIAL_FINDINGS`

Stage-6P independently found:

- `CPI6P-001` S1 — canonical form underspecified across languages;
- `CPI6P-002` S1 — public Mapping->artifact helpers can launder a nonconforming carrier;
- `CPI6P-003` S1 — public-key object pin leaks a non-CapsuleError.

Stage-6P also independently established:

```text
CPI6N-001 = CLOSED AT CLAIMED OBSERVED-ONLY SCOPE
CPI6N-002 = CLOSED
S3 = 0
S2 = 0
HARD_GATE_PREMISE_FAILURE = NONE
```

## Stage-6Q artifacts under audit

Preregistration:

`prototype/cpi0/stage6q/STAGE6Q_PORTABILITY_API_HYGIENE_PREREGISTRATION_0_1_0.md`

Specification:

`prototype/cpi0/stage6q/AUTHORITY_CAPSULE_RESEARCH_SPEC_0_1_2.md`

Implementation:

`prototype/cpi0/stage6q/authority_capsule_v0_1_2.py`

Tests:

`prototype/cpi0/stage6q/test_authority_capsule_v0_1_2.py`

Report:

`prototype/cpi0/stage6q/EXPERIMENT_REPORT_0_1_0.md`

Qualification provenance:

- initial workflow-bearing commit `146c2051aa38804b50106057eb1b401932c3778d`
- initial run `37249331417` = FAILURE due stale internal canonical helper reference
- repair/qualified commit `da3b3c405e46e540ac184c79595c863535c90dd3`
- controlling run `37249379733` = SUCCESS, 34/34 tests
- report-bearing commit `00cf4f22a02be3cdb7c577203a1e8fe6a3392740`
- report-bearing run `37249460488` = SUCCESS

The failed first run is part of provenance, not qualification evidence.

## A. Execute independently

From a fresh checkout of launch-control:

1. install exactly Stage-6Q requirements;
2. compile implementation/tests;
3. run the full committed suite;
4. reproduce the Stage-6M deterministic vector independently;
5. build independent probes rather than relying only on committed tests.

## B. Re-adjudicate CPI6P-001 — cross-language canonicalization

Independently determine whether the written 0.1.2 specification now defines a portable canonical representation.

Test at minimum:

- ASCII;
- solidus;
- quotes;
- backslash;
- C0 controls U+0000..U+001F;
- DEL;
- BMP non-ASCII;
- supplementary-plane Unicode;
- U+2028/U+2029;
- <>&;
- NFC/NFD;
- integer sequence edge cases.

Compare against RFC 8785/JCS semantics using an implementation independent of the prototype.

Confirm:

- prototype bytes are RFC-8785 compatible for the capsule schema;
- two conforming implementations produce identical bytes;
- nonconforming PHP/Go/default-library escapes fail closed;
- deterministic Stage-6M signature/digest are unchanged.

If the spec still admits multiple reasonable conforming encodings, report it.

## C. Re-adjudicate CPI6P-002 — mapping laundering

Audit the actual public module surface.

Confirm or falsify:

- no public function accepts arbitrary Mapping and emits a capsule artifact;
- no public function accepts arbitrary Mapping and returns an authority result;
- public digest accepts canonical raw bytes only;
- public authoring accepts typed fields and returns raw bytes;
- duplicate-key polyglot cannot be converted into a verifying artifact through any public API;
- internal underscore helpers are not exported through `__all__`;
- ordinary integrations using only the declared public surface cannot reintroduce first-wins/last-wins laundering.

Search for alternate public or repository-local adapter paths that bypass the raw boundary.

Historical Stage-6M/6O modules are frozen history; distinguish their existence from a current Stage-6Q consumer actually importing them.

## D. Re-adjudicate CPI6P-003 — pin typing/error contract

Test:

- valid raw 32-byte pin;
- `Ed25519PublicKey` object;
- bytearray;
- memoryview;
- string;
- null;
- short/long bytes;
- identity/torsion/mixed-order/noncanonical points;
- wrong but valid key.

All malformed pin inputs claimed in scope must fail through the CapsuleError hierarchy.

Verify there is no later path that assumes the stored pin is an object after raw-byte validation.

## E. Preserved observed-only semantics

Re-run critical Stage-6N closure cases:

- PASS -> WITHDRAW;
- suppressed WITHDRAW;
- owner fork present;
- fork branch withheld;
- head-only replay;
- sequence gap;
- duplicate raw artifacts;
- duplicate-key raw polyglot.

Confirm:

```text
observed_chain_valid = true  # only for valid observed chain
current_decision = null
completeness_status = NOT_ESTABLISHED
execution_authorized_by_cpi = false
```

Search for any Stage-6Q consumer that converts latest_observed_decision into current/accepted/execution semantics.

## F. Per-artifact failure scope

Verify the 0.1.2 specification and implementation agree:

- malformed/noncanonical artifact aborts whole verification;
- forged target artifact aborts;
- valid canonical foreign-binding artifact is partitioned.

Classify any mismatch by consequence.

## G. Signature/pin interoperability

Independently test Ed25519:

- canonical R;
- S < L;
- valid deterministic key;
- identity/torsion/mixed-order keys;
- signature malleation if practical.

Do not treat out-of-model owner-crafted verifier-divergent signatures as material unless Stage 6Q overclaims them.

## H. New-defect search

Adversarially inspect:

- `__all__` / public API leakage;
- import aliases;
- raw parser bypass;
- digest semantics;
- Unicode scalar handling;
- malformed iterator/artifact behavior;
- duplicate artifact resource behavior;
- stale historical module confusion;
- result field naming;
- accidental native-I/O/effect paths.

Search specifically for any new S2/S3.

## I. Boundaries

Confirm no mutation to:

- HiVenues;
- NFC;
- FCP;
- PGH;
- Evidence-Based-Market-Methods;
- Project Observatory.

Confirm no:

- real owner key;
- native capsule deployment;
- currentness/completeness mechanism;
- live Observatory integration;
- live federation.

## J. False bridge / optionality

Reconfirm:

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

and:

`FEDERATION_OPTIONALITY = PASS`

unless native evidence falsifies them.

## Severity / disposition

Use the CPI severity scale.

Final disposition must be exactly one:

- `PASS__STAGE6P_NONMATERIAL_FINDINGS_CLOSED`
- `PASS_WITH_NONMATERIAL_FINDINGS`
- `REPAIR_REQUIRED`
- `ARCHITECTURE_RECONSIDERATION_REQUIRED`
- `INSUFFICIENT_AUDIT`

Any unresolved S2 requires at least `REPAIR_REQUIRED`.

Use architecture reconsideration only for a hard-gate premise failure.

## Required output

Write exactly one report:

`prototype/cpi0/stage6r/STAGE6R_INDEPENDENT_PORTABILITY_API_HYGIENE_REAUDIT_REPORT_0_1_0.md`

Include:

- evaluator identity/independence;
- exact launch-control identity;
- audited blobs;
- independent execution;
- CPI6P-001/002/003 adjudication;
- preserved Stage-6N closure;
- new findings by severity;
- boundaries;
- false bridge / federation optionality;
- final disposition.

If push access is unavailable, create the exact raw .md report locally and report:

- local audit commit;
- parent launch-control;
- exact report Git blob;
- raw .md attachment;
- optional patch.

Then stop.

Do not repair.
Do not merge.
Do not implement adoption/currentness/federation.
