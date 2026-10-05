# CPI-0 Stage-6T Independent JCS Integer-Domain Portability Re-Audit Launch Prompt 0.1.0

You are the independent evaluator for CPI-0 Stage 6T.

## Independence

Do not use prior conversation memory as audit evidence.

Treat Stage-6S specification, code, tests, CI and report as claims to independently verify.

Do not repair findings.
Do not merge.
Do not modify observed projects or Project Observatory.
Do not implement native adoption, completeness/currentness, or federation.

## Repository / branch

Repository:

`etblink/Project-Continuity-Research`

Audit branch:

`audit/cpi0-stage6t-independent-jcs-integer-domain`

Start from the exact launch-control commit containing this prompt.

## Controlling prior independent audit

Stage-6R:

- audit commit: `fb89b8052be339a0b404f4a1b05af216d6adc288`
- report blob: `99705d59555b6faf1d54bfa391c613ed1019443a`
- disposition: `PASS_WITH_NONMATERIAL_FINDINGS`

Stage-6R independently adjudicated:

```text
CPI6P-001 = PARTIALLY CLOSED
CPI6P-002 = CLOSED
CPI6P-003 = CLOSED
CPI6N-001 = CLOSED AT OBSERVED-ONLY SCOPE
CPI6N-002 = CLOSED
S3 = 0
S2 = 0
HARD_GATE_PREMISE_FAILURE = NONE
```

Residual Stage-6R S1:

`CPI6R-001 — sequence above 2^53 is not RFC-8785/JCS portable as an exact JSON number`.

## Stage-6S artifacts under audit

Preregistration:

`prototype/cpi0/stage6s/STAGE6S_JCS_INTEGER_DOMAIN_PREREGISTRATION_0_1_0.md`

Specification:

`prototype/cpi0/stage6s/AUTHORITY_CAPSULE_RESEARCH_SPEC_0_1_3.md`

Implementation:

`prototype/cpi0/stage6s/authority_capsule_v0_1_3.py`

Tests:

`prototype/cpi0/stage6s/test_authority_capsule_v0_1_3.py`

Report:

`prototype/cpi0/stage6s/EXPERIMENT_REPORT_0_1_0.md`

Qualified workflow-bearing commit:

`73928a3ebe104a84bd1dc45a41f00262abce8136`

Qualification run:

`37250522536` — claimed SUCCESS, 26/26 tests

Report-bearing commit:

`6a451f4bfda3ccf23a354bb8c1ae416c89c72bf0`

Report-bearing run:

`37250596669` — claimed SUCCESS

Treat all CI/run claims as claims to inspect where access permits and independently reproduce regardless.

## A. Execute independently

From a fresh checkout of launch-control:

1. install exactly Stage-6S requirements;
2. py_compile implementation/tests;
3. run the complete committed test suite;
4. reproduce the Stage-6M deterministic key/signature/capsule vector independently;
5. build independent probes rather than relying only on committed tests.

## B. Re-adjudicate CPI6R-001

The Stage-6S repair changes the allowed sequence domain to:

`1 <= sequence <= 2^53 - 1`

Independently determine whether this closes the RFC-8785/JCS portability gap.

Use at least two implementations/runtimes where available, including an ECMAScript implementation.

Test exact sequence boundary values:

- 1;
- 2^53 - 2;
- 2^53 - 1;
- 2^53;
- 2^53 + 1;
- 2^63 - 1;
- zero;
- negative values;
- float/exponent/string/bool variants.

Confirm or falsify:

- every accepted sequence is exactly representable under ECMAScript Number;
- RFC-8785/JCS serialization of every accepted boundary integer is the same exact decimal spelling as the prototype;
- every out-of-domain sequence is rejected before signature authority semantics;
- no accepted pair of distinct sequences collapses to the same ECMAScript/JCS value;
- deterministic Stage-6M vector remains unchanged.

Search the implementation/spec for any other numeric field or hidden path that bypasses this bound.

## C. Independent cross-runtime canonicalization

Re-test the Stage-6R portability surface at least enough to ensure the sequence repair did not regress string portability:

- solidus;
- quotes/backslash;
- C0 controls;
- DEL;
- BMP/supplementary Unicode;
- U+2028/U+2029;
- <>&;
- NFC/NFD.

Confirm the written spec and implementation still agree with RFC-8785/JCS for every valid capsule.

## D. Re-adjudicate Stage-6R S0 cleanup

### CPI6R-002

