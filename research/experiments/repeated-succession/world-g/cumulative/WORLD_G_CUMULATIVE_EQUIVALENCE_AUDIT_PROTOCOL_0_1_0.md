# World G Cumulative — Blind Compiled-Handoff Equivalence Audit Protocol 0.1.0

Date: 2026-09-21
Status: FROZEN

## Auditor identity

OpenAI GPT-5.6 Sol High, High reasoning, one genuinely fresh context per audit.

## Inputs

The auditor receives only:
1. raw outgoing successor handoff;
2. compiled candidate handoff;
3. canonical records available through that generation;
4. this audit task.

No condition label, chain outcome, scoring, hypothesis, or matched-chain output is supplied.

## Audit task

Determine whether the compiled handoff preserves the same operative project state while changing only explicitness/relational presentation.

Reject if the compiled version:
- changes a decision-critical fact;
- adds/removes authority;
- converts permission to prohibition or vice versa;
- changes scope or exception membership;
- changes current/historical/prospective status;
- changes a reopen/admission predicate;
- changes an unfinished obligation or negative constraint;
- makes an unavailable fact appear known;
- deletes a proposition necessary to recover the same bounded continuation.

Also judge whether the candidate meaningfully changes relational explicitness rather than merely paraphrasing.

## Allowed per-handoff disposition

- `EQUIVALENT_PRESSURE_PASS`
- `EQUIVALENT_BUT_WEAK_PRESSURE`
- `FAIL_FACT_OR_STATE_CHANGE`
- `FAIL_DECISION_CRITICAL_DELETION`
- `FAIL_SCOPE_OR_AUTHORITY_DISTORTION`

`EQUIVALENT_PRESSURE_PASS` is required before use.

If the audit fails, freeze the raw failure. A fresh compiler may make the smallest repair necessary, after which a fresh auditor must re-audit. Do not strengthen pressure beyond the frozen compiler instruction.