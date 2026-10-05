from __future__ import annotations

import base64
import inspect
import json
import typing
import unittest

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

import authority_capsule_v0_1_2 as A


PROJECT = "etblink/HiVenues"
DOMAIN = "stage5d.owner_acceptance"
SUBJECT = "issue:374"
CANDIDATE = "pr:399"
REV_A = "a" * 40
REV_B = "b" * 40


class AuthorityCapsuleV012Tests(unittest.TestCase):
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
            provenance_id="native:owner-key",
            provenance_revision="rev:1",
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
        return A.sign_capsule_artifact(
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

    def verify(self, artifacts, *, rev=REV_A, pin=None):
        return A.verify_observed_chain(
            artifacts,
            pin or self.pin,
            expected_subject=SUBJECT,
            expected_candidate=CANDIDATE,
            expected_candidate_revision=rev,
        )

    def test_001_stage6m_vector_unchanged(self):
        key = Ed25519PrivateKey.from_private_bytes(bytes(range(32)))
        raw = A.sign_capsule_artifact(
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
        parsed = A.parse_capsule_artifact(raw)
        self.assertEqual(
            parsed["signer_key_id"],
            "ed25519-sha256:56475aa75463474c0285df5dbf2bcab73da651358839e9b77481b2eab107708c",
        )
        self.assertEqual(
            parsed["signature"],
            "EaEyWmU+y/o7pJ42NLBrJja5Ii6CMB040iDtfY25V32xo9C3kgwNVVUOCGRpp6OAezaQydjn6s4oV6uYlQFuBw==",
        )
        self.assertEqual(
            A.capsule_artifact_digest(raw),
            "f8e9c77a95b206a58d553200a58405075357c80a21f5ea72bb3c8e7808f0105b",
        )

    def test_002_public_api_declares_no_mapping_to_artifact_helper(self):
        forbidden = {
            "serialize_capsule",
            "canonical_envelope_bytes",
            "canonical_signed_bytes",
            "capsule_digest",
            "sign_capsule",
        }
        self.assertFalse(forbidden & set(A.__all__))
        for name in forbidden:
            self.assertFalse(hasattr(A, name))

    def test_003_public_authoring_takes_typed_fields_and_returns_bytes(self):
        raw = self.make()
        self.assertIs(type(raw), bytes)
        sig = inspect.signature(A.sign_capsule_artifact)
        self.assertNotIn("capsule", sig.parameters)
        self.assertNotIn("mapping", sig.parameters)

    def test_004_public_digest_accepts_canonical_bytes(self):
        raw = self.make()
        self.assertEqual(A.capsule_artifact_digest(raw), A.capsule_artifact_digest(bytes(raw)))

    def test_005_public_digest_rejects_mapping(self):
        parsed = A.parse_capsule_artifact(self.make())
        with self.assertRaises(A.CapsuleError):
            A.capsule_artifact_digest(parsed)

    def test_006_duplicate_key_polyglot_cannot_be_publicly_laundered(self):
        c1 = self.make(decision="PASS")
        c2 = self.make(
            seq=2,
            pred=A.capsule_artifact_digest(c1),
            decision="WITHDRAW",
        )
        d1, d2 = json.loads(c1), json.loads(c2)
        members = lambda d: ",".join(
            json.dumps(k) + ":" + json.dumps(d[k], ensure_ascii=False)
            for k in d
        )
        poly = ("{" + members(d2) + "," + members(d1) + "}").encode()
        with self.assertRaises(A.CapsuleError):
            self.verify([c1, poly])
        with self.assertRaises(A.CapsuleError):
            A.capsule_artifact_digest(poly)
        forbidden = {
            n for n in A.__all__
            if "serialize" in n or "canonical" in n
        }
        self.assertEqual(forbidden, set())

    def test_007_pin_requires_exact_raw_bytes(self):
        A.validate_pin(self.pin)
        bad = A.PinnedAuthorityKey(
            public_key=self.owner.public_key(),
            project=PROJECT,
            authority_domain=DOMAIN,
            provenance_id="p",
            provenance_revision="r",
        )
        with self.assertRaises(A.PinValidationError):
            A.validate_pin(bad)

    def test_008_other_pin_types_fail_in_error_hierarchy(self):
        for value in (
            bytearray(self.owner_pub),
            memoryview(self.owner_pub),
            self.owner_pub.hex(),
            None,
        ):
            bad = A.PinnedAuthorityKey(
                public_key=value,
                project=PROJECT,
                authority_domain=DOMAIN,
                provenance_id="p",
                provenance_revision="r",
            )
            with self.assertRaises(A.PinValidationError):
                A.validate_pin(bad)

    def test_009_valid_raw_pin_verifies(self):
        r = self.verify([self.make()])
        self.assertTrue(r["observed_chain_valid"])

    def test_010_result_uses_observed_chain_name_only(self):
        r = self.verify([self.make()])
        self.assertTrue(r["observed_chain_valid"])
        self.assertNotIn("capsule_chain_valid", r)
        self.assertEqual(r["authority_state"], "OBSERVED_CHAIN_ONLY")
        self.assertIsNone(r["current_decision"])
        self.assertEqual(r["completeness_status"], "NOT_ESTABLISHED")

    def test_011_currentness_helper_never_returns(self):
        hints = typing.get_type_hints(A.require_current_decision)
        self.assertIs(hints["return"], typing.NoReturn)
        with self.assertRaises(A.CapsuleCompletenessError):
            A.require_current_decision(self.verify([self.make()]))

    def test_012_pass_withdraw_complete_observed_chain(self):
        c1 = self.make(decision="PASS")
        c2 = self.make(
            seq=2,
            pred=A.capsule_artifact_digest(c1),
            decision="WITHDRAW",
        )
        r = self.verify([c1, c2])
        self.assertEqual(r["latest_observed_decision"], "WITHDRAW")
        self.assertIsNone(r["current_decision"])

    def test_013_suppressed_withdraw_never_becomes_current_pass(self):
        c1 = self.make(decision="PASS")
        r = self.verify([c1])
        self.assertEqual(r["latest_observed_decision"], "PASS")
        self.assertIsNone(r["current_decision"])
        self.assertEqual(r["completeness_status"], "NOT_ESTABLISHED")

    def test_014_duplicate_keys_rejected(self):
        raw = self.make()
        duplicate = raw[:-1] + b',"decision":"PASS"}'
        with self.assertRaises(A.CapsuleSchemaError):
            A.parse_capsule_artifact(duplicate)

    def test_015_php_style_solidus_escape_rejected(self):
        raw = self.make()
        altered = raw.replace(b"etblink/HiVenues", b"etblink\\/HiVenues")
        with self.assertRaises(A.CapsuleSchemaError):
            A.parse_capsule_artifact(altered)

    def test_016_go_style_html_escape_rejected(self):
        raw = self.make(subject="gate:<a&b>")
        altered = raw.replace(b"<a&b>", b"\\u003ca\\u0026b\\u003e")
        with self.assertRaises(A.CapsuleSchemaError):
            A.parse_capsule_artifact(altered)

    def test_017_u2028_escape_rejected_literal_is_canonical(self):
        raw = self.make(subject="gate:\u2028")
        self.assertIn("\u2028".encode("utf-8"), raw)
        altered = raw.replace("\u2028".encode("utf-8"), b"\\u2028")
        with self.assertRaises(A.CapsuleSchemaError):
            A.parse_capsule_artifact(altered)

    def test_018_control_short_escape_is_canonical(self):
        raw = self.make(subject="gate:\n")
        self.assertIn(b"gate:\\n", raw)
        altered = raw.replace(b"gate:\\n", b"gate:\\u000a")
        with self.assertRaises(A.CapsuleSchemaError):
            A.parse_capsule_artifact(altered)

    def test_019_control_hex_escape_is_lowercase(self):
        raw = self.make(subject="gate:\x1f")
        self.assertIn(b"gate:\\u001f", raw)
        altered = raw.replace(b"gate:\\u001f", b"gate:\\u001F")
        with self.assertRaises(A.CapsuleSchemaError):
            A.parse_capsule_artifact(altered)

    def test_020_del_is_literal(self):
        raw = self.make(subject="gate:\x7f")
        self.assertIn(b"gate:\x7f", raw)
        altered = raw.replace(b"gate:\x7f", b"gate:\\u007f")
        with self.assertRaises(A.CapsuleSchemaError):
            A.parse_capsule_artifact(altered)

    def test_021_bmp_and_supplementary_unicode_are_literal(self):
        raw = self.make(subject="gate:é中😀")
        self.assertIn("gate:é中😀".encode("utf-8"), raw)

    def test_022_quotes_and_backslash_have_ecmascript_escapes(self):
        raw = self.make(subject='gate:"\\')
        self.assertIn(b'gate:\\"\\\\', raw)

    def test_023_malformed_artifact_aborts_entire_set(self):
        good = self.make()
        bad = b"not-json"
        with self.assertRaises(A.CapsuleSchemaError):
            self.verify([good, bad])

    def test_024_forged_target_artifact_aborts(self):
        forged = self.make(key=self.automation)
        with self.assertRaises(A.CapsuleSignatureError):
            self.verify([forged])

    def test_025_valid_foreign_artifact_is_partitioned(self):
        target = self.make()
        foreign = self.make(subject="issue:999")
        r = self.verify([target, foreign])
        self.assertEqual(r["foreign_artifact_count"], 1)
        self.assertEqual(r["target_unique_capsule_count"], 1)

    def test_026_identity_pin_rejected(self):
        bad = A.PinnedAuthorityKey(
            public_key=(1).to_bytes(32, "little"),
            project=PROJECT,
            authority_domain=DOMAIN,
            provenance_id="bad",
            provenance_revision="bad",
        )
        with self.assertRaises(A.PinValidationError):
            A.validate_pin(bad)

    def test_027_wrong_valid_pin_rejected(self):
        wrong = A.PinnedAuthorityKey(
            public_key=self.automation_pub,
            project=PROJECT,
            authority_domain=DOMAIN,
            provenance_id="other",
            provenance_revision="other",
        )
        with self.assertRaises(A.CapsuleSignatureError):
            self.verify([self.make()], pin=wrong)

    def test_028_sequence_gap_fails_without_large_range(self):
        c1 = self.make(decision="HOLD")
        c3 = self.make(
            seq=3,
            pred=A.capsule_artifact_digest(c1),
            decision="PASS",
        )
        with self.assertRaises(A.CapsuleChainError):
            self.verify([c1, c3])

    def test_029_revision_replay_fails(self):
        with self.assertRaises(A.CapsuleBindingError):
            self.verify([self.make(rev=REV_A)], rev=REV_B)

    def test_030_contextual_prose_is_not_authority_input(self):
        with self.assertRaises(A.CapsuleSchemaError):
            self.verify([b"OWNER: PASS. Approved for merge."])

    def test_031_consequence_separation_remains_false(self):
        r = self.verify([self.make(decision="PASS")])
        self.assertFalse(r["execution_authorized_by_cpi"])
        self.assertIsNone(r["current_decision"])

    def test_032_no_github_identity_inputs_on_public_verifier(self):
        params = set(inspect.signature(A.verify_observed_chain).parameters)
        self.assertFalse(
            params & {
                "owner",
                "author",
                "author_association",
                "github_user",
                "review",
                "label",
                "issue_state",
                "comment",
            }
        )

    def test_033_pin_provenance_is_content_bound_not_authenticated(self):
        r1 = self.verify([self.make()])
        pin2 = A.PinnedAuthorityKey(
            public_key=self.owner_pub,
            project=PROJECT,
            authority_domain=DOMAIN,
            provenance_id="native:owner-key",
            provenance_revision="rev:2",
        )
        r2 = self.verify([self.make()], pin=pin2)
        self.assertNotEqual(
            r1["pin_provenance_digest"],
            r2["pin_provenance_digest"],
        )
        self.assertNotIn("pin_provenance_authenticated", r1)

    def test_034_public_surface_is_versioned_012(self):
        self.assertEqual(A.RESEARCH_VERIFIER_VERSION, "0.1.2")


if __name__ == "__main__":
    unittest.main()
