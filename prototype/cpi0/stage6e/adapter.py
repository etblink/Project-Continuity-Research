from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Mapping

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from cpi_profile_v0_1_2 import validate_projection
from collector import (
    collect_git_blob_only,
    collect_git_source,
    collect_hivenues,
    public_source,
)


ADAPTER_VERSION = "cpi0-stage6e-native-binding-0.1.2"
PROFILE_VERSION = "0.1.2"


class AdapterIncomplete(RuntimeError):
    pass


class AdapterInconsistent(RuntimeError):
    pass


def _base(project_id: str, projection_id: str, observed_at: str) -> Dict[str, Any]:
    return {
        "profile_version": PROFILE_VERSION,
        "producer": ADAPTER_VERSION,
        "observed_at": observed_at,
        "project_id": project_id,
        "projection_id": projection_id,
    }


def _finish(projection: Dict[str, Any]) -> Dict[str, Any]:
    validate_projection(projection)
    return projection


def _must(text: str, marker: str, label: str) -> None:
    if marker not in text:
        raise AdapterIncomplete(f"{label}: missing required marker: {marker}")


def _unique(text: str, marker: str, label: str) -> None:
    count = text.count(marker)
    if count != 1:
        raise AdapterIncomplete(
            f"{label}: expected one occurrence of {marker!r}, found {count}"
        )


def _code_block_around(text: str, marker: str, label: str) -> str:
    idx = text.find(marker)
    if idx < 0:
        raise AdapterIncomplete(f"{label}: marker not found")
    fence = chr(96) * 3
    starts = [text.rfind(fence + "text", 0, idx), text.rfind(fence, 0, idx)]
    start = max(starts)
    if start < 0:
        raise AdapterIncomplete(f"{label}: controlling marker is not fenced")
    newline = text.find("\n", start)
    end = text.find(fence, idx)
    if newline < 0 or end < 0:
        raise AdapterIncomplete(f"{label}: malformed fenced block")
    return text[newline + 1 : end]


