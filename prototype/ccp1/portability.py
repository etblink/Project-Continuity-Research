from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple
import hashlib
import json

from prototype.ccp0.ccp import ValidationError
from prototype.ccp1.authority import Principal
from prototype.ccp1.kernel_omission import (
    KernelViewProfile,
    OrientationContract,
    OrientationRequirement,
    generate_operation_kernel,
)
from prototype.ccp1.policy import PolicySpec, PolicyTransitionSpec
from prototype.ccp1.reopen import ReopenControlPlane


@dataclass(frozen=True)
class PortableProjectProfile:
    profile_id: str
    purpose: str
    phase_subject: str
    from_state: str
    to_state: str
    transition_name: str
    required_action: str
    authority_scope: str
    held_route: str
    hold_basis: str

    def validate(self) -> None:
        values = {
            "profile_id": self.profile_id,
            "purpose": self.purpose,
            "phase_subject": self.phase_subject,
            "from_state": self.from_state,
            "to_state": self.to_state,
            "transition_name": self.transition_name,
            "required_action": self.required_action,
            "authority_scope": self.authority_scope,
            "held_route": self.held_route,
            "hold_basis": self.hold_basis,
        }
        missing = [name for name, value in values.items() if not str(value).strip()]
        if missing:
            raise ValidationError(f"portable profile missing required fields: {missing}")
        if "|" in self.required_action or "|" in self.authority_scope:
            raise ValidationError("portable profile action/scope may not contain '|'")

    def canonical(self) -> Dict[str, str]:
        return {
            "profile_id": self.profile_id,
            "purpose": self.purpose,
            "phase_subject": self.phase_subject,
            "from_state": self.from_state,
            "to_state": self.to_state,
            "transition_name": self.transition_name,
            "required_action": self.required_action,
            "authority_scope": self.authority_scope,
            "held_route": self.held_route,
            "hold_basis": self.hold_basis,
        }

    @property
    def digest(self) -> str:
        self.validate()
        raw = json.dumps(
            self.canonical(), sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


@dataclass
class PortableProjectInstance:
    profile: PortableProjectProfile
    plane: ReopenControlPlane
    orientation_contract: OrientationContract

    def generate_operation_kernel(self):
        view = KernelViewProfile(
            frozenset({"purpose", "phase", "policy", "authority", "route"})
        )
        return generate_operation_kernel(
            self.plane,
            self.orientation_contract,
            view,
        )


def instantiate_profile(profile: PortableProjectProfile) -> PortableProjectInstance:
    """Instantiate one domain profile without domain-specific control-plane logic."""
    profile.validate()

    cp = ReopenControlPlane(profile.profile_id, profile.purpose)
    cp.authority_registry.register_principal(Principal("lead", kind="human"))
    cp.authority_registry.register_principal(Principal("worker", kind="agent"))
    cp.authority_registry.bootstrap_grant(
        grant_id=f"{profile.profile_id}:lead",
        actor_id="lead",
        role="PROJECT_LEAD",
        actions=["ACTIVATE_POLICY", profile.required_action],
        scopes=[f"policy:{profile.profile_id}", profile.authority_scope],
        authority_source=f"profile:{profile.profile_id}",
    )
    cp.bootstrap_phase_state(
        profile.phase_subject,
        profile.from_state,
        authority_source=f"profile:{profile.profile_id}:baseline",
    )
    cp.authority_registry.seal_bootstrap()

    policy = PolicySpec(
        policy_id=profile.profile_id,
        version="1.0.0",
        authority_source=f"profile:{profile.profile_id}:policy",
        transitions=(
            PolicyTransitionSpec(
                name=profile.transition_name,
                from_state=profile.from_state,
                to_state=profile.to_state,
                required_action=profile.required_action,
                scope=profile.authority_scope,
            ),
        ),
        required_regressions=frozenset(),
    )
    cp.policy_registry.register(policy)
    cp.activate_policy(policy.policy_id, policy.version, actor_id="lead")

    cp.append_event(
        "ROUTE_HELD",
        profile.held_route,
        {
            "basis": profile.hold_basis,
            "authority": f"profile:{profile.profile_id}:hold",
            "scope": profile.authority_scope,
            "reopen_requires": [],
        },
        actor="lead",
        authority=f"profile:{profile.profile_id}:hold",
    )

    contract = OrientationContract(
        operation=f"{profile.profile_id}:operation",
        version="1.0.0",
        requirements=(
            OrientationRequirement("purpose", "purpose"),
            OrientationRequirement("phase", "phase", profile.phase_subject),
            OrientationRequirement("policy", "policy"),
            OrientationRequirement(
                "authority",
                "authority",
                f"{profile.required_action}|{profile.authority_scope}",
            ),
            OrientationRequirement("held-route", "route", profile.held_route),
        ),
    )

    return PortableProjectInstance(
        profile=profile,
        plane=cp,
        orientation_contract=contract,
    )
