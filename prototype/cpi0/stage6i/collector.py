from __future__ import annotations

import hashlib
import json
import os
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Tuple


class CollectorError(RuntimeError):
    pass


REPOSITORY = "etblink/HiVenues"


def _utcnow() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _canonical_json_bytes(obj: Any) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _sha256_json(obj: Any) -> str:
    return hashlib.sha256(_canonical_json_bytes(obj)).hexdigest()


def _sorted_rows(rows: List[Mapping[str, Any]]) -> List[Mapping[str, Any]]:
    def key(row: Mapping[str, Any]):
        value = row.get("number", row.get("id"))
        return (0, int(value)) if isinstance(value, int) else (1, str(value))

    return sorted(rows, key=key)


class _GitHubRestTransport:
    """Raw GitHub JSON transport used only by the production collector."""

    def __init__(self, token: str | None = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")

    def get_json(self, url: str) -> Any:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "cpi0-stage6i-native-collector",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))


def _page_ids(rows: List[Mapping[str, Any]]) -> List[Any]:
    return [row.get("id", row.get("number")) for row in rows]


def _enumerate_pages(
    transport: Any,
    repository: str,
    endpoint: str,
) -> Tuple[List[Mapping[str, Any]], Dict[str, Any]]:
    rows_all: List[Mapping[str, Any]] = []
    pages: List[Dict[str, Any]] = []
    page = 1

    while True:
        separator = "&" if "?" in endpoint else "?"
        url = (
            f"https://api.github.com/repos/{repository}/{endpoint}"
            f"{separator}per_page=100&page={page}"
        )
        rows = transport.get_json(url)
        if not isinstance(rows, list):
            raise CollectorError(f"{endpoint}: expected list response")

        typed = [x for x in rows if isinstance(x, Mapping)]
        if len(typed) != len(rows):
            raise CollectorError(f"{endpoint}: non-object row returned")

        page_record = {
            "page": page,
            "endpoint": endpoint,
            "url": url,
            "count": len(typed),
            "ids": _page_ids(typed),
            "page_sha256": _sha256_json(typed),
        }
        pages.append(page_record)

        if len(typed) == 0:
            break

        rows_all.extend(typed)
        page += 1
        if page > 1000:
            raise CollectorError(f"{endpoint}: pagination guard exceeded")

    return _sorted_rows(rows_all), {
        "repository": repository,
        "endpoint": endpoint,
        "pages": pages,
        "termination": "empty_page",
        "terminal_page": page,
        "collector_generated": True,
    }


def _get_object(
    transport: Any,
    repository: str,
    endpoint: str,
) -> Mapping[str, Any]:
    url = f"https://api.github.com/repos/{repository}/{endpoint}"
    value = transport.get_json(url)
    if not isinstance(value, Mapping):
        raise CollectorError(f"{endpoint}: expected object response")
    return value


def _validate_receipt(
    receipt: Mapping[str, Any],
    repository: str,
    endpoint: str,
    rows: List[Mapping[str, Any]],
) -> None:
    if receipt.get("collector_generated") is not True:
        raise CollectorError(f"{endpoint}: receipt is not collector-generated")
    if receipt.get("repository") != repository:
        raise CollectorError(f"{endpoint}: receipt repository mismatch")
    if receipt.get("endpoint") != endpoint:
        raise CollectorError(f"{endpoint}: receipt endpoint mismatch")
    if receipt.get("termination") != "empty_page":
        raise CollectorError(f"{endpoint}: enumeration not exhausted")

    pages = receipt.get("pages")
    if not isinstance(pages, list) or not pages:
        raise CollectorError(f"{endpoint}: receipt pages missing")
    if [p.get("page") for p in pages] != list(range(1, len(pages) + 1)):
        raise CollectorError(f"{endpoint}: noncontiguous page sequence")
    if pages[-1].get("count") != 0:
        raise CollectorError(f"{endpoint}: no empty terminal page")
    if receipt.get("terminal_page") != pages[-1].get("page"):
        raise CollectorError(f"{endpoint}: terminal page mismatch")

    flattened_ids: List[Any] = []
    total = 0
    for page in pages[:-1]:
        count = page.get("count")
        ids = page.get("ids")
        if not isinstance(count, int) or not isinstance(ids, list):
            raise CollectorError(f"{endpoint}: malformed page receipt")
        if count != len(ids):
            raise CollectorError(f"{endpoint}: page count/ID mismatch")
        total += count
        flattened_ids.extend(ids)

    if total != len(rows):
        raise CollectorError(f"{endpoint}: receipt row count mismatch")
    if flattened_ids != _page_ids(rows):
        raise CollectorError(f"{endpoint}: receipt IDs do not match returned rows")


