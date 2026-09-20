import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from prototype.ccp1.authority import AuthorizationError, Principal
from prototype.ccp1.correction import CorrectionControlPlane, EventCorrectionError
from prototype.ccp1.evidence import (
    EvidenceVerificationError,
    GitEvidenceBinding,
    GitObjectEvidenceAdapter,
    GitObservation,
)


def binding(evidence_id, commit_char, blob_char):
    return GitEvidenceBinding(
        evidence_id=evidence_id,
        repository="etblink/evidence",
        revision=commit_char * 40,
        path=f"{evidence_id}.md",
        expected_blob_sha=blob_char * 40,
    )


def adapter_for(b):
    return GitObjectEvidenceAdapter(
        lambda repository, revision, path: GitObservation(
            available=True,
            repository=b.repository,
            resolved_commit_sha=b.revision,
            path=b.path,
            blob_sha=b.expected_blob_sha,
        )
    )


class AcceptedEventCorrectionAttackTests(unittest.TestCase):
    def make_plane(self):
        cp = CorrectionControlPlane("P", "truthful correction")
        cp.authority_registry.register_principal(Principal("lead", kind="human"))
        cp.authority_registry.register_principal(Principal("worker", kind="agent"))
        cp.authority_registry.bootstrap_grant(
            grant_id="lead-correction",
            actor_id="lead",
            role="PROJECT_LEAD",
            actions=["QUALIFY_CLAIM", "DISPUTE_EVENT", "INVALIDATE_EVENT"],
            scopes=["claim:result", "event:*"],
            authority_source="PROJECT_CHARTER",
        )
        cp.authority_registry.seal_bootstrap()

        claim_binding = binding("claim-evidence", "a", "b")
        correction_binding = binding("correction-evidence", "c", "d")
        for item in (claim_binding, correction_binding):
            cp.register_git_evidence(item)
            cp.verify_git_evidence(item.evidence_id, adapter_for(item))
        return cp

    def accepted_wrong_claim(self, cp):
        prior = cp.append_event(
            "CLAIM_SET",
            "result",
            {"value": "OLD"},
            actor="observer",
            authority="BASELINE",
        )
        wrong = cp.qualify_claim_with_verified_evidence(
            "result",
            "WRONG",
            evidence_ids=["claim-evidence"],
            actor_id="lead",
        )
        return prior, wrong

    def test_original_event_history_cannot_be_silently_deleted(self):
        cp = self.make_plane()
        _, wrong = self.accepted_wrong_claim(cp)
        before = len(cp.events)
        with self.assertRaises(AttributeError):
            cp.events.pop()
        self.assertEqual(len(cp.events), before)
        self.assertTrue(any(e.seq == wrong.seq for e in cp.events))

    def test_unauthorized_actor_cannot_invalidate(self):
        cp = self.make_plane()
        _, wrong = self.accepted_wrong_claim(cp)
        with self.assertRaises(AuthorizationError):
            cp.invalidate_claim_event(
                wrong.seq,
                reason="resolver proved wrong object",
                correction_evidence_ids=["correction-evidence"],
                actor_id="worker",
            )

    def test_invalidation_requires_verified_correction_evidence(self):
        cp = self.make_plane()
        _, wrong = self.accepted_wrong_claim(cp)
        with self.assertRaises(EvidenceVerificationError):
            cp.invalidate_claim_event(
                wrong.seq,
                reason="unsupported invalidation",
                correction_evidence_ids=[],
                actor_id="lead",
            )

    def test_unknown_event_cannot_be_invalidated(self):
        cp = self.make_plane()
        with self.assertRaises(EventCorrectionError):
            cp.invalidate_claim_event(
                9999,
                reason="unknown",
                correction_evidence_ids=["correction-evidence"],
                actor_id="lead",
            )

    def test_dispute_preserves_event_but_marks_effective_claim_unsettled(self):
        cp = self.make_plane()
        _, wrong = self.accepted_wrong_claim(cp)
        cp.dispute_claim_event(
            wrong.seq,
            reason="evidence identity challenged",
            actor_id="lead",
        )
        effective = cp.effective_claim("result")
        self.assertEqual(effective["value"], "WRONG")
        self.assertEqual(effective["status"], "DISPUTED")
        self.assertFalse(effective["settled"])
        self.assertTrue(any(e.seq == wrong.seq for e in cp.events))

    def test_invalidation_preserves_history_and_falls_back_to_prior_claim(self):
        cp = self.make_plane()
        prior, wrong = self.accepted_wrong_claim(cp)
        cp.dispute_claim_event(
            wrong.seq,
            reason="evidence identity challenged",
            actor_id="lead",
        )
        correction = cp.invalidate_claim_event(
            wrong.seq,
            reason="verified correction demonstrates wrong evidence object",
            correction_evidence_ids=["correction-evidence"],
            actor_id="lead",
        )
        effective = cp.effective_claim("result")
        self.assertEqual(effective["value"], "OLD")
        self.assertEqual(effective["event_seq"], prior.seq)
        self.assertTrue(any(e.seq == wrong.seq for e in cp.events))
        self.assertEqual(
            correction.payload["target_event_seq"],
            wrong.seq,
        )
        self.assertIn(
            "correction-evidence",
            correction.payload["verification_digests"],
        )

    def test_same_event_cannot_be_invalidated_twice(self):
        cp = self.make_plane()
        _, wrong = self.accepted_wrong_claim(cp)
        cp.invalidate_claim_event(
            wrong.seq,
            reason="verified correction",
            correction_evidence_ids=["correction-evidence"],
            actor_id="lead",
        )
        with self.assertRaises(EventCorrectionError):
            cp.invalidate_claim_event(
                wrong.seq,
                reason="repeat",
                correction_evidence_ids=["correction-evidence"],
                actor_id="lead",
            )

    def test_newer_independent_valid_claim_survives_older_invalidation(self):
        cp = self.make_plane()
        _, wrong = self.accepted_wrong_claim(cp)
        newer = cp.append_event(
            "CLAIM_SET",
            "result",
            {"value": "NEWER_VALID"},
            actor="independent-review",
            authority="INDEPENDENT_REVIEW",
        )
        cp.invalidate_claim_event(
            wrong.seq,
            reason="older claim invalid",
            correction_evidence_ids=["correction-evidence"],
            actor_id="lead",
        )
        effective = cp.effective_claim("result")
        self.assertEqual(effective["value"], "NEWER_VALID")
        self.assertEqual(effective["event_seq"], newer.seq)

    def test_public_claim_projection_is_correction_aware(self):
        cp = self.make_plane()
        _, wrong = self.accepted_wrong_claim(cp)
        cp.invalidate_claim_event(
            wrong.seq,
            reason="verified correction",
            correction_evidence_ids=["correction-evidence"],
            actor_id="lead",
        )
        self.assertEqual(cp.claims["result"]["value"], "OLD")
        projection = cp.state_projection()
        self.assertEqual(projection["claims"]["result"]["value"], "OLD")
        self.assertEqual(
            projection["event_corrections"][str(wrong.seq)]["status"],
            "INVALIDATED",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
