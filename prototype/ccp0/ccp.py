from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple
import copy
import hashlib
import json


class TransitionRejected(RuntimeError):
    """Raised when a requested material transition does not satisfy its guards."""


class ValidationError(RuntimeError):
    """Raised when a proposed event violates semantic invariants."""


@dataclass(frozen=True)
class SourceRef:
    id: str
    repository: Optional[str] = None
    artifact: Optional[str] = None
    revision: Optional[str] = None
    authority_class: Optional[str] = None
    historical: bool = False


@dataclass(frozen=True)
class Event:
    seq: int
    event_type: str
    subject: str
    payload: Dict[str, Any]
    actor: str
    authority: Optional[str]
    evidence_refs: Tuple[str, ...]
    accepted_at: str


@dataclass
class WorkerReturn:
    return_id: str
    operation: str
    worker: str
    proposed_events: List[Dict[str, Any]]
    evidence_refs: List[str]
    reported_outcome: Optional[str] = None
    observations: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NegativeKnowledge:
    route: str
    state: str  # HELD | REJECTED | EXHAUSTED | FORBIDDEN | OPEN
    basis: str
    authority: str
    scope: str
    reopen_requires: Set[str] = field(default_factory=set)
    reopened_by_event: Optional[int] = None


@dataclass(frozen=True)
class Supersession:
    prior: str
    superseding: str
    scope: frozenset[str]
    unaffected: frozenset[str]
    reason: str
    authority: str
    event_seq: int


@dataclass
class TransitionRule:
    name: str
    from_state: Optional[str]
    to_state: str
    guards: List[Callable[["ControlPlane", Dict[str, Any]], Tuple[bool, str]]]


@dataclass(frozen=True)
class KernelSnapshot:
    projection_event_seq: int
    projection_graph_revision: int
    projection_digest: str
    policy_version: str
    intent_version: int
    computed_at: str
    markdown: str

    def freshness_identity(self) -> Dict[str, Any]:
        return {
            "projection_event_seq": self.projection_event_seq,
            "projection_graph_revision": self.projection_graph_revision,
            "projection_digest": self.projection_digest,
            "policy_version": self.policy_version,
            "intent_version": self.intent_version,
        }