def _single_sweep(transport: Any, repository: str) -> Dict[str, Any]:
    started_at = _utcnow()

    issue398 = _get_object(transport, repository, "issues/398")
    issue374 = _get_object(transport, repository, "issues/374")

    issue398_comments, r398 = _enumerate_pages(
        transport, repository, "issues/398/comments"
    )
    issue374_comments, r374 = _enumerate_pages(
        transport, repository, "issues/374/comments"
    )
    open_prs, ropen = _enumerate_pages(
        transport, repository, "pulls?state=open"
    )

    _validate_receipt(r398, repository, "issues/398/comments", issue398_comments)
    _validate_receipt(r374, repository, "issues/374/comments", issue374_comments)
    _validate_receipt(ropen, repository, "pulls?state=open", open_prs)

    pr_details: Dict[str, Mapping[str, Any]] = {}
    pr_comments: Dict[str, List[Mapping[str, Any]]] = {}
    pr_reviews: Dict[str, List[Mapping[str, Any]]] = {}
    pr_inline: Dict[str, List[Mapping[str, Any]]] = {}
    receipts: Dict[str, Any] = {
        "issue398_comments": r398,
        "issue374_comments": r374,
        "open_prs": ropen,
    }

    for listed in open_prs:
        number = int(listed["number"])
        key = str(number)
        detail = _get_object(transport, repository, f"pulls/{number}")
        if int(detail["number"]) != number:
            raise CollectorError(f"PR #{number}: detail identity mismatch")
        if listed["head"]["sha"] != detail["head"]["sha"]:
            raise CollectorError(f"PR #{number}: list/detail head mismatch")

        comments, rc = _enumerate_pages(
            transport, repository, f"issues/{number}/comments"
        )
        reviews, rr = _enumerate_pages(
            transport, repository, f"pulls/{number}/reviews"
        )
        inline, ri = _enumerate_pages(
            transport, repository, f"pulls/{number}/comments"
        )

        _validate_receipt(rc, repository, f"issues/{number}/comments", comments)
        _validate_receipt(rr, repository, f"pulls/{number}/reviews", reviews)
        _validate_receipt(ri, repository, f"pulls/{number}/comments", inline)

        pr_details[key] = detail
        pr_comments[key] = comments
        pr_reviews[key] = reviews
        pr_inline[key] = inline
        receipts[f"pr{number}_comments"] = rc
        receipts[f"pr{number}_reviews"] = rr
        receipts[f"pr{number}_inline_comments"] = ri

    raw_source_set = {
        "issue398": issue398,
        "issue398_comments": issue398_comments,
        "issue374": issue374,
        "issue374_comments": issue374_comments,
        "open_prs": open_prs,
        "pr_details": pr_details,
        "pr_comments": pr_comments,
        "pr_reviews": pr_reviews,
        "pr_inline_comments": pr_inline,
    }
    digest = _sha256_json(raw_source_set)
    ended_at = _utcnow()

    return {
        "repository": repository,
        "started_at": started_at,
        "ended_at": ended_at,
        "digest": digest,
        "receipts": receipts,
        "raw_source_set": raw_source_set,
    }


def _issue_source(
    repository: str,
    obj: Mapping[str, Any],
    source_id: str,
    role: str,
) -> Dict[str, Any]:
    digest = _sha256_json(obj)
    number = int(obj["number"])
    updated = obj["updated_at"]
    return {
        "source_id": source_id,
        "repository": repository,
        "ref": f"issue-{number}",
        "role": role,
        "source_kind": "github_issue",
        "native_id": f"github_issue:{repository}:{number}",
        "content_sha256": digest,
        "revision": (
            f"github_issue:{repository}:{number}:updated_at:{updated}:sha256:{digest}"
        ),
        "issue_number": number,
        "updated_at": updated,
        "_object": dict(obj),
    }


