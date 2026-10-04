from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Mapping


class CPIValidationError(ValueError):
    pass


SUPPORTED_PROFILE_VERSION = "0.1.3"

ALLOWED_SOURCE_KINDS = {
    "git",
    "github_issue",
    "github_issue_comment",
    "github_pull_request",
    "derived_snapshot",
}

ALLOWED_DEPENDENCY_CLASSES = {"HARD", "SOFT", "CONTEXTUAL", "NONE", "UNKNOWN"}

ALLOWED_TRANSITION_STATES = {
    "selected_authorized",
    "selected_not_authorized",
    "blocked_external",
    "waiting_for_trigger",
    "held",
    "prohibited",
    "deferred",
    "complete_pending_acceptance",
    "none_selected",
    "rejected",
}

HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def _require(obj: Mapping[str, Any], keys: Iterable[str], where: str) -> None:
    missing = [key for key in keys if key not in obj]
    if missing:
        raise CPIValidationError(f"{where}: missing required fields: {', '.join(missing)}")


def _nonempty(value: Any, where: str) -> None:
    if value is None or value == "" or value == [] or value == {}:
        raise CPIValidationError(f"{where}: must be non-empty")


def _bool_token(value: bool) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    raise CPIValidationError("draft must be boolean")


def validate_source(source: Mapping[str, Any], where: str = "source") -> None:
    _require(
        source,
        [
            "source_id",
            "repository",
            "ref",
            "role",
            "source_kind",
            "native_id",
            "content_sha256",
            "revision",
        ],
        where,
    )
    repository = str(source["repository"])
    if not REPOSITORY.match(repository):
        raise CPIValidationError(f"{where}: repository must be normalized owner/name")

    kind = source["source_kind"]
    if kind not in ALLOWED_SOURCE_KINDS:
        raise CPIValidationError(f"{where}: unsupported source_kind {kind}")
    if not HEX64.match(str(source["content_sha256"])):
        raise CPIValidationError(f"{where}: content_sha256 must be 64 lowercase hex")

    digest = source["content_sha256"]

    if kind == "git":
        _require(source, ["commit", "path", "blob_sha"], where)
        commit = str(source["commit"])
        blob = str(source["blob_sha"])
        if not HEX40.match(commit) or not HEX40.match(blob):
            raise CPIValidationError(f"{where}: invalid Git commit/blob identity")
        expected_native = f"git:{repository}:{source['path']}@{commit}"
        expected_revision = f"git:{repository}:{commit}:blob:{blob}:sha256:{digest}"

    elif kind == "github_issue":
        _require(source, ["issue_number", "updated_at"], where)
        number = int(source["issue_number"])
        expected_native = f"github_issue:{repository}:{number}"
        expected_revision = (
            f"github_issue:{repository}:{number}:updated_at:{source['updated_at']}:"
            f"sha256:{digest}"
        )

    elif kind == "github_issue_comment":
        _require(
            source,
            ["comment_id", "issue_number", "updated_at", "author_association"],
            where,
        )
        comment = int(source["comment_id"])
        issue = int(source["issue_number"])
        expected_native = f"github_issue_comment:{repository}:{comment}"
        expected_revision = (
            f"github_issue_comment:{repository}:{comment}:issue:{issue}:"
            f"updated_at:{source['updated_at']}:sha256:{digest}"
        )

    elif kind == "github_pull_request":
        _require(
            source,
            [
                "pr_number",
                "head_sha",
                "base_sha",
                "state",
                "draft",
                "updated_at",
            ],
            where,
        )
        number = int(source["pr_number"])
        head = str(source["head_sha"])
        base = str(source["base_sha"])
        if not HEX40.match(head) or not HEX40.match(base):
            raise CPIValidationError(f"{where}: invalid PR head/base SHA")
        draft = _bool_token(source["draft"])
        expected_native = f"github_pull_request:{repository}:{number}"
        expected_revision = (
            f"github_pull_request:{repository}:{number}:head:{head}:base:{base}:"
            f"state:{source['state']}:draft:{draft}:updated_at:{source['updated_at']}:"
            f"sha256:{digest}"
        )

    else:
        _nonempty(source["native_id"], f"{where}.native_id")
        expected_native = str(source["native_id"])
        expected_revision = f"derived_snapshot:{repository}:{expected_native}:sha256:{digest}"

    if source["native_id"] != expected_native:
        raise CPIValidationError(
            f"{where}: native_id mismatch; expected {expected_native!r}"
        )
    if source["revision"] != expected_revision:
        raise CPIValidationError(
            f"{where}: revision does not match repository/source/content fields"
        )


