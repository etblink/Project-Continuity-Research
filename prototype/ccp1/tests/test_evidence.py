import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from prototype.ccp0.ccp import ValidationError
from prototype.ccp1.authority import AuthorizationError, Principal
from prototype.ccp1.evidence import (
    EvidenceControlPlane,
    EvidenceVerificationError,
    GitEvidenceBinding,
    GitObjectEvidenceAdapter,
    GitObservation,
)


GOOD_COMMIT = "a" * 40
GOOD_BLOB = "b" * 40


def good_binding(evidence_id="ev-1"):
    return GitEvidenceBinding(
        evidence_id=evidence_id,
        repository="etblink/example",
        revision=GOOD_COMMIT,
        path="artifact.md",
        expected_blob_sha=GOOD_BLOB,
    )


def adapter_for(observation):
    return GitObjectEvidenceAdapter(
        lambda repository, revision, path: observation
    )


def good_observation():
    return GitObservation(
        available=True,
        repository="etblink/example",
        resolved_commit_sha=GOOD_COMMIT,
        path="artifact.md",
        blob_sha=GOOD_BLOB,
    )


class EvidenceAuthenticityAttackTests(unittest.TestCase):
    def make_plane(self):
        cp = EvidenceControlPlane("P", "truthful evidence identity")
        cp.authority_registry.register_principal(Principal("lead", kind="human"))
        cp.authority_registry.register_principal(Principal("worker", kind="agent"))
        cp.authority_registry.bootstrap_grant(
            grant_id="lead-claims",
            actor_id="lead",
            role="PROJECT_LEAD",
            actions=["QUALIFY_CLAIM"],
            scopes=["claim:result"],
            authority_source="PROJECT_CHARTER",
        )
        cp.authority_registry.seal_bootstrap()
        return cp

    def test_wrong_repository_fails_verification(self):
        cp = self.make_plane()
        cp.register_git_evidence(good_binding())
        record = cp.verify_git_evidence(
            "ev-1",
            adapter_for(
                GitObservation(
                    available=True,
                    repository="attacker/other",
                    resolved_commit_sha=GOOD_COMMIT,
                    path="artifact.md",
                    blob_sha=GOOD_BLOB,
                )
            ),
        )
        self.assertEqual(record.status, "FAIL")
        self.assertFalse(record.checks["repository"])

    def test_wrong_commit_fails_verification(self):
        cp = self.make_plane()
        cp.register_git_evidence(good_binding())
        record = cp.verify_git_evidence(
            "ev-1",
            adapter_for(
                GitObservation(
                    available=True,
                    repository="etblink/example",
                    resolved_commit_sha="c" * 40,
                    path="artifact.md",
                    blob_sha=GOOD_BLOB,
                )
            ),
        )
        self.assertEqual(record.status, "FAIL")
        self.assertFalse(record.checks["commit"])

    def test_wrong_blob_fails_verification(self):
        cp = self.make_plane()
        cp.register_git_evidence(good_binding())
        record = cp.verify_git_evidence(
            "ev-1",
            adapter_for(
                GitObservation(
                    available=True,
                    repository="etblink/example",
                    resolved_commit_sha=GOOD_COMMIT,
                    path="artifact.md",
                    blob_sha="d" * 40,
                )
            ),
        )
        self.assertEqual(record.status, "FAIL")
        self.assertFalse(record.checks["blob"])

    def test_unavailable_object_fails_verification(self):
        cp = self.make_plane()
        cp.register_git_evidence(good_binding())
        record = cp.verify_git_evidence(
            "ev-1",
            adapter_for(GitObservation(available=False)),
        )
        self.assertEqual(record.status, "FAIL")
        self.assertFalse(record.checks["available"])

    def test_failed_or_unverified_evidence_cannot_qualify_claim(self):
        cp = self.make_plane()
        cp.register_git_evidence(good_binding("failed"))
        cp.verify_git_evidence(
            "failed",
            adapter_for(GitObservation(available=False)),
        )
        with self.assertRaises(EvidenceVerificationError):
            cp.qualify_claim_with_verified_evidence(
                "result", "PASS", evidence_ids=["failed"], actor_id="lead"
            )

        cp.register_git_evidence(good_binding("never-verified"))
        with self.assertRaises(EvidenceVerificationError):
            cp.qualify_claim_with_verified_evidence(
                "result", "PASS", evidence_ids=["never-verified"], actor_id="lead"
            )

    def test_direct_qualification_bypass_is_rejected(self):
        cp = self.make_plane()
        with self.assertRaises(EvidenceVerificationError):
            cp.append_event(
                "CLAIM_QUALIFIED",
                "result",
                {"value": "PASS"},
                actor="lead",
                authority="PROJECT_LEAD",
            )

    def test_exact_object_verifies_and_can_qualify_claim(self):
        cp = self.make_plane()
        cp.register_git_evidence(good_binding())
        record = cp.verify_git_evidence("ev-1", adapter_for(good_observation()))
        self.assertEqual(record.status, "PASS")

        event = cp.qualify_claim_with_verified_evidence(
            "result", "PASS", evidence_ids=["ev-1"], actor_id="lead"
        )
        self.assertEqual(cp.claims["result"]["value"], "PASS")
        self.assertEqual(
            event.payload["verification_digests"]["ev-1"],
            record.digest,
        )
        self.assertEqual(event.evidence_refs, ("ev-1",))

    def test_verification_digest_is_reproducible(self):
        cp = self.make_plane()
        cp.register_git_evidence(good_binding())
        adapter = adapter_for(good_observation())
        first = cp.verify_git_evidence("ev-1", adapter)
        second = cp.verify_git_evidence("ev-1", adapter)
        self.assertEqual(first.digest, second.digest)
        self.assertEqual(first.canonical(), second.canonical())

    def test_evidence_id_cannot_silently_rebind(self):
        cp = self.make_plane()
        cp.register_git_evidence(good_binding())
        changed = GitEvidenceBinding(
            evidence_id="ev-1",
            repository="etblink/example",
            revision="e" * 40,
            path="artifact.md",
            expected_blob_sha=GOOD_BLOB,
        )
        with self.assertRaises(ValidationError):
            cp.register_git_evidence(changed)

    def test_verified_evidence_still_requires_claim_authority(self):
        cp = self.make_plane()
        cp.register_git_evidence(good_binding())
        cp.verify_git_evidence("ev-1", adapter_for(good_observation()))
        with self.assertRaises(AuthorizationError):
            cp.qualify_claim_with_verified_evidence(
                "result", "PASS", evidence_ids=["ev-1"], actor_id="worker"
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
