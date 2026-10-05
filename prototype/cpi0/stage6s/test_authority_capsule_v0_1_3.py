from __future__ import annotations

import hashlib
import inspect
import json
import typing
import unittest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

import authority_capsule_v0_1_3 as A


PROJECT = "etblink/HiVenues"
DOMAIN = "stage5d.owner_acceptance"
SUBJECT = "issue:374"
CANDIDATE = "pr:399"
REV_A = "a" * 40
REV_B = "b" * 40
MAX_SAFE = 2**53 - 1


class AuthorityCapsuleV013Tests(unittest.TestCase):
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

    def test_001_sequence_one_succeeds(self):
        self.assertEqual(A.parse_capsule_artifact(self.make(seq=1))["sequence"], 1)

    def test_002_max_safe_sequence_can_be_authored_and_parsed(self):
        raw = self.make(seq=MAX_SAFE, pred="0" * 64)
        self.assertEqual(A.parse_capsule_artifact(raw)["sequence"], MAX_SAFE)

    def test_003_two_to_53_is_rejected(self):
        with self.assertRaises(A.CapsuleSchemaError):
            self.make(seq=2**53, pred="0" * 64)

    def test_004_two_to_53_plus_one_is_rejected(self):
        with self.assertRaises(A.CapsuleSchemaError):
            self.make(seq=2**53 + 1, pred="0" * 64)

    def test_005_two_to_63_minus_one_is_rejected(self):
        with self.assertRaises(A.CapsuleSchemaError):
            self.make(seq=2**63 - 1, pred="0" * 64)

    def test_006_stage6m_vector_unchanged(self):
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

    def test_007_dead_stale_digest_helper_is_absent(self):
        self.assertFalse(hasattr(A, "_capsule_digest_mapping"))
        source = inspect.getsource(A)
        self.assertNotIn("__canonical_envelope_bytes", source)

    def test_008_authoring_signature_is_explicit_keyword_only(self):
        sig = inspect.signature(A.sign_capsule_artifact)
        expected = {
            "private_key", "project", "authority_domain", "subject", "candidate",
            "candidate_revision", "sequence", "predecessor", "decision",
            "note_digest_value",
        }
        self.assertEqual(set(sig.parameters), expected)
        self.assertTrue(all(
            p.kind is inspect.Parameter.KEYWORD_ONLY
            for p in sig.parameters.values()
        ))

    def test_009_unknown_authoring_keyword_is_call_contract_typeerror(self):
        with self.assertRaises(TypeError):
            A.sign_capsule_artifact(
                private_key=self.owner,
                project=PROJECT,
                authority_domain=DOMAIN,
                subject=SUBJECT,
                candidate=CANDIDATE,
                candidate_revision=REV_A,
                sequence=1,
                predecessor=None,
                decision="PASS",
                surprise=True,
            )

    def test_010_bad_field_value_is_capsule_error_after_entry(self):
        with self.assertRaises(A.CapsuleError):
            self.make(seq=True)

    def test_011_caller_iterator_error_propagates(self):
        def bad_iter():
            yield self.make()
            raise RuntimeError("caller iterator failed")
        with self.assertRaisesRegex(RuntimeError, "caller iterator failed"):
            self.verify(bad_iter())

    def test_012_foreign_binding_is_partitioned_without_target_auth(self):
        target = self.make()
        foreign_other_key = self.make(subject="issue:999", key=self.automation)
        r = self.verify([target, foreign_other_key])
        self.assertEqual(r["foreign_artifact_count"], 1)
        self.assertEqual(r["latest_observed_decision"], "PASS")

    def test_013_foreign_tally_is_not_authority(self):
        r = self.verify([self.make(), self.make(subject="issue:999", key=self.automation)])
        self.assertNotIn("foreign_authority", r)
        self.assertIsNone(r["current_decision"])

    def test_014_malformed_foreign_looking_artifact_aborts(self):
        with self.assertRaises(A.CapsuleSchemaError):
            self.verify([self.make(), b'{"project":"other"}'])

    def test_015_pin_provenance_digest_exact_record(self):
        expected_record = {
            "authority_domain": DOMAIN,
            "key_id": A.public_key_id(self.owner_pub),
            "project": PROJECT,
            "provenance_id": "native:owner-key",
            "provenance_revision": "rev:1",
        }
        expected_bytes = json.dumps(
            expected_record,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        self.assertEqual(
            A.pin_provenance_digest(self.pin),
            hashlib.sha256(expected_bytes).hexdigest(),
        )

    def test_016_pin_provenance_digest_changes_with_each_field(self):
        base = A.pin_provenance_digest(self.pin)
        variants = [
            A.PinnedAuthorityKey(self.automation_pub, PROJECT, DOMAIN, "native:owner-key", "rev:1"),
            A.PinnedAuthorityKey(self.owner_pub, PROJECT + "x", DOMAIN, "native:owner-key", "rev:1"),
            A.PinnedAuthorityKey(self.owner_pub, PROJECT, DOMAIN + "x", "native:owner-key", "rev:1"),
            A.PinnedAuthorityKey(self.owner_pub, PROJECT, DOMAIN, "native:owner-key-x", "rev:1"),
            A.PinnedAuthorityKey(self.owner_pub, PROJECT, DOMAIN, "native:owner-key", "rev:2"),
        ]
        for pin in variants:
            self.assertNotEqual(base, A.pin_provenance_digest(pin))

    def test_017_no_stale_011_currentness_text(self):
        source = inspect.getsource(A.require_current_decision)
        self.assertNotIn("0.1.1", source)
        self.assertNotIn("0.1.2", source)

    def test_018_currentness_helper_is_noreturn(self):
        self.assertIs(
            typing.get_type_hints(A.require_current_decision)["return"],
            typing.NoReturn,
        )
        with self.assertRaises(A.CapsuleCompletenessError):
            A.require_current_decision({})

    def test_019_pass_withdraw_remains_observed_only(self):
        c1 = self.make(decision="PASS")
        c2 = self.make(
            seq=2,
            pred=A.capsule_artifact_digest(c1),
            decision="WITHDRAW",
        )
        r = self.verify([c1, c2])
        self.assertTrue(r["observed_chain_valid"])
        self.assertEqual(r["latest_observed_decision"], "WITHDRAW")
        self.assertIsNone(r["current_decision"])
        self.assertEqual(r["completeness_status"], "NOT_ESTABLISHED")
        self.assertFalse(r["execution_authorized_by_cpi"])

    def test_020_suppressed_withdraw_never_becomes_current(self):
        r = self.verify([self.make(decision="PASS")])
        self.assertEqual(r["latest_observed_decision"], "PASS")
        self.assertIsNone(r["current_decision"])
        self.assertEqual(r["completeness_status"], "NOT_ESTABLISHED")

    def test_021_duplicate_key_polyglot_still_rejected(self):
        raw = self.make()
        poly = raw[:-1] + b',"decision":"PASS"}'
        with self.assertRaises(A.CapsuleSchemaError):
            self.verify([poly])
        with self.assertRaises(A.CapsuleSchemaError):
            A.capsule_artifact_digest(poly)

    def test_022_public_mapping_laundering_remains_closed(self):
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

    def test_023_raw_pin_contract_remains_closed(self):
        A.validate_pin(self.pin)
        for bad_value in (
            self.owner.public_key(),
            bytearray(self.owner_pub),
            memoryview(self.owner_pub),
            self.owner_pub.hex(),
            None,
        ):
            bad = A.PinnedAuthorityKey(
                public_key=bad_value,
                project=PROJECT,
                authority_domain=DOMAIN,
                provenance_id="p",
                provenance_revision="r",
            )
            with self.assertRaises(A.PinValidationError):
                A.validate_pin(bad)

    def test_024_no_github_identity_or_prose_authority_input(self):
        params = set(inspect.signature(A.verify_observed_chain).parameters)
        self.assertFalse(params & {
            "owner", "author", "author_association", "github_user",
            "review", "label", "issue_state", "comment",
        })
        with self.assertRaises(A.CapsuleSchemaError):
            self.verify([b"OWNER: PASS"])

    def test_025_consequence_separation_remains_false(self):
        r = self.verify([self.make()])
        self.assertFalse(r["execution_authorized_by_cpi"])

    def test_026_version_is_013(self):
        self.assertEqual(A.RESEARCH_VERIFIER_VERSION, "0.1.3")


if __name__ == "__main__":
    unittest.main()
