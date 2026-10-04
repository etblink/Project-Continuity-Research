from __future__ import annotations

import hashlib
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Protocol, Tuple


class CollectorError(RuntimeError):
    pass


REPOSITORY = "etblink/HiVenues"
HERE = Path(__file__).resolve().parent


def _sha256_json(obj: Any) -> str:
    data = json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


class NativeReader(Protocol):
    mode: str

    def observed_at(self) -> str: ...
    def get_issue(self, repository: str, number: int) -> Mapping[str, Any]: ...
    def list_issue_comments(
        self, repository: str, number: int
    ) -> Tuple[List[Mapping[str, Any]], Mapping[str, Any]]: ...
    def list_open_prs(
        self, repository: str
    ) -> Tuple[List[Mapping[str, Any]], Mapping[str, Any]]: ...
    def get_pr(self, repository: str, number: int) -> Mapping[str, Any]: ...
    def list_pr_reviews(
        self, repository: str, number: int
    ) -> Tuple[List[Mapping[str, Any]], Mapping[str, Any]]: ...
    def list_pr_inline_comments(
        self, repository: str, number: int
    ) -> Tuple[List[Mapping[str, Any]], Mapping[str, Any]]: ...


class GitHubRestReader:
    """Direct native GitHub REST reader.

    Current completeness claims are permitted only from this/native-direct mode
    (or another reader that truthfully exposes mode='native_direct').
    """

    mode = "native_direct"

    def __init__(self, token: str | None = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")

    def observed_at(self) -> str:
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    def _get(self, url: str) -> Any:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "cpi0-stage6g-native-reader",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _pages(
        self, repository: str, endpoint: str
    ) -> Tuple[List[Mapping[str, Any]], Mapping[str, Any]]:
        objects: List[Mapping[str, Any]] = []
        pages: List[Dict[str, Any]] = []
        page = 1
        while True:
            sep = "&" if "?" in endpoint else "?"
            url = (
                f"https://api.github.com/repos/{repository}/{endpoint}"
                f"{sep}per_page=100&page={page}"
            )
            rows = self._get(url)
            if not isinstance(rows, list):
                raise CollectorError(f"native enumeration returned non-list for {endpoint}")
            ids = [
                row.get("id", row.get("number"))
                for row in rows
                if isinstance(row, Mapping)
            ]
            pages.append(
                {
                    "page": page,
                    "url": url,
                    "count": len(rows),
                    "ids": ids,
                }
            )
            if len(rows) == 0:
                break
            objects.extend(rows)
            page += 1
            if page > 1000:
                raise CollectorError("pagination guard exceeded")
        return objects, {
            "mode": self.mode,
            "repository": repository,
            "endpoint": endpoint,
            "pages": pages,
            "termination": "empty_page",
            "terminal_page": page,
        }

    def get_issue(self, repository: str, number: int) -> Mapping[str, Any]:
        return self._get(f"https://api.github.com/repos/{repository}/issues/{number}")

    def list_issue_comments(self, repository: str, number: int):
        return self._pages(repository, f"issues/{number}/comments")

    def list_open_prs(self, repository: str):
        return self._pages(repository, "pulls?state=open")

    def get_pr(self, repository: str, number: int) -> Mapping[str, Any]:
        return self._get(f"https://api.github.com/repos/{repository}/pulls/{number}")

    def list_pr_reviews(self, repository: str, number: int):
        return self._pages(repository, f"pulls/{number}/reviews")

    def list_pr_inline_comments(self, repository: str, number: int):
        return self._pages(repository, f"pulls/{number}/comments")


class FrozenFixtureReader:
    """Deterministic Stage-6E fixture.

    It is intentionally not eligible to establish present-tense completeness.
    """

    mode = "fixture"

    def __init__(self):
        base = HERE.parent / "stage6e" / "native"
        self.core = json.loads(
            (base / "HIVENUES_GITHUB_NATIVE_CORE.json").read_text(encoding="utf-8")
        )
        self.prs = json.loads(
            (base / "HIVENUES_GITHUB_NATIVE_PRS.json").read_text(encoding="utf-8")
        )
        self.aux = json.loads(
            (base / "HIVENUES_GITHUB_NATIVE_PR_AUX.json").read_text(encoding="utf-8")
        )

    def observed_at(self) -> str:
        return "2026-10-04T19:50:00Z"

    def _receipt(self, endpoint: str, rows: List[Mapping[str, Any]]) -> Mapping[str, Any]:
        return {
            "mode": self.mode,
            "repository": REPOSITORY,
            "endpoint": endpoint,
            "pages": [{"page": 1, "count": len(rows), "ids": [x.get("id", x.get("number")) for x in rows]}],
            "termination": "fixture_snapshot",
        }

    def get_issue(self, repository: str, number: int):
        if repository != REPOSITORY:
            raise CollectorError("fixture repository mismatch")
        key = f"issue{number}"
        if key not in self.core["objects"]:
            raise CollectorError(f"fixture issue #{number} unavailable")
        return self.core["objects"][key]

    def list_issue_comments(self, repository: str, number: int):
        if repository != REPOSITORY:
            raise CollectorError("fixture repository mismatch")
        key = f"issue{number}_comments"
        rows = self.core["objects"].get(key, [])
        return rows, self._receipt(f"issues/{number}/comments", rows)

    def list_open_prs(self, repository: str):
        if repository != REPOSITORY:
            raise CollectorError("fixture repository mismatch")
        rows = self.core["objects"]["open_pull_requests"]
        return rows, self._receipt("pulls?state=open", rows)

    def get_pr(self, repository: str, number: int):
        if repository != REPOSITORY:
            raise CollectorError("fixture repository mismatch")
        return self.prs["objects"][f"pr{number}"]

    def list_pr_reviews(self, repository: str, number: int):
        rows = self.prs["objects"][f"pr{number}_reviews"]
        return rows, self._receipt(f"pulls/{number}/reviews", rows)

    def list_pr_inline_comments(self, repository: str, number: int):
        rows = self.aux["objects"][f"pr{number}_inline_comments"]
        return rows, self._receipt(f"pulls/{number}/comments", rows)


def _require_native_receipt(receipt: Mapping[str, Any], repository: str) -> None:
    if receipt.get("mode") != "native_direct":
        raise CollectorError("current completeness requires native_direct enumeration")
    if receipt.get("repository") != repository:
        raise CollectorError("enumeration receipt repository mismatch")
    if receipt.get("termination") != "empty_page":
        raise CollectorError("native enumeration did not terminate at an empty page")
    pages = receipt.get("pages")
    if not isinstance(pages, list) or not pages:
        raise CollectorError("native enumeration receipt missing pages")
    terminal = pages[-1]
    if terminal.get("count") != 0:
        raise CollectorError("native enumeration receipt lacks empty terminal page")
    expected = list(range(1, len(pages) + 1))
    actual = [p.get("page") for p in pages]
    if actual != expected:
        raise CollectorError("native enumeration page sequence is not contiguous")


def _issue_source(repository: str, obj: Mapping[str, Any], source_id: str, role: str):
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
        "revision": f"github_issue:{repository}:{number}:updated_at:{updated}:sha256:{digest}",
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
):
    digest = _sha256_json(obj)
    cid = int(obj["id"])
    updated = obj["updated_at"]
    return {
        "source_id": source_id,
        "repository": repository,
        "ref": f"issue-{issue_number}-comment-{cid}",
        "role": role,
        "source_kind": "github_issue_comment",
        "native_id": f"github_issue_comment:{repository}:{cid}",
        "content_sha256": digest,
        "revision": (
            f"github_issue_comment:{repository}:{cid}:issue:{issue_number}:"
            f"updated_at:{updated}:sha256:{digest}"
        ),
        "comment_id": cid,
        "issue_number": int(issue_number),
        "updated_at": updated,
        "author_association": obj.get("author_association") or "",
        "_object": dict(obj),
    }


