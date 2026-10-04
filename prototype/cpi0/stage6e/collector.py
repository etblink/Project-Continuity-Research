from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping


class CollectorError(RuntimeError):
    pass


HERE = Path(__file__).resolve().parent


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json_bytes(obj: Any) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _git_blob_sha(data: bytes) -> str:
    prefix = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(prefix + data).hexdigest()


def load_manifest() -> Mapping[str, Any]:
    return _read_json(HERE / "native" / "NATIVE_SOURCE_MANIFEST.json")


def collect_git_source(key: str, source_id: str, role: str) -> Dict[str, Any]:
    manifest = load_manifest()
    try:
        spec = manifest["git_sources"][key]
    except KeyError as exc:
        raise CollectorError(f"unknown Git source contract: {key}") from exc

    mirror = HERE / spec["mirror"]
    if not mirror.exists():
        raise CollectorError(f"{key}: native mirror missing")

    data = mirror.read_bytes()
    actual_blob = _git_blob_sha(data)
    expected_blob = spec["blob_sha"]
    if actual_blob != expected_blob:
        raise CollectorError(
            f"{key}: mirror does not match declared native Git blob "
            f"{expected_blob}; got {actual_blob}"
        )

    digest = _sha256_bytes(data)
    commit = spec.get("commit")
    if not commit:
        raise CollectorError(f"{key}: Git source missing commit identity")

    return {
        "source_id": source_id,
        "repository": spec["repository"],
        "ref": spec["ref"],
        "role": role,
        "source_kind": "git",
        "native_id": f"git:{spec['repository']}:{spec['path']}@{commit}",
        "content_sha256": digest,
        "revision": f"git:{commit}:blob:{expected_blob}:sha256:{digest}",
        "commit": commit,
        "path": spec["path"],
        "blob_sha": expected_blob,
        "_content": data.decode("utf-8"),
    }


def collect_git_blob_only(key: str) -> Dict[str, Any]:
    """Verify a mirrored Git file even when it is used outside a CPI projection."""
    manifest = load_manifest()
    spec = manifest["git_sources"][key]
    data = (HERE / spec["mirror"]).read_bytes()
    actual_blob = _git_blob_sha(data)
    if actual_blob != spec["blob_sha"]:
        raise CollectorError(
            f"{key}: mirror does not match declared native Git blob"
        )
    return {
        "spec": dict(spec),
        "content": data.decode("utf-8"),
        "content_sha256": _sha256_bytes(data),
        "blob_sha": actual_blob,
    }


def _issue_source(
    obj: Mapping[str, Any], source_id: str, role: str
) -> Dict[str, Any]:
    digest = _sha256_bytes(_canonical_json_bytes(obj))
    number = int(obj["number"])
    updated_at = obj["updated_at"]
    repo = "etblink/HiVenues"
    return {
        "source_id": source_id,
        "repository": repo,
        "ref": f"issue-{number}",
        "role": role,
        "source_kind": "github_issue",
        "native_id": f"issue:{number}",
        "content_sha256": digest,
        "revision": (
            f"github_issue:{number}:updated_at:{updated_at}:sha256:{digest}"
        ),
        "issue_number": number,
        "updated_at": updated_at,
        "_object": dict(obj),
    }


def _comment_source(
    obj: Mapping[str, Any],
    issue_number: int,
    source_id: str,
    role: str,
) -> Dict[str, Any]:
    digest = _sha256_bytes(_canonical_json_bytes(obj))
    comment_id = int(obj["id"])
    updated_at = obj["updated_at"]
    association = obj.get("author_association") or ""
    return {
        "source_id": source_id,
        "repository": "etblink/HiVenues",
        "ref": f"issue-{issue_number}-comment-{comment_id}",
        "role": role,
        "source_kind": "github_issue_comment",
        "native_id": f"issue_comment:{comment_id}",
        "content_sha256": digest,
        "revision": (
            f"github_issue_comment:{comment_id}:issue:{issue_number}:"
            f"updated_at:{updated_at}:sha256:{digest}"
        ),
        "comment_id": comment_id,
        "issue_number": int(issue_number),
        "updated_at": updated_at,
        "author_association": association,
        "_object": dict(obj),
    }


