from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict, Mapping

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

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


def _load_stage6e_adapter():
    path = ROOT / "stage6e" / "adapter.py"
    spec = importlib.util.spec_from_file_location("cpi_stage6e_adapter_for_stage6g", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Stage-6E adapter")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
            f"Stage-6G legacy upgrade does not accept non-Git source kind {kind}"
        )
    return s


def _upgrade_stage6e_projection(project_id: str) -> Dict[str, Any]:
    e = _load_stage6e_adapter()
    fn = {"NFC": e.adapt_nfc, "FCP": e.adapt_fcp, "PGH": e.adapt_pgh}[project_id]
    p = copy.deepcopy(fn())
    p["profile_version"] = PROFILE_VERSION
    p["producer"] = ADAPTER_VERSION
    p["observed_sources"] = [_upgrade_source(x) for x in p["observed_sources"]]
    validate_projection(p)
    return p


def adapt_nfc() -> Dict[str, Any]:
    return _upgrade_stage6e_projection("NFC")


def adapt_fcp() -> Dict[str, Any]:
    return _upgrade_stage6e_projection("FCP")


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

    # Reuse the already independently closed Stage-6E Git binding for merged-main
    # README; upgrade only its profile revision form.
    e = _load_stage6e_adapter()
    old = e.adapt_hivenues()
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
