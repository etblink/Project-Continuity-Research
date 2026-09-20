from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple
import hashlib
import json

from prototype.ccp0.ccp import TransitionRejected, ValidationError
from prototype.ccp1.concurrency import ConcurrencyControlPlane


class ReopenPolicyError(TransitionRejected):
    """Raised when a held route cannot be reopened under its structured policy."""


@dataclass(frozen=True)
class EvidenceFact:
    fact_id: str
    attributes: Mapping[str, Any]
    evidence_refs: Tuple[str, ...] = ()

    def canonical(self) -> Dict[str, Any]:
        return {
            "fact_id": self.fact_id,
            "attributes": dict(sorted(self.attributes.items())),
            "evidence_refs": list(self.evidence_refs),
        }


@dataclass(frozen=True)
class AttributePredicate:
    field: str
    expected: Any

    def matches(self, fact: EvidenceFact) -> bool:
        return fact.attributes.get(self.field) == self.expected

    def canonical(self) -> Dict[str, Any]:
        return {"field": self.field, "expected": self.expected}


@dataclass(frozen=True)
class ReopenRequirement:
    requirement_id: str
    predicates: Tuple[AttributePredicate, ...]

    def matches(self, fact: EvidenceFact) -> bool:
        return all(predicate.matches(fact) for predicate in self.predicates)

    def canonical(self) -> Dict[str, Any]:
        return {
            "requirement_id": self.requirement_id,
            "predicates": [p.canonical() for p in self.predicates],
        }


@dataclass(frozen=True)
class StructuredReopenPolicy:
    route: str
    version: str
    authority_source: str
    requirements: Tuple[ReopenRequirement, ...]

    def canonical(self) -> Dict[str, Any]:
        return {
            "route": self.route,
            "version": self.version,
            "authority_source": self.authority_source,
            "requirements": [r.canonical() for r in self.requirements],
        }

    @property
    def digest(self) -> str:
        raw = json.dumps(
            self.canonical(), sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


class StructuredReopenRegistry:
    def __init__(self) -> None:
        self._policies: Dict[Tuple[str, str], StructuredReopenPolicy] = {}

    def register(self, policy: StructuredReopenPolicy) -> StructuredReopenPolicy:
        if not policy.authority_source:
            raise ValidationError("reopen policy authority_source is required")
        if not policy.requirements:
            raise ValidationError("reopen policy requires at least one requirement")
        ids = [r.requirement_id for r in policy.requirements]
        if len(ids) != len(set(ids)):
            raise ValidationError("reopen requirement IDs must be unique")

        key = (policy.route, policy.version)
        existing = self._policies.get(key)
        if existing is not None:
            if existing.digest == policy.digest:
                return existing
            raise ValidationError(
                f"reopen policy {policy.route}@{policy.version} already bound to a different digest"
            )
        self._policies[key] = policy
        return policy

    def get(self, route: str, version: str) -> StructuredReopenPolicy:
        return self._policies[(route, version)]


def evaluate_reopen_policy(
    policy: StructuredReopenPolicy,
    facts: Iterable[EvidenceFact],
) -> Tuple[bool, Dict[str, Tuple[str, ...]], Tuple[str, ...]]:
    facts = tuple(facts)
    matched: Dict[str, Tuple[str, ...]] = {}
    missing = []

    seen_ids = [fact.fact_id for fact in facts]
    if len(seen_ids) != len(set(seen_ids)):
        raise ValidationError("evidence fact IDs must be unique")

    for requirement in policy.requirements:
        ids = tuple(
            sorted(fact.fact_id for fact in facts if requirement.matches(fact))
        )
        if ids:
            matched[requirement.requirement_id] = ids
        else:
            missing.append(requirement.requirement_id)

    return (not missing, matched, tuple(sorted(missing)))


class ReopenControlPlane(ConcurrencyControlPlane):
    """CCP-1 structured negative-knowledge reopening semantics."""

    def __init__(self, project: str, purpose: str):
        super().__init__(project, purpose)
        self.reopen_registry = StructuredReopenRegistry()

    def hold_route_structured(
        self,
        route: str,
        *,
        basis: str,
        authority: str,
        scope: str,
        policy: StructuredReopenPolicy,
        actor: str,
    ):
        if policy.route != route:
            raise ValidationError("reopen policy route does not match held route")
        self.reopen_registry.register(policy)
        return self.append_event(
            "ROUTE_HELD",
            route,
            {
                "basis": basis,
                "authority": authority,
                "scope": scope,
                # CCP-0 literal reopen tokens are intentionally unused in this slice.
                "reopen_requires": [],
                "structured_reopen_policy": {
                    "version": policy.version,
                    "digest": policy.digest,
                    "authority_source": policy.authority_source,
                },
            },
            actor=actor,
            authority=authority,
        )

    def reopen_route_structured(
        self,
        route: str,
        *,
        policy_version: str,
        facts: Iterable[EvidenceFact],
        actor_id: str,
    ):
        if route not in self._routes:
            raise ReopenPolicyError(f"route {route!r} is not held")
        route_record = self._routes[route]
        if route_record.state != "HELD":
            raise ReopenPolicyError(
                f"route {route!r} is {route_record.state}, not HELD"
            )

        policy = self.reopen_registry.get(route, policy_version)
        self.authority_registry.require(actor_id, "REOPEN_ROUTE", f"route:{route}")

        fact_tuple = tuple(facts)
        ok, matched, missing = evaluate_reopen_policy(policy, fact_tuple)
        if not ok:
            raise ReopenPolicyError(
                f"route {route!r} remains held; missing requirements: {list(missing)}"
            )

        fact_map = {fact.fact_id: fact for fact in fact_tuple}
        used_fact_ids = sorted({fact_id for ids in matched.values() for fact_id in ids})
        evidence_refs = sorted(
            {
                ref
                for fact_id in used_fact_ids
                for ref in fact_map[fact_id].evidence_refs
            }
        )

        grant = self.authority_registry.require(
            actor_id, "REOPEN_ROUTE", f"route:{route}"
        )
        return self.append_event(
            "ROUTE_REOPENED",
            route,
            {
                "policy_version": policy.version,
                "policy_digest": policy.digest,
                "policy_authority_source": policy.authority_source,
                "matched_requirements": {
                    requirement_id: list(fact_ids)
                    for requirement_id, fact_ids in sorted(matched.items())
                },
                "used_fact_ids": used_fact_ids,
                "authority_grant_id": grant.grant_id,
                "authority_role": grant.role,
                "authority_source": grant.authority_source,
            },
            actor=actor_id,
            authority=f"{grant.role}@{grant.grant_id}",
            evidence_refs=evidence_refs,
        )