Confirm the stale private helper / `__canonical_envelope_bytes` NameError is gone, not merely uncalled.

### CPI6R-003

Confirm public `sign_capsule_artifact` exposes explicit keyword-only fields.

Distinguish:
- Python call-signature misuse, which may raise normal `TypeError`;
- malformed authority field values after entry, which should remain within `CapsuleError`.

Check whether this distinction is stated consistently by the spec.

### CPI6R-004

Confirm caller iterator exceptions may propagate by explicit contract and cannot be mistaken for an authority result.

### CPI6R-005

Confirm:
- malformed/noncanonical artifacts abort;
- canonical foreign-binding artifacts are partitioned before target signature verification;
- `foreign_artifact_count` is not presented as authenticated foreign authority.

### CPI6R-006

Independently reproduce `pin_provenance_digest` from the exact specified record and RFC-8785 bytes.

Verify:
- it changes with every bound input;
- it is not claimed as authenticated provenance;
- no stale v0.1.1/v0.1.2 currentness error text remains.

## E. Preserve prior closures

Re-run critical regressions sufficient to verify no regression of:

- CPI6P-002 Mapping-laundering closure;
- CPI6P-003 raw-pin/error closure;
- CPI6N-001 observed-only suppression/currentness closure;
- CPI6N-002 duplicate-key raw parsing closure.

At minimum test:

- PASS -> WITHDRAW;
- suppressed WITHDRAW;
- owner fork;
- head-only replay;
- sequence gap;
- duplicate-key polyglot;
- public API surface;
- Ed25519PublicKey-object pin;
- identity/torsion pin if practical.

Valid results must still carry:

```text
observed_chain_valid = true
authority_state = OBSERVED_CHAIN_ONLY
completeness_status = NOT_ESTABLISHED
current_decision = null
execution_authorized_by_cpi = false
```

## F. New-defect search

Search adversarially for new S2/S3, including:

- off-by-one safe-integer errors;
- parse-time vs authoring-time bound disagreement;
- signed artifact manually constructed with out-of-domain sequence;
- digesting out-of-domain raw artifacts;
- foreign-chain out-of-domain artifacts;
- sequence continuity behavior near the maximum;
- public/private API leaks;
- stale version confusion;
- accidental effect/I/O paths.

Do not inflate fail-closed nonmaterial issues into S2 unless they can create materially wrong owner authority/state/next action.

## G. Architecture status

Do not reopen Signed Authority Capsule architecture unless a hard-gate premise genuinely fails.

Distinguish:

- closure of CPI6R-001;
- nonmaterial cleanup findings;
- deferred adoption prerequisites;
- architecture-level defects.

## H. Boundaries

Confirm Stage 6S did not modify:

- HiVenues;
- NFC;
- FCP;
- PGH;
- Evidence-Based-Market-Methods;
- Project Observatory.

Confirm no:

- real owner private key;
- native capsule adoption;
- completeness/currentness mechanism;
- live Project Observatory integration;
- live federation.

## I. False bridge / optionality

Reconfirm unless native evidence falsifies:

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
FEDERATION_OPTIONALITY = PASS
```

## Severity / final disposition

Use the existing CPI severity scale.

Final disposition must be exactly one:

- `PASS__CPI6R_001_CLOSED`
- `PASS_WITH_NONMATERIAL_FINDINGS`
- `REPAIR_REQUIRED`
- `ARCHITECTURE_RECONSIDERATION_REQUIRED`
- `INSUFFICIENT_AUDIT`

Any unresolved S2 requires at least `REPAIR_REQUIRED`.

Use architecture reconsideration only if a hard-gate premise fails.

## Required output

Write exactly one report:

`prototype/cpi0/stage6t/STAGE6T_INDEPENDENT_JCS_INTEGER_DOMAIN_REAUDIT_REPORT_0_1_0.md`

The report must include:

- evaluator identity / independence;
- exact launch-control identity;
- audited blobs;
- independent execution;
- CPI6R-001 adjudication;
- S0 cleanup adjudication;
- preserved prior closures;
- new findings by severity;
- architecture status;
- mutation/adoption boundary;
- false bridge / federation optionality;
- final disposition.

If push is unavailable, create the exact raw Markdown report locally and provide:

- local audit commit;
- parent launch-control;
- exact report Git blob;
- raw .md attachment;
- optional format-patch backup.

Then stop.

Do not repair.
Do not merge.
Do not implement native adoption/currentness/federation.
