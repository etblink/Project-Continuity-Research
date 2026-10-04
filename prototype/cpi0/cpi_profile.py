from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional


class CPIValidationError(ValueError):
    pass


ALLOWED_DEPENDENCY_CLASSES = {"HARD", "SOFT", "CONTEXTUAL", "NONE", "UNKNOWN"}
ALLOWED_IMPORT_DISPOSITIONS = {
    "evidence_only",
    "trigger_candidate",
    "dependency_update_candidate",
    "contradiction",
    "quarantined",
    "rejected",
    "accepted_for_local_scope",
}
SUPPORTED_PROFILE_VERSION = "0.1.0"


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
}


def _require(obj: Mapping[str, Any], keys: Iterable[str], where: str) -> None:
    missing = [key for key in keys if key not in obj]
    if missing:
        raise CPIValidationError(f"{where}: missing required fields: {', '.join(missing)}")


def _require_nonempty(value: Any, label: str) -> None:
    if value is None or value == "" or value == [] or value == {}:
        raise CPIValidationError(f"{label}: must be non-empty")


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
    _require_nonempty(projection["observed_sources"], "projection.observed_sources")

    source_ids = set()
    for idx, source in enumerate(projection["observed_sources"]):
        _require(source, ["source_id", "repository", "ref", "commit", "role"], f"source[{idx}]")
        if source["source_id"] in source_ids:
            raise CPIValidationError(f"duplicate source_id: {source['source_id']}")
        source_ids.add(source["source_id"])

    authority_purposes = set()
    for idx, mapping in enumerate(projection["authority_map"]):
        _require(mapping, ["purpose", "source_id", "authority_scope"], f"authority_map[{idx}]")
        if mapping["source_id"] not in source_ids:
            raise CPIValidationError(
                f"authority_map[{idx}]: unknown source_id {mapping['source_id']}"
            )
        if mapping["purpose"] in authority_purposes:
            raise CPIValidationError(f"duplicate authority purpose: {mapping['purpose']}")
        authority_purposes.add(mapping["purpose"])

    for idx, nk in enumerate(projection["negative_knowledge"]):
        _require(nk, ["kind", "subject", "basis"], f"negative_knowledge[{idx}]")
        if nk["kind"] in {"held", "rejected", "exhausted", "forbidden", "suspended"}:
            if "reopen_if" not in nk:
                raise CPIValidationError(
                    f"negative_knowledge[{idx}]: {nk['kind']} requires reopen_if (may be null)"
                )

    for idx, dep in enumerate(projection["dependencies"]):
        validate_dependency(dep, where=f"dependencies[{idx}]")

    for idx, trigger in enumerate(projection["triggers"]):
        _require(trigger, ["trigger_id", "trigger_type", "status", "consequence"], f"triggers[{idx}]")

    for idx, transition in enumerate(projection["transitions"]):
        _require(transition, ["transition_id", "state", "consequence_class"], f"transitions[{idx}]")
        if transition["state"] not in ALLOWED_TRANSITION_STATES:
            raise CPIValidationError(
                f"transitions[{idx}]: unsupported state {transition['state']}"
            )


def resolve_authority(projection: Mapping[str, Any], purpose: str) -> Mapping[str, Any]:
    validate_projection(projection)
    mappings = [m for m in projection["authority_map"] if m["purpose"] == purpose]
    if len(mappings) != 1:
        raise CPIValidationError(
            f"authority purpose {purpose!r} resolved to {len(mappings)} mappings"
        )
    source_id = mappings[0]["source_id"]
    return next(s for s in projection["observed_sources"] if s["source_id"] == source_id)