def _pr_source(repository: str, obj: Mapping[str, Any], source_id: str, role: str):
    digest = _sha256_json(obj)
    number = int(obj["number"])
    head = obj["head"]["sha"]
    base = obj["base"]["sha"]
    state = obj["state"]
    draft = bool(obj["draft"])
    updated = obj["updated_at"]
    dt = "true" if draft else "false"
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
            f"state:{state}:draft:{dt}:updated_at:{updated}:sha256:{digest}"
        ),
        "pr_number": number,
        "head_sha": head,
        "base_sha": base,
        "state": state,
        "draft": draft,
        "updated_at": updated,
        "_object": dict(obj),
    }


def public_source(source: Mapping[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in source.items() if not k.startswith("_")}


def collect_hivenues_current(
    reader: NativeReader,
    repository: str = REPOSITORY,
) -> Dict[str, Any]:
    """Collect present-tense HiVenues authority from native GitHub.

    This function deliberately has no snapshot fallback.
    """
    if getattr(reader, "mode", None) != "native_direct":
        raise CollectorError("present-tense collection requires native_direct reader")

    issue398 = reader.get_issue(repository, 398)
    issue398_comments, issue398_receipt = reader.list_issue_comments(repository, 398)
    _require_native_receipt(issue398_receipt, repository)

    issue374 = reader.get_issue(repository, 374)
    issue374_comments, issue374_receipt = reader.list_issue_comments(repository, 374)
    _require_native_receipt(issue374_receipt, repository)

    listed_prs, open_pr_receipt = reader.list_open_prs(repository)
    _require_native_receipt(open_pr_receipt, repository)

    pr_numbers = sorted(int(x["number"]) for x in listed_prs)
    pr_sources: Dict[int, Dict[str, Any]] = {}
    pr_comment_sources: Dict[int, List[Dict[str, Any]]] = {}
    receipts: Dict[str, Any] = {
        "issue398_comments": issue398_receipt,
        "issue374_comments": issue374_receipt,
        "open_prs": open_pr_receipt,
    }

    for number in pr_numbers:
        pr = reader.get_pr(repository, number)
        if int(pr["number"]) != number:
            raise CollectorError(f"PR #{number} detail identity mismatch")
        listed = next(x for x in listed_prs if int(x["number"]) == number)
        if listed["head"]["sha"] != pr["head"]["sha"]:
            raise CollectorError(f"PR #{number} list/detail head mismatch")

        comments, comment_receipt = reader.list_issue_comments(repository, number)
        reviews, review_receipt = reader.list_pr_reviews(repository, number)
        inline, inline_receipt = reader.list_pr_inline_comments(repository, number)
        for receipt in [comment_receipt, review_receipt, inline_receipt]:
            _require_native_receipt(receipt, repository)

        receipts[f"pr{number}_comments"] = comment_receipt
        receipts[f"pr{number}_reviews"] = review_receipt
        receipts[f"pr{number}_inline_comments"] = inline_receipt

        pr_sources[number] = _pr_source(
            repository, pr, f"pr{number}", "open_pull_request_candidate"
        )
        pr_comment_sources[number] = [
            _comment_source(
                repository,
                x,
                number,
                f"pr{number}-comment-{x['id']}",
                "pull_request_conversation_comment",
            )
            for x in comments
        ]

    return {
        "mode": "native_direct",
        "observed_at": reader.observed_at(),
        "repository": repository,
        "receipts": receipts,
        "open_pr_numbers": pr_numbers,
        "issue398": _issue_source(
            repository, issue398, "issue398", "active_bounded_work_charter"
        ),
        "issue398_comments": [
            _comment_source(
                repository,
                x,
                398,
                f"issue398-comment-{x['id']}",
                "governing_issue_conversation_comment",
            )
            for x in issue398_comments
        ],
        "issue374": _issue_source(
            repository, issue374, "issue374", "usability_gate_charter"
        ),
        "issue374_comments": [
            _comment_source(
                repository,
                x,
                374,
                f"issue374-comment-{x['id']}",
                "usability_gate_conversation_comment",
            )
            for x in issue374_comments
        ],
        "pr_sources": pr_sources,
        "pr_comment_sources": pr_comment_sources,
    }


def collect_hivenues_fixture() -> Dict[str, Any]:
    """Expose frozen Stage-6E material only as non-authoritative fixture evidence."""
    reader = FrozenFixtureReader()
    return {
        "mode": reader.mode,
        "repository": REPOSITORY,
        "observed_at": reader.observed_at(),
        "current_completeness_authorized": False,
    }
