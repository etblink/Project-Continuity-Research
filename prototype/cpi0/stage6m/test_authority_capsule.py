from __future__ import annotations

import base64
import copy
import json
import unittest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

import authority_capsule as A


PROJECT = "etblink/HiVenues"
DOMAIN = "stage5d.owner_acceptance"
SUBJECT = "issue:374"
CANDIDATE = "pr:399"
REV_A = "a" * 40
REV_B = "b" * 40


class AuthorityCapsuleTests(unittest.TestCase):
    def setUp(self):
        self.owner = Ed25519PrivateKey.generate()
        self.owner_pub = self.owner.public_key().public_bytes(
            Encoding.Raw, PublicFormat.Raw
        )
        self.automation = Ed25519PrivateKey.generate()
        self.automation_pub = self.automation.public_key().public_bytes(
            Encoding.Raw, PublicFormat.Raw
        )

    def make(
        self,
        *,
        seq=1,
        pred=None,
        decision="PASS",
        rev=REV_A,
        key=None,
        project=PROJECT,
        domain=DOMAIN,
        subject=SUBJECT,
        candidate=CANDIDATE,
    ):
        return A.sign_capsule(
            private_key=key or self.owner,
            project=project,
            authority_domain=domain,
            subject=subject,
            candidate=candidate,
            candidate_revision=rev,
            sequence=seq,
            predecessor=pred,
            decision=decision,
        )

    def verify(self, capsules, *, rev=REV_A, pub=None):
        return A.verify_chain(
            capsules,
            pub or self.owner_pub,
            expected_project=PROJECT,
            expected_authority_domain=DOMAIN,
            expected_subject=SUBJECT,
            expected_candidate=CANDIDATE,
            expected_candidate_revision=rev,
        )

    def test_001_automation_prose_pass_is_not_authority_input(self):
        c1 = self.make(decision="HOLD")
        contextual_prose = "OWNER: PASS. Approved for merge."
        result = self.verify([c1])
        self.assertEqual(contextual_prose, "OWNER: PASS. Approved for merge.")
        self.assertEqual(result["observed_decision"], "HOLD")

    def test_002_structured_looking_record_without_owner_credential_fails(self):
        forged = self.make(key=self.automation)
        with self.assertRaises(A.CapsuleSignatureError):
            self.verify([forged])

    def test_003_edit_old_capsule_breaks_signature(self):
        c1 = self.make(decision="HOLD")
        c2 = self.make(
            seq=2,
            pred=A.capsule_digest(c1),
            decision="PASS",
        )
        edited = copy.deepcopy(c1)
        edited["decision"] = "PASS"
        with self.assertRaises(A.CapsuleSignatureError):
            self.verify([edited, c2])

    def test_004_resigned_old_capsule_breaks_successor_link(self):
        c1 = self.make(decision="HOLD")
        c2 = self.make(
            seq=2,
            pred=A.capsule_digest(c1),
            decision="PASS",
        )
        changed_c1 = self.make(decision="REJECT")
        with self.assertRaises(A.CapsuleChainError):
            self.verify([changed_c1, c2])

    def test_005_pass_then_withdraw_yields_withdraw(self):
        c1 = self.make(decision="PASS")
        c2 = self.make(
            seq=2,
            pred=A.capsule_digest(c1),
            decision="WITHDRAW",
        )
        result = self.verify([c2, c1])
        self.assertEqual(result["observed_decision"], "WITHDRAW")

    def test_006_revision_a_pass_replayed_for_revision_b_fails(self):
        c1 = self.make(decision="PASS", rev=REV_A)
        with self.assertRaises(A.CapsuleBindingError):
            self.verify([c1], rev=REV_B)

    def test_007_later_pass_for_revision_b_is_valid_for_b(self):
        c1 = self.make(decision="HOLD", rev=REV_A)
        c2 = self.make(
            seq=2,
            pred=A.capsule_digest(c1),
            decision="PASS",
            rev=REV_B,
        )
        result = self.verify([c1, c2], rev=REV_B)
        self.assertEqual(result["observed_decision"], "PASS")
        self.assertEqual(result["candidate_revision"], REV_B)

    def test_008_same_sequence_fork_fails(self):
        c1 = self.make(decision="HOLD")
        pred = A.capsule_digest(c1)
        c2a = self.make(seq=2, pred=pred, decision="PASS")
        c2b = self.make(seq=2, pred=pred, decision="REJECT")
        with self.assertRaises(A.CapsuleChainError):
            self.verify([c1, c2a, c2b])

    def test_009_exact_duplicate_replication_is_not_a_fork(self):
        c1 = self.make(decision="PASS")
        result = self.verify([c1, copy.deepcopy(c1)])
        self.assertEqual(result["observed_decision"], "PASS")

    def test_010_predecessor_mismatch_fails(self):
        c1 = self.make(decision="HOLD")
        c2 = self.make(seq=2, pred="0" * 64, decision="PASS")
        with self.assertRaises(A.CapsuleChainError):
            self.verify([c1, c2])

    def test_011_cross_project_copy_fails_binding(self):
        c1 = self.make(project="other/Project")
        with self.assertRaises(A.CapsuleBindingError):
            self.verify([c1])

    def test_012_wrong_pinned_key_fails(self):
        c1 = self.make()
        with self.assertRaises(A.CapsuleSignatureError):
            self.verify([c1], pub=self.automation_pub)

    def test_013_offline_json_replay_succeeds(self):
        c1 = self.make(decision="PASS")
        preserved = json.loads(json.dumps([c1]))
        result = self.verify(preserved)
        self.assertTrue(result["capsule_chain_valid"])
        self.assertEqual(result["observed_decision"], "PASS")

    def test_014_contextual_prose_never_changes_decision(self):
        c1 = self.make(decision="REJECT")
        prose = [
            "PASS",
            "Approved!",
            "I don't approve this yet.",
            "The gate is satisfied.",
            "not good to go",
        ]
        for _ in prose:
            result = self.verify([c1])
            self.assertEqual(result["observed_decision"], "REJECT")

    def test_015_valid_pass_never_authorizes_execution_by_cpi(self):
        c1 = self.make(decision="PASS")
        result = self.verify([c1])
        self.assertFalse(result["execution_authorized_by_cpi"])

    def test_016_signature_tamper_fails(self):
        c1 = self.make()
        raw = bytearray(base64.b64decode(c1["signature"]))
        raw[0] ^= 1
        c1["signature"] = base64.b64encode(bytes(raw)).decode("ascii")
        with self.assertRaises(A.CapsuleSignatureError):
            self.verify([c1])

    def test_017_malformed_base64_fails(self):
        c1 = self.make()
        c1["signature"] = "not base64!"
        with self.assertRaises(A.CapsuleSchemaError):
            self.verify([c1])

    def test_018_extra_field_fails(self):
        c1 = self.make()
        c1["comment"] = "PASS"
        with self.assertRaises(A.CapsuleSchemaError):
            self.verify([c1])

    def test_019_boolean_sequence_fails(self):
        c1 = self.make()
        c1["sequence"] = True
        with self.assertRaises(A.CapsuleSchemaError):
            self.verify([c1])

    def test_020_float_sequence_fails(self):
        c1 = self.make()
        c1["sequence"] = 1.0
        with self.assertRaises(A.CapsuleSchemaError):
            self.verify([c1])

    def test_021_unknown_decision_fails(self):
        c1 = self.make()
        c1["decision"] = "APPROVED"
        with self.assertRaises(A.CapsuleSchemaError):
            self.verify([c1])

    def test_022_noncanonical_predecessor_fails(self):
        with self.assertRaises(A.CapsuleSchemaError):
            self.make(seq=2, pred="A" * 64, decision="PASS")

    def test_023_missing_sequence_fails(self):
        c1 = self.make()
        c3 = self.make(
            seq=3,
            pred=A.capsule_digest(c1),
            decision="PASS",
        )
        with self.assertRaises(A.CapsuleChainError):
            self.verify([c1, c3])

    def test_024_subject_rebinding_fails(self):
        c1 = self.make(subject="issue:999")
        with self.assertRaises(A.CapsuleBindingError):
            self.verify([c1])

    def test_025_candidate_rebinding_fails(self):
        c1 = self.make(candidate="pr:400")
        with self.assertRaises(A.CapsuleBindingError):
            self.verify([c1])

    def test_026_domain_rebinding_fails(self):
        c1 = self.make(domain="other.domain")
        with self.assertRaises(A.CapsuleBindingError):
            self.verify([c1])

    def test_027_note_digest_binds_note_hash_without_semantics(self):
        digest = A.note_digest("Human note: PASS because the candidate is ready.")
        c1 = A.sign_capsule(
            private_key=self.owner,
            project=PROJECT,
            authority_domain=DOMAIN,
            subject=SUBJECT,
            candidate=CANDIDATE,
            candidate_revision=REV_A,
            sequence=1,
            predecessor=None,
            decision="HOLD",
            note_digest_value=digest,
        )
        result = self.verify([c1])
        self.assertEqual(result["observed_decision"], "HOLD")
        self.assertEqual(c1["note_digest"], digest)

    def test_028_key_id_is_derived_from_pinned_raw_key(self):
        c1 = self.make()
        self.assertEqual(c1["signer_key_id"], A.public_key_id(self.owner_pub))

    def test_029_noncanonical_signature_base64_fails(self):
        c1 = self.make()
        c1["signature"] = c1["signature"].rstrip("=")
        with self.assertRaises(A.CapsuleSchemaError):
            self.verify([c1])

    def test_030_empty_chain_fails(self):
        with self.assertRaises(A.CapsuleChainError):
            self.verify([])

    def test_031_deterministic_ed25519_vector(self):
        key = Ed25519PrivateKey.from_private_bytes(bytes(range(32)))
        capsule = A.sign_capsule(
            private_key=key,
            project="example/project",
            authority_domain="owner.acceptance",
            subject="gate:1",
            candidate="candidate:alpha",
            candidate_revision="rev-001",
            sequence=1,
            predecessor=None,
            decision="PASS",
        )
        self.assertEqual(
            capsule["signer_key_id"],
            "ed25519-sha256:56475aa75463474c0285df5dbf2bcab73da651358839e9b77481b2eab107708c",
        )
        self.assertEqual(
            capsule["signature"],
            "EaEyWmU+y/o7pJ42NLBrJja5Ii6CMB040iDtfY25V32xo9C3kgwNVVUOCGRpp6OAezaQydjn6s4oV6uYlQFuBw==",
        )
        self.assertEqual(
            A.capsule_digest(capsule),
            "f8e9c77a95b206a58d553200a58405075357c80a21f5ea72bb3c8e7808f0105b",
        )


if __name__ == "__main__":
    unittest.main()