def classify_freshness(
    projection: Mapping[str, Any], current_revisions: Mapping[str, str]
) -> Dict[str, Any]:
    validate_projection(projection)
    comparisons: List[Dict[str, Any]] = []
    stale = False
    unknown = False
    for source in projection["observed_sources"]:
        sid = source["source_id"]
        observed = source["commit"]
        current = current_revisions.get(sid)
        if current is None:
            state = "unknown"
            unknown = True
        elif current == observed:
            state = "fresh"
        else:
            state = "stale"
            stale = True
        comparisons.append(
            {"source_id": sid, "observed": observed, "current": current, "state": state}
        )
    overall = "stale" if stale else ("unknown" if unknown else "fresh")
    return {"overall": overall, "comparisons": comparisons}


def validate_dependency(dep: Mapping[str, Any], where: str = "dependency") -> None:
    _require(dep, ["dependency_id", "class", "status", "basis", "counterfactual"], where)
    if dep["class"] not in ALLOWED_DEPENDENCY_CLASSES:
        raise CPIValidationError(f"{where}: unsupported dependency class {dep['class']}")
    basis_kind = dep.get("basis_kind")
    if dep["class"] in {"HARD", "SOFT"} and basis_kind == "thematic_similarity":
        raise CPIValidationError(f"{where}: thematic similarity cannot establish load-bearing dependency")


def validate_event(event: Mapping[str, Any]) -> None:
    _require(
        event,
        ["specversion", "id", "source", "type", "time", "subject", "predicate_type", "data"],
        "event",
    )
    _require(event["subject"], ["project_id", "source_identity"], "event.subject")
    if event["data"].get("direct_local_canonical_effect") is True:
        raise CPIValidationError(
            "event: remote event may not declare direct local canonical effect"
        )


def validate_event_batch(events: Iterable[Mapping[str, Any]]) -> None:
    seen = set()
    for idx, event in enumerate(events):
        validate_event(event)
        event_id = event["id"]
        if event_id in seen:
            raise CPIValidationError(f"events[{idx}]: duplicate event id {event_id}")
        seen.add(event_id)


def validate_import_record(record: Mapping[str, Any]) -> None:
    _require(
        record,
        [
            "import_id",
            "remote_object_id",
            "receiving_project",
            "disposition",
            "local_scope",
            "local_authority",
            "reason",
            "canonical_mutation_authorized",
        ],
        "import_record",
    )
    if record["disposition"] not in ALLOWED_IMPORT_DISPOSITIONS:
        raise CPIValidationError(f"import_record: unsupported disposition {record['disposition']}")
    if record["canonical_mutation_authorized"]:
        if record["disposition"] != "accepted_for_local_scope":
            raise CPIValidationError(
                "import_record: canonical mutation requires accepted_for_local_scope"
            )
        _require_nonempty(record["local_authority"], "import_record.local_authority")
        if not record.get("local_transition_id"):
            raise CPIValidationError(
                "import_record: canonical mutation requires separate local_transition_id"
            )


def validate_derivation(record: Mapping[str, Any]) -> None:
    _require(
        record,
        ["derivation_id", "inputs", "transformation_version", "output_id", "ambiguities"],
        "derivation_record",
    )
    _require_nonempty(record["inputs"], "derivation_record.inputs")
    _require_nonempty(record["transformation_version"], "derivation_record.transformation_version")


def material_roles(projection: Mapping[str, Any]) -> List[str]:
    validate_projection(projection)
    return [obj.get("role") for obj in projection["material_objects"]]


def transition_by_id(projection: Mapping[str, Any], transition_id: str) -> Mapping[str, Any]:
    validate_projection(projection)
    matches = [t for t in projection["transitions"] if t["transition_id"] == transition_id]
    if len(matches) != 1:
        raise CPIValidationError(
            f"transition {transition_id!r} resolved to {len(matches)} records"
        )
    return matches[0]


def dependency_by_id(projection: Mapping[str, Any], dependency_id: str) -> Mapping[str, Any]:
    validate_projection(projection)
    matches = [d for d in projection["dependencies"] if d["dependency_id"] == dependency_id]
    if len(matches) != 1:
        raise CPIValidationError(
            f"dependency {dependency_id!r} resolved to {len(matches)} records"
        )
    return matches[0]