def _comment_source(
    repository: str,
    obj: Mapping[str, Any],
    issue_number: int,
    source_id: str,
    role: str,
) -> Dict[str, Any]:
    digest = _sha256_json(obj)
    comment_id = int(obj["id"])
    updated = obj["updated_at"]
    return {
        "source_id": source_id,
        "repository": repository,
        "ref": f"issue-{issue_number}-comment-{comment_id}",
        "role": role,
        "source_kind": "github_issue_comment",
        "native_id": f"github_issue_comment:{repository}:{comment_id}",
        "content_sha256": digest,
        "revision": (
            f"github_issue_comment:{repository}:{comment_id}:issue:{issue_number}:"
            f"updated_at:{updated}:sha256:{digest}"
        ),
        "comment_id": comment_id,
        "issue_number": int(issue_number),
        "updated_at": updated,
        "author_association": obj.get("author_association") or "",
        "_object": dict(obj),
    }


def _pr_source(
    repository: str,
    obj: Mapping[str, Any],
    source_id: str,
    role: str,
) -> Dict[str, Any]:
    digest = _sha256_json(obj)
    number = int(obj["number"])
    head = obj["head"]["sha"]
    base = obj["base"]["sha"]
    state = obj["state"]
    draft = bool(obj["draft"])
    updated = obj["updated_at"]
    draft_token = "true" if draft else "false"
    return {
        "source_id": source_id,
        "repository": repository,
        "ref": f"PR-{number}",
        "role": role,
        "source_kind": "github_pull_request",
        "native_id": f"github_pull_request:{repository}:{number}",
        "content_sha256": digest,
        "revision": (
            f"github_pull_request:{repository}:{number}:head:{head}:base:{base}:"
            f"state:{state}:draft:{draft_token}:updated_at:{updated}:sha256:{digest}"
        ),
        "pr_number": number,
        "head_sha": head,
        "base_sha": base,
        "state": state,
        "draft": draft,
        "updated_at": updated,
        "_object": dict(obj),
    }


def _review_source(
    repository: str,
    obj: Mapping[str, Any],
    pr_number: int,
) -> Dict[str, Any]:
    digest = _sha256_json(obj)
    review_id = int(obj["id"])
    commit_id = obj["commit_id"]
    state = obj["state"]
    submitted = obj["submitted_at"]
    return {
        "source_id": f"pr{pr_number}-review-{review_id}",
        "repository": repository,
        "ref": f"PR-{pr_number}-review-{review_id}",
        "role": "pull_request_review",
        "source_kind": "github_pull_request_review",
        "native_id": f"github_pull_request_review:{repository}:{review_id}",
        "content_sha256": digest,
        "revision": (
            f"github_pull_request_review:{repository}:{review_id}:pr:{pr_number}:"
            f"state:{state}:submitted_at:{submitted}:commit:{commit_id}:"
            f"sha256:{digest}"
        ),
        "review_id": review_id,
        "pr_number": int(pr_number),
        "state": state,
        "submitted_at": submitted,
        "commit_id": commit_id,
        "author_association": obj.get("author_association") or "",
        "_object": dict(obj),
    }


def _inline_review_comment_source(
    repository: str,
    obj: Mapping[str, Any],
    pr_number: int,
) -> Dict[str, Any]:
    digest = _sha256_json(obj)
    comment_id = int(obj["id"])
    review_id = int(obj["pull_request_review_id"])
    updated = obj["updated_at"]
    commit_id = obj["commit_id"]
    return {
        "source_id": f"pr{pr_number}-review-comment-{comment_id}",
        "repository": repository,
        "ref": f"PR-{pr_number}-review-comment-{comment_id}",
        "role": "pull_request_review_comment",
        "source_kind": "github_pull_request_review_comment",
        "native_id": (
            f"github_pull_request_review_comment:{repository}:{comment_id}"
        ),
        "content_sha256": digest,
        "revision": (
            f"github_pull_request_review_comment:{repository}:{comment_id}:"
            f"pr:{pr_number}:review:{review_id}:updated_at:{updated}:"
            f"commit:{commit_id}:sha256:{digest}"
        ),
        "comment_id": comment_id,
        "pr_number": int(pr_number),
        "pull_request_review_id": review_id,
        "updated_at": updated,
        "commit_id": commit_id,
        "author_association": obj.get("author_association") or "",
        "_object": dict(obj),
    }


