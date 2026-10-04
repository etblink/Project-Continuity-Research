from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any, Dict, Mapping

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

from cpi_profile_v0_1_3 import validate_projection
from collector import (
    CollectorError,
    NativeReader,
    collect_hivenues_current,
    public_source,
)


ADAPTER_VERSION = "cpi0-stage6g-live-enumeration-0.1.3"
PROFILE_VERSION = "0.1.3"


class AdapterIncomplete(RuntimeError):
    pass


class AdapterInconsistent(RuntimeError):
    pass


def _stage6e_projection(project_id: str) -> Dict[str, Any]:
    data = json.loads(
        (ROOT / "stage6e" / "generated_projections.json").read_text(encoding="utf-8")
    )
    return copy.deepcopy(data[project_id])


def _upgrade_source(source: Mapping[str, Any]) -> Dict[str, Any]:
    s = copy.deepcopy(dict(source))
    repo = s["repository"]
    kind = s["source_kind"]
    digest = s["content_sha256"]

    if kind == "git":
        s["revision"] = (
            f"git:{repo}:{s['commit']}:blob:{s['blob_sha']}:sha256:{digest}"
        )
    elif kind == "derived_snapshot":
        s["revision"] = f"derived_snapshot:{repo}:{s['native_id']}:sha256:{digest}"
    else:
        raise AdapterIncomplete(
            f"unchanged-project upgrade does not accept source kind {kind}"
        )
    return s


def _upgrade_stage6e_projection(project_id: str) -> Dict[str, Any]:
    p = _stage6e_projection(project_id)
    p["profile_version"] = PROFILE_VERSION
    p["producer"] = ADAPTER_VERSION
    p["observed_sources"] = [_upgrade_source(x) for x in p["observed_sources"]]
    validate_projection(p)
    return p


def _fcp_native_current_block() -> Dict[str, str]:
    path = ROOT / "stage6e" / "native" / "FCP_CURRENT_STATE.md"
    text = path.read_text(encoding="utf-8")
    if text.count("NEXT_RECOMMENDED_OPERATION =") <= 1:
        raise AdapterIncomplete("FCP regression fixture lost historical repeated routing keys")
    precedence = (
        "Operational-routing fields inside named completed-milestone sections in "
        "this document are checkpoint-era historical snapshots. They remain "
        "intentionally preserved; the controlling present-tense routing is the "
        "Open dependencies and Next-task status material above."
    )
    if precedence not in text.replace(chr(96), ""):
        raise AdapterIncomplete("FCP native precedence rule missing")
    marker = (
        "EVIDENCE_TRIGGER_PGH = "
        "T1_STABLE_NEW_FOUNDATIONAL_COMPETITOR_CANDIDATE__FULFILLED"
    )
    if text.count(marker) != 1:
        raise AdapterIncomplete("FCP fulfilled-PGH current marker is not unique")
    idx = text.index(marker)
    fence = chr(96) * 3
    start = text.rfind(fence, 0, idx)
    newline = text.find("\n", start)
    end = text.find(fence, idx)
    if start < 0 or newline < 0 or end < 0:
        raise AdapterIncomplete("FCP current block malformed")
    targeted = {
        "EVIDENCE_TRIGGER_PGH",
        "ACTIVE_SCIENTIFIC_OPERATION",
        "NEXT_EXECUTION_STEP",
        "NEXT_RECOMMENDED_OPERATION",
        "NEXT_OPERATION_CLASS",
        "NEXT_OPERATION_AUTHORIZED",
        "NEXT_OPERATION_AUTHORIZATION_BOUNDARY",
        "FCP27_SELECTED",
        "NEXT_SCIENTIFIC_PHASE",
    }
    kv: Dict[str, str] = {}
    for line in text[newline + 1 : end].splitlines():
        if " = " not in line:
            continue
        key, value = line.split(" = ", 1)
        key = key.strip()
        if key not in targeted:
            continue
        if key in kv:
            raise AdapterIncomplete(f"FCP current block duplicate targeted key: {key}")
        kv[key] = value.strip()
    return kv


