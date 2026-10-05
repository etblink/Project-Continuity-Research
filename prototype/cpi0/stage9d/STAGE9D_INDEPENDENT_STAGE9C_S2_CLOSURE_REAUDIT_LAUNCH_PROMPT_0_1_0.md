# CPI-0 Stage-9D Independent Stage-9C S2 Closure Re-Audit Launch Prompt 0.1.0

You are the independent Stage-9D evaluator for CPI-0.

Repository:

`https://github.com/etblink/Project-Continuity-Research`

Audit branch:

`audit/cpi0-stage9d-independent-stage9c-s2-closure`

Governing issue:

`#55 — [CPI-0 Stage 9D] Independent re-audit of narrowed Stage-9C S2 repair`

## 1. Exact launch lineage

The audit branch was created directly from the frozen Stage-9C corrective report commit:

`50a3d380589a3cf0f717bf8d06cac6367a985c0e`

Frozen Stage-9C report:

`prototype/cpi0/stage9c/STAGE9C_STAGE9B_S2_CORRECTIVE_REPORT_0_1_0.md`

Expected report blob:

`edc9d1f043efc60709b522f541f9a39d06bc8889`

This launch-prompt commit is the Stage-9D launch-control commit.

Before substantive audit work, independently verify:

1. current branch is exactly the named Stage-9D audit branch;
2. launch-control's parent is exactly `50a3d380589a3cf0f717bf8d06cac6367a985c0e`;
3. launch-control is exactly one commit ahead of that parent;
4. the only changed file is this launch prompt;
5. the Stage-9C report blob matches exactly;
6. the Stage-9C implementation/test/workflow blobs below match exactly.

If repository state disagrees, stop and report the discrepancy.

## 2. Controlling prior independent finding

Stage-9B independent audit:

- audit commit: `65324ed684ab3e14bd30cf0994c2053e8b2d6f0c`
- report blob: `711dfc3e79d37d335f92d17d4682cd49750f89e7`
- disposition: `REPAIR_REQUIRED`
- findings: 0×S3, 2×S2, 5×S1, 1×S0

Material findings to re-audit:

### F-01 — S2

Stage 9A falsely claimed its produced-only synthetic check could not report target irreversibility earlier than frozen Hive reference logic.

Independent counterexamples included:

- mainnet pre-voting behavior below block 864000;
- future-witness-schedule divergence;
- competing-fork witness production;
- a vacuous monotonicity self-check.

### F-02 — S2

Stage 9A emitted native/authenticated-looking positive booleans for attacker-authored synthetic fixtures and did not fully bind genesis-authority input.

Do not soften or reclassify those findings.

## 3. Stage-9C corrective identities

Preregistration:

- path: `prototype/cpi0/stage9c/STAGE9C_STAGE9B_S2_CORRECTIVE_PREREGISTRATION_0_1_0.md`
- expected blob: `e2f16a76a2faa9533852eba6d4e2f529d77b106c`

Implementation:

- path: `prototype/cpi0/stage9c/synthetic_hive_authority_binding.py`
- expected blob: `6b4588f76b4fb9f49b7b4d2e5fa0fe83f93eabc3`

Tests:

- path: `prototype/cpi0/stage9c/test_synthetic_hive_authority_binding.py`
- expected blob: `3b165af469138ab67d40b4651898056a80ea3873`

Workflow:

- path: `.github/workflows/cpi0-stage9c.yml`
- expected blob: `19a5ecaad82125d8a0e0af87289ad3c682900f91`

Qualification runs:

- `37269196169` — expected SUCCESS on `7968c057d7cb449bbae8e5e622ec251b1f880126`
- `37269307817` — expected SUCCESS on corrective report commit `50a3d380589a3cf0f717bf8d06cac6367a985c0e`

CI is execution evidence only, not independent proof.

## 4. Stage-9C self-disposition under audit

`STAGE9C_S2_CORRECTIVE_CLAIM_NARROWING_PASS__INDEPENDENT_REAUDIT_REQUIRED`

The selected repair strategy is claim narrowing, not partial reimplementation of Hive finality.

Do not require Stage 9C to implement native finality merely because Stage 9A attempted to claim it.

The audit question is whether the narrowed profile now truthfully exposes only synthetic structural/binding results.

## 5. Required independent audit work

### A. Reproduce F-02's attacker-authored minimal fixture

Construct the smallest reasonable attacker-authored synthetic history, including a one-block / one-witness case.

Determine whether:

- `synthetic_history_self_consistent` may be true;
- `synthetic_produced_threshold_met` may be true;

while all of the following remain false:

- `real_hive_chain_identity_authenticated`
- `real_hive_history_authenticated`
- `native_hive_consensus_validated`
- `native_hive_target_irreversibility_established`
- `real_hive_authority_snapshot_authenticated`
- `authority_state_provenance_authenticated`
- `current_authority_established`
- `execution_authorized_by_cpi`

Search for any alternative field or nested field that launders the synthetic result back into a native/authenticated claim.

### B. Hostile field-level vocabulary audit

Treat the returned object as though a downstream machine consumer sees only the object and not the prose report.

Enumerate all output fields and nested threshold-observation fields.

Determine whether any positive field can reasonably be interpreted as:

- Hive consensus validation;
- Hive irreversibility/finality;
- authenticated Hive chain state;
- authenticated Hive authority-state provenance;
- current authority;
- CPI execution authority.

Pay special attention to words such as:

- validated;
- authenticated;
- finality;
- irreversible;
- native;
- consensus;
- provenance;
- bound.

A deliberate explicit `false` native/authenticated field is not a defect merely because the word appears.

### C. Reproduce F-01 counterexample classes against the narrowed semantics