def validate_projection(projection: Mapping[str, Any]) -> None:
    _require(
        projection,
        [
            "profile_version",
            "project_id",
            "projection_id",
            "producer",
            "observed_at",
            "observed_sources",
            "authority_map",
            "material_objects",
            "negative_knowledge",
            "dependencies",
            "triggers",
            "transitions",
        ],
        "projection",
    )
    if projection["profile_version"] != SUPPORTED_PROFILE_VERSION:
        raise CPIValidationError(
            f"projection: unsupported profile_version {projection['profile_version']}"
        )
    _nonempty(projection["producer"], "projection.producer")
    _nonempty(projection["observed_at"], "projection.observed_at")
    _nonempty(projection["observed_sources"], "projection.observed_sources")

    source_ids = set()
    for idx, source in enumerate(projection["observed_sources"]):
        validate_source(source, f"source[{idx}]")
        sid = source["source_id"]
        if sid in source_ids:
            raise CPIValidationError(f"duplicate source_id: {sid}")
        source_ids.add(sid)

    purposes = set()
    for idx, mapping in enumerate(projection["authority_map"]):
        _require(mapping, ["purpose", "source_id", "authority_scope"], f"authority_map[{idx}]")
        if mapping["source_id"] not in source_ids:
            raise CPIValidationError(
                f"authority_map[{idx}]: unknown source_id {mapping['source_id']}"
            )
        if mapping["purpose"] in purposes:
            raise CPIValidationError(f"duplicate authority purpose: {mapping['purpose']}")
        purposes.add(mapping["purpose"])

    for idx, nk in enumerate(projection["negative_knowledge"]):
        _require(nk, ["kind", "subject", "basis"], f"negative_knowledge[{idx}]")
        if nk["kind"] in {"held", "rejected", "exhausted", "forbidden", "suspended"}:
            if "reopen_if" not in nk:
                raise CPIValidationError(
                    f"negative_knowledge[{idx}]: {nk['kind']} requires reopen_if"
                )

    for idx, dep in enumerate(projection["dependencies"]):
        validate_dependency(dep, f"dependencies[{idx}]")

    for idx, trigger in enumerate(projection["triggers"]):
        _require(
            trigger,
            ["trigger_id", "trigger_type", "status", "consequence"],
            f"triggers[{idx}]",
        )

    for idx, transition in enumerate(projection["transitions"]):
        _require(
            transition,
            ["transition_id", "state", "consequence_class"],
            f"transitions[{idx}]",
        )
        if transition["state"] not in ALLOWED_TRANSITION_STATES:
            raise CPIValidationError(
                f"transitions[{idx}]: unsupported state {transition['state']}"
            )


def validate_dependency(dep: Mapping[str, Any], where: str = "dependency") -> None:
    _require(dep, ["dependency_id", "class", "status", "basis", "counterfactual"], where)
    if dep["class"] not in ALLOWED_DEPENDENCY_CLASSES:
        raise CPIValidationError(f"{where}: unsupported dependency class {dep['class']}")
    if dep.get("basis_kind") == "thematic_similarity" and dep["class"] in {"HARD", "SOFT"}:
        raise CPIValidationError(
            f"{where}: thematic similarity cannot establish load-bearing dependency"
        )


def classify_freshness(
    projection: Mapping[str, Any],
    current_sources: Mapping[str, Mapping[str, Any]],
) -> Dict[str, Any]:
    validate_projection(projection)
    stale = False
    unknown = False
    comparisons: List[Dict[str, Any]] = []

    for observed in projection["observed_sources"]:
        sid = observed["source_id"]
        current = current_sources.get(sid)
        if current is None:
            state = "unknown"
            unknown = True
            current_revision = None
        else:
            validate_source(current, f"current_sources[{sid}]")
            if current["source_kind"] != observed["source_kind"]:
                raise CPIValidationError(f"current_sources[{sid}]: source_kind changed")
            if current["repository"] != observed["repository"]:
                raise CPIValidationError(f"current_sources[{sid}]: repository changed")
            if current["native_id"] != observed["native_id"]:
                raise CPIValidationError(f"current_sources[{sid}]: native_id changed")
            current_revision = current["revision"]
            state = "fresh" if current_revision == observed["revision"] else "stale"
            stale = stale or state == "stale"

        comparisons.append(
            {
                "source_id": sid,
                "source_kind": observed["source_kind"],
                "repository": observed["repository"],
                "observed": observed["revision"],
                "current": current_revision,
                "state": state,
            }
        )

    overall = "stale" if stale else ("unknown" if unknown else "fresh")
    return {"overall": overall, "comparisons": comparisons}
