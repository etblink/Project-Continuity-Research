from __future__ import annotations

from pathlib import Path
import json

from ccp import ControlPlane


BOUNDARY = "2026-09-14T21:04:00Z"
SHADOW_OBSERVED_DATE = "2026-09-20"

# Read-only identities established from the current public repositories during
# the shadow trial. This file does not mutate Project Observatory or any
# observed project.
LIVE_OBSERVATIONS = {
    "NFC_PUBLICATION_MAIN": "5072d563b0a3dd4a7643be427cd47108216d8793",
    "FCP_MAIN": "a41bc6101b63140ee2687e0cf67a47ab6be77215",
    "PGH_MAIN": "2923875b40ea6901dfafda56a771c36876c4a220",
    "HIVENUES_MAIN": "21075c541189fbe236e8b113568933406ecc759f",
}


def build_shadow() -> ControlPlane:
    cp = ControlPlane(
        "Project Observatory — shadow CCP trial",
        (
            "Read-only cross-project reconstruction of canonical state, dependencies, "
            "uncertainty, external decision triggers, and bounded adversarial findings "
            "without silently changing observed projects."
        ),
        policy_version="ccp0-shadow-0.1.0",
    )

    cp.append_event(
        "PHASE_STATE_SET",
        "observatory_snapshot",
        {"state": "FROZEN_V0_2"},
        actor="shadow-import",
        authority="PROJECT_OBSERVATORY_SNAPSHOT_V0_2",
    )

    # Current reconstructed project-state claims at the frozen v0.2 boundary.
    for subject, value in {
        "NFC.project_state": "READY_FOR_NEXT_OPERATION",
        "FCP.project_state": "WAITING_FOR_EVIDENCE",
        "PGH.project_state": "BLOCKED_EXTERNAL",
        "HiVenues.project_state": "ACTIVE",
    }.items():
        cp.append_event(
            "CLAIM_SET",
            subject,
            {"value": value, "status": "FROZEN_RECONSTRUCTION_V0_2"},
            actor="shadow-import",
            authority="PROJECT_OBSERVATORY_SNAPSHOT_V0_2",
        )

    # Negative knowledge / hold semantics derived from the frozen routing.
    cp.append_event(
        "ROUTE_HELD",
        "NFC.new_adversarial_audit",
        {
            "basis": "Snapshot v0.2 selects no new NFC target.",
            "authority": "PROJECT_OBSERVATORY_SNAPSHOT_V0_2",
            "scope": "NFC post-snapshot routing",
            "reopen_requires": ["TARGET_SELECTION", "FRESH_PREREGISTRATION"],
        },
        actor="shadow-import",
        authority="PROJECT_OBSERVATORY_SNAPSHOT_V0_2",
    )
    cp.append_event(
        "ROUTE_HELD",
        "FCP.next_scientific_operation",
        {
            "basis": "FCP remains on evidence-triggered hold.",
            "authority": "PROJECT_OBSERVATORY_SNAPSHOT_V0_2",
            "scope": "FCP scientific routing",
            "reopen_requires": ["MATERIAL_NEW_EVIDENCE", "FRESH_PREREGISTRATION"],
        },
        actor="shadow-import",
        authority="PROJECT_OBSERVATORY_SNAPSHOT_V0_2",
    )
    cp.append_event(
        "ROUTE_HELD",
        "PGH.physical_trial",
        {
            "basis": "No real conforming D1 apparatus/target/data exist at the frozen boundary.",
            "authority": "PROJECT_OBSERVATORY_SNAPSHOT_V0_2",
            "scope": "PGH empirical routing",
            "reopen_requires": [
                "REAL_D1_APPARATUS",
                "PROSPECTIVE_BINDING",
                "TARGET_FREEZE",
                "ANALYSIS_PREREGISTRATION",
            ],
        },
        actor="shadow-import",
        authority="PROJECT_OBSERVATORY_SNAPSHOT_V0_2",
    )
    cp.append_event(
        "ROUTE_HELD",
        "HiVenues.external_effects",
        {
            "basis": "Live-host migration and Hive/provider/payment/signing/deployment/DNS/VPS effects are outside the frozen active phase authority.",
            "authority": "PROJECT_OBSERVATORY_SNAPSHOT_V0_2",
            "scope": "HiVenues external effects",
            "reopen_requires": [
                "SEPARATELY_QUALIFIED_OPERATION",
                "EXPLICIT_EXTERNAL_EFFECT_AUTHORIZATION",
            ],
        },
        actor="shadow-import",
        authority="PROJECT_OBSERVATORY_SNAPSHOT_V0_2",
    )

    # External source bindings from Snapshot v0.2 / Project Register.
    cp.bind_external_source(
        "NFC_CANON_ARCHIVE",
        repository="etblink/Nested-Fibrational-Cosmology",
        ref="archive/nfc-canonical-ed3047c2",
        bound_revision="ed3047c2cbc0abc34d2549dd27754e4d3d05af78",
        observed_at_boundary=BOUNDARY,
        actor="shadow-import",
        authority="PROJECT_OBSERVATORY_SNAPSHOT_V0_2",
    )
    cp.bind_external_source(
        "NFC_PUBLICATION_MAIN",
        repository="etblink/Nested-Fibrational-Cosmology",
        ref="main",
        bound_revision="5072d563b0a3dd4a7643be427cd47108216d8793",
        observed_at_boundary=BOUNDARY,
        actor="shadow-import",
        authority="PROJECT_OBSERVATORY_SNAPSHOT_V0_2",
    )
    cp.bind_external_source(
        "FCP_MAIN",
        repository="etblink/Foundational-Convergence-Program",
        ref="main",
        bound_revision="a41bc6101b63140ee2687e0cf67a47ab6be77215",
        observed_at_boundary=BOUNDARY,
        actor="shadow-import",
        authority="PROJECT_OBSERVATORY_SNAPSHOT_V0_2",
    )
    cp.bind_external_source(
        "PGH_MAIN",
        repository="etblink/Physical-Grammar-Hypothesis",
        ref="main",
        bound_revision="2923875b40ea6901dfafda56a771c36876c4a220",
        observed_at_boundary=BOUNDARY,
        actor="shadow-import",
        authority="PROJECT_OBSERVATORY_SNAPSHOT_V0_2",
    )
    cp.bind_external_source(
        "HIVENUES_MAIN",
        repository="etblink/HiVenues",
        ref="main",
        bound_revision="bf9a0b4e61d57eed6bb5a81504d6e030f8b6ff7c",
        observed_at_boundary=BOUNDARY,
        actor="shadow-import",
        authority="PROJECT_OBSERVATORY_SNAPSHOT_V0_2",
    )

    # Read-only current observations. NFC archive ref was not independently
    # re-resolved in this bounded shadow pass, so it remains UNVERIFIED_SINCE_BOUNDARY.
    for source_id, revision in LIVE_OBSERVATIONS.items():
        cp.observe_external_source(
            source_id,
            observed_revision=revision,
            observed_at=SHADOW_OBSERVED_DATE,
            actor="read-only-github-observer",
        )

    return cp


if __name__ == "__main__":
    cp = build_shadow()
    outdir = Path(__file__).resolve().parent / "generated"
    outdir.mkdir(exist_ok=True)

    kernel = cp.generate_kernel()
    (outdir / "PROJECT_OBSERVATORY_SHADOW_KERNEL_0_1_0.md").write_text(
        kernel.markdown,
        encoding="utf-8",
    )
    (outdir / "PROJECT_OBSERVATORY_SHADOW_STATE_0_1_0.json").write_text(
        json.dumps(cp.state_projection(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "event_seq": cp.event_seq,
        "projection_digest": cp.projection_digest(),
        "projection_consistent": cp.projection_consistent_with_ledger(),
        "external_status": cp.external_source_statuses(),
        "all_external_sources_match_boundary": cp.all_external_sources_match_boundary(),
    }, indent=2, sort_keys=True))
