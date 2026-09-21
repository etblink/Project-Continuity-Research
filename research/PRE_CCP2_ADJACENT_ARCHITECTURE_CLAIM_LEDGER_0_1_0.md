# Pre-CCP-2 Adjacent Architecture Claim / Nonclaim Ledger 0.1.0

Date: 2026-09-21
Status: **FORWARD-LOOKING RESEARCH — DOES NOT AUTHORIZE CCP-2 OR LIVE-PROJECT MUTATION**
Governing issue: #7

## Purpose

Maintain a conservative claim/nonclaim comparison between PCR/CCP requirements and adjacent continuity/state-governance work. `D/P/N` labels indicate mechanism-level scope overlap only; they do not mean independently validated / partially validated / falsified.

## R5 scoped-supersession update — 2026-09-20 abstract attack

Issue #8's first abstract same-scenario comparison is now frozen in:

`research/PRE_CCP2_R5_SCOPED_SUPERSESSION_CASCADE_ATTACK_0_1_0.md`

### Result

MemTX-style dependency-aware cascade repair reproduces PCR R5's desired propagation behavior **when independently defeasible subclaims are represented as separately dependency-addressable nodes and provenance is complete**.

A monolithic source record containing both affected and unaffected subclaims causes safe but over-broad repair: descendants of the whole record are invalidated/quarantined even when only one subclaim was corrected. Splitting the source into atomic nodes removes that counterexample.

### Disposition

- R5 empirical requirement: **RETAIN**.
- Bespoke PCR invalidation/cascade mechanism: **NOT ESTABLISHED**.
- Mechanism relation to MemTX: **REPRESENTATIONAL COMPLEMENT / LIKELY SIMPLIFY**.
- Residual prerequisite: sufficiently fine-grained claim identity plus complete dependency provenance.
- Explicit negative-result `REOPEN_IF` semantics remain a separate residual question; they are not supplied merely by cascade repair and should not be counted as R5 mechanism novelty.

Provisional decomposition:

`scoped supersession = dependency-addressable claim granularity + correction/supersession relation + dependency-aware repair`

This update narrows PCR's prospective invention surface rather than expanding it.

## Source-status caution

MemTX (arXiv:2607.23929) is a 2026 preprint. Its reported protocol properties and experiments remain author claims unless independently reproduced. The #8 attack is an abstract mechanism comparison, not a replication.