def _kv_block(block: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    duplicates = set()
    for line in block.splitlines():
        if " = " not in line:
            continue
        key, value = line.split(" = ", 1)
        key = key.strip()
        value = value.strip()
        if key in out:
            duplicates.add(key)
        out[key] = value
    if duplicates:
        raise AdapterIncomplete(
            "controlling block contains duplicate keys: " + ", ".join(sorted(duplicates))
        )
    return out


def _manifest_observed_at() -> str:
    return json.loads(
        (HERE / "native" / "NATIVE_SOURCE_MANIFEST.json").read_text(encoding="utf-8")
    )["observed_at"]


def adapt_nfc() -> Dict[str, Any]:
    src = collect_git_source(
        "nfc_provenance",
        "publication-main",
        "publication_provenance_surface",
    )
    text = src["_content"]
    for marker in [
        "REF = archive/nfc-canonical-ed3047c2",
        "COMMIT = ed3047c2cbc0abc34d2549dd27754e4d3d05af78",
        "TREE = 00ef55ff36d5e9663ca1ef2c9566e2bc1396f973",
        "HUMAN_POLICY_INTENT = UNRESOLVED",
        "Do not use default-branch presence as a proxy for scientific authority.",
    ]:
        _must(text, marker, "NFC provenance")

    canon_ref = re.search(r"^REF = (.+)$", text, re.M).group(1)
    canon_commit = re.search(r"^COMMIT = ([0-9a-f]{40})$", text, re.M).group(1)
    canon_tree = re.search(r"^TREE = ([0-9a-f]{40})$", text, re.M).group(1)

    canon_identity = f"{canon_ref}@{canon_commit}:tree:{canon_tree}".encode()
    canon_sha256 = hashlib.sha256(canon_identity).hexdigest()
    native_id = f"NFC_THEOREM_CANON:{canon_commit}:{canon_tree}"
    canon_source = {
        "source_id": "frozen-theorem-canon",
        "repository": "etblink/Nested-Fibrational-Cosmology",
        "ref": canon_ref,
        "role": "scientific_theorem_canon",
        "source_kind": "derived_snapshot",
        "native_id": native_id,
        "content_sha256": canon_sha256,
        "revision": f"derived_snapshot:{native_id}:sha256:{canon_sha256}",
    }

    p = _base("NFC", f"NFC:{src['commit'][:12]}", _manifest_observed_at())
    p.update(
        observed_sources=[public_source(src), canon_source],
        authority_map=[
            {
                "purpose": "publication_routing",
                "source_id": "publication-main",
                "authority_scope": "publication_and_provenance",
            },
            {
                "purpose": "scientific_theorem_analysis",
                "source_id": "frozen-theorem-canon",
                "authority_scope": "frozen_theorem_bearing_corpus",
            },
        ],
        material_objects=[],
        negative_knowledge=[
            {
                "kind": "unresolved",
                "subject": "historical_remove_human_policy_intent",
                "basis": "HUMAN_POLICY_INTENT = UNRESOLVED",
            }
        ],
        dependencies=[],
        triggers=[],
        transitions=[],
    )
    return _finish(p)


def adapt_fcp() -> Dict[str, Any]:
    current = collect_git_source(
        "fcp_current_state",
        "current-state",
        "current_scientific_and_routing_state",
    )
    charter = collect_git_source(
        "fcp_charter",
        "charter",
        "governance_authority",
    )
    text = current["_content"]
    charter_text = charter["_content"]

    precedence = (
        "Operational-routing fields inside named completed-milestone sections in "
        "this document are checkpoint-era historical snapshots. They remain "
        "intentionally preserved; the controlling present-tense routing is the "
        "Open dependencies and Next-task status material above."
    )
    normalized = text.replace(chr(96), "")
    _must(normalized, precedence, "FCP current state")

    trigger_marker = (
        "EVIDENCE_TRIGGER_PGH = "
        "T1_STABLE_NEW_FOUNDATIONAL_COMPETITOR_CANDIDATE__FULFILLED"
    )
    _unique(text, trigger_marker, "FCP current state")
    block = _code_block_around(text, trigger_marker, "FCP current routing")
    kv = _kv_block(block)

    required = {
        "ACTIVE_SCIENTIFIC_OPERATION": "NONE",
        "NEXT_EXECUTION_STEP": "POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION",
        "NEXT_RECOMMENDED_OPERATION": "POST_PGH_STAGE2_SCIENTIFIC_SEQUENCING_ADJUDICATION",
        "NEXT_OPERATION_CLASS": "READ_ONLY_SCIENTIFIC_SEQUENCING_ADJUDICATION",
        "NEXT_OPERATION_AUTHORIZED": "YES__STANDING_PROJECT_LEAD_DELEGATION",
        "NEXT_OPERATION_AUTHORIZATION_BOUNDARY": "SEQUENCING_ONLY__NO_SUBSEQUENT_FCP_SCIENCE_BEFORE_SELECTION",
        "FCP27_SELECTED": "NO",
        "NEXT_SCIENTIFIC_PHASE": "NONE__POST_PGH_STAGE2_SEQUENCING_PENDING",
        "EVIDENCE_TRIGGER_PGH": "T1_STABLE_NEW_FOUNDATIONAL_COMPETITOR_CANDIDATE__FULFILLED",
    }
    for key, expected in required.items():
        if kv.get(key) != expected:
            raise AdapterIncomplete(
                f"FCP controlling block: {key} expected {expected!r}, got {kv.get(key)!r}"
            )

    _must(
        charter_text,
        "Every substantive future phase requires separate bounded authorization "
        "and an explicit source/provenance window",
        "FCP charter",
    )
    _must(text, "METHOD = 0.2.1_ACTIVE_PROSPECTIVELY", "FCP method")

    p = _base("FCP", f"FCP:{current['commit'][:12]}", _manifest_observed_at())
    p.update(
        observed_sources=[public_source(current), public_source(charter)],
        authority_map=[
            {
                "purpose": "current_routing",
                "source_id": "current-state",
                "authority_scope": "native_current_state_precedence_and_post_pgh_block",
            },
            {
                "purpose": "future_phase_authorization_rule",
                "source_id": "charter",
                "authority_scope": "governance_rule",
            },
        ],
        material_objects=[
            {
                "object_id": "method",
                "role": "current_prospective_method",
                "status": "0.2.1_ACTIVE_PROSPECTIVELY",
            },
            {
                "object_id": "routing",
                "role": "current_routing_state",
                "status": kv["NEXT_RECOMMENDED_OPERATION"],
            },
            {
                "object_id": "fcp27",
                "role": "phase_selection",
                "status": "not_selected",
            },
        ],
        negative_knowledge=[
            {
                "kind": "historical_marker",
                "subject": "prior_evidence_triggered_hold",
                "basis": "prior EVIDENCE_TRIGGERED_HOLD fulfilled by named PGH T1",
                "status": "fulfilled",
            },
            {
                "kind": "authorization_boundary",
                "subject": "subsequent_fcp_science",
                "basis": kv["NEXT_OPERATION_AUTHORIZATION_BOUNDARY"],
            },
        ],
        dependencies=[],
        triggers=[
            {
                "trigger_id": "PGH-T1",
                "trigger_type": "evidence_event",
                "status": "fulfilled",
                "consequence": "prior hold satisfied; PGH Stage 1/2 canonically completed",
            }
        ],
        transitions=[
            {
                "transition_id": kv["NEXT_RECOMMENDED_OPERATION"],
                "state": "selected_authorized",
                "consequence_class": "read_only_scientific_sequencing",
                "operation_class": kv["NEXT_OPERATION_CLASS"],
                "authorization_basis": kv["NEXT_OPERATION_AUTHORIZED"],
                "authorization_boundary": kv["NEXT_OPERATION_AUTHORIZATION_BOUNDARY"],
                "next_scientific_phase": kv["NEXT_SCIENTIFIC_PHASE"],
            }
        ],
    )
    return _finish(p)


def _parse_pgh_capsule(text: str) -> Mapping[str, Any]:
    start = "<!-- PGH_CURRENT_STATE_CAPSULE_BEGIN -->"
    end = "<!-- PGH_CURRENT_STATE_CAPSULE_END -->"
    if start not in text or end not in text:
        raise AdapterIncomplete("PGH: current-state capsule missing")
    segment = text.split(start, 1)[1].split(end, 1)[0]
    fence_json = (chr(96) * 3) + "json"
    fence = chr(96) * 3
    if fence_json not in segment:
        raise AdapterIncomplete("PGH: JSON fence missing")
    payload = segment.split(fence_json, 1)[1].split(fence, 1)[0].strip()
    return json.loads(payload)


def adapt_pgh() -> Dict[str, Any]:
    current = collect_git_source(
        "pgh_current_state",
        "current-state",
        "current_research_and_governance_state",
    )
    text = current["_content"]
    for marker in [
        "NEXT_SCIENTIFIC_OPERATION = APPARATUS_REALIZATION_AND_TARGET_FREEZE",
        "PHYSICAL_TRIAL_EXECUTION_AUTHORIZED = NO",
        "WEB_TARGET_SEARCH = FORBIDDEN_WITHOUT_NEW_INDEPENDENT_TRIGGER",
        "REGISTRY_TARGET_SEARCH = FORBIDDEN_WITHOUT_NEW_INDEPENDENT_TRIGGER",
    ]:
        _must(text, marker, "PGH current state")

    capsule = _parse_pgh_capsule(text)
    if capsule.get("actual_apparatus") is not None:
        raise AdapterInconsistent("PGH: actual apparatus unexpectedly bound")
    if capsule.get("physical_trials_authorized") is not False:
        raise AdapterInconsistent("PGH: physical trials unexpectedly authorized")

    p = _base("PGH", f"PGH:{current['commit'][:12]}", _manifest_observed_at())
    p.update(
        observed_sources=[public_source(current)],
        authority_map=[
            {
                "purpose": "current_research_and_governance_state",
                "source_id": "current-state",
                "authority_scope": "canonical_markdown_plus_git_provenance",
            }
        ],
        material_objects=[
            {
                "object_id": capsule["active_candidate_package"],
                "role": "active_candidate_package",
                "status": "empirically_untested",
            }
        ],
        negative_knowledge=[
            {
                "kind": "forbidden_assumptions",
                "subject": capsule["active_candidate_package"],
                "basis": "current-state do_not_assume capsule",
                "items": capsule["do_not_assume"],
            },
            {
                "kind": "suspended",
                "subject": "target_search",
                "basis": "new independent trigger required",
                "reopen_if": "new_independent_trigger",
            },
        ],
        dependencies=[
            {
                "dependency_id": "real-apparatus",
                "class": "HARD",
                "status": "UNSATISFIED",
                "basis": "actual apparatus is unbound",
                "counterfactual": "synthetic readiness cannot replace physical apparatus",
            }
        ],
        triggers=[
            {
                "trigger_id": "apparatus-realization",
                "trigger_type": "physical_prerequisite",
                "status": "unsatisfied",
                "consequence": capsule["next_scientific_operation"],
            }
        ],
        transitions=[
            {
                "transition_id": capsule["next_scientific_operation"],
                "state": "blocked_external",
                "consequence_class": "physical_experiment_preparation",
            },
            {
                "transition_id": "PHYSICAL_TRIAL_EXECUTION",
                "state": "prohibited",
                "consequence_class": "physical_experiment",
            },
        ],
    )
    return _finish(p)


def adapt_hivenues() -> Dict[str, Any]:
    readme = collect_git_source(
        "hivenues_readme",
        "main",
        "canonical_merged_code",
    )
    collected = collect_hivenues()
    if not collected["discovery"]["complete"]:
        raise AdapterIncomplete("HiVenues: discovery is not complete")

    issue398 = collected["issue398"]
    issue374 = collected["issue374"]
    issue398_body = issue398["_object"].get("body") or ""
    _must(issue398_body, "owner acceptance governs #374", "HiVenues Issue #398")

    candidate_numbers = []
    for number, source in collected["pr_sources"].items():
        obj = source["_object"]
        body = obj.get("body") or ""
        title = obj.get("title") or ""
        if "#398" in body and "Stage 5D" in (title + "\n" + body):
            candidate_numbers.append(number)
    candidate_numbers.sort()
    if candidate_numbers != [399]:
        raise AdapterIncomplete(
            f"HiVenues: expected current Stage-5D candidate [399], got {candidate_numbers}"
        )

    pr399 = collected["pr_sources"][399]
    pr397 = collected["pr_sources"][397]
    if pr399["state"] != "open" or pr399["draft"] is not True:
        raise AdapterInconsistent("HiVenues: PR #399 must be open/draft")
    if pr399["_object"].get("merged_at") is not None:
        raise AdapterInconsistent("HiVenues: PR #399 unexpectedly merged")

    issue_decisions = []
    for source in collected["issue398_comments"]:
        body = source["_object"].get("body") or ""
        if (
            source["author_association"] == "OWNER"
            and "Current A–C owner acceptance: **FAIL**" in body
            and "PR #399 must remain draft/unmerged." in body
            and "Do not proceed to D–E." in body
            and "Do not declare #374 satisfied." in body
        ):
            issue_decisions.append(source)
    if len(issue_decisions) != 1:
        raise AdapterIncomplete(
            f"HiVenues: expected one decisive Issue #398 owner decision, got {len(issue_decisions)}"
        )
    owner_issue = issue_decisions[0]

    pr_decisions = []
    for source in collected["pr_comment_sources"][399]:
        body = source["_object"].get("body") or ""
        if (
            source["author_association"] == "OWNER"
            and "Owner review result — HOLD / redesign required" in body
            and "Keep this PR draft/unmerged." in body
            and "Do not proceed to D–E from this candidate." in body
        ):
            pr_decisions.append(source)
    if len(pr_decisions) != 1:
        raise AdapterIncomplete(
            f"HiVenues: expected one concordant PR #399 owner decision, got {len(pr_decisions)}"
        )
    owner_pr = pr_decisions[0]

    observed = [
        public_source(readme),
        public_source(issue398),
        public_source(issue374),
        public_source(pr397),
        public_source(pr399),
        public_source(owner_issue),
        public_source(owner_pr),
    ]

    p = _base(
        "HIVenues",
        f"HIVenues:{readme['commit'][:12]}:issue398:pr399",
        collected["observed_at"],
    )
    p.update(
        observed_sources=observed,
        authority_map=[
            {
                "purpose": "canonical_merged_code",
                "source_id": "main",
                "authority_scope": "merged_main",
            },
            {
                "purpose": "stage5d_work_charter",
                "source_id": "issue398",
                "authority_scope": "bounded_stage5d_work",
            },
            {
                "purpose": "stage5_usability_gate",
                "source_id": "issue374",
                "authority_scope": "owner_acceptance_gate",
            },
            {
                "purpose": "stage5d_current_candidate",
                "source_id": "pr399",
                "authority_scope": "candidate_only",
            },
            {
                "purpose": "stage5d_usability_acceptance",
                "source_id": owner_issue["source_id"],
                "authority_scope": "owner_acceptance_decision",
            },
            {
                "purpose": "stage5d_candidate_review_confirmation",
                "source_id": owner_pr["source_id"],
                "authority_scope": "concordant_owner_hold_decision",
            },
        ],
        material_objects=[
            {
                "object_id": "OPEN-PR-SET",
                "role": "discovery_result",
                "status": "complete",
                "members": collected["discovery"]["open_pr_numbers"],
            },
            {
                "object_id": "PR-397",
                "role": "prior_candidate",
                "status": "open_unmerged_prior_lineage",
            },
            {
                "object_id": "PR-399",
                "role": "current_candidate",
                "status": "rejected_by_owner_draft_unmerged",
            },
            {
                "object_id": "OWNER-ISSUE-DECISION",
                "role": "human_acceptance_decision",
                "status": "FAIL",
            },
            {
                "object_id": "OWNER-PR399-CONFIRMATION",
                "role": "human_acceptance_confirmation",
                "status": "HOLD_REDESIGN_REQUIRED",
            },
        ],
        negative_knowledge=[
            {
                "kind": "rejected",
                "subject": "PR-399-current-A-C-candidate",
                "basis": "owner acceptance FAIL on complete Issue #398 comment stream",
                "reopen_if": "new_redesign_candidate_plus_owner_acceptance",
            },
            {
                "kind": "forbidden",
                "subject": "proceed_to_D_E",
                "basis": "both owner decision surfaces prohibit D-E progression",
                "reopen_if": "later_explicit_owner_acceptance_and_bounded_authorization",
            },
            {
                "kind": "forbidden",
                "subject": "declare_issue_374_satisfied",
                "basis": "owner decision says do not declare #374 satisfied",
                "reopen_if": "later_explicit_owner_acceptance",
            },
            {
                "kind": "forbidden",
                "subject": "shadow_reconstruction_authorizes_external_effect",
                "basis": "read-only CPI reconstruction has no consequence authority",
                "reopen_if": "separate_project_local_authorization",
            },
        ],
        dependencies=[
            {
                "dependency_id": "owner-usability-acceptance",
                "class": "HARD",
                "status": "CURRENT_CANDIDATE_REJECTED",
                "basis": "complete owner decision set for Issue #398/current PR #399",
                "counterfactual": "a redesigned candidate must return for owner acceptance",
            }
        ],
        triggers=[
            {
                "trigger_id": "redesign-review",
                "trigger_type": "human_owner_acceptance",
                "status": "new_candidate_required",
                "consequence": "only a later redesigned candidate may return to owner acceptance",
            }
        ],
        transitions=[
            {
                "transition_id": "stage5d-current-candidate",
                "state": "rejected",
                "consequence_class": "product_canonicalization",
                "owner_result": "FAIL",
                "next_action": "redesign_review_before_further_broad_implementation",
            }
        ],
    )
    return _finish(p)


def compare_observatory_snapshot() -> Dict[str, Any]:
    snapshot = collect_git_blob_only("observatory_snapshot")
    text = snapshot["content"]
    _must(text, "FCP_PROJECT_STATE = WAITING_FOR_EVIDENCE", "Observatory v0.2")
    _must(
        text,
        "FCP_CANONICAL_COMMIT = a41bc6101b63140ee2687e0cf67a47ab6be77215",
        "Observatory v0.2",
    )
    _must(
        text,
        "HIVENUES_CANONICAL_COMMIT = bf9a0b4e61d57eed6bb5a81504d6e030f8b6ff7c",
        "Observatory v0.2",
    )

    fcp = adapt_fcp()
    fcp_commit = re.search(r"FCP_CANONICAL_COMMIT = ([0-9a-f]{40})", text).group(1)
    hv_commit = re.search(r"HIVENUES_CANONICAL_COMMIT = ([0-9a-f]{40})", text).group(1)
    hivenues = adapt_hivenues()
    current_hv_main = next(
        x["commit"] for x in hivenues["observed_sources"] if x["source_id"] == "main"
    )

    return {
        "adapter_version": ADAPTER_VERSION,
        "snapshot_identity": "PROJECT_OBSERVATORY_SNAPSHOT_V0_2",
        "snapshot_blob_sha": snapshot["blob_sha"],
        "snapshot_content_sha256": snapshot["content_sha256"],
        "overall_validity": "MIXED__NO_BLANKET_VALIDITY",
        "rewrite_authorized": False,
        "project_results": {
            "FCP": {
                "snapshot_commit": fcp_commit,
                "snapshot_state": "WAITING_FOR_EVIDENCE",
                "native_current_routing_at_same_commit": fcp["transitions"][0][
                    "transition_id"
                ],
                "historical_validity": "CONTRADICTED_BY_REFERENCED_NATIVE_STATE",
                "freshness": "same_revision_semantic_conflict",
                "rewrite_authorized": False,
            },
            "HIVenues": {
                "observed_commit": hv_commit,
                "current_commit": current_hv_main,
                "historical_validity": "VALID_IDENTITY_AT_OBSERVATION_BOUNDARY",
                "freshness": "fresh" if hv_commit == current_hv_main else "stale",
                "rewrite_authorized": False,
            },
        },
    }


def generate_all() -> Dict[str, Any]:
    return {
        "NFC": adapt_nfc(),
        "FCP": adapt_fcp(),
        "PGH": adapt_pgh(),
        "HIVenues": adapt_hivenues(),
        "OBSERVATORY_COMPARISON": compare_observatory_snapshot(),
    }