def public_source(source: Mapping[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in source.items() if not k.startswith("_")}


def _materialize_stable_bundle(
    previous: Mapping[str, Any],
    current: Mapping[str, Any],
    authoritative: bool,
) -> Dict[str, Any]:
    raw = current["raw_source_set"]
    repository = current["repository"]

    issue398 = _issue_source(
        repository, raw["issue398"], "issue398", "active_bounded_work_charter"
    )
    issue374 = _issue_source(
        repository, raw["issue374"], "issue374", "usability_gate_charter"
    )

    issue398_comments = [
        _comment_source(
            repository,
            obj,
            398,
            f"issue398-comment-{obj['id']}",
            "governing_issue_conversation_comment",
        )
        for obj in raw["issue398_comments"]
    ]
    issue374_comments = [
        _comment_source(
            repository,
            obj,
            374,
            f"issue374-comment-{obj['id']}",
            "usability_gate_conversation_comment",
        )
        for obj in raw["issue374_comments"]
    ]

    pr_sources: Dict[int, Dict[str, Any]] = {}
    pr_comments: Dict[int, List[Dict[str, Any]]] = {}
    pr_reviews: Dict[int, List[Dict[str, Any]]] = {}
    pr_inline: Dict[int, List[Dict[str, Any]]] = {}

    for key, detail in raw["pr_details"].items():
        number = int(key)
        pr_sources[number] = _pr_source(
            repository, detail, f"pr{number}", "open_pull_request_candidate"
        )
        pr_comments[number] = [
            _comment_source(
                repository,
                obj,
                number,
                f"pr{number}-comment-{obj['id']}",
                "pull_request_conversation_comment",
            )
            for obj in raw["pr_comments"][key]
        ]
        pr_reviews[number] = [
            _review_source(repository, obj, number)
            for obj in raw["pr_reviews"][key]
        ]
        pr_inline[number] = [
            _inline_review_comment_source(repository, obj, number)
            for obj in raw["pr_inline_comments"][key]
        ]

    return {
        "authoritative": authoritative,
        "repository": repository,
        "observation": {
            "mode": "stabilized_native_window",
            "repository": repository,
            "window_start": previous["started_at"],
            "window_end": current["ended_at"],
            "stable_digest": current["digest"],
            "consecutive_equal_sweeps": 2,
        },
        "stabilization": {
            "previous_digest": previous["digest"],
            "current_digest": current["digest"],
            "previous_receipts": previous["receipts"],
            "current_receipts": current["receipts"],
        },
        "open_pr_numbers": sorted(pr_sources),
        "issue398": issue398,
        "issue398_comments": issue398_comments,
        "issue374": issue374,
        "issue374_comments": issue374_comments,
        "pr_sources": pr_sources,
        "pr_comment_sources": pr_comments,
        "pr_review_sources": pr_reviews,
        "pr_inline_review_comment_sources": pr_inline,
    }


def _stabilize_with_transport(
    transport: Any,
    repository: str,
    max_sweeps: int,
    authoritative: bool,
) -> Dict[str, Any]:
    if max_sweeps < 2:
        raise CollectorError("max_sweeps must be at least 2")

    previous = None
    for _ in range(max_sweeps):
        current = _single_sweep(transport, repository)
        if previous is not None and current["digest"] == previous["digest"]:
            return _materialize_stable_bundle(
                previous, current, authoritative=authoritative
            )
        previous = current

    raise CollectorError(
        "current native state did not stabilize across two consecutive complete sweeps"
    )


def collect_hivenues_current(
    token: str | None = None,
    max_sweeps: int = 4,
) -> Dict[str, Any]:
    """Production current-state collector.

    No caller-supplied reader or receipt object is accepted.
    """
    transport = _GitHubRestTransport(token=token)
    return _stabilize_with_transport(
        transport,
        REPOSITORY,
        max_sweeps=max_sweeps,
        authoritative=True,
    )


def _collect_hivenues_with_transport_for_test(
    transport: Any,
    max_sweeps: int = 4,
) -> Dict[str, Any]:
    """Internal deterministic test seam.

    Results from this path can never establish current authority.
    """
    return _stabilize_with_transport(
        transport,
        REPOSITORY,
        max_sweeps=max_sweeps,
        authoritative=False,
    )