def adapt_nfc() -> Dict[str, Any]:
    return _upgrade_stage6e_projection("NFC")


def adapt_fcp() -> Dict[str, Any]:
    p = _upgrade_stage6e_projection("FCP")
    kv = _fcp_native_current_block()
    expected = p["transitions"][0]
    if kv.get("NEXT_RECOMMENDED_OPERATION") != expected["transition_id"]:
        raise AdapterInconsistent("FCP frozen projection disagrees with full native file")
    if kv.get("NEXT_OPERATION_AUTHORIZED") != expected["authorization_basis"]:
        raise AdapterInconsistent("FCP authorization disagrees with full native file")
    if kv.get("NEXT_OPERATION_AUTHORIZATION_BOUNDARY") != expected["authorization_boundary"]:
        raise AdapterInconsistent("FCP boundary disagrees with full native file")
    return p


def adapt_pgh() -> Dict[str, Any]:
    return _upgrade_stage6e_projection("PGH")


def _owner_decision_sources(collected: Mapping[str, Any]) -> Dict[str, list[Mapping[str, Any]]]:
    issue_decisions = []
    for source in collected["issue398_comments"]:
        body = source["_object"].get("body") or ""
        if source["author_association"] == "OWNER" and (
            "owner acceptance" in body.lower()
            or "owner usability result" in body.lower()
        ):
            issue_decisions.append(source)

    pr_decisions = []
    for number, sources in collected["pr_comment_sources"].items():
        for source in sources:
            body = source["_object"].get("body") or ""
            if source["author_association"] == "OWNER" and (
                "owner review result" in body.lower()
                or "owner acceptance" in body.lower()
            ):
                pr_decisions.append(source)

    return {"issue": issue_decisions, "pr": pr_decisions}


