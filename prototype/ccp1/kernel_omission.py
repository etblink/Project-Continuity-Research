from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple
import hashlib
import json

from prototype.ccp0.ccp import KernelSnapshot, ValidationError


@dataclass(frozen=True)
class OrientationRequirement:
    requirement_id: str
    kind: str
    key: Optional[str] = None
    rationale: str = ""

    def canonical(self) -> Dict[str, Any]:
        return {
            "requirement_id": self.requirement_id,
            "kind": self.kind,
            "key": self.key,
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class OrientationContract:
    operation: str
    version: str
    requirements: Tuple[OrientationRequirement, ...]

    @property
    def digest(self) -> str:
        payload = {
            "operation": self.operation,
            "version": self.version,
            "requirements": [r.canonical() for r in self.requirements],
        }
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class KernelViewProfile:
    included_kinds: frozenset[str]


@dataclass(frozen=True)
class AuditedKernelSnapshot:
    base_freshness: KernelSnapshot
    operation: str
    contract_version: str
    contract_digest: str
    covered_requirement_ids: frozenset[str]
    missing_requirement_ids: frozenset[str]
    coverage: Dict[str, Dict[str, Any]]
    markdown: str


def _scope_matches(grant_scope: str, requested_scope: str) -> bool:
    if grant_scope == "*":
        return True
    if grant_scope.endswith("*"):
        return requested_scope.startswith(grant_scope[:-1])
    return grant_scope == requested_scope


def _action_matches(grant_action: str, requested_action: str) -> bool:
    return grant_action == "*" or grant_action == requested_action


def _resolve_requirement(cp, requirement: OrientationRequirement) -> Tuple[bool, str, Any]:
    kind = requirement.kind
    key = requirement.key

    if kind == "purpose":
        return True, f"purpose: {cp.purpose}", cp.purpose

    if kind == "phase":
        if key is None or key not in cp.phase_state:
            return False, f"phase {key!r} unresolved", None
        value = cp.phase_state[key]
        return True, f"phase {key}: {value}", value

    if kind == "policy":
        spec = getattr(cp, "active_policy", None)
        if spec is None:
            return False, "active policy unresolved", None
        value = {
            "policy_id": spec.policy_id,
            "version": spec.version,
            "digest": spec.digest,
            "authority_source": spec.authority_source,
        }
        return (
            True,
            f"active policy: {spec.policy_id}@{spec.version} digest={spec.digest}",
            value,
        )

    if kind == "authority":
        if not key or "|" not in key:
            raise ValidationError("authority requirement key must be ACTION|SCOPE")
        action, scope = key.split("|", 1)
        grants = []
        registry = getattr(cp, "authority_registry", None)
        if registry is None:
            return False, f"authority registry unavailable for {key}", None
        for grant in registry.grants:
            if not grant.active:
                continue
            if not any(_action_matches(a, action) for a in grant.actions):
                continue
            if not any(_scope_matches(s, scope) for s in grant.scopes):
                continue
            grants.append(
                {
                    "grant_id": grant.grant_id,
                    "actor_id": grant.actor_id,
                    "role": grant.role,
                    "authority_source": grant.authority_source,
                }
            )
        if not grants:
            return False, f"no active authority for {action} in {scope}", None
        grants.sort(key=lambda x: (x["actor_id"], x["grant_id"]))
        return True, f"authority {action} in {scope}: {grants}", grants

    if kind == "route":
        routes = cp.routes
        if key is None or key not in routes:
            return False, f"route {key!r} unresolved", None
        route = routes[key]
        value = {
            "state": route.state,
            "basis": route.basis,
            "authority": route.authority,
            "scope": route.scope,
            "reopen_requires": sorted(route.reopen_requires),
        }
        return (
            True,
            f"route {key}: {route.state}; reopen_if={sorted(route.reopen_requires)}",
            value,
        )

    if kind == "claim":
        claims = cp.claims
        if key is None or key not in claims:
            return False, f"claim {key!r} unresolved", None
        value = claims[key]
        return True, f"claim {key}: {value['value']}", value

    if kind == "external":
        if key is None:
            return False, "external source key missing", None
        try:
            value = cp.external_source_status(key)
        except (KeyError, AttributeError):
            return False, f"external source {key!r} unresolved", None
        return True, f"external {key}: {value['status']}", value

    raise ValidationError(f"unsupported orientation requirement kind {kind!r}")


def generate_operation_kernel(cp, contract: OrientationContract, profile: KernelViewProfile) -> AuditedKernelSnapshot:
    base = cp.generate_kernel()
    coverage: Dict[str, Dict[str, Any]] = {}
    rendered = []
    covered = set()
    missing = set()

    ids = [r.requirement_id for r in contract.requirements]
    if len(ids) != len(set(ids)):
        raise ValidationError("orientation requirement IDs must be unique")

    for requirement in contract.requirements:
        if requirement.kind not in profile.included_kinds:
            coverage[requirement.requirement_id] = {
                "status": "OMITTED_BY_PROFILE",
                "kind": requirement.kind,
                "key": requirement.key,
            }
            missing.add(requirement.requirement_id)
            continue

        ok, line, value = _resolve_requirement(cp, requirement)
        if ok:
            coverage[requirement.requirement_id] = {
                "status": "COVERED",
                "kind": requirement.kind,
                "key": requirement.key,
                "value": value,
            }
            covered.add(requirement.requirement_id)
            rendered.append(f"- [{requirement.requirement_id}] {line}")
        else:
            coverage[requirement.requirement_id] = {
                "status": "UNRESOLVED_IN_STATE",
                "kind": requirement.kind,
                "key": requirement.key,
            }
            missing.add(requirement.requirement_id)

    markdown = "\n".join(
        [
            f"# Operation Kernel — {contract.operation}",
            "",
            f"contract_version: `{contract.version}`",
            f"contract_digest: `{contract.digest}`",
            f"projection_event_seq: `{base.projection_event_seq}`",
            f"projection_digest: `{base.projection_digest}`",
            "",
            "## Required orientation",
            *(rendered or ["- None rendered."]),
            "",
            "## Coverage status",
            f"covered: `{sorted(covered)}`",
            f"missing: `{sorted(missing)}`",
            "",
        ]
    )

    return AuditedKernelSnapshot(
        base_freshness=base,
        operation=contract.operation,
        contract_version=contract.version,
        contract_digest=contract.digest,
        covered_requirement_ids=frozenset(covered),
        missing_requirement_ids=frozenset(missing),
        coverage=coverage,
        markdown=markdown,
    )


def operation_kernel_is_fresh(cp, kernel: AuditedKernelSnapshot) -> bool:
    return cp.kernel_is_fresh(kernel.base_freshness)


def operation_kernel_is_sufficient(kernel: AuditedKernelSnapshot, contract: OrientationContract) -> bool:
    return kernel.contract_digest == contract.digest and not kernel.missing_requirement_ids
