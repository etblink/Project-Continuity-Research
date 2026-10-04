from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from typing import Any, Dict, Mapping


ADAPTER_VERSION = "cpi0-stage6a-source-contract-0.1.0"


class AdapterIncomplete(RuntimeError):
    pass


class AdapterInconsistent(RuntimeError):
    pass


def _stable_source_hash(src: Mapping[str, Any]) -> str:
    core = {k: v for k, v in src.items() if k != "packet_sha256"}
    raw = json.dumps(core, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def _verify_source(src: Mapping[str, Any], label: str) -> None:
    if "packet_sha256" not in src:
        raise AdapterIncomplete(f"{label}: missing packet fingerprint")
    if _stable_source_hash(src) != src["packet_sha256"]:
        raise AdapterInconsistent(f"{label}: packet fingerprint mismatch")
    if "text" in src and "content_sha256" in src:
        actual = hashlib.sha256(src["text"].encode()).hexdigest()
        if actual != src["content_sha256"]:
            raise AdapterInconsistent(f"{label}: content fingerprint mismatch")


def _require_source(packet: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    sources = packet.get("sources", {})
    if key not in sources:
        raise AdapterIncomplete(f"missing required source: {key}")
    src = sources[key]
    _verify_source(src, key)
    return src


def _must(text: str, marker: str, label: str) -> None:
    if marker not in text:
        raise AdapterIncomplete(f"{label}: missing required semantic marker: {marker}")


def adapt_nfc(packet: Mapping[str, Any]) -> Dict[str, Any]:
    src = _require_source(packet, "provenance")
    text = src["text"]
    for marker in [
        "REF = archive/nfc-canonical-ed3047c2",
        "COMMIT = ed3047c2cbc0abc34d2549dd27754e4d3d05af78",
        "HUMAN_POLICY_INTENT = UNRESOLVED",
        "Do not use default-branch presence as a proxy for scientific authority.",
    ]:
        _must(text, marker, "NFC provenance")
    canon_ref = re.search(r"^REF = (.+)$", text, re.M).group(1)
    canon_commit = re.search(r"^COMMIT = ([0-9a-f]{40})$", text, re.M).group(1)
    canon_tree = re.search(r"^TREE = ([0-9a-f]{40})$", text, re.M).group(1)
    projection = {
        "profile_version": "0.1.0",
        "adapter_version": ADAPTER_VERSION,
        "project_id": "NFC",
        "projection_id": f"NFC:{packet['current_main'][:12]}",
        "observed_sources": [
            {"source_id": "publication-main", "repository": src["repository"], "ref": "main", "commit": packet["current_main"], "role": "publication_provenance_surface"},
            {"source_id": "frozen-theorem-canon", "repository": src["repository"], "ref": canon_ref, "commit": canon_commit, "tree": canon_tree, "role": "scientific_theorem_canon"},
        ],
        "authority_map": [
            {"purpose": "publication_routing", "source_id": "publication-main", "authority_scope": "publication_and_provenance"},
            {"purpose": "scientific_theorem_analysis", "source_id": "frozen-theorem-canon", "authority_scope": "frozen_theorem_bearing_corpus"},
        ],
        "material_objects": [],
        "negative_knowledge": [
            {"kind": "unresolved", "subject": "historical_remove_human_policy_intent", "basis": "HUMAN_POLICY_INTENT = UNRESOLVED"}
        ],
        "dependencies": [], "triggers": [], "transitions": [],
        "completeness": "COMPLETE",
    }
    return projection


def adapt_fcp(packet: Mapping[str, Any]) -> Dict[str, Any]:
    current = _require_source(packet, "current_state")
    charter = _require_source(packet, "charter")
    c = current["text"]
    g = charter["text"]
    for marker in [
        "HISTORICAL_RESULT", "CURRENT_PROSPECTIVE_RESULT", "CURRENT_ROUTING_STATE",
        "METHOD = 0.2.1_ACTIVE_PROSPECTIVELY", "FCP27_SELECTED = NO",
        "NEXT_RECOMMENDED_OPERATION = POST_RECURRENCE_SCIENTIFIC_SEQUENCING_ADJUDICATION",
        "NEXT_SCIENTIFIC_PHASE = NONE__POST_RECURRENCE_SCIENTIFIC_SEQUENCING_ADJUDICATION_PENDING_SEPARATE_READ_ONLY_AUTHORIZATION",
    ]:
        _must(c, marker, "FCP current state")
    _must(g, "Every substantive future phase requires separate bounded authorization and an explicit source/provenance window", "FCP charter")
    method = re.search(r"METHOD = (.+)", c).group(1).strip()
    next_op = re.search(r"NEXT_RECOMMENDED_OPERATION = (.+)", c).group(1).strip()
    next_phase = re.search(r"NEXT_SCIENTIFIC_PHASE = (.+)", c).group(1).strip()
    projection = {
        "profile_version": "0.1.0", "adapter_version": ADAPTER_VERSION,
        "project_id": "FCP", "projection_id": f"FCP:{packet['current_main'][:12]}",
        "observed_sources": [
            {"source_id":"current-state","repository":current["repository"],"ref":"main","commit":packet["current_main"],"role":"current_scientific_and_routing_state"},
            {"source_id":"charter","repository":charter["repository"],"ref":"main","commit":packet["current_main"],"role":"governance_authority"},
        ],
        "authority_map": [
            {"purpose":"current_routing","source_id":"current-state","authority_scope":"CURRENT_STATE"},
            {"purpose":"future_phase_authorization_rule","source_id":"charter","authority_scope":"governance_rule"},
        ],
        "material_objects": [
            {"object_id":"historical","role":"historical_result","status":"distinct"},
            {"object_id":"prospective","role":"current_prospective_result","status":method},
            {"object_id":"routing","role":"current_routing_state","status":next_op},
            {"object_id":"fcp27","role":"phase_selection","status":"not_selected"},
        ],
        "negative_knowledge": [
            {"kind":"historical_marker","subject":"prior_evidence_triggered_hold","basis":"PRIOR_SEQUENCING_SELECTION = EVIDENCE_TRIGGERED_HOLD"},
            {"kind":"authorization_boundary","subject":"future_substantive_phase","basis":"separate bounded authorization and explicit source/provenance window required"},
        ],
        "dependencies": [], "triggers": [],
        "transitions": [
            {"transition_id":next_op,"state":"selected_not_authorized","consequence_class":"read_only_scientific_sequencing","next_scientific_phase":next_phase}
        ],
        "completeness":"COMPLETE",
    }
    return projection


def _parse_pgh_capsule(text: str) -> Mapping[str, Any]:
    start = "<!-- PGH_CURRENT_STATE_CAPSULE_BEGIN -->"
    end = "<!-- PGH_CURRENT_STATE_CAPSULE_END -->"
    if start not in text or end not in text:
        raise AdapterIncomplete("PGH: missing current-state capsule")
    segment = text.split(start,1)[1].split(end,1)[0]
    match = re.search(r"```json\s*(\{.*\})\s*```", segment, re.S)
    if not match:
        raise AdapterIncomplete("PGH: malformed current-state capsule")
    return json.loads(match.group(1))


def adapt_pgh(packet: Mapping[str, Any]) -> Dict[str, Any]:
    src = _require_source(packet, "current_state")
    text = src["text"]
    for marker in [
        "NEXT_SCIENTIFIC_OPERATION = APPARATUS_REALIZATION_AND_TARGET_FREEZE",
        "NEXT_SCIENTIFIC_OPERATION_REQUIRES_EXTERNAL_PHYSICAL_ACTION = YES",
        "PHYSICAL_TRIAL_EXECUTION_AUTHORIZED = NO",
        "WEB_TARGET_SEARCH = FORBIDDEN_WITHOUT_NEW_INDEPENDENT_TRIGGER",
        "REGISTRY_TARGET_SEARCH = FORBIDDEN_WITHOUT_NEW_INDEPENDENT_TRIGGER",
    ]:
        _must(text, marker, "PGH current state")
    capsule = _parse_pgh_capsule(text)
    if capsule.get("actual_apparatus") is not None:
        raise AdapterInconsistent("PGH: capsule contradicts NONE_BOUND apparatus state")
    if capsule.get("physical_trials_authorized") is not False:
        raise AdapterInconsistent("PGH: trials unexpectedly authorized")
    projection = {
        "profile_version":"0.1.0","adapter_version":ADAPTER_VERSION,
        "project_id":"PGH","projection_id":f"PGH:{packet['current_main'][:12]}",
        "observed_sources":[{"source_id":"current-state","repository":src["repository"],"ref":"main","commit":packet["current_main"],"role":"current_research_and_governance_state"}],
        "authority_map":[{"purpose":"current_research_and_governance_state","source_id":"current-state","authority_scope":"canonical_markdown_plus_git_provenance"}],
        "material_objects":[{"object_id":capsule["active_candidate_package"],"role":"active_candidate_package","status":"empirically_untested"}],
        "negative_knowledge":[
            {"kind":"forbidden_assumptions","subject":capsule["active_candidate_package"],"basis":"current-state do_not_assume capsule","items":capsule["do_not_assume"]},
            {"kind":"suspended","subject":"target_search","basis":"new independent trigger required","reopen_if":"new_independent_trigger"},
        ],
        "dependencies":[{"dependency_id":"real-apparatus","class":"HARD","status":"UNSATISFIED","basis":"actual apparatus is unbound","counterfactual":"synthetic readiness cannot replace physical apparatus"}],
        "triggers":[{"trigger_id":"apparatus-realization","trigger_type":"physical_prerequisite","status":"unsatisfied","consequence":capsule["next_scientific_operation"]}],
        "transitions":[
            {"transition_id":capsule["next_scientific_operation"],"state":"blocked_external","consequence_class":"physical_experiment_preparation"},
            {"transition_id":"PHYSICAL_TRIAL_EXECUTION","state":"prohibited","consequence_class":"physical_experiment"},
        ],
        "completeness":"COMPLETE",
    }
    return projection


def adapt_hivenues(packet: Mapping[str, Any]) -> Dict[str, Any]:
    readme = _require_source(packet, "readme")
    issue = _require_source(packet, "issue_398")
    pr = _require_source(packet, "pr_397")
    _must(readme["text"], "Doctrine defines the destination, the roadmap defines the journey, active issue charters define bounded work, and current product tests protect accepted contracts.", "HiVenues README")
    _must(issue["text"], "owner acceptance governs #374", "HiVenues issue 398")
    if issue.get("state") != "open":
        raise AdapterInconsistent("HiVenues: Issue #398 is not open")
    if pr.get("base_sha") != packet["current_main"]:
        raise AdapterInconsistent("HiVenues: PR #397 base does not match supplied current main")
    if pr.get("merged") is True and pr.get("head_sha") != packet["current_main"]:
        raise AdapterInconsistent("HiVenues: PR marked merged but supplied canonical main does not contain head identity")
    projection = {
        "profile_version":"0.1.0","adapter_version":ADAPTER_VERSION,
        "project_id":"HIVenues","projection_id":f"HIVenues:{packet['current_main'][:12]}:issue398",
        "observed_sources":[
            {"source_id":"main","repository":readme["repository"],"ref":"main","commit":packet["current_main"],"role":"canonical_merged_code"},
            {"source_id":"pr397","repository":pr["repository"],"ref":"PR-397","commit":pr["head_sha"],"role":"candidate_pr_head"},
            {"source_id":"issue398","repository":issue["repository"],"ref":"issue-398","commit":packet["current_main"],"role":"active_bounded_work_charter"},
        ],
        "authority_map":[
            {"purpose":"canonical_merged_code","source_id":"main","authority_scope":"merged_main"},
            {"purpose":"stage5c_candidate_review","source_id":"pr397","authority_scope":"candidate_only"},
            {"purpose":"stage5d_usability_acceptance","source_id":"issue398","authority_scope":"owner_acceptance"},
        ],
        "material_objects":[
            {"object_id":"PR-397","role":"candidate","status":"open_not_merged" if not pr["merged"] else "merged"},
            {"object_id":"ISSUE-398","role":"active_work_charter","status":"owner_acceptance_required"},
            {"object_id":"authority-model","role":"project_governance","status":"doctrine_roadmap_issue_test_roles_distinct"},
        ],
        "negative_knowledge":[
            {"kind":"forbidden","subject":"machine_pass_as_owner_acceptance","basis":"owner acceptance governs usability gate","reopen_if":None},
            {"kind":"forbidden","subject":"shadow_reconstruction_authorizes_external_effect","basis":"read-only shadow adapter has no consequence authority","reopen_if":"separate_project_local_authorization"},
        ],
        "dependencies":[{"dependency_id":"owner-usability-acceptance","class":"HARD","status":"UNSATISFIED","basis":"Issue #398 owner acceptance rule","counterfactual":"machine qualification alone cannot close gate"}],
        "triggers":[{"trigger_id":"owner-acceptance","trigger_type":"human_owner_acceptance","status":"unsatisfied","consequence":"usability gate may close"}],
        "transitions":[{"transition_id":"stage5d_acceptance","state":"complete_pending_acceptance","consequence_class":"product_canonicalization"}],
        "completeness":"COMPLETE",
    }
    return projection


def compare_observatory_snapshot(snapshot_packet: Mapping[str, Any], current_hivenues_main: str) -> Dict[str, Any]:
    src = _require_source(snapshot_packet, "snapshot")
    text = src["text"]
    _must(text, "Snapshot v0.1 is not rewritten or retroactively corrected. V0.2 supersedes it only as the current reconstruction layer.", "Observatory snapshot")
    m = re.search(r"HIVENUES_CANONICAL_COMMIT = ([0-9a-f]{40})", text)
    if not m:
        raise AdapterIncomplete("Observatory: missing HiVenues canonical commit")
    observed = m.group(1)
    return {
        "snapshot_identity": src["snapshot_identity"],
        "historical_validity": "VALID_AT_OBSERVATION_BOUNDARY",
        "observed_commit": observed,
        "current_commit": current_hivenues_main,
        "freshness": "fresh" if observed == current_hivenues_main else "stale",
        "rewrite_authorized": False,
        "adapter_version": ADAPTER_VERSION,
    }


def adapt(project_id: str, packet: Mapping[str, Any]) -> Dict[str, Any]:
    if project_id == "NFC": return adapt_nfc(packet)
    if project_id == "FCP": return adapt_fcp(packet)
    if project_id == "PGH": return adapt_pgh(packet)
    if project_id == "HIVenues": return adapt_hivenues(packet)
    raise AdapterIncomplete(f"no adapter contract for {project_id}")
