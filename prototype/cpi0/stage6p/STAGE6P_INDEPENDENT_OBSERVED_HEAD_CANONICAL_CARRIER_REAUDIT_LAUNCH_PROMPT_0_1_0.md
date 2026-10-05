# CPI-0 Stage-6P Independent Observed-Head / Canonical-Carrier Re-Audit Launch Prompt 0.1.0

You are the independent evaluator for CPI-0 Stage 6P.

## Independence

Do not use prior conversation memory as audit evidence.

Treat Stage-6O specification, code, tests, CI and report as claims to independently verify.

Do not repair findings.

Do not merge.

Do not modify NFC, FCP, PGH, HiVenues, Evidence-Based-Market-Methods, Project Observatory, or any planned/future project.

Do not create a live authority surface, native capsule deployment or federation.

## Repository / branch

Repository:

`etblink/Project-Continuity-Research`

Audit branch:

`audit/cpi0-stage6p-independent-observed-head-canonical-carrier`

The audit branch must start from the exact Stage-6P launch-control commit containing this prompt.

## Controlling prior evidence

Stage-6N independent audit:

- published commit: `109f641108ffe94b32e22e579b51124bd3c2db5d`
- report blob: `75ce1814b1daf69ba9ba903f9e4c774166d82b15`
- disposition: `REPAIR_REQUIRED`

Stage-6N S2 findings:

- `CPI6N-001` — suppression/truncation can restore an earlier signed PASS if a supplied chain head is called current;
- `CPI6N-002` — duplicate JSON keys permit parser-dependent authority because raw carrier parsing was unspecified.

Stage-6O corrective preregistration:

`prototype/cpi0/stage6o/STAGE6O_OBSERVED_HEAD_CANONICAL_CARRIER_CORRECTIVE_PREREGISTRATION_0_1_0.md`

Corrective specification:

`prototype/cpi0/stage6o/AUTHORITY_CAPSULE_RESEARCH_SPEC_0_1_1.md`

Corrective implementation:

`prototype/cpi0/stage6o/authority_capsule_v0_1_1.py`

Corrective tests:

`prototype/cpi0/stage6o/test_authority_capsule_v0_1_1.py`

Corrective report:

`prototype/cpi0/stage6o/EXPERIMENT_REPORT_0_1_0.md`

Exact implementation/workflow qualification:

- commit: `4219ce2e862b45f0ba7716d3ed8e356360e6dbba`
- run: `37247135673`
- claim: 42/42 tests PASS

Specification-bearing qualification:

- commit: `d7d583677414d379e08d251750340e9b6cd91f10`
- run: `37247224183`
- claim: SUCCESS

Report-bearing qualification:

- commit: `76b7afc6cf6c8381480211f20515c1f708be5609`
- run: `37247311431`
- claim: SUCCESS

Treat every CI result as a claim to inspect where access permits and independently reproduce regardless.

## A. Execute the corrective prototype

From a fresh checkout of launch-control:

1. install exactly `prototype/cpi0/stage6o/requirements.txt`;
2. run `py_compile` on the Stage-6O implementation and tests;
3. run the full committed Stage-6O unittest suite;
4. reproduce the deterministic Stage-6M vector;
5. independently implement or script additional probes rather than relying only on the committed tests.

Do not treat 42/42 PASS as proof.

## B. Re-adjudicate CPI6N-001 — completeness / suppression

The Stage-6O repair does **not** claim to prove chain completeness.

Its claim is narrower:

- a verified supplied chain yields only `latest_observed_decision`;
- `current_decision` remains null;
- `completeness_status = NOT_ESTABLISHED`;
- requesting current authority fails closed;
- therefore suppression/truncation changes observed history but cannot be misreported as established current authority.

Independently test at minimum:

1. PASS -> WITHDRAW complete chain;
2. same chain with WITHDRAW suppressed;
3. REJECT(A) -> PASS(B) -> WITHDRAW(B);
4. same chain with sequence 3 suppressed;
5. owner-signed same-sequence fork with both branches present;
6. same fork with one branch withheld;
7. head-only replay;
8. missing middle sequence;
9. arbitrary input order;
10. exact duplicate carrier replication.

Then search every Stage-6O authority-bearing API/result/spec statement for any residual path that still converts an incomplete observed set into "current", "accepted", "authorized", or equivalent semantics.

Determine whether retiring the currentness claim genuinely closes CPI6N-001 at the claimed scope or merely renames the stale decision while downstream consumers can still mistake it for current authority.

Pay particular attention to field names, helper functions, report language, versioning and whether `capsule_chain_valid = true` could reasonably be confused with completeness.

## C. Re-adjudicate CPI6N-002 — raw parsing / duplicate keys

Independently reconstruct the raw artifact parser from the 0.1.1 specification.

Test at minimum:

1. Stage-6N duplicate-key first/last-wins polyglot;
2. duplicate key with equal values;
3. duplicate key in a nested object if the parser can reach one;
4. leading/trailing whitespace;
5. trailing newline;
6. UTF-8 BOM;
7. malformed UTF-8;
8. alternate key order;
9. equivalent Unicode escape vs literal Unicode;
10. equivalent ASCII escape such as `\u0050ASS`;
11. escaped solidus;
12. control-character escape forms;
13. NaN / Infinity / -Infinity;
14. floats / exponent forms;
15. multiple concatenated JSON values;
16. non-object JSON roots;
17. extra/missing fields.

Verify that the public authority-bearing API accepts raw artifacts, not arbitrary mappings.

Search for any alternate public path that bypasses canonical raw parsing.

## D. Cross-language canonicalization audit

Stage 6O now requires exact canonical envelope bytes.

Independently determine whether the specification is sufficiently precise for another conforming implementation to reproduce the same artifact bytes.

Test at least:

- ASCII;
- BMP non-ASCII;
- supplementary-plane Unicode;
- quote and backslash;
- U+0000 through U+001F controls;
- U+2028 / U+2029;
- solidus;
- NFC vs NFD identifiers;
- integer representation.

If two reasonable implementations following the written spec can emit different "canonical" bytes, classify the effect according to whether the same authority record can become nonportable or parser-dependent.

Do not assume Python `json.dumps` defines a cross-language standard merely because the prototype uses it.

## E. Pin-validation audit

Independently test Stage-6O public-key validation.

At minimum:

- identity point;
- known small-order/torsion points if available;
- noncanonical y encoding;
- invalid/non-curve encoding;
- valid deterministic Stage-6M key;
- several generated valid keys;
- wrong but valid key;
- key-ID substitution.

Check whether the custom prime-order subgroup validation is mathematically and operationally sound or introduces its own acceptance/rejection defects.

## F. Pin-provenance audit

Stage 6O does not claim to solve native pin bootstrap.

It claims only that provenance is explicit and auditable.

Verify:

- output binds to the exact pin key ID;
- project and authority domain are in the pin object;
- provenance ID/revision are surfaced;
- provenance digest changes if key or provenance metadata changes;
- the verifier does not claim that the provenance itself is authenticated;
- native adoption remains blocked on an independently authoritative pin bootstrap.

Do not upgrade the explicitly deferred bootstrap problem to S2 merely because it remains deferred unless Stage 6O overclaims it.

## G. Binding-partition / DoS audit

Test:

- valid foreign subject capsule injected into target set;
- foreign project;
- foreign domain;
- foreign candidate;
- multiple foreign chains at overlapping sequence numbers;
- foreign capsule signed by owner key;
- foreign capsule signed by another key;
- malformed foreign-looking artifact;
- forged target-binding artifact.

Determine whether unrelated valid chains are partitioned without allowing a forged target capsule through.

Classify fail-closed malformed-input DoS proportionately.