Re-check the critical frozen-source facts independently:

- mainnet `HIVE_START_MINER_VOTING_BLOCK = 864000`;
- testnet value = 30;
- below the mainnet start, native logic uses the pre-voting rule;
- modern frozen logic can use a future witness schedule;
- fork-DB witness production can differ from one supplied linear branch.

Then determine whether Stage 9C makes any positive native-finality conclusion in those cases.

The expected repair is NOT that Stage 9C reproduces the reference result.

The expected repair is that Stage 9C labels its threshold result as synthetic only and keeps native Hive irreversibility/finality unestablished.

If Stage 9C still states or implies monotonicity/equivalence to native Hive finality, F-01 remains open.

### D. Complete genesis-input binding

Create two otherwise identical inputs where an authority account outside the Stage-8 closure differs.

Confirm:

- `complete_genesis_authorities_digest` changes;
- `joint_synthetic_binding_digest` changes.

Attempt other reasonable genesis substitutions.

If any supplied genesis authority can change without changing the complete-genesis digest, classify severity.

### E. Confirmation-tip / trailing-history binding

Attempt to supply history beyond the declared confirmation context.

Expected behavior:

fail closed rather than accept a result with unbound trailing history.

### F. Reindex-LIB laundering

Attempt at least:

- object/dict;
- string;
- boolean;
- float;
- negative integer;
- oversized integer.

Expected:

reject all except null or a bounded non-negative integer.

Also confirm an accepted integer is observational only and does not influence synthetic threshold or any native-finality field.

### G. Regression execution

Run independently:

- Stage-9C corrective suite;
- frozen Stage-9A suite;
- Stage-8A suite.

Record exact environment, dependency version and executed head.

A green suite is necessary execution evidence only.

### H. Corrective report audit

Read the Stage-9C corrective report as a hostile downstream consumer.

Determine whether it:

- preserves Stage-9B F-01/F-02 rather than rewriting them;
- makes clear Stage 9A remains historical failed evidence at those claims;
- avoids claiming native Hive finality;
- avoids claiming a real-history executor;
- avoids authorizing Keychain or current authority;
- explicitly requires CPI parking after successful independent closure.

### I. Search for new material defects

Search specifically for new S2/S3 defects introduced by claim narrowing.

Do not promote nonmaterial Stage-9B S1 findings into a material failure unless Stage 9C changed them in a way that creates a new material consequence.

## 6. Severity guidance

Use:

- S3 — critical: false trusted/native authority or execution effect;
- S2 — material: Stage 9C still produces or reasonably enables a false native/authenticated conclusion at its claimed narrowed scope;
- S1 — meaningful hardening/precision/evidence issue that does not defeat the narrowed claim;
- S0 — editorial/ergonomic issue.

## 7. Hard-gate premise status

Report explicitly:

- exact lineage/blob match;
- F-01 claim-narrowing closure status;
- F-02 machine-readable overclaim closure status;
- complete genesis binding status;
- reindex laundering status;
- mutation-boundary status.

## 8. Allowed final dispositions

Choose exactly one:

`PASS__STAGE9B_F01_F02_CLOSED_AT_NARROWED_SYNTHETIC_SCOPE`

`PASS_WITH_NONMATERIAL_FINDINGS`

`REPAIR_REQUIRED`

`ARCHITECTURE_RECONSIDERATION_REQUIRED`

`INSUFFICIENT_AUDIT`

Do not invent a softer disposition to preserve momentum.

## 9. Output artifact

Create exactly:

`prototype/cpi0/stage9d/STAGE9D_INDEPENDENT_STAGE9C_S2_CLOSURE_REAUDIT_REPORT_0_1_0.md`

The report must include:

- audit date;
- exact launch-control commit;
- exact parent/lineage verification;
- exact report blob after commit;
- exact Stage-9C blobs checked;
- test/probe evidence;
- findings with severity;
- hard-gate status;
- chosen allowed disposition;
- explicit statement that real-history execution and Keychain ceremony remain unauthorized.

## 10. Commit discipline

Commit ONLY the Stage-9D independent audit report.

Do not commit scratch probes, caches, dependency directories or generated files.

After committing:

1. push the audit branch;
2. verify the working tree is clean;
3. report audit commit SHA;
4. report parent SHA;
5. report exact report blob SHA;
6. report final disposition;
7. stop.

Do NOT:

- repair Stage 9C;
- merge anything;
- close issues;
- implement a real-history executor;
- invoke Keychain;
- request a real `@etblink` signature;
- broadcast to Hive;
- mutate any observed project;
- integrate Project Observatory;
- create live federation;
- authorize CCP-2.

## 11. Program-level boundary

Issue #53 governs post-audit routing.

A successful Stage-9D closure means only that the bounded CPI repair is independently closed at the narrowed synthetic scope.

It does NOT authorize further CPI advancement.

Project Lead will then park CPI-0 and return program center of gravity to the CCP-1 unfamiliar-human cold-start/usability gate.

## 12. Mutation boundary

```text
REAL_HISTORY_EXECUTOR = NOT AUTHORIZED
REAL_KEYCHAIN_CALL = FORBIDDEN
REAL_ETBLINK_SIGNATURE = FORBIDDEN
HIVE_BROADCAST = FORBIDDEN
NATIVE_ADOPTION = NOT AUTHORIZED
CURRENT_AUTHORITY = NOT ESTABLISHED
PROJECT_OBSERVATORY_INTEGRATION = NOT AUTHORIZED
LIVE_FEDERATION = NOT_AUTHORIZED
EXECUTION_AUTHORIZED_BY_CPI = FALSE
CCP2 = NOT_AUTHORIZED
```

Stop after the single report commit.
