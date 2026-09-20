from __future__ import annotations

from pathlib import Path
from typing import Dict, Any
import json

from ccp import (
    ControlPlane,
    SourceRef,
    TransitionRule,
    TransitionRejected,
    WorkerReturn,
    claim_equals,
    source_repository_is,
    environment_target_is_dedicated,
)


def ar01_machine_green_semantic_fail() -> Dict[str, Any]:
    cp = ControlPlane("HiVenues", "Host-first frontend factory for Hive.")
    cp.append_event("PHASE_STATE_SET", "release", {"state": "CANDIDATE"}, actor="lead", authority="PROJECT_LEAD")
    cp.append_event("CLAIM_SET", "ci_pass", {"value": True}, actor="ci", authority="CI")
    cp.append_event("CLAIM_SET", "release_name_semantic_pass", {"value": False}, actor="review", authority="PROJECT_LEAD")
    cp.register_transition(TransitionRule(
        "TAG_RELEASE",
        "CANDIDATE",
        "RELEASED",
        [claim_equals("ci_pass", True), claim_equals("release_name_semantic_pass", True)],
    ))
    blocked = False
    try:
        cp.request_transition("TAG_RELEASE", subject="release", actor="lead", authority="PROJECT_LEAD")
    except TransitionRejected:
        blocked = True
    return {"blocked": blocked, "state": cp.phase_state["release"]}


def ar02_wrong_repository_identity() -> Dict[str, Any]:
    cp = ControlPlane("FCP", "Truth-seeking framework comparison.")
    cp.register_source(SourceRef(
        "sentinel",
        repository="etblink/Nested-Fibrational-Cosmology",
        revision="b8587ce3409e34c0dd4e56c61ee585c07798b0e5",
        authority_class="HISTORICAL_SOURCE",
    ))
    cp.append_event("PHASE_STATE_SET", "recurrence", {"state": "READY"}, actor="lead", authority="PROJECT_LEAD")
    cp.register_transition(TransitionRule(
        "START_RECURRENCE",
        "READY",
        "RUNNING",
        [source_repository_is("sentinel", "etblink/Foundational-Convergence-Program")],
    ))
    blocked = False
    try:
        cp.request_transition("START_RECURRENCE", subject="recurrence", actor="lead", authority="PROJECT_LEAD")
    except TransitionRejected:
        blocked = True
    return {"blocked": blocked, "state": cp.phase_state["recurrence"]}


def ar03_partial_supersession() -> Dict[str, Any]:
    cp = ControlPlane("FCP", "Truth-seeking framework comparison.")
    cp.append_event(
        "CLAIM_SET",
        "FCP6",
        {"value": {"K1": "E5", "K2": "E5", "K3": "E5", "K4": "NONE"}},
        actor="lead",
        authority="CANONICAL_FCP",
    )
    cp.append_event(
        "CLAIM_SET",
        "FCP22",
        {"value": {"K2": "NONE"}},
        actor="lead",
        authority="CANONICAL_FCP",
    )
    cp.append_event(
        "CLAIM_SUPERSEDED",
        "FCP6::FCP22",
        {
            "prior": "FCP6",
            "superseding": "FCP22",
            "scope": ["K2"],
            "unaffected": ["K1", "K3", "K4"],
            "reason": "partial current-subclaim supersession",
        },
        actor="lead",
        authority="CANONICAL_FCP",
    )
    return {"current": cp.current_subclaims("FCP6")}


def ar04_functional_accepted_visual_hold() -> Dict[str, Any]:
    cp = ControlPlane("HiVenues", "Host-first frontend factory for Hive.")
    cp.append_event("PHASE_STATE_SET", "astra", {"state": "FUNCTIONAL_ACCEPTED"}, actor="lead", authority="PROJECT_LEAD")
    cp.append_event("CLAIM_SET", "visual_gate", {"value": "FAIL"}, actor="lead", authority="PROJECT_LEAD")
    cp.register_transition(TransitionRule(
        "START_ASTRA_REGRESSION",
        "FUNCTIONAL_ACCEPTED",
        "ASTRA_AUTHORIZED",
        [claim_equals("visual_gate", "PASS")],
    ))
    blocked = False
    try:
        cp.request_transition("START_ASTRA_REGRESSION", subject="astra", actor="lead", authority="PROJECT_LEAD")
    except TransitionRejected:
        blocked = True
    return {"blocked": blocked, "state": cp.phase_state["astra"]}