## H. Error/resource audit

Probe malformed values beyond committed tests:

- unhashable/list/dict values;
- lone surrogates;
- deeply nested JSON;
- very long strings;
- sequence 0 / -1 / 2^63-1 / 2^63;
- huge numeric token;
- generator/iterator failures;
- duplicate artifacts at scale.

Verify malformed public inputs fail through the intended `CapsuleError` family where claimed and that sequence handling no longer allocates proportional to an attacker-controlled maximum value.

## I. Consequence separation

Reconfirm:

- `execution_authorized_by_cpi` is never true;
- no current decision is produced in version 0.1.1;
- ordinary prose, GitHub OWNER, review/label/issue state have no authority input path;
- Stage 6O cannot trigger HiVenues or another project effect;
- no completeness witness was silently introduced;
- no real owner key exists.

## J. Architecture status

Do not automatically reopen Stage-6M architecture selection.

Reconsider Candidate E only if Stage 6O reveals a hard-gate premise failure.

Otherwise distinguish:

- closure of Stage-6N S2s;
- new repairable prototype/spec findings;
- deferred adoption problems;
- architecture-level failure.

## K. Mutation / adoption audit

Confirm Stage 6O did not modify:

- HiVenues;
- NFC;
- FCP;
- PGH;
- Evidence-Based-Market-Methods;
- Project Observatory.

Confirm:

- no historical #374/#398/#399 conversion;
- no native capsule deployment;
- no real owner private key;
- no live authority surface;
- no live Project Observatory integration;
- no federation.

## L. False bridge / optionality

Reconfirm:

```text
HiVenues/Hive -> NFC/PGH
DEPENDENCY = NONE / NOT ESTABLISHED
STATUS = HELD SPECULATION
```

and:

`FEDERATION_OPTIONALITY = PASS`

unless native evidence falsifies them.

## Severity

Use the existing CPI severity scale.

Any path that makes an incomplete observed set become established current authority is material.

Any raw carrier that can validly produce different owner authority under two conforming parsers is material.

Any path that makes a non-owner key accepted under a sound pinned owner key is material.

Any path that turns CPI observation into external-effect authorization is severe.

Fail-closed availability or error-taxonomy defects are normally lower severity unless they invalidate a frozen claim.

## Final disposition

Use exactly one:

- `PASS__STAGE6N_S2_FINDINGS_CLOSED`
- `PASS_WITH_NONMATERIAL_FINDINGS`
- `REPAIR_REQUIRED`
- `ARCHITECTURE_RECONSIDERATION_REQUIRED`
- `INSUFFICIENT_AUDIT`

Any unresolved S2 requires at least `REPAIR_REQUIRED`.

Use `ARCHITECTURE_RECONSIDERATION_REQUIRED` only if a hard-gate premise of the selected Signed Authority Capsule architecture fails.

## Required output

Write exactly one report:

`prototype/cpi0/stage6p/STAGE6P_INDEPENDENT_OBSERVED_HEAD_CANONICAL_CARRIER_REAUDIT_REPORT_0_1_0.md`

The report must include:

- evaluator identity / independence;
- exact launch-control identity;
- exact audited file blobs;
- independent executable results;
- CPI6N-001 re-adjudication;
- CPI6N-002 re-adjudication;
- canonicalization/parser findings;
- pin-validation/provenance findings;
- binding/resource findings;
- new findings by severity;
- architecture status;
- mutation/adoption audit;
- false-bridge / federation-optionalitity results;
- final disposition.

If the environment cannot push, still create the exact raw Markdown report locally and provide:

- local audit commit;
- parent launch-control;
- exact report Git blob;
- raw .md attachment;
- optional git-format patch backup.

## Stop rule

After the report is frozen:

- stop;
- do not repair;
- do not merge;
- do not modify observed projects;
- do not implement completeness/currentness protocol;
- do not implement native adoption;
- do not enter live federation.