def _pr_source(
    obj: Mapping[str, Any], source_id: str, role: str
) -> Dict[str, Any]:
    digest = _sha256_bytes(_canonical_json_bytes(obj))
    number = int(obj["number"])
    head_sha = obj["head"]["sha"]
    base_sha = obj["base"]["sha"]
    state = obj["state"]
    draft = bool(obj["draft"])
    updated_at = obj["updated_at"]
    draft_token = "true" if draft else "false"
    return {
        "source_id": source_id,
        "repository": "etblink/HiVenues",
        "ref": f"PR-{number}",
        "role": role,
        "source_kind": "github_pull_request",
        "native_id": f"pull_request:{number}",
        "content_sha256": digest,
        "revision": (
            f"github_pull_request:{number}:head:{head_sha}:base:{base_sha}:"
            f"state:{state}:draft:{draft_token}:updated_at:{updated_at}:"
            f"sha256:{digest}"
        ),
        "pr_number": number,
        "head_sha": head_sha,
        "base_sha": base_sha,
        "state": state,
        "draft": draft,
        "updated_at": updated_at,
        "_object": dict(obj),
    }


def _public_source(source: Mapping[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in source.items() if not k.startswith("_")}


def public_source(source: Mapping[str, Any]) -> Dict[str, Any]:
    return _public_source(source)


def collect_hivenues() -> Dict[str, Any]:
    manifest = load_manifest()
    contract = manifest["completeness_contract"]
    core = _read_json(HERE / manifest["github_sources"]["hivenues_core_snapshot"])
    prs = _read_json(HERE / manifest["github_sources"]["hivenues_pr_snapshot"])
    aux = _read_json(HERE / manifest["github_sources"]["hivenues_pr_aux_snapshot"])

    if not core["discovery"]["open_prs"]["page2_empty"]:
        raise CollectorError("HiVenues: open-PR enumeration incomplete")
    if not core["discovery"]["issue398_comments"]["page2_empty"]:
        raise CollectorError("HiVenues: Issue #398 comments incomplete")
    if not core["discovery"]["issue374_comments"]["page2_empty"]:
        raise CollectorError("HiVenues: Issue #374 comments incomplete")

    open_numbers = sorted(core["discovery"]["open_prs"]["discovered_numbers"])
    actual_open_numbers = sorted(x["number"] for x in core["objects"]["open_pull_requests"])
    if open_numbers != actual_open_numbers:
        raise CollectorError("HiVenues: open-PR discovery/object mismatch")

    expected = sorted(contract["expected_frozen_open_pr_numbers"])
    if open_numbers != expected:
        raise CollectorError(
            f"HiVenues: frozen open-PR set mismatch; expected {expected}, got {open_numbers}"
        )

    issue398_ids = core["discovery"]["issue398_comments"]["discovered_ids"]
    actual_issue398_ids = [x["id"] for x in core["objects"]["issue398_comments"]]
    if issue398_ids != actual_issue398_ids:
        raise CollectorError("HiVenues: Issue #398 discovery/object mismatch")
    if issue398_ids != contract["expected_frozen_issue398_comment_ids"]:
        raise CollectorError("HiVenues: Issue #398 comment set mismatch")

    issue374_ids = core["discovery"]["issue374_comments"]["discovered_ids"]
    actual_issue374_ids = [x["id"] for x in core["objects"]["issue374_comments"]]
    if issue374_ids != actual_issue374_ids:
        raise CollectorError("HiVenues: Issue #374 discovery/object mismatch")

    detail_map = {
        397: prs["objects"]["pr397"],
        399: prs["objects"]["pr399"],
    }
    for number in open_numbers:
        if number not in detail_map:
            raise CollectorError(f"HiVenues: missing full PR object #{number}")
        listed = next(
            x for x in core["objects"]["open_pull_requests"] if x["number"] == number
        )
        detail = detail_map[number]
        if listed["head"]["sha"] != detail["head"]["sha"]:
            raise CollectorError(f"HiVenues: PR #{number} head mismatch")
        if listed["state"] != detail["state"] or bool(listed["draft"]) != bool(detail["draft"]):
            raise CollectorError(f"HiVenues: PR #{number} state mismatch")

    for number in open_numbers:
        name = f"pr{number}_issue_comments"
        disc = prs["discovery"][name]
        if not disc["page2_empty"]:
            raise CollectorError(f"HiVenues: PR #{number} conversation comments incomplete")
        raw_issue_comments = prs["objects"][f"pr{number}_issue_comments"]
        if disc["page1_count"] != len(raw_issue_comments):
            raise CollectorError(f"HiVenues: PR #{number} conversation comment count mismatch")
        if disc["discovered_ids"] != [x["id"] for x in raw_issue_comments]:
            raise CollectorError(f"HiVenues: PR #{number} conversation comment ID mismatch")

        reviews = prs["discovery"][f"pr{number}_reviews"]
        if not aux["discovery"][f"pr{number}_reviews"]["page2_empty"]:
            raise CollectorError(f"HiVenues: PR #{number} reviews incomplete")
        if reviews["page1_count"] != len(prs["objects"][f"pr{number}_reviews"]):
            raise CollectorError(f"HiVenues: PR #{number} review count mismatch")
        if reviews["discovered_ids"] != [x["id"] for x in prs["objects"][f"pr{number}_reviews"]]:
            raise CollectorError(f"HiVenues: PR #{number} review ID mismatch")

        inline = aux["discovery"][f"pr{number}_inline_comments"]
        if not inline["page2_empty"]:
            raise CollectorError(f"HiVenues: PR #{number} inline comments incomplete")
        raw_inline = aux["objects"][f"pr{number}_inline_comments"]
        if inline["page1_count"] != len(raw_inline):
            raise CollectorError(f"HiVenues: PR #{number} inline comment count mismatch")
        if inline["discovered_ids"] != [x["id"] for x in raw_inline]:
            raise CollectorError(f"HiVenues: PR #{number} inline comment ID mismatch")

        threads = aux["objects"][f"pr{number}_review_threads"]
        if aux["discovery"][f"pr{number}_review_threads"]["count"] != len(threads):
            raise CollectorError(f"HiVenues: PR #{number} review-thread count mismatch")

    pr399_comment_ids = prs["discovery"]["pr399_issue_comments"]["discovered_ids"]
    if pr399_comment_ids != contract["expected_frozen_pr399_conversation_comment_ids"]:
        raise CollectorError("HiVenues: PR #399 comment set mismatch")

    issue398 = _issue_source(
        core["objects"]["issue398"],
        "issue398",
        "active_bounded_work_charter",
    )

    issue398_comments = [
        _comment_source(
            x,
            398,
            f"issue398-comment-{x['id']}",
            "governing_issue_conversation_comment",
        )
        for x in core["objects"]["issue398_comments"]
    ]

    issue374 = _issue_source(
        core["objects"]["issue374"],
        "issue374",
        "usability_gate_charter",
    )

    pr_sources = {
        number: _pr_source(
            detail_map[number],
            f"pr{number}",
            "open_pull_request_candidate",
        )
        for number in open_numbers
    }

    pr_comment_sources: Dict[int, list[Dict[str, Any]]] = {}
    for number in open_numbers:
        raw = prs["objects"][f"pr{number}_issue_comments"]
        pr_comment_sources[number] = [
            _comment_source(
                x,
                number,
                f"pr{number}-comment-{x['id']}",
                "pull_request_conversation_comment",
            )
            for x in raw
        ]

    return {
        "observed_at": manifest["observed_at"],
        "discovery": {
            "open_pr_numbers": open_numbers,
            "issue398_comment_ids": issue398_ids,
            "pr399_comment_ids": pr399_comment_ids,
            "complete": True,
            "core": core["discovery"],
            "prs": prs["discovery"],
            "aux": aux["discovery"],
        },
        "issue398": issue398,
        "issue398_comments": issue398_comments,
        "issue374": issue374,
        "pr_sources": pr_sources,
        "pr_comment_sources": pr_comment_sources,
        "raw": {
            "core": core,
            "prs": prs,
            "aux": aux,
        },
    }


def strip_private_fields(source: Mapping[str, Any]) -> Dict[str, Any]:
    return _public_source(source)