def ar05_evidence_triggered_hold() -> Dict[str, Any]:
    cp = ControlPlane("FCP", "Truth-seeking framework comparison.")
    cp.append_event(
        "ROUTE_HELD",
        "FCP27",
        {
            "basis": "no qualifying evidence trigger",
            "authority": "POST_RECURRENCE_ADJUDICATION",
            "scope": "program",
            "reopen_requires": ["MATERIAL_EVIDENCE_EVENT", "FRESH_PREREGISTRATION"],
        },
        actor="lead",
        authority="POST_RECURRENCE_ADJUDICATION",
    )
    first_blocked = False
    try:
        cp.reopen_route(
            "FCP27",
            ["MATERIAL_EVIDENCE_EVENT"],
            actor="lead",
            authority="POST_RECURRENCE_ADJUDICATION",
        )
    except TransitionRejected:
        first_blocked = True
    cp.reopen_route(
        "FCP27",
        ["MATERIAL_EVIDENCE_EVENT", "FRESH_PREREGISTRATION"],
        actor="lead",
        authority="POST_RECURRENCE_ADJUDICATION",
    )
    return {"blocked_without_full_predicate": first_blocked, "state": cp.routes["FCP27"].state}


def ar06_worker_but_evidence_meets_c() -> Dict[str, Any]:
    cp = ControlPlane("Observatory/NFC", "Truth-seeking adversarial audit.")
    cp.register_source(SourceRef("audit", repository="etblink/Project-Observatory", revision="audit-1"))
    cp.configure_outcomes(
        ["A", "B", "C"],
        {
            "A": {"SOURCE_SELECTOR_FOUND"},
            "B": {"BRANCH_SPECIFIC_SELECTOR"},
            "C": {"CONSERVATIVE_EXTENSION_NONFORCING"},
        },
    )
    ret = WorkerReturn(
        return_id="ret-1",
        operation="source_forcing",
        worker="executor",
        proposed_events=[],
        evidence_refs=["audit"],
        reported_outcome="B",
        observations={"test4": "conservative extension"},
    )
    cp.submit_worker_return(ret)
    before = cp.claims.get("source_forcing.outcome")
    cp.adjudicate_worker_return(
        "ret-1",
        actor="adjudicator",
        authority="INDEPENDENT_ADJUDICATION",
        observed_features=["BRANCH_SPECIFIC_SELECTOR", "CONSERVATIVE_EXTENSION_NONFORCING"],
    )
    after = cp.claims["source_forcing.outcome"]["value"]
    return {"before_adjudication": before, "worker_reported": "B", "canonical_after": after}


def ar07_reconstruction_paralysis() -> Dict[str, Any]:
    cp = ControlPlane("HiVenues", "Host-first frontend factory for Hive.")
    cp.append_event(
        "SAFEGUARD_OPENED",
        "successor_bootstrap",
        {
            "required_exit_facts": [
                "EXACT_COMMIT_VERIFIED",
                "AUTHORITY_MAP_LOADED",
                "CURRENT_OPERATION_IDENTIFIED",
            ]
        },
        actor="successor",
        authority="SUCCESSION_PROTOCOL",
    )
    facts = ["EXACT_COMMIT_VERIFIED", "AUTHORITY_MAP_LOADED", "CURRENT_OPERATION_IDENTIFIED"]
    ready, missing = cp.safeguard_exit_ready("successor_bootstrap", facts)
    cp.exit_safeguard("successor_bootstrap", facts, actor="successor", authority="SUCCESSION_PROTOCOL")
    return {
        "exit_ready": ready,
        "missing": sorted(missing),
        "state": cp.safeguards["successor_bootstrap"]["state"],
    }


def ar08_occupied_target() -> Dict[str, Any]:
    cp = ControlPlane("HiVenues", "Host-first frontend factory for Hive.")
    cp.append_event("PHASE_STATE_SET", "deploy", {"state": "PRECHECK"}, actor="lead", authority="PROJECT_LEAD")
    cp.append_event(
        "ENVIRONMENT_SET",
        "server",
        {"public_tcp_ports": [22, 80, 443], "system_caddy_active": True},
        actor="inspector",
        authority="ENVIRONMENT_OBSERVATION",
    )
    cp.register_transition(TransitionRule(
        "BOOTSTRAP_TARGET",
        "PRECHECK",
        "MUTATION_AUTHORIZED",
        [environment_target_is_dedicated],
    ))
    blocked = False
    try:
        cp.request_transition(
            "BOOTSTRAP_TARGET",
            subject="deploy",
            actor="lead",
            authority="PROJECT_LEAD",
            context={"allowed_public_tcp_ports": [22]},
        )
    except TransitionRejected:
        blocked = True
    return {"blocked": blocked, "state": cp.phase_state["deploy"]}


