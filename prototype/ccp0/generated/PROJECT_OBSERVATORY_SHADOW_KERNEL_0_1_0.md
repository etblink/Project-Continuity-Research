# Project Kernel — Project Observatory — shadow CCP trial

## Purpose
Read-only cross-project reconstruction of canonical state, dependencies, uncertainty, external decision triggers, and bounded adversarial findings without silently changing observed projects.

## Freshness identity
- projection_event_seq: `18`
- projection_graph_revision: `0`
- projection_digest: `eba71d475ca583f003d1ea27c7e3b6da51cbe0e27799e0dc461a2f6382e6c316`
- policy_version: `ccp0-shadow-0.1.0`
- intent_version: `1`

## Current phase/state
- `observatory_snapshot` = `FROZEN_V0_2`

## Current material claims
- `FCP.project_state` = `WAITING_FOR_EVIDENCE` (FROZEN_RECONSTRUCTION_V0_2, authority=PROJECT_OBSERVATORY_SNAPSHOT_V0_2)
- `HiVenues.project_state` = `ACTIVE` (FROZEN_RECONSTRUCTION_V0_2, authority=PROJECT_OBSERVATORY_SNAPSHOT_V0_2)
- `NFC.project_state` = `READY_FOR_NEXT_OPERATION` (FROZEN_RECONSTRUCTION_V0_2, authority=PROJECT_OBSERVATORY_SNAPSHOT_V0_2)
- `PGH.project_state` = `BLOCKED_EXTERNAL` (FROZEN_RECONSTRUCTION_V0_2, authority=PROJECT_OBSERVATORY_SNAPSHOT_V0_2)

## Held / closed routes
- `NFC.new_adversarial_audit`: **HELD** — Snapshot v0.2 selects no new NFC target. — reopen if: FRESH_PREREGISTRATION, TARGET_SELECTION
- `FCP.next_scientific_operation`: **HELD** — FCP remains on evidence-triggered hold. — reopen if: FRESH_PREREGISTRATION, MATERIAL_NEW_EVIDENCE
- `PGH.physical_trial`: **HELD** — No real conforming D1 apparatus/target/data exist at the frozen boundary. — reopen if: ANALYSIS_PREREGISTRATION, PROSPECTIVE_BINDING, REAL_D1_APPARATUS, TARGET_FREEZE
- `HiVenues.external_effects`: **HELD** — Live-host migration and Hive/provider/payment/signing/deployment/DNS/VPS effects are outside the frozen active phase authority. — reopen if: EXPLICIT_EXTERNAL_EFFECT_AUTHORIZATION, SEPARATELY_QUALIFIED_OPERATION

## Open safeguards
- None.

## External observation freshness
- `FCP_MAIN`: **MATCHES_BOUNDARY** — bound `a41bc6101b63140ee2687e0cf67a47ab6be77215`; observed `a41bc6101b63140ee2687e0cf67a47ab6be77215`
- `HIVENUES_MAIN`: **SOURCE_MOVED_SINCE_BOUNDARY** — bound `bf9a0b4e61d57eed6bb5a81504d6e030f8b6ff7c`; observed `21075c541189fbe236e8b113568933406ecc759f`
- `NFC_CANON_ARCHIVE`: **UNVERIFIED_SINCE_BOUNDARY** — bound `ed3047c2cbc0abc34d2549dd27754e4d3d05af78`; observed `None`
- `NFC_PUBLICATION_MAIN`: **MATCHES_BOUNDARY** — bound `5072d563b0a3dd4a7643be427cd47108216d8793`; observed `5072d563b0a3dd4a7643be427cd47108216d8793`
- `PGH_MAIN`: **MATCHES_BOUNDARY** — bound `2923875b40ea6901dfafda56a771c36876c4a220`; observed `2923875b40ea6901dfafda56a771c36876c4a220`

- all_external_sources_match_boundary: `False`

## Orientation rule
This kernel is a projection. If its freshness identity does not match the control plane, regenerate it before relying on it.
