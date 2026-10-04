from __future__ import annotations

import copy
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

from cpi_profile_v0_1_5 import validate_projection
from collector import collect_hivenues_current, public_source


ADAPTER_VERSION = "cpi0-stage6k-owner-authority-reducer-0.1.5"
PROFILE_VERSION = "0.1.5"


class AdapterIncomplete(RuntimeError):
    pass


class AdapterInconsistent(RuntimeError):
    pass


def _stage6e_projection(project_id: str) -> Dict[str, Any]:
    data = json.loads(
        (ROOT / "stage6e" / "generated_projections.json").read_text(
            encoding="utf-8"
        )
    )
    return copy.deepcopy(data[project_id])


def _upgrade_source(source: Mapping[str, Any]) -> Dict[str, Any]:
    s = copy.deepcopy(dict(source))
    repository = s["repository"]
    kind = s["source_kind"]
    digest = s["content_sha256"]

    if kind == "git":
        s["revision"] = (
            f"git:{repository}:{s['commit']}:blob:{s['blob_sha']}:sha256:{digest}"
        )
    elif kind == "derived_snapshot":
        s["revision"] = (
            f"derived_snapshot:{repository}:{s['native_id']}:sha256:{digest}"
        )
    else:
        raise AdapterIncomplete(
            f"legacy project upgrade does not accept source kind {kind}"
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
    if text.count("NEXT_RECOMMENDED_OPERATION =") != 14:
        raise AdapterIncomplete(
            "FCP regression fixture no longer preserves expected historical multiplicity"
        )

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
        raise AdapterIncomplete("FCP fulfilled-PGH marker is not unique")

    idx = text.index(marker)
    fence = chr(96) * 3
    start = text.rfind(fence, 0, idx)
    newline = text.find("\n", start)
    end = text.find(fence, idx)
    if start < 0 or newline < 0 or end < 0:
        raise AdapterIncomplete("FCP current routing block malformed")

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
            raise AdapterIncomplete(f"FCP duplicate controlling key: {key}")
        kv[key] = value.strip()
    return kv


def adapt_nfc() -> Dict[str, Any]:
    return _upgrade_stage6e_projection("NFC")


def adapt_fcp() -> Dict[str, Any]:
    p = _upgrade_stage6e_projection("FCP")
    kv = _fcp_native_current_block()
    t = p["transitions"][0]
    if kv.get("NEXT_RECOMMENDED_OPERATION") != t["transition_id"]:
        raise AdapterInconsistent("FCP transition disagrees with full native file")
    if kv.get("NEXT_OPERATION_AUTHORIZED") != t["authorization_basis"]:
        raise AdapterInconsistent("FCP authorization disagrees with native file")
    if (
        kv.get("NEXT_OPERATION_AUTHORIZATION_BOUNDARY")
        != t["authorization_boundary"]
    ):
        raise AdapterInconsistent("FCP boundary disagrees with native file")
    return p


def adapt_pgh() -> Dict[str, Any]:
    return _upgrade_stage6e_projection("PGH")


def _main_git_source() -> Dict[str, Any]:
    old = _stage6e_projection("HIVenues")
    source = next(x for x in old["observed_sources"] if x["source_id"] == "main")
    return _upgrade_source(source)


def _all_sources(bundle: Mapping[str, Any]) -> List[Mapping[str, Any]]:
    sources: List[Mapping[str, Any]] = [
        bundle["issue398"],
        bundle["issue374"],
        *bundle["issue398_comments"],
        *bundle["issue374_comments"],
    ]
    for number in sorted(bundle["pr_sources"]):
        sources.append(bundle["pr_sources"][number])
        sources.extend(bundle["pr_comment_sources"][number])
        sources.extend(bundle["pr_review_sources"][number])
        sources.extend(bundle["pr_inline_review_comment_sources"][number])
    return sources


def _body(source: Mapping[str, Any]) -> str:
    return str(source.get("_object", {}).get("body") or "")


def _parse_time(value: Any) -> datetime:
    if not isinstance(value, str) or not value:
        raise AdapterIncomplete("authority event lacks native timestamp")
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise AdapterIncomplete("authority event has invalid native timestamp") from exc


def _event_time(source: Mapping[str, Any]) -> str:
    kind = source["source_kind"]
    obj = source.get("_object", {})
    if kind == "github_pull_request_review":
        value = source.get("submitted_at") or obj.get("submitted_at")
    elif kind in {
        "github_issue_comment",
        "github_pull_request_review_comment",
        "github_issue",
    }:
        value = (
            source.get("updated_at")
            or obj.get("updated_at")
            or source.get("created_at")
            or obj.get("created_at")
        )
    else:
        raise AdapterIncomplete(
            f"unsupported authority-event source kind: {kind}"
        )
    _parse_time(value)
    return str(value)


PASS_PATTERNS = [
    re.compile(r"\bpass(?:ed)?\b", re.I),
    re.compile(r"\baccepted\b", re.I),
    re.compile(r"\bacceptance\s+(?:is\s+)?granted\b", re.I),
    re.compile(r"\bapprov(?:e|ed)\b", re.I),
    re.compile(r"\blgtm\b", re.I),
    re.compile(r"\bship\s+it\b", re.I),
    re.compile(r"\bgood\s+to\s+go\b", re.I),
    re.compile(r"\b(?:gate|#374)\b.{0,50}\bsatisfied\b", re.I | re.S),
    re.compile(r"\bwould\s+continue\s+using\b", re.I),
]

FAIL_PATTERNS = [
    re.compile(r"\bfail(?:ed)?\b", re.I),
    re.compile(r"\bnot\s+accepted\b", re.I),
    re.compile(r"\bacceptance\s+(?:is\s+)?not\s+granted\b", re.I),
    re.compile(r"\breject(?:ed|s|ion)?\b", re.I),
    re.compile(r"\bhold\b", re.I),
    re.compile(r"\bchanges\s+requested\b", re.I),
    re.compile(r"\bredesign\s+required\b", re.I),
    re.compile(r"\bdo\s+not\s+proceed\b", re.I),
    re.compile(r"\bwould\s+(?:exit|quit)\b", re.I),
    re.compile(r"\bmust\s+remain\s+(?:draft|unmerged)\b", re.I),
]


def _classify_owner_source(source: Mapping[str, Any]) -> str:
    body = _body(source)
    kind = source["source_kind"]

    pass_signal = False
    fail_signal = False

    if kind == "github_pull_request_review":
        state = str(source.get("state", "")).upper()
        if state == "APPROVED":
            pass_signal = True
        if state == "CHANGES_REQUESTED":
            fail_signal = True

    if any(pattern.search(body) for pattern in PASS_PATTERNS):
        pass_signal = True
    if any(pattern.search(body) for pattern in FAIL_PATTERNS):
        fail_signal = True

    if pass_signal and fail_signal:
        return "AMBIGUOUS_AUTHORITY"
    if pass_signal:
        return "PASS"
    if fail_signal:
        return "FAIL_OR_HOLD"
    return "NONDECISIONAL_OWNER_EVENT"


def _repository_owner(source: Mapping[str, Any]) -> str:
    return str(source["repository"]).split("/", 1)[0].lower()


def _is_owner_source(source: Mapping[str, Any]) -> bool:
    if source.get("author_association") == "OWNER":
        return True
    obj = source.get("_object", {})
    if obj.get("author_association") == "OWNER":
        return True
    login = str((obj.get("user") or {}).get("login") or "").lower()
    return bool(login) and login == _repository_owner(source)


def _authority_lane(
    source: Mapping[str, Any],
    current_pr_number: int,
) -> Optional[str]:
    kind = source["source_kind"]
    sid = str(source["source_id"])

    if sid == "issue374":
        return "gate"
    if kind == "github_issue_comment" and source.get("issue_number") == 374:
        return "gate"

    if kind == "github_issue_comment" and source.get("issue_number") == 398:
        return "candidate"

    if kind == "github_issue_comment" and source.get("issue_number") == current_pr_number:
        return "candidate"

    if kind in {
        "github_pull_request_review",
        "github_pull_request_review_comment",
    } and source.get("pr_number") == current_pr_number:
        return "candidate"

    return None


def _authority_events(
    bundle: Mapping[str, Any],
    current_pr_number: int,
) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []

    for source in _all_sources(bundle):
        lane = _authority_lane(source, current_pr_number)
        if lane is None:
            continue

        if source["source_id"] == "issue374":
            if not _is_owner_source(source):
                continue
        elif not _is_owner_source(source):
            continue

        classification = _classify_owner_source(source)
        event = {
            "source_id": source["source_id"],
            "lane": lane,
            "classification": classification,
            "event_time": _event_time(source),
            "source_kind": source["source_kind"],
        }
        events.append(event)

    events.sort(
        key=lambda x: (
            _parse_time(x["event_time"]),
            x["source_id"],
        )
    )
    return events


def _latest_decision(
    events: List[Mapping[str, Any]],
    lane: str,
) -> Optional[Dict[str, Any]]:
    decisional = [
        dict(event)
        for event in events
        if event["lane"] == lane
        and event["classification"] != "NONDECISIONAL_OWNER_EVENT"
    ]
    return decisional[-1] if decisional else None


def _latest_overall_decision(
    gate_latest: Optional[Mapping[str, Any]],
    candidate_latest: Optional[Mapping[str, Any]],
) -> Optional[Dict[str, Any]]:
    values = [
        dict(x) for x in [gate_latest, candidate_latest] if x is not None
    ]
    if not values:
        return None
    values.sort(
        key=lambda x: (
            _parse_time(x["event_time"]),
            x["source_id"],
        )
    )
    return values[-1]


def _reduce_authority(
    events: List[Mapping[str, Any]],
) -> Dict[str, Any]:
    gate_latest = _latest_decision(events, "gate")
    candidate_latest = _latest_decision(events, "candidate")

    for latest in [gate_latest, candidate_latest]:
        if latest and latest["classification"] == "AMBIGUOUS_AUTHORITY":
            raise AdapterIncomplete(
                f"ambiguous owner authority at {latest['source_id']}"
            )

    latest = _latest_overall_decision(gate_latest, candidate_latest)
    if latest is None:
        raise AdapterIncomplete("no current owner decision exists")

    if latest["classification"] == "FAIL_OR_HOLD":
        return {
            "state": "rejected",
            "owner_result": "FAIL_OR_HOLD",
            "next_action": "redesign_review_before_further_broad_implementation",
            "gate_latest": gate_latest,
            "candidate_latest": candidate_latest,
            "latest_overall": latest,
            "d_e_authorized": False,
        }

    if latest["classification"] != "PASS":
        raise AdapterIncomplete("unsupported current owner decision")

    if gate_latest and gate_latest["classification"] == "PASS":
        return {
            "state": "accepted",
            "owner_result": "PASS",
            "next_action": "native_project_post_acceptance_authorization_gate",
            "gate_latest": gate_latest,
            "candidate_latest": candidate_latest,
            "latest_overall": latest,
            "d_e_authorized": False,
        }

    return {
        "state": "accepted_pending_gate_sync",
        "owner_result": "PASS_PENDING_GATE_SYNC",
        "next_action": "synchronize_explicit_issue_374_owner_gate_acceptance",
        "gate_latest": gate_latest,
        "candidate_latest": candidate_latest,
        "latest_overall": latest,
        "d_e_authorized": False,
    }


def _adapt_hivenues_bundle(
    bundle: Mapping[str, Any],
    require_authoritative: bool,
) -> Dict[str, Any]:
    if require_authoritative and bundle.get("authoritative") is not True:
        raise AdapterIncomplete(
            "current HiVenues projection requires authoritative production collection"
        )

    observation = bundle.get("observation")
    if not isinstance(observation, Mapping):
        raise AdapterIncomplete("HiVenues stabilized observation metadata missing")
    if observation.get("mode") != "stabilized_native_window":
        raise AdapterIncomplete("HiVenues observation is not stabilized")
    if int(observation.get("consecutive_equal_sweeps", 0)) < 2:
        raise AdapterIncomplete("HiVenues observation lacks two equal sweeps")

    issue398_body = _body(bundle["issue398"])
    if "owner acceptance governs #374" not in issue398_body:
        raise AdapterIncomplete("HiVenues governing owner-acceptance rule missing")

    candidates: List[int] = []
    for number, source in bundle["pr_sources"].items():
        obj = source["_object"]
        text = (obj.get("title") or "") + "\n" + (obj.get("body") or "")
        if "#398" in text and "Stage 5D" in text:
            candidates.append(int(number))
    candidates.sort()
    if len(candidates) != 1:
        raise AdapterIncomplete(
            f"HiVenues current Stage-5D candidate set ambiguous: {candidates}"
        )

    current_number = candidates[0]
    current_pr = bundle["pr_sources"][current_number]
    if current_pr["state"] != "open" or current_pr["draft"] is not True:
        raise AdapterInconsistent(
            "HiVenues current Stage-5D candidate must remain open/draft at this boundary"
        )
    if current_pr["_object"].get("merged_at") is not None:
        raise AdapterInconsistent("HiVenues current Stage-5D candidate is merged")

    events = _authority_events(bundle, current_number)
    reduced = _reduce_authority(events)

    main = _main_git_source()
    observed_sources = [main] + [
        public_source(x) for x in _all_sources(bundle)
    ]

    negative_knowledge = [
        {
            "kind": "forbidden",
            "subject": "shadow_reconstruction_authorizes_external_effect",
            "basis": "read-only CPI reconstruction has no consequence authority",
            "reopen_if": "separate_project_local_authorization",
        },
        {
            "kind": "forbidden",
            "subject": "claim_atomic_github_observation",
            "basis": "GitHub REST collection is stabilized across a window, not transactional",
            "reopen_if": "native_transactional_snapshot_primitive",
        },
    ]

    dependencies: List[Dict[str, Any]] = []
    triggers: List[Dict[str, Any]] = []

    if reduced["state"] == "rejected":
        negative_knowledge.extend(
            [
                {
                    "kind": "rejected",
                    "subject": f"PR-{current_number}-current-stage5d-candidate",
                    "basis": "latest native owner authority is FAIL/HOLD",
                    "reopen_if": "later_explicit_owner_acceptance",
                },
                {
                    "kind": "forbidden",
                    "subject": "proceed_to_D_E",
                    "basis": "latest native owner authority is FAIL/HOLD",
                    "reopen_if": "later_explicit_owner_acceptance_and_native_authorization",
                },
                {
                    "kind": "forbidden",
                    "subject": "declare_issue_374_satisfied",
                    "basis": "latest native owner authority does not establish gate PASS",
                    "reopen_if": "later_explicit_issue_374_owner_gate_pass",
                },
            ]
        )
        dependencies.append(
            {
                "dependency_id": "owner-usability-acceptance",
                "class": "HARD",
                "status": "CURRENT_CANDIDATE_REJECTED",
                "basis": "latest temporally reduced owner authority",
                "counterfactual": "later explicit owner PASS changes the authority state",
            }
        )
        triggers.append(
            {
                "trigger_id": "later-owner-decision",
                "trigger_type": "human_owner_acceptance",
                "status": "waiting_for_later_decision",
                "consequence": "recompute temporally ordered owner authority",
            }
        )

    elif reduced["state"] == "accepted_pending_gate_sync":
        negative_knowledge.append(
            {
                "kind": "forbidden",
                "subject": "proceed_to_D_E",
                "basis": "candidate-level owner PASS is newer but #374 gate has not synchronized PASS",
                "reopen_if": "explicit_issue_374_owner_gate_pass_plus_native_authorization",
            }
        )
        dependencies.append(
            {
                "dependency_id": "issue-374-gate-sync",
                "class": "HARD",
                "status": "PASS_PENDING_GATE_SYNC",
                "basis": "latest candidate authority is PASS while latest #374 gate decision is not PASS",
                "counterfactual": "explicit #374 PASS resolves gate synchronization",
            }
        )
        triggers.append(
            {
                "trigger_id": "issue-374-owner-pass",
                "trigger_type": "human_owner_acceptance",
                "status": "waiting_for_gate_sync",
                "consequence": "record explicit #374 gate PASS then recompute",
            }
        )

    else:
        dependencies.append(
            {
                "dependency_id": "native-post-acceptance-authorization",
                "class": "HARD",
                "status": "OWNER_GATE_ACCEPTED__EXECUTION_NOT_GRANTED_BY_CPI",
                "basis": "latest #374 gate authority is PASS",
                "counterfactual": "CPI acceptance alone cannot execute D-E or other project effects",
            }
        )
        triggers.append(
            {
                "trigger_id": "native-post-acceptance-authorization",
                "trigger_type": "project_local_authorization",
                "status": "required_for_external_effect",
                "consequence": "native project decides any post-acceptance execution",
            }
        )

    p: Dict[str, Any] = {
        "profile_version": PROFILE_VERSION,
        "producer": ADAPTER_VERSION,
        "observed_at": observation["capture_cutoff"],
        "observation": dict(observation),
        "project_id": "HIVenues",
        "projection_id": (
            f"HIVenues:{main['commit'][:12]}:pr{current_number}:"
            f"stable:{observation['stable_digest'][:12]}"
        ),
        "observed_sources": observed_sources,
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
                "purpose": "stage5_owner_acceptance_gate",
                "source_id": "issue374",
                "authority_scope": "final_owner_acceptance_gate",
            },
            {
                "purpose": "stage5d_current_candidate",
                "source_id": f"pr{current_number}",
                "authority_scope": "candidate_only",
            },
        ],
        "material_objects": [
            {
                "object_id": "STABILIZED-NATIVE-SOURCE-SET",
                "role": "native_enumeration_result",
                "status": "stable_across_two_consecutive_complete_native_sweeps",
                "members": bundle["open_pr_numbers"],
                "stable_digest": observation["stable_digest"],
            },
            {
                "object_id": f"PR-{current_number}",
                "role": "current_candidate",
                "status": reduced["state"],
            },
            {
                "object_id": "OWNER-AUTHORITY-HISTORY",
                "role": "temporally_ordered_owner_authority",
                "status": reduced["owner_result"],
                "events": events,
                "gate_latest": reduced["gate_latest"],
                "candidate_latest": reduced["candidate_latest"],
                "latest_overall": reduced["latest_overall"],
            },
        ],
        "negative_knowledge": negative_knowledge,
        "dependencies": dependencies,
        "triggers": triggers,
        "transitions": [
            {
                "transition_id": "stage5d-current-candidate",
                "state": reduced["state"],
                "consequence_class": "product_canonicalization",
                "owner_result": reduced["owner_result"],
                "d_e_authorized_by_cpi": False,
                "next_action": reduced["next_action"],
            }
        ],
    }

    validate_projection(p)
    return p


def adapt_hivenues_current(
    token: str | None = None,
    max_sweeps: int = 4,
) -> Dict[str, Any]:
    bundle = collect_hivenues_current(token=token, max_sweeps=max_sweeps)
    return _adapt_hivenues_bundle(bundle, require_authoritative=True)


def _adapt_hivenues_bundle_for_test(
    bundle: Mapping[str, Any],
) -> Dict[str, Any]:
    return _adapt_hivenues_bundle(bundle, require_authoritative=False)
