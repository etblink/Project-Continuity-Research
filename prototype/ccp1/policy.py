from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional, Tuple
import hashlib
import json

from prototype.ccp0.ccp import ValidationError, TransitionRejected, claim_equals
from prototype.ccp1.authority import (
    AuthorityControlPlane,
    AuthorizedTransitionRule,
)


class PolicyAdmissionError(TransitionRejected):
    """Raised when a policy cannot be activated under the admission rules."""


@dataclass(frozen=True)
class PolicyTransitionSpec:
    name: str
    from_state: Optional[str]
    to_state: str
    required_action: str
    scope: str
    claim_guards: Tuple[Tuple[str, Any], ...] = ()

    def canonical(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "from_state": self.from_state,
            "to_state": self.to_state,
            "required_action": self.required_action,
            "scope": self.scope,
            "claim_guards": [list(x) for x in self.claim_guards],
        }


@dataclass(frozen=True)
class PolicySpec:
    policy_id: str
    version: str
    authority_source: str
    transitions: Tuple[PolicyTransitionSpec, ...]
    required_regressions: frozenset[str]

    def canonical(self) -> Dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "version": self.version,
            "authority_source": self.authority_source,
            "transitions": [x.canonical() for x in self.transitions],
            "required_regressions": sorted(self.required_regressions),
        }

    @property
    def digest(self) -> str:
        payload = json.dumps(
            self.canonical(), sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class PolicyRegressionCase:
    name: str
    transition_name: str
    current_state: str
    claims: Mapping[str, Any]
    expected_allowed: bool


class PolicyRegistry:
    def __init__(self) -> None:
        self._policies: Dict[Tuple[str, str], PolicySpec] = {}
        self._results: Dict[Tuple[str, str], Dict[str, Dict[str, Any]]] = {}

    def register(self, spec: PolicySpec) -> PolicySpec:
        if not spec.authority_source:
            raise ValidationError("policy authority_source is required")
        key = (spec.policy_id, spec.version)
        existing = self._policies.get(key)
        if existing is not None:
            if existing.digest == spec.digest:
                return existing
            raise ValidationError(
                f"policy identity {spec.policy_id}@{spec.version} already bound to digest {existing.digest}"
            )
        self._policies[key] = spec
        self._results[key] = {}
        return spec

    def get(self, policy_id: str, version: str) -> PolicySpec:
        return self._policies[(policy_id, version)]

    def evaluate_and_record_regression(
        self,
        policy_id: str,
        version: str,
        *,
        case: "PolicyRegressionCase",
        evidence: str,
    ) -> bool:
        key = (policy_id, version)
        if key not in self._policies:
            raise ValidationError(f"unknown policy {policy_id}@{version}")
        if not evidence:
            raise ValidationError("regression evidence is required")
        spec = self._policies[key]
        passed = run_policy_regression(spec, case)
        self._results[key][case.name] = {
            "passed": passed,
            "evidence": evidence,
            "expected_allowed": case.expected_allowed,
        }
        return passed

    def admission_status(self, policy_id: str, version: str) -> Tuple[bool, Tuple[str, ...]]:
        spec = self.get(policy_id, version)
        results = self._results[(policy_id, version)]
        missing_or_failed = tuple(
            sorted(
                name
                for name in spec.required_regressions
                if name not in results or not results[name]["passed"]
            )
        )
        return (not missing_or_failed, missing_or_failed)

    def result_snapshot(self, policy_id: str, version: str) -> Dict[str, Dict[str, Any]]:
        return dict(self._results[(policy_id, version)])


def evaluate_transition_semantics(
    spec: PolicySpec,
    *,
    transition_name: str,
    current_state: str,
    claims: Mapping[str, Any],
) -> bool:
    rules = [x for x in spec.transitions if x.name == transition_name]
    if len(rules) != 1:
        return False
    rule = rules[0]
    if rule.from_state is not None and current_state != rule.from_state:
        return False
    return all(claims.get(claim_id) == expected for claim_id, expected in rule.claim_guards)


def run_policy_regression(spec: PolicySpec, case: PolicyRegressionCase) -> bool:
    allowed = evaluate_transition_semantics(
        spec,
        transition_name=case.transition_name,
        current_state=case.current_state,
        claims=case.claims,
    )
    return allowed == case.expected_allowed


class PolicyControlPlane(AuthorityControlPlane):
    """Authority-aware control plane with explicit policy identity/admission."""

    def __init__(self, project: str, purpose: str):
        super().__init__(project, purpose, policy_version="ccp1-policy-bootstrap")
        self.policy_registry = PolicyRegistry()
        self._active_policy: Optional[PolicySpec] = None

    @property
    def active_policy(self) -> Optional[PolicySpec]:
        return self._active_policy

    def state_projection(self) -> Dict[str, Any]:
        projection = super().state_projection()
        if self._active_policy is None:
            projection["active_policy"] = None
        else:
            projection["active_policy"] = {
                "policy_id": self._active_policy.policy_id,
                "version": self._active_policy.version,
                "digest": self._active_policy.digest,
                "authority_source": self._active_policy.authority_source,
            }
        return projection

    def activate_policy(self, policy_id: str, version: str, *, actor_id: str) -> None:
        spec = self.policy_registry.get(policy_id, version)
        self.authority_registry.require(actor_id, "ACTIVATE_POLICY", f"policy:{policy_id}")
        ok, missing_or_failed = self.policy_registry.admission_status(policy_id, version)
        if not ok:
            raise PolicyAdmissionError(
                f"policy {policy_id}@{version} failed admission: {list(missing_or_failed)}"
            )
        if self._active_policy is not None:
            raise PolicyAdmissionError("this bounded prototype permits one policy activation per plane")

        for rule in spec.transitions:
            guards = tuple(claim_equals(claim_id, expected) for claim_id, expected in rule.claim_guards)
            self.register_authorized_transition(
                AuthorizedTransitionRule(
                    name=rule.name,
                    from_state=rule.from_state,
                    to_state=rule.to_state,
                    guards=guards,
                    required_action=rule.required_action,
                    scope=rule.scope,
                )
            )

        self._active_policy = spec
        self.policy_version = f"{spec.policy_id}@{spec.version}:{spec.digest[:12]}"
        super().append_event(
            "POLICY_ACTIVATED",
            f"{spec.policy_id}@{spec.version}",
            {
                "policy_id": spec.policy_id,
                "version": spec.version,
                "digest": spec.digest,
                "authority_source": spec.authority_source,
                "regressions": self.policy_registry.result_snapshot(policy_id, version),
            },
            actor=actor_id,
            authority="POLICY_ACTIVATOR",
        )

    def request_authorized_transition(self, rule_name: str, **kwargs):
        if self._active_policy is None:
            raise PolicyAdmissionError("no active policy")
        event = super().request_authorized_transition(rule_name, **kwargs)
        super().append_event(
            "POLICY_TRANSITION_BOUND",
            event.subject,
            {
                "transition_event_seq": event.seq,
                "policy_id": self._active_policy.policy_id,
                "version": self._active_policy.version,
                "digest": self._active_policy.digest,
                "authority_source": self._active_policy.authority_source,
            },
            actor=kwargs["actor_id"],
            authority="ACTIVE_POLICY_BINDING",
        )
        return event
