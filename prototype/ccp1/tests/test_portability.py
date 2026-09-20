import sys
import unittest
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from prototype.ccp0.ccp import ValidationError
from prototype.ccp1.authority import AuthorizationError
from prototype.ccp1.kernel_omission import (
    KernelViewProfile,
    generate_operation_kernel,
    operation_kernel_is_fresh,
    operation_kernel_is_sufficient,
)
from prototype.ccp1.portability import PortableProjectProfile, instantiate_profile


PROFILES = (
    PortableProjectProfile(
        profile_id="software-release",
        purpose="ship a qualified software release",
        phase_subject="release:v1",
        from_state="CANDIDATE",
        to_state="RELEASED",
        transition_name="TAG_RELEASE",
        required_action="APPROVE_RELEASE",
        authority_scope="release:v1",
        held_route="production-deploy",
        hold_basis="deployment is separately gated",
    ),
    PortableProjectProfile(
        profile_id="research-adjudication",
        purpose="adjudicate a bounded research claim",
        phase_subject="finding:alpha",
        from_state="UNDER_REVIEW",
        to_state="ADJUDICATED",
        transition_name="ADJUDICATE_FINDING",
        required_action="ADJUDICATE",
        authority_scope="finding:alpha",
        held_route="stronger-promotion",
        hold_basis="stronger claim lacks its separate burden",
    ),
    PortableProjectProfile(
        profile_id="editorial-publication",
        purpose="publish an editorial artifact with bounded authority",
        phase_subject="article:one",
        from_state="DRAFT",
        to_state="PUBLISHED",
        transition_name="PUBLISH_ARTICLE",
        required_action="PUBLISH",
        authority_scope="article:one",
        held_route="third-party-media",
        hold_basis="third-party media clearance is unresolved",
    ),
    PortableProjectProfile(
        profile_id="q7",
        purpose="p9",
        phase_subject="s4",
        from_state="x1",
        to_state="x2",
        transition_name="t6",
        required_action="a3",
        authority_scope="z8",
        held_route="r5",
        hold_basis="b2",
    ),
)


class ProjectAgnosticPortabilityAttackTests(unittest.TestCase):
    def test_all_profiles_use_same_engine_and_reach_sufficient_orientation(self):
        engine_types = set()
        for profile in PROFILES:
            instance = instantiate_profile(profile)
            engine_types.add(type(instance.plane))
            kernel = instance.generate_operation_kernel()
            self.assertTrue(operation_kernel_is_fresh(instance.plane, kernel))
            self.assertTrue(
                operation_kernel_is_sufficient(
                    kernel,
                    instance.orientation_contract,
                )
            )
        self.assertEqual(len(engine_types), 1)

    def test_authorized_transition_works_in_every_profile(self):
        for profile in PROFILES:
            instance = instantiate_profile(profile)
            instance.plane.request_authorized_transition(
                profile.transition_name,
                subject=profile.phase_subject,
                actor_id="lead",
            )
            self.assertEqual(
                instance.plane.phase_state[profile.phase_subject],
                profile.to_state,
            )

    def test_unauthorized_actor_fails_in_every_profile(self):
        for profile in PROFILES:
            instance = instantiate_profile(profile)
            with self.assertRaises(AuthorizationError):
                instance.plane.request_authorized_transition(
                    profile.transition_name,
                    subject=profile.phase_subject,
                    actor_id="worker",
                )
            self.assertEqual(
                instance.plane.phase_state[profile.phase_subject],
                profile.from_state,
            )

    def test_orientation_omitting_domain_held_route_is_insufficient(self):
        for profile in PROFILES:
            instance = instantiate_profile(profile)
            incomplete_view = KernelViewProfile(
                frozenset({"purpose", "phase", "policy", "authority"})
            )
            kernel = generate_operation_kernel(
                instance.plane,
                instance.orientation_contract,
                incomplete_view,
            )
            self.assertTrue(operation_kernel_is_fresh(instance.plane, kernel))
            self.assertFalse(
                operation_kernel_is_sufficient(
                    kernel,
                    instance.orientation_contract,
                )
            )
            self.assertIn("held-route", kernel.missing_requirement_ids)

    def test_opaque_profile_works_without_semantic_vocabulary(self):
        opaque = PROFILES[-1]
        instance = instantiate_profile(opaque)
        kernel = instance.generate_operation_kernel()
        self.assertTrue(
            operation_kernel_is_sufficient(kernel, instance.orientation_contract)
        )
        event = instance.plane.request_authorized_transition(
            opaque.transition_name,
            subject=opaque.phase_subject,
            actor_id="lead",
        )
        self.assertEqual(event.payload["state"], "x2")

    def test_profile_digest_is_deterministic_and_changes_with_semantics(self):
        p = PROFILES[0]
        self.assertEqual(p.digest, p.digest)
        changed = replace(p, to_state="ARCHIVED")
        self.assertNotEqual(p.digest, changed.digest)

    def test_missing_required_profile_field_is_rejected(self):
        bad = replace(PROFILES[0], required_action="")
        with self.assertRaises(ValidationError):
            instantiate_profile(bad)

    def test_cross_profile_state_does_not_leak(self):
        left = instantiate_profile(PROFILES[0])
        right = instantiate_profile(PROFILES[1])

        left_projection = repr(left.plane.state_projection())
        right_projection = repr(right.plane.state_projection())

        self.assertIn("release:v1", left_projection)
        self.assertNotIn("finding:alpha", left_projection)
        self.assertIn("finding:alpha", right_projection)
        self.assertNotIn("release:v1", right_projection)

    def test_profile_data_not_core_branching_controls_vocabulary(self):
        for profile in PROFILES:
            instance = instantiate_profile(profile)
            projection = instance.plane.state_projection()
            self.assertEqual(projection["project"], profile.profile_id)
            self.assertEqual(projection["purpose"], profile.purpose)
            self.assertIn(profile.phase_subject, projection["phase_state"])
            self.assertIn(profile.held_route, projection["routes"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
