import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from prototype.ccp0.ccp import ValidationError
from prototype.ccp1.durable_authority import (
    ActorAssertion,
    DurableAuthorityRegistry,
    DurableAuthorizationError,
    IdentityAssertionError,
)


TRUSTED = "oidc:test-authenticator"


def valid_assertion():
    return ActorAssertion(
        actor_id="lead",
        external_subject="sub:evan",
        authenticator_id=TRUSTED,
        verified=True,
        evidence_id="token-verification-1",
    )


class AuthorityDurabilityIdentityAttackTests(unittest.TestCase):
    def make_registry(self):
        reg = DurableAuthorityRegistry(trusted_authenticators=[TRUSTED])
        reg.register_principal(
            actor_id="lead",
            external_subject="sub:evan",
            kind="human",
        )
        reg.grant(
            grant_id="lead-release",
            actor_id="lead",
            role="PROJECT_LEAD",
            actions=["APPROVE_RELEASE"],
            scopes=["release:*"],
            authority_source="PROJECT_CHARTER",
            granted_by="BOOTSTRAP",
        )
        return reg

    def test_bare_actor_identity_is_rejected(self):
        reg = self.make_registry()
        with self.assertRaises(IdentityAssertionError):
            reg.authorize(
                "lead",
                action="APPROVE_RELEASE",
                scope="release:v1",
            )

    def test_unverified_assertion_is_rejected(self):
        reg = self.make_registry()
        assertion = ActorAssertion(
            actor_id="lead",
            external_subject="sub:evan",
            authenticator_id=TRUSTED,
            verified=False,
            evidence_id="token-verification-1",
        )
        with self.assertRaises(IdentityAssertionError):
            reg.authorize(
                assertion,
                action="APPROVE_RELEASE",
                scope="release:v1",
            )

    def test_untrusted_authenticator_is_rejected(self):
        reg = self.make_registry()
        assertion = ActorAssertion(
            actor_id="lead",
            external_subject="sub:evan",
            authenticator_id="self-asserted",
            verified=True,
            evidence_id="fake",
        )
        with self.assertRaises(IdentityAssertionError):
            reg.authorize(
                assertion,
                action="APPROVE_RELEASE",
                scope="release:v1",
            )

    def test_verified_subject_mismatch_is_rejected(self):
        reg = self.make_registry()
        assertion = ActorAssertion(
            actor_id="lead",
            external_subject="sub:someone-else",
            authenticator_id=TRUSTED,
            verified=True,
            evidence_id="token-verification-2",
        )
        with self.assertRaises(IdentityAssertionError):
            reg.authorize(
                assertion,
                action="APPROVE_RELEASE",
                scope="release:v1",
            )

    def test_unknown_principal_cannot_receive_grant(self):
        reg = DurableAuthorityRegistry(trusted_authenticators=[TRUSTED])
        with self.assertRaises(ValidationError):
            reg.grant(
                grant_id="ghost",
                actor_id="ghost",
                role="PROJECT_LEAD",
                actions=["APPROVE_RELEASE"],
                scopes=["release:*"],
                authority_source="PROJECT_CHARTER",
                granted_by="BOOTSTRAP",
            )

    def test_principal_external_subject_cannot_silently_rebind(self):
        reg = self.make_registry()
        with self.assertRaises(ValidationError):
            reg.register_principal(
                actor_id="lead",
                external_subject="sub:attacker",
                kind="human",
            )

    def test_active_grant_and_digest_survive_replay(self):
        reg = self.make_registry()
        before = reg.authority_digest()
        rebuilt = DurableAuthorityRegistry.replay(
            reg.events,
            trusted_authenticators=[TRUSTED],
        )
        after = rebuilt.authority_digest()
        self.assertEqual(before, after)
        grant = rebuilt.authorize(
            valid_assertion(),
            action="APPROVE_RELEASE",
            scope="release:v1",
        )
        self.assertEqual(grant.grant_id, "lead-release")
        self.assertTrue(grant.active)

    def test_revoked_grant_stays_revoked_after_replay(self):
        reg = self.make_registry()
        reg.revoke("lead-release", revoked_by="security-review")
        rebuilt = DurableAuthorityRegistry.replay(
            reg.events,
            trusted_authenticators=[TRUSTED],
        )
        with self.assertRaises(DurableAuthorizationError):
            rebuilt.authorize(
                valid_assertion(),
                action="APPROVE_RELEASE",
                scope="release:v1",
            )
        grant = {g.grant_id: g for g in rebuilt.grants}["lead-release"]
        self.assertFalse(grant.active)

    def test_valid_identity_loses_authority_immediately_after_revocation(self):
        reg = self.make_registry()
        assertion = valid_assertion()
        self.assertEqual(
            reg.authorize(
                assertion,
                action="APPROVE_RELEASE",
                scope="release:v1",
            ).grant_id,
            "lead-release",
        )
        reg.revoke("lead-release", revoked_by="security-review")
        with self.assertRaises(DurableAuthorizationError):
            reg.authorize(
                assertion,
                action="APPROVE_RELEASE",
                scope="release:v1",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