class ControlPlane:
    """
    Minimal semantic prototype of Composite E.

    This is deliberately not production infrastructure. It tests whether a
    small set of reusable semantics can replay historically observed failure
    modes without encoding those incidents as special cases.
    """

    WORKER_ADMISSIBLE_EVENT_TYPES = frozenset({"CLAIM_SET"})

    def __init__(self, project: str, purpose: str, *, policy_version: str = "0.1.1"):
        self.project = project
        self._initial_purpose = purpose
        self.purpose = purpose
        self.intent_version = 1
        self.policy_version = policy_version

        self._events: List[Event] = []
        self._sources: Dict[str, SourceRef] = {}
        self.graph_revision = 0

        self._claims: Dict[str, Dict[str, Any]] = {}
        self._phase_state: Dict[str, str] = {}
        self._routes: Dict[str, NegativeKnowledge] = {}
        self._supersessions: List[Supersession] = []
        self._environment: Dict[str, Any] = {}
        self._safeguards: Dict[str, Dict[str, Any]] = {}
        self._external_bindings: Dict[str, Dict[str, Any]] = {}
        self._external_observations: Dict[str, Dict[str, Any]] = {}

        self._transitions: Dict[str, TransitionRule] = {}
        self._worker_returns: Dict[str, WorkerReturn] = {}
        self.outcome_burdens: Dict[str, Set[str]] = {}
        self.outcome_rank: List[str] = []

    # ---------- read-only public views ----------

    @property
    def events(self) -> Tuple[Event, ...]:
        return tuple(self._events)

    @property
    def sources(self):
        return MappingProxyType(self._sources)

    @property
    def claims(self) -> Dict[str, Dict[str, Any]]:
        return copy.deepcopy(self._claims)

    @property
    def phase_state(self):
        return MappingProxyType(self._phase_state)

    @property
    def routes(self) -> Dict[str, NegativeKnowledge]:
        return copy.deepcopy(self._routes)

    @property
    def safeguards(self) -> Dict[str, Dict[str, Any]]:
        return copy.deepcopy(self._safeguards)

    # ---------- durable history / provenance ----------

    @property
    def event_seq(self) -> int:
        return len(self._events)

    def register_source(self, ref: SourceRef) -> None:
        existing = self._sources.get(ref.id)
        if existing is not None:
            if existing == ref:
                return
            raise ValidationError(
                f"source id {ref.id!r} is immutable and already bound to a different source"
            )
        self._sources[ref.id] = ref
        self.graph_revision += 1

    def update_intent(self, new_purpose: str, *, actor: str, authority: str) -> Event:
        return self.append_event(
            "INTENT_UPDATED",
            self.project,
            {"purpose": new_purpose},
            actor=actor,
            authority=authority,
        )

    def append_event(
        self,
        event_type: str,
        subject: str,
        payload: Dict[str, Any],
        *,
        actor: str,
        authority: Optional[str] = None,
        evidence_refs: Optional[Iterable[str]] = None,
    ) -> Event:
        refs = tuple(evidence_refs or ())
        missing = [r for r in refs if r not in self._sources]
        if missing:
            raise ValidationError(f"unknown evidence refs: {missing}")

        event = Event(
            seq=self.event_seq + 1,
            event_type=event_type,
            subject=subject,
            payload=copy.deepcopy(payload),
            actor=actor,
            authority=authority,
            evidence_refs=refs,
            accepted_at=datetime.now(timezone.utc).isoformat(),
        )
        self._events.append(event)
        self._apply_event(event)
        return event

    def _apply_event(self, event: Event) -> None:
        p = event.payload

        if event.event_type in {"CLAIM_SET", "CLAIM_QUALIFIED"}:
            self._claims[event.subject] = {
                "value": copy.deepcopy(p["value"]),
                "status": p.get(
                    "status",
                    "QUALIFIED" if event.event_type == "CLAIM_QUALIFIED" else "CURRENT",
                ),
                "authority": event.authority,
                "evidence_refs": list(event.evidence_refs),
                "event_seq": event.seq,
            }

        elif event.event_type == "PHASE_STATE_SET":
            self._phase_state[event.subject] = p["state"]

        elif event.event_type == "ROUTE_HELD":
            self._routes[event.subject] = NegativeKnowledge(
                route=event.subject,
                state=p.get("state", "HELD"),
                basis=p["basis"],
                authority=event.authority or p["authority"],
                scope=p.get("scope", "project"),
                reopen_requires=set(p.get("reopen_requires", [])),
            )

        elif event.event_type == "ROUTE_REOPENED":
            route = self._routes[event.subject]
            route.state = "OPEN"
            route.reopened_by_event = event.seq

        elif event.event_type == "CLAIM_SUPERSEDED":
            scope = frozenset(p["scope"])
            unaffected = frozenset(p.get("unaffected", []))
            self._supersessions.append(
                Supersession(
                    prior=p["prior"],
                    superseding=p["superseding"],
                    scope=scope,
                    unaffected=unaffected,
                    reason=p["reason"],
                    authority=event.authority or "",
                    event_seq=event.seq,
                )
            )
            self.graph_revision += 1

        elif event.event_type == "SAFEGUARD_OPENED":
            self._safeguards[event.subject] = {
                "state": "OPEN",
                "required_exit_facts": set(p["required_exit_facts"]),
                "event_seq": event.seq,
            }

        elif event.event_type == "SAFEGUARD_EXITED":
            self._safeguards[event.subject]["state"] = "COMPLETE"
            self._safeguards[event.subject]["exit_event_seq"] = event.seq

        elif event.event_type == "ENVIRONMENT_SET":
            self._environment.update(copy.deepcopy(p))

        elif event.event_type == "EXTERNAL_SOURCE_BOUND":
            self._external_bindings[event.subject] = {
                "repository": p["repository"],
                "ref": p.get("ref"),
                "bound_revision": p["bound_revision"],
                "observed_at_boundary": p.get("observed_at_boundary"),
                "authority": event.authority,
                "event_seq": event.seq,
            }

        elif event.event_type == "EXTERNAL_SOURCE_OBSERVED":
            self._external_observations[event.subject] = {
                "observed_revision": p["observed_revision"],
                "observed_at": p["observed_at"],
                "actor": event.actor,
                "event_seq": event.seq,
            }

        elif event.event_type == "INTENT_UPDATED":
            self.purpose = p["purpose"]
            self.intent_version += 1

    # ---------- projection integrity ----------

    def _routes_projection(self) -> Dict[str, Any]:
        return {
            k: {
                "route": v.route,
                "state": v.state,
                "basis": v.basis,
                "authority": v.authority,
                "scope": v.scope,
                "reopen_requires": sorted(v.reopen_requires),
                "reopened_by_event": v.reopened_by_event,
            }
            for k, v in self._routes.items()
        }

    def state_projection(self) -> Dict[str, Any]:
        return {
            "project": self.project,
            "purpose": self.purpose,
            "intent_version": self.intent_version,
            "policy_version": self.policy_version,
            "event_seq": self.event_seq,
            "graph_revision": self.graph_revision,
            "phase_state": copy.deepcopy(self._phase_state),
            "claims": copy.deepcopy(self._claims),
            "routes": self._routes_projection(),
            "supersessions": [
                {
                    "prior": s.prior,
                    "superseding": s.superseding,
                    "scope": sorted(s.scope),
                    "unaffected": sorted(s.unaffected),
                    "reason": s.reason,
                    "authority": s.authority,
                    "event_seq": s.event_seq,
                }
                for s in self._supersessions
            ],
            "environment": copy.deepcopy(self._environment),
            "safeguards": {
                k: {
                    **{kk: vv for kk, vv in v.items() if kk != "required_exit_facts"},
                    "required_exit_facts": sorted(v["required_exit_facts"]),
                }
                for k, v in self._safeguards.items()
            },
            "external_bindings": copy.deepcopy(self._external_bindings),
            "external_observations": copy.deepcopy(self._external_observations),
            "external_status": self.external_source_statuses(),
        }

    def projection_digest(self) -> str:
        payload = json.dumps(
            self.state_projection(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def rebuild_from_ledger(self) -> "ControlPlane":
        rebuilt = ControlPlane(
            self.project,
            self._initial_purpose,
            policy_version=self.policy_version,
        )
        # Sources are immutable provenance bindings outside accepted project events
        # in this minimal prototype. Preserve them exactly.
        for source in self._sources.values():
            rebuilt.register_source(source)

        for event in self._events:
            rebuilt._events.append(event)
            rebuilt._apply_event(event)
        return rebuilt

    def projection_consistent_with_ledger(self) -> bool:
        rebuilt = self.rebuild_from_ledger()
        return rebuilt.state_projection() == self.state_projection()

    # ---------- external observation freshness ----------

    def bind_external_source(
        self,
        source_id: str,
        *,
        repository: str,
        bound_revision: str,
        actor: str,
        authority: str,
        ref: Optional[str] = None,
        observed_at_boundary: Optional[str] = None,
    ) -> Event:
        return self.append_event(
            "EXTERNAL_SOURCE_BOUND",
            source_id,
            {
                "repository": repository,
                "ref": ref,
                "bound_revision": bound_revision,
                "observed_at_boundary": observed_at_boundary,
            },
            actor=actor,
            authority=authority,
        )

    def observe_external_source(
        self,
        source_id: str,
        *,
        observed_revision: str,
        observed_at: str,
        actor: str,
        authority: str = "READ_ONLY_OBSERVATION",
    ) -> Event:
        if source_id not in self._external_bindings:
            raise ValidationError(f"external source {source_id!r} is not bound")
        return self.append_event(
            "EXTERNAL_SOURCE_OBSERVED",
            source_id,
            {
                "observed_revision": observed_revision,
                "observed_at": observed_at,
            },
            actor=actor,
            authority=authority,
        )

    def external_source_status(self, source_id: str) -> Dict[str, Any]:
        binding = self._external_bindings[source_id]
        observation = self._external_observations.get(source_id)
        if observation is None:
            status = "UNVERIFIED_SINCE_BOUNDARY"
        elif observation["observed_revision"] == binding["bound_revision"]:
            status = "MATCHES_BOUNDARY"
        else:
            status = "SOURCE_MOVED_SINCE_BOUNDARY"
        return {
            "status": status,
            "repository": binding["repository"],
            "ref": binding.get("ref"),
            "bound_revision": binding["bound_revision"],
            "observed_revision": None if observation is None else observation["observed_revision"],
            "observed_at_boundary": binding.get("observed_at_boundary"),
            "latest_observed_at": None if observation is None else observation["observed_at"],
        }

    def external_source_statuses(self) -> Dict[str, Dict[str, Any]]:
        return {
            source_id: self.external_source_status(source_id)
            for source_id in sorted(self._external_bindings)
        }

    def all_external_sources_match_boundary(self) -> bool:
        statuses = self.external_source_statuses().values()
        return all(x["status"] == "MATCHES_BOUNDARY" for x in statuses)

    # ---------- scoped supersession ----------

    def current_subclaims(self, claim_id: str) -> Dict[str, Any]:
        if claim_id not in self._claims:
            raise KeyError(claim_id)
        base = copy.deepcopy(self._claims[claim_id]["value"])
        if not isinstance(base, dict):
            return base

        for rel in sorted(self._supersessions, key=lambda x: x.event_seq):
            if rel.prior != claim_id:
                continue
            replacement = self._claims[rel.superseding]["value"]
            if not isinstance(replacement, dict):
                raise ValidationError("scoped supersession requires dict-valued claims")
            for key in rel.scope:
                if key in replacement:
                    base[key] = copy.deepcopy(replacement[key])
        return base

    # ---------- negative knowledge ----------

    def can_reopen_route(self, route: str, supplied_conditions: Iterable[str]) -> Tuple[bool, Set[str]]:
        record = self._routes[route]
        supplied = set(supplied_conditions)
        missing = record.reopen_requires - supplied
        return (not missing, missing)

    def reopen_route(
        self,
        route: str,
        supplied_conditions: Iterable[str],
        *,
        actor: str,
        authority: str,
        evidence_refs: Optional[Iterable[str]] = None,
    ) -> Event:
        ok, missing = self.can_reopen_route(route, supplied_conditions)
        if not ok:
            raise TransitionRejected(
                f"route {route} remains held; missing reopen conditions: {sorted(missing)}"
            )
        return self.append_event(
            "ROUTE_REOPENED",
            route,
            {"satisfied_conditions": sorted(set(supplied_conditions))},
            actor=actor,
            authority=authority,
            evidence_refs=evidence_refs,
        )

    # ---------- guarded transitions ----------

    def register_transition(self, rule: TransitionRule) -> None:
        if rule.name in self._transitions:
            raise ValidationError(
                f"transition {rule.name!r} already exists in policy {self.policy_version}"
            )
        self._transitions[rule.name] = rule

    def request_transition(
        self,
        rule_name: str,
        *,
        subject: str,
        actor: str,
        authority: str,
        context: Optional[Dict[str, Any]] = None,
        evidence_refs: Optional[Iterable[str]] = None,
    ) -> Event:
        rule = self._transitions[rule_name]
        ctx = dict(context or {})
        current = self._phase_state.get(subject)
        if rule.from_state is not None and current != rule.from_state:
            raise TransitionRejected(
                f"{rule_name}: state {current!r} does not match required {rule.from_state!r}"
            )

        failures = []
        for guard in rule.guards:
            ok, why = guard(self, ctx)
            if not ok:
                failures.append(why)
        if failures:
            raise TransitionRejected(f"{rule_name}: " + "; ".join(failures))

        return self.append_event(
            "PHASE_STATE_SET",
            subject,
            {"state": rule.to_state, "transition": rule_name},
            actor=actor,
            authority=authority,
            evidence_refs=evidence_refs,
        )

    # ---------- safeguards with explicit exit ----------

    def safeguard_exit_ready(self, safeguard: str, facts: Iterable[str]) -> Tuple[bool, Set[str]]:
        sg = self._safeguards[safeguard]
        missing = set(sg["required_exit_facts"]) - set(facts)
        return (not missing, missing)

    def exit_safeguard(
        self,
        safeguard: str,
        facts: Iterable[str],
        *,
        actor: str,
        authority: str,
    ) -> Event:
        ok, missing = self.safeguard_exit_ready(safeguard, facts)
        if not ok:
            raise TransitionRejected(
                f"safeguard {safeguard} cannot exit; missing: {sorted(missing)}"
            )
        return self.append_event(
            "SAFEGUARD_EXITED",
            safeguard,
            {"facts": sorted(set(facts))},
            actor=actor,
            authority=authority,
        )

    # ---------- worker return -> adjudication ----------

    def submit_worker_return(self, ret: WorkerReturn) -> None:
        if ret.return_id in self._worker_returns:
            raise ValidationError(f"duplicate return id {ret.return_id}")
        self._worker_returns[ret.return_id] = copy.deepcopy(ret)

    def configure_outcomes(self, outcome_rank: List[str], burdens: Dict[str, Iterable[str]]) -> None:
        self.outcome_rank = list(outcome_rank)
        self.outcome_burdens = {k: set(v) for k, v in burdens.items()}

    def strongest_justified_outcome(self, observed_features: Iterable[str]) -> Optional[str]:
        features = set(observed_features)
        justified = [
            outcome
            for outcome in self.outcome_rank
            if self.outcome_burdens.get(outcome, set()).issubset(features)
        ]
        return justified[-1] if justified else None

    def adjudicate_worker_return(
        self,
        return_id: str,
        *,
        actor: str,
        authority: str,
        observed_features: Optional[Iterable[str]] = None,
    ) -> List[Event]:
        ret = self._worker_returns[return_id]
        accepted: List[Event] = []

        if ret.reported_outcome is not None and self.outcome_rank:
            strongest = self.strongest_justified_outcome(observed_features or [])
            if strongest is None:
                raise TransitionRejected("worker outcome has no justified disposition")
            accepted.append(
                self.append_event(
                    "CLAIM_QUALIFIED",
                    f"{ret.operation}.outcome",
                    {
                        "value": strongest,
                        "status": "QUALIFIED",
                        "worker_reported": ret.reported_outcome,
                    },
                    actor=actor,
                    authority=authority,
                    evidence_refs=ret.evidence_refs,
                )
            )

        for proposed in ret.proposed_events:
            event_type = proposed["event_type"]
            if event_type not in self.WORKER_ADMISSIBLE_EVENT_TYPES:
                raise TransitionRejected(
                    f"worker return cannot directly canonicalize {event_type}; "
                    "material transitions must use the transition/policy layer"
                )
            accepted.append(
                self.append_event(
                    event_type,
                    proposed["subject"],
                    proposed["payload"],
                    actor=actor,
                    authority=authority,
                    evidence_refs=proposed.get("evidence_refs", ret.evidence_refs),
                )
            )
        return accepted

    # ---------- kernel projection ----------

    def generate_kernel(self) -> KernelSnapshot:
        held = [r for r in self._routes.values() if r.state != "OPEN"]
        phase_lines = [
            f"- `{k}` = `{v}`" for k, v in sorted(self._phase_state.items())
        ] or ["- None recorded."]
        held_lines = [
            f"- `{r.route}`: **{r.state}** — {r.basis} — reopen if: "
            + (
                ", ".join(sorted(r.reopen_requires))
                if r.reopen_requires
                else "no automatic predicate"
            )
            for r in held
        ] or ["- None."]

        claim_lines = [
            f"- `{cid}` = `{c['value']}` ({c['status']}, authority={c['authority']})"
            for cid, c in sorted(self._claims.items())
        ] or ["- None."]

        open_safeguards = [
            name for name, data in self._safeguards.items() if data["state"] == "OPEN"
        ]
        external_statuses = self.external_source_statuses()
        external_lines = [
            f"- `{sid}`: **{info['status']}** — bound `{info['bound_revision']}`; "
            f"observed `{info['observed_revision']}`"
            for sid, info in external_statuses.items()
        ] or ["- None bound."]

        digest = self.projection_digest()
        markdown = "\n".join([
            f"# Project Kernel — {self.project}",
            "",
            "## Purpose",
            self.purpose,
            "",
            "## Freshness identity",
            f"- projection_event_seq: `{self.event_seq}`",
            f"- projection_graph_revision: `{self.graph_revision}`",
            f"- projection_digest: `{digest}`",
            f"- policy_version: `{self.policy_version}`",
            f"- intent_version: `{self.intent_version}`",
            "",
            "## Current phase/state",
            *phase_lines,
            "",
            "## Current material claims",
            *claim_lines,
            "",
            "## Held / closed routes",
            *held_lines,
            "",
            "## Open safeguards",
            *(
                [f"- `{x}`" for x in sorted(open_safeguards)]
                if open_safeguards
                else ["- None."]
            ),
            "",
            "## External observation freshness",
            *external_lines,
            "",
            f"- all_external_sources_match_boundary: `{self.all_external_sources_match_boundary()}`",
            "",
            "## Orientation rule",
            "This kernel is a projection. If its freshness identity does not match the control plane, regenerate it before relying on it.",
            "",
        ])
        return KernelSnapshot(
            projection_event_seq=self.event_seq,
            projection_graph_revision=self.graph_revision,
            projection_digest=digest,
            policy_version=self.policy_version,
            intent_version=self.intent_version,
            computed_at=datetime.now(timezone.utc).isoformat(),
            markdown=markdown,
        )

    def kernel_is_fresh(self, kernel: KernelSnapshot) -> bool:
        return kernel.freshness_identity() == {
            "projection_event_seq": self.event_seq,
            "projection_graph_revision": self.graph_revision,
            "projection_digest": self.projection_digest(),
            "policy_version": self.policy_version,
            "intent_version": self.intent_version,
        }


# ---------- reusable guard helpers ----------

def claim_equals(
    claim_id: str, expected: Any
) -> Callable[[ControlPlane, Dict[str, Any]], Tuple[bool, str]]:
    def guard(cp: ControlPlane, ctx: Dict[str, Any]) -> Tuple[bool, str]:
        actual = cp._claims.get(claim_id, {}).get("value")
        return (
            actual == expected,
            f"{claim_id} expected {expected!r}, found {actual!r}",
        )
    return guard


def context_equals(
    key: str, expected: Any
) -> Callable[[ControlPlane, Dict[str, Any]], Tuple[bool, str]]:
    def guard(cp: ControlPlane, ctx: Dict[str, Any]) -> Tuple[bool, str]:
        actual = ctx.get(key)
        return (
            actual == expected,
            f"context {key} expected {expected!r}, found {actual!r}",
        )
    return guard


def source_repository_is(
    evidence_ref: str, repository: str
) -> Callable[[ControlPlane, Dict[str, Any]], Tuple[bool, str]]:
    def guard(cp: ControlPlane, ctx: Dict[str, Any]) -> Tuple[bool, str]:
        src = cp._sources.get(evidence_ref)
        actual = None if src is None else src.repository
        return (
            actual == repository,
            f"evidence {evidence_ref} repository expected {repository!r}, found {actual!r}",
        )
    return guard


def environment_target_is_dedicated(
    cp: ControlPlane, ctx: Dict[str, Any]
) -> Tuple[bool, str]:
    ports = set(cp._environment.get("public_tcp_ports", []))
    allowed = set(ctx.get("allowed_public_tcp_ports", [22]))
    unexpected = ports - allowed
    caddy = bool(cp._environment.get("system_caddy_active"))
    ok = not unexpected and not caddy
    why = (
        f"target occupied: unexpected_ports={sorted(unexpected)}, "
        f"system_caddy_active={caddy}"
    )
    return ok, why


def route_is_open(
    route: str,
) -> Callable[[ControlPlane, Dict[str, Any]], Tuple[bool, str]]:
    def guard(cp: ControlPlane, ctx: Dict[str, Any]) -> Tuple[bool, str]:
        record = cp._routes.get(route)
        actual = None if record is None else record.state
        return (actual == "OPEN", f"route {route} is {actual}, not OPEN")
    return guard
