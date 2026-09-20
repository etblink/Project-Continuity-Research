import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from prototype.ccp1.authority import (
    AuthorityControlPlane,
    AuthorizedTransitionRule,
    AuthorizationError,
    Principal,
)


class AuthoritySpoofingAttackTests(unittest.TestCase):
    def make_plane(self):
        cp = AuthorityControlPlane("P", "purpose")
        cp.authority_registry.register_principal(Principal("lead", kind="human"))
        cp.authority_registry.register_principal(Principal("worker", kind="agent"))
        cp.authority_registry.register_principal(Principal("reviewer", kind="human"))
        cp.authority_registry.bootstrap_grant(
            grant_id="grant-lead-root",
            actor_id="lead",
            role="PROJECT_LEAD",
            actions=["APPROVE_RELEASE", "GRANT_AUTHORITY"],
            scopes=["release:*"],
            authority_source="PROJECT_CHARTER",
        )
        cp.bootstrap_phase_state("release:v1", "CANDIDATE", authority_source="FROZEN_BASELINE")
        cp.bootstrap_phase_state("deploy:prod", "CANDIDATE", authority_source="FROZEN_BASELINE")
        cp.authority_registry.seal_bootstrap()
        cp.register_authorized_transition(
            AuthorizedTransitionRule(
                name="TAG_RELEASE",
                from_state="CANDIDATE",
                to_state="RELEASED",
                guards=(),
                required_action="APPROVE_RELEASE",
                scope="release:v1",
            )
        )
        return cp

    def test_spoofed_project_lead_label_is_rejected(self):
        cp = self.make_plane()
        with self.assertRaises(AuthorizationError):
            cp.request_authorized_transition(
                "TAG_RELEASE",
                subject="release:v1",
                actor_id="worker",
                claimed_role="PROJECT_LEAD",
            )
        self.assertEqual(cp.phase_state["release:v1"], "CANDIDATE")

    def test_valid_grant_allows_transition(self):
        cp = self.make_plane()
        event = cp.request_authorized_transition(
            "TAG_RELEASE",
            subject="release:v1",
            actor_id="lead",
            claimed_role="PROJECT_LEAD",
        )
        self.assertEqual(cp.phase_state["release:v1"], "RELEASED")
        self.assertEqual(event.payload["authority_grant_id"], "grant-lead-root")
        self.assertEqual(event.payload["authority_source"], "PROJECT_CHARTER")

    def test_real_role_wrong_scope_is_rejected(self):
        cp = self.make_plane()
        cp.register_authorized_transition(
            AuthorizedTransitionRule(
                name="DEPLOY_PROD",
                from_state="CANDIDATE",
                to_state="DEPLOYED",
                guards=(),
                required_action="APPROVE_RELEASE",
                scope="deploy:prod",
            )
        )
        with self.assertRaises(AuthorizationError):
            cp.request_authorized_transition(
                "DEPLOY_PROD",
                subject="deploy:prod",
                actor_id="lead",
                claimed_role="PROJECT_LEAD",
            )
        self.assertEqual(cp.phase_state["deploy:prod"], "CANDIDATE")

    def test_direct_material_event_bypass_is_rejected(self):
        cp = self.make_plane()
        with self.assertRaises(AuthorizationError):
            cp.append_event(
                "PHASE_STATE_SET",
                "release:v1",
                {"state": "RELEASED"},
                actor="worker",
                authority="PROJECT_LEAD",
            )
        self.assertEqual(cp.phase_state["release:v1"], "CANDIDATE")

    def test_unprivileged_actor_cannot_mint_authority(self):
        cp = self.make_plane()
        with self.assertRaises(AuthorizationError):
            cp.authority_registry.grant(
                grantor_actor_id="worker",
                grant_id="grant-reviewer",
                actor_id="reviewer",
                role="RELEASE_REVIEWER",
                actions=["APPROVE_RELEASE"],
                scopes=["release:v1"],
                authority_source="DELEGATION",
            )

    def test_authorized_delegation_can_mint_bounded_authority(self):
        cp = self.make_plane()
        cp.authority_registry.grant(
            grantor_actor_id="lead",
            grant_id="grant-reviewer",
            actor_id="reviewer",
            role="RELEASE_REVIEWER",
            actions=["APPROVE_RELEASE"],
            scopes=["release:v1"],
            authority_source="PROJECT_LEAD_DELEGATION",
        )
        event = cp.request_authorized_transition(
            "TAG_RELEASE",
            subject="release:v1",
            actor_id="reviewer",
            claimed_role="PROJECT_LEAD",
        )
        self.assertEqual(event.payload["authority_role"], "RELEASE_REVIEWER")
        self.assertEqual(event.payload["claimed_role"], "PROJECT_LEAD")
        self.assertEqual(cp.phase_state["release:v1"], "RELEASED")

    def test_revoked_grant_no_longer_authorizes(self):
        cp = self.make_plane()
        cp.authority_registry.grant(
            grantor_actor_id="lead",
            grant_id="grant-reviewer",
            actor_id="reviewer",
            role="RELEASE_REVIEWER",
            actions=["APPROVE_RELEASE"],
            scopes=["release:v1"],
            authority_source="PROJECT_LEAD_DELEGATION",
        )
        cp.authority_registry.revoke(revoker_actor_id="lead", grant_id="grant-reviewer")
        with self.assertRaises(AuthorizationError):
            cp.request_authorized_transition(
                "TAG_RELEASE",
                subject="release:v1",
                actor_id="reviewer",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
