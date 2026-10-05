from __future__ import annotations

import base64
import copy
import inspect
import json
import unittest
import unicodedata

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

import authority_capsule_v0_1_1 as A


PROJECT = "etblink/HiVenues"
DOMAIN = "stage5d.owner_acceptance"
SUBJECT = "issue:374"
CANDIDATE = "pr:399"
REV_A = "a" * 40
REV_B = "b" * 40


class AuthorityCapsuleV011Tests(unittest.TestCase):
    def setUp(self):
        self.owner = Ed25519PrivateKey.generate()
        self.owner_pub = self.owner.public_key().public_bytes(
            Encoding.Raw, PublicFormat.Raw
        )
        self.automation = Ed25519PrivateKey.generate()
        self.automation_pub = self.automation.public_key().public_bytes(
            Encoding.Raw, PublicFormat.Raw
        )
        self.pin = A.PinnedAuthorityKey(
            public_key=self.owner_pub,
            project=PROJECT,
            authority_domain=DOMAIN,
            provenance_id="native-governance:owner-key",
            provenance_revision="sha256:" + "1" * 64,
        )

    def make_dict(
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

    def make(
        self,
        **kwargs,
    ):
        return A.serialize_capsule(self.make_dict(**kwargs))

    def verify(self, artifacts, *, rev=REV_A, pin=None):
        return A.verify_observed_chain(
            artifacts,
            pin or self.pin,
            expected_subject=SUBJECT,
            expected_candidate=CANDIDATE,
            expected_candidate_revision=rev,
        )

    def test_001_complete_pass_withdraw_is_observed_not_current(self):
        c1 = self.make_dict(decision="PASS")
        c2 = self.make_dict(
            seq=2,
            pred=A.capsule_digest(c1),
            decision="WITHDRAW",
        )
        r = self.verify([A.serialize_capsule(c1), A.serialize_capsule(c2)])
        self.assertEqual(r["latest_observed_decision"], "WITHDRAW")
        self.assertIsNone(r["current_decision"])
        self.assertEqual(r["completeness_status"], "NOT_ESTABLISHED")
        self.assertEqual(r["authority_state"], "OBSERVED_CHAIN_ONLY")

    def test_002_suppressed_withdraw_never_becomes_current_pass(self):
        c1 = self.make(decision="PASS")
        r = self.verify([c1])
        self.assertEqual(r["latest_observed_decision"], "PASS")
        self.assertIsNone(r["current_decision"])
        self.assertEqual(r["completeness_status"], "NOT_ESTABLISHED")

    def test_003_currentness_request_fails_even_for_complete_observed_chain(self):
        c1 = self.make(decision="PASS")
        with self.assertRaises(A.CapsuleCompletenessError):
            A.require_current_decision(self.verify([c1]))

    def test_004_currentness_request_fails_for_truncated_chain(self):
        c1 = self.make_dict(decision="PASS")
        c2 = self.make_dict(
            seq=2,
            pred=A.capsule_digest(c1),
            decision="WITHDRAW",
        )
        _ = c2
        with self.assertRaises(A.CapsuleCompletenessError):
            A.require_current_decision(self.verify([A.serialize_capsule(c1)]))

    def test_005_three_decision_chain_reports_latest_observed_withdraw(self):
        c1 = self.make_dict(decision="REJECT", rev=REV_A)
        c2 = self.make_dict(
            seq=2,
            pred=A.capsule_digest(c1),
            decision="PASS",
            rev=REV_B,
        )
        c3 = self.make_dict(
            seq=3,
            pred=A.capsule_digest(c2),
            decision="WITHDRAW",
            rev=REV_B,
        )
        r = self.verify(
            [A.serialize_capsule(c1), A.serialize_capsule(c2), A.serialize_capsule(c3)],
            rev=REV_B,
        )
        self.assertEqual(r["latest_observed_decision"], "WITHDRAW")
        self.assertIsNone(r["current_decision"])

    def test_006_suppressed_seq3_reports_only_observed_pass(self):
        c1 = self.make_dict(decision="REJECT", rev=REV_A)
        c2 = self.make_dict(
            seq=2,
            pred=A.capsule_digest(c1),
            decision="PASS",
            rev=REV_B,
        )
        r = self.verify(
            [A.serialize_capsule(c1), A.serialize_capsule(c2)],
            rev=REV_B,
        )
        self.assertEqual(r["latest_observed_decision"], "PASS")
        self.assertIsNone(r["current_decision"])
        self.assertEqual(r["verified_through_sequence"], 2)

    def test_007_full_owner_fork_fails_closed(self):
        c1 = self.make_dict(decision="HOLD")
        pred = A.capsule_digest(c1)
        c2a = self.make_dict(seq=2, pred=pred, decision="PASS")
        c2b = self.make_dict(seq=2, pred=pred, decision="REJECT")
        with self.assertRaises(A.CapsuleChainError):
            self.verify(list(map(A.serialize_capsule, [c1, c2a, c2b])))

    def test_008_withheld_fork_branch_does_not_claim_global_currentness(self):
        c1 = self.make_dict(decision="HOLD")
        c2a = self.make_dict(
            seq=2,
            pred=A.capsule_digest(c1),
            decision="PASS",
        )
        r = self.verify(list(map(A.serialize_capsule, [c1, c2a])))
        self.assertEqual(r["latest_observed_decision"], "PASS")
        self.assertIsNone(r["current_decision"])
        with self.assertRaises(A.CapsuleCompletenessError):
            A.require_current_decision(r)

    def test_009_duplicate_key_polyglot_is_rejected(self):
        c1 = self.make_dict(decision="PASS")
        c2 = self.make_dict(
            seq=2,
            pred=A.capsule_digest(c1),
            decision="WITHDRAW",
        )

        def members(c):
            return ",".join(
                json.dumps(k, ensure_ascii=False)
                + ":"
                + json.dumps(v, ensure_ascii=False, separators=(",", ":"))
                for k, v in c.items()
            )

        poly = ("{" + members(c2) + "," + members(c1) + "}").encode("utf-8")
        with self.assertRaises(A.CapsuleSchemaError):
            A.parse_capsule_artifact(poly)
        with self.assertRaises(A.CapsuleSchemaError):
            self.verify([A.serialize_capsule(c1), poly])

    def test_010_leading_whitespace_is_noncanonical(self):
        raw = self.make()
        with self.assertRaises(A.CapsuleSchemaError):
            A.parse_capsule_artifact(b" " + raw)

    def test_011_alternate_key_order_is_noncanonical(self):
        c = self.make_dict()
        raw = json.dumps(c, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        self.assertNotEqual(raw, A.serialize_capsule(c))
        with self.assertRaises(A.CapsuleSchemaError):
            A.parse_capsule_artifact(raw)

    def test_012_equivalent_string_escape_is_noncanonical(self):
        raw = self.make()
        altered = raw.replace(b'"decision":"PASS"', b'"decision":"\\u0050ASS"')
        self.assertNotEqual(raw, altered)
        with self.assertRaises(A.CapsuleSchemaError):
            A.parse_capsule_artifact(altered)

    def test_013_trailing_newline_is_noncanonical(self):
        with self.assertRaises(A.CapsuleSchemaError):
            A.parse_capsule_artifact(self.make() + b"\n")

    def test_014_exact_canonical_artifact_parses_and_verifies(self):
        raw = self.make()
        parsed = A.parse_capsule_artifact(raw)
        self.assertEqual(A.serialize_capsule(parsed), raw)
        r = self.verify([raw])
        self.assertTrue(r["capsule_chain_valid"])

    def test_015_utf8_bom_is_rejected(self):
        with self.assertRaises(A.CapsuleSchemaError):
            A.parse_capsule_artifact(b"\xef\xbb\xbf" + self.make())

    def test_016_malformed_utf8_is_capsule_error(self):
        with self.assertRaises(A.CapsuleError):
            A.parse_capsule_artifact(b"\xff")

    def test_017_float_and_nan_are_rejected(self):
        raw = self.make()
        with self.assertRaises(A.CapsuleSchemaError):
            A.parse_capsule_artifact(
                raw.replace(b'"sequence":1', b'"sequence":1.0')
            )
        with self.assertRaises(A.CapsuleSchemaError):
            A.parse_capsule_artifact(
                raw.replace(b'"sequence":1', b'"sequence":NaN')
            )

    def test_018_identity_pin_is_rejected(self):
        bad = A.PinnedAuthorityKey(
            public_key=(1).to_bytes(32, "little"),
            project=PROJECT,
            authority_domain=DOMAIN,
            provenance_id="bad",
            provenance_revision="bad",
        )
        with self.assertRaises(A.PinValidationError):
            A.validate_pin(bad)

    def test_019_noncanonical_point_pin_is_rejected(self):
        bad = A.PinnedAuthorityKey(
            public_key=(2**255 - 19).to_bytes(32, "little"),
            project=PROJECT,
            authority_domain=DOMAIN,
            provenance_id="bad",
            provenance_revision="bad",
        )
        with self.assertRaises(A.PinValidationError):
            A.validate_pin(bad)

    def test_020_wrong_well_formed_pin_rejects_target_signature(self):
        wrong = A.PinnedAuthorityKey(
            public_key=self.automation_pub,
            project=PROJECT,
            authority_domain=DOMAIN,
            provenance_id="other",
            provenance_revision="other",
        )
        with self.assertRaises(A.CapsuleSignatureError):
            self.verify([self.make()], pin=wrong)

    def test_021_pin_provenance_is_explicit_in_result(self):
        r = self.verify([self.make()])
        self.assertEqual(r["pin_provenance_id"], self.pin.provenance_id)
        self.assertEqual(
            r["pin_provenance_revision"],
            self.pin.provenance_revision,
        )
        self.assertEqual(
            len(r["pin_provenance_digest"]),
            64,
        )

    def test_022_foreign_valid_chain_injection_is_partitioned_not_forked(self):
        target = self.make()
        foreign = self.make(subject="issue:375")
        r = self.verify([target, foreign])
        self.assertEqual(r["latest_observed_decision"], "PASS")
        self.assertEqual(r["foreign_artifact_count"], 1)
        self.assertEqual(r["target_unique_capsule_count"], 1)

    def test_023_target_binding_forgery_still_fails_signature(self):
        forged = self.make(key=self.automation)
        with self.assertRaises(A.CapsuleSignatureError):
            self.verify([forged])

    def test_024_lone_surrogate_is_capsule_error(self):
        raw = self.make()
        altered = raw.replace(
            b'"candidate":"pr:399"',
            b'"candidate":"pr:\\ud800"',
        )
        with self.assertRaises(A.CapsuleError):
            A.parse_capsule_artifact(altered)

    def test_025_list_decision_is_capsule_error(self):
        raw = self.make()
        altered = raw.replace(b'"decision":"PASS"', b'"decision":["PASS"]')
        with self.assertRaises(A.CapsuleError):
            A.parse_capsule_artifact(altered)

    def test_026_huge_sequence_is_bounded_without_huge_range(self):
        raw = self.make()
        altered = raw.replace(
            b'"sequence":1',
            b'"sequence":9223372036854775808',
        )
        with self.assertRaises(A.CapsuleSchemaError):
            A.parse_capsule_artifact(altered)

    def test_027_unicode_normalization_is_exact_not_normalized(self):
        composed = "gate:caf\u00e9"
        decomposed = unicodedata.normalize("NFD", composed)
        raw = self.make(subject=composed)
        pin = self.pin
        with self.assertRaises(A.CapsuleChainError):
            A.verify_observed_chain(
                [raw],
                pin,
                expected_subject=decomposed,
                expected_candidate=CANDIDATE,
                expected_candidate_revision=REV_A,
            )

    def test_028_identifier_case_is_exact(self):
        raw = self.make(project="etblink/hivenues")
        with self.assertRaises(A.CapsuleChainError):
            self.verify([raw])

    def test_029_duplicate_identical_artifact_deduplicates(self):
        raw = self.make()
        r = self.verify([raw, raw, bytes(raw)])
        self.assertEqual(r["artifact_count"], 3)
        self.assertEqual(r["target_unique_capsule_count"], 1)

    def test_030_sequence_gap_fails(self):
        c1 = self.make_dict(decision="HOLD")
        c3 = self.make_dict(
            seq=3,
            pred=A.capsule_digest(c1),
            decision="PASS",
        )
        with self.assertRaises(A.CapsuleChainError):
            self.verify(list(map(A.serialize_capsule, [c1, c3])))

    def test_031_predecessor_mismatch_fails(self):
        c1 = self.make_dict(decision="HOLD")
        c2 = self.make_dict(seq=2, pred="0" * 64, decision="PASS")
        with self.assertRaises(A.CapsuleChainError):
            self.verify(list(map(A.serialize_capsule, [c1, c2])))

    def test_032_revision_a_pass_cannot_be_replayed_for_b(self):
        with self.assertRaises(A.CapsuleBindingError):
            self.verify([self.make(rev=REV_A)], rev=REV_B)

    def test_033_cross_project_is_not_target_chain(self):
        with self.assertRaises(A.CapsuleChainError):
            self.verify([self.make(project="other/Project")])

    def test_034_cross_domain_is_not_target_chain(self):
        with self.assertRaises(A.CapsuleChainError):
            self.verify([self.make(domain="other.domain")])

    def test_035_cross_subject_is_not_target_chain(self):
        with self.assertRaises(A.CapsuleChainError):
            self.verify([self.make(subject="issue:999")])

    def test_036_cross_candidate_is_not_target_chain(self):
        with self.assertRaises(A.CapsuleChainError):
            self.verify([self.make(candidate="pr:400")])

    def test_037_contextual_prose_is_not_a_capsule_artifact(self):
        with self.assertRaises(A.CapsuleSchemaError):
            self.verify([b"OWNER: PASS. Approved for merge."])

    def test_038_valid_observed_pass_never_authorizes_execution(self):
        r = self.verify([self.make(decision="PASS")])
        self.assertEqual(r["latest_observed_decision"], "PASS")
        self.assertFalse(r["execution_authorized_by_cpi"])
        self.assertIsNone(r["current_decision"])

    def test_039_public_verifier_has_no_github_owner_author_input(self):
        names = set(inspect.signature(A.verify_observed_chain).parameters)
        forbidden = {
            "owner",
            "author",
            "author_association",
            "github_user",
            "comment",
            "review",
        }
        self.assertFalse(names & forbidden)

    def test_040_deterministic_stage6m_vector_is_unchanged(self):
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

    def test_041_offline_preserved_canonical_bytes_replay(self):
        c1 = self.make_dict(decision="PASS")
        c2 = self.make_dict(
            seq=2,
            pred=A.capsule_digest(c1),
            decision="WITHDRAW",
        )
        preserved = [
            bytes(A.serialize_capsule(c1)),
            bytes(A.serialize_capsule(c2)),
        ]
        r = self.verify(preserved)
        self.assertEqual(r["latest_observed_decision"], "WITHDRAW")
        self.assertEqual(r["completeness_status"], "NOT_ESTABLISHED")

    def test_042_result_does_not_reuse_stage6m_current_style_key(self):
        r = self.verify([self.make()])
        self.assertNotIn("observed_decision", r)
        self.assertIn("latest_observed_decision", r)
        self.assertIsNone(r["current_decision"])


if __name__ == "__main__":
    unittest.main()