def ar09_historical_provenance_recovery() -> Dict[str, Any]:
    cp = ControlPlane("Project Observatory", "Read-only cross-project reconstruction.")
    cp.register_source(SourceRef(
        "historic-audit",
        repository="etblink/Project-Observatory",
        revision="cde62683",
        historical=True,
        authority_class="HISTORICAL_EXECUTION_PROVENANCE",
    ))
    before = cp.event_seq
    # Recovery makes a historical object discoverable but does not synthesize a new execution event.
    cp.append_event(
        "CLAIM_SET",
        "historic-audit.discoverability",
        {"value": "RECOVERED_CURRENT_LINEAGE"},
        actor="observatory",
        authority="PROVENANCE_RECOVERY",
        evidence_refs=["historic-audit"],
    )
    return {
        "new_execution_event_created": any(e.event_type == "AUDIT_EXECUTED" for e in cp.events[before:]),
        "source_historical": cp.sources["historic-audit"].historical,
    }


def ar10_separate_selection_prereg_execution() -> Dict[str, Any]:
    cp = ControlPlane("Project Observatory", "Truth-seeking adversarial audit selection.")
    cp.append_event("PHASE_STATE_SET", "audit", {"state": "UNSELECTED"}, actor="lead", authority="OBSERVATORY")
    cp.register_transition(TransitionRule("SELECT_TARGET", "UNSELECTED", "SELECTED", []))
    cp.register_transition(TransitionRule("PREREGISTER", "SELECTED", "PREREGISTERED", []))
    cp.register_transition(TransitionRule("EXECUTE", "PREREGISTERED", "EXECUTED", []))

    skip_blocked = False
    try:
        cp.request_transition("EXECUTE", subject="audit", actor="lead", authority="OBSERVATORY")
    except TransitionRejected:
        skip_blocked = True

    cp.request_transition("SELECT_TARGET", subject="audit", actor="lead", authority="OBSERVATORY")
    cp.request_transition("PREREGISTER", subject="audit", actor="lead", authority="OBSERVATORY")
    cp.request_transition("EXECUTE", subject="audit", actor="lead", authority="OBSERVATORY")
    return {"skip_blocked": skip_blocked, "final_state": cp.phase_state["audit"]}


def kernel_staleness_and_regeneration() -> Dict[str, Any]:
    cp = ControlPlane("Demo", "Demonstrate kernel freshness.")
    cp.append_event("PHASE_STATE_SET", "phase", {"state": "ONE"}, actor="lead", authority="LEAD")
    k1 = cp.generate_kernel()
    initially_fresh = cp.kernel_is_fresh(k1)
    cp.append_event("PHASE_STATE_SET", "phase", {"state": "TWO"}, actor="lead", authority="LEAD")
    stale_after_event = not cp.kernel_is_fresh(k1)
    k2 = cp.generate_kernel()
    regenerated_fresh = cp.kernel_is_fresh(k2)
    return {
        "initially_fresh": initially_fresh,
        "stale_after_event": stale_after_event,
        "regenerated_fresh": regenerated_fresh,
        "old_seq": k1.projection_event_seq,
        "new_seq": k2.projection_event_seq,
        "kernel": k2.markdown,
    }


SCENARIOS = {
    "AR-01": ar01_machine_green_semantic_fail,
    "AR-02": ar02_wrong_repository_identity,
    "AR-03": ar03_partial_supersession,
    "AR-04": ar04_functional_accepted_visual_hold,
    "AR-05": ar05_evidence_triggered_hold,
    "AR-06": ar06_worker_but_evidence_meets_c,
    "AR-07": ar07_reconstruction_paralysis,
    "AR-08": ar08_occupied_target,
    "AR-09": ar09_historical_provenance_recovery,
    "AR-10": ar10_separate_selection_prereg_execution,
}


def run_all() -> Dict[str, Any]:
    return {name: fn() for name, fn in SCENARIOS.items()}


if __name__ == "__main__":
    out = run_all()
    out["KERNEL"] = kernel_staleness_and_regeneration()
    print(json.dumps(out, indent=2, sort_keys=True))