def adapt_hivenues_current(reader: NativeReader) -> Dict[str, Any]:
    collected = collect_hivenues_current(reader)

    # Reuse the already independently closed Stage-6E Git-bound merged-main
    # source descriptor; only the profile revision form changes in 0.1.3.
    old = _stage6e_projection("HIVenues")
    main_old = next(x for x in old["observed_sources"] if x["source_id"] == "main")
    main = _upgrade_source(main_old)

    issue398 = collected["issue398"]
    issue374 = collected["issue374"]
    issue398_body = issue398["_object"].get("body") or ""
    if "owner acceptance governs #374" not in issue398_body:
        raise AdapterIncomplete("HiVenues: governing owner-acceptance rule missing")

    candidates = []
    for number, source in collected["pr_sources"].items():
        obj = source["_object"]
        text = (obj.get("title") or "") + "\n" + (obj.get("body") or "")
        if "#398" in text and "Stage 5D" in text:
            candidates.append(number)
    candidates.sort()
    if len(candidates) != 1:
        raise AdapterIncomplete(
            f"HiVenues: current Stage-5D candidate set is ambiguous: {candidates}"
        )
    current_number = candidates[0]
    current_pr = collected["pr_sources"][current_number]

    decisions = _owner_decision_sources(collected)
    all_decisions = decisions["issue"] + decisions["pr"]
    if not all_decisions:
        raise AdapterIncomplete("HiVenues: no owner decision found in native-direct set")

    bodies = [x["_object"].get("body") or "" for x in all_decisions]
    rejection = any(
        "acceptance: **FAIL**" in b
        or "rejects this candidate" in b
        or "HOLD / redesign required" in b
        for b in bodies
    )
    progression = any(
        "acceptance: **PASS**" in b
        or "approved for merge" in b.lower()
        for b in bodies
    )
    if rejection and progression:
        raise AdapterIncomplete("HiVenues: conflicting owner authority requires adjudication")
    if not rejection:
        raise AdapterIncomplete("HiVenues: frozen boundary no longer yields rejection")

    stop_de = any("Do not proceed to D–E" in b or "Do not proceed to D-E" in b for b in bodies)
    stop_374 = any("Do not declare #374 satisfied" in b for b in bodies)
    redesign = any("redesign" in b.lower() for b in bodies)
    if not (stop_de and stop_374 and redesign):
        raise AdapterIncomplete("HiVenues: required owner stop/redesign consequences incomplete")

    if current_pr["state"] != "open" or current_pr["draft"] is not True:
        raise AdapterInconsistent("HiVenues: rejected Stage-5D candidate is not open/draft")
    if current_pr["_object"].get("merged_at") is not None:
        raise AdapterInconsistent("HiVenues: rejected candidate unexpectedly merged")

    observed = [main, public_source(issue398), public_source(issue374)]
    for n in sorted(collected["pr_sources"]):
        observed.append(public_source(collected["pr_sources"][n]))
    for source in all_decisions:
        observed.append(public_source(source))

    p = {
        "profile_version": PROFILE_VERSION,
        "producer": ADAPTER_VERSION,
        "observed_at": collected["observed_at"],
        "project_id": "HIVenues",
        "projection_id": (
            f"HIVenues:{main['commit'][:12]}:issue398:pr{current_number}:native-direct"
        ),
        "observed_sources": observed,
        "authority_map": [
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
                "source_id": f"pr{current_number}",
                "authority_scope": "candidate_only",
            },
        ],
        "material_objects": [
            {
                "object_id": "NATIVE-DIRECT-OPEN-PR-SET",
                "role": "native_enumeration_result",
                "status": "complete_at_observation",
                "members": collected["open_pr_numbers"],
                "receipt_mode": "native_direct",
            },
            {
                "object_id": f"PR-{current_number}",
                "role": "current_candidate",
                "status": "rejected_by_owner_draft_unmerged",
            },
            {
                "object_id": "OWNER-DECISION-SET",
                "role": "human_acceptance_decisions",
                "status": "REJECTION_AND_REDESIGN",
                "source_ids": [x["source_id"] for x in all_decisions],
            },
        ],
        "negative_knowledge": [
            {
                "kind": "rejected",
                "subject": f"PR-{current_number}-current-stage5d-candidate",
                "basis": "native-direct owner decision set",
                "reopen_if": "new_redesign_candidate_plus_owner_acceptance",
            },
            {
                "kind": "forbidden",
                "subject": "proceed_to_D_E",
                "basis": "native-direct owner decision set prohibits progression",
                "reopen_if": "later_explicit_owner_acceptance_and_bounded_authorization",
            },
            {
                "kind": "forbidden",
                "subject": "declare_issue_374_satisfied",
                "basis": "native-direct owner decision set",
                "reopen_if": "later_explicit_owner_acceptance",
            },
            {
                "kind": "forbidden",
                "subject": "snapshot_fixture_asserts_current_completeness",
                "basis": "current completeness requires native_direct enumeration",
                "reopen_if": "never_for_fixture_only_current_claim",
            },
            {
                "kind": "forbidden",
                "subject": "shadow_reconstruction_authorizes_external_effect",
                "basis": "read-only CPI reconstruction has no consequence authority",
                "reopen_if": "separate_project_local_authorization",
            },
        ],
        "dependencies": [
            {
                "dependency_id": "owner-usability-acceptance",
                "class": "HARD",
                "status": "CURRENT_CANDIDATE_REJECTED",
                "basis": "native-direct owner decision set",
                "counterfactual": "a redesigned candidate must return for owner acceptance",
            }
        ],
        "triggers": [
            {
                "trigger_id": "redesign-review",
                "trigger_type": "human_owner_acceptance",
                "status": "new_candidate_required",
                "consequence": "only a later redesigned candidate may return to owner acceptance",
            }
        ],
        "transitions": [
            {
                "transition_id": "stage5d-current-candidate",
                "state": "rejected",
                "consequence_class": "product_canonicalization",
                "owner_result": "FAIL_OR_HOLD",
                "next_action": "redesign_review_before_further_broad_implementation",
            }
        ],
        "enumeration_receipts": collected["receipts"],
    }

    # enumeration_receipts is projection metadata outside the common core; core validator
    # ignores additional fields but all observed sources remain profile-conformant.
    validate_projection(p)
    return p
