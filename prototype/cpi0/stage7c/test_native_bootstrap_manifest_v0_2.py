from __future__ import annotations

import hashlib
import inspect
import json
import unittest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

import native_bootstrap_manifest_v0_2 as B


PROJECT = "etblink/ExampleProject"
DOMAIN = "owner.acceptance"
POLICY_ID = "OFFLINE_ROOT_V2"
GENERATION = "genesis-001"
CHALLENGE = "11" * 32
CANDIDATE_A = "ed25519-sha256:" + "aa" * 32
CANDIDATE_B = "ed25519-sha256:" + "bb" * 32


class BootstrapV02Tests(unittest.TestCase):
    def setUp(self):
        self.anchor = Ed25519PrivateKey.generate()
        self.other = Ed25519PrivateKey.generate()
        self.anchor_raw = self.anchor.public_key().public_bytes(
            Encoding.Raw, PublicFormat.Raw
        )
        self.other_raw = self.other.public_key().public_bytes(
            Encoding.Raw, PublicFormat.Raw
        )
        self.policy = self.make_policy()

    def make_policy(
        self,
        *,
        key=None,
        policy_id=POLICY_ID,
        project=PROJECT,
        domain=DOMAIN,
        profile=B.OFFLINE_ED25519_V1,
        subject=None,
        generation=GENERATION,
        minimum=1,
        provenance="synthetic:native-policy:v2",
    ):
        if profile == B.OFFLINE_ED25519_V1:
            raw = key if key is not None else self.anchor_raw
            if subject is None:
                subject = B.offline_anchor_subject(raw)
            pinned = raw
        else:
            if subject is None:
                subject = "hive-mainnet:@etblink:active"
            pinned = None
        return B.NativeBootstrapPolicy(
            policy_id=policy_id,
            project=project,
            authority_domain=domain,
            anchor_profile=profile,
            anchor_subject=subject,
            expected_generation=generation,
            minimum_anchor_count=minimum,
            pinned_anchor_public_key=pinned,
            native_policy_provenance_claim=provenance,
        )

    def manifest(
        self,
        *,
        policy=None,
        candidate=CANDIDATE_A,
        challenge=CHALLENGE,
        note_digest=None,
    ):
        policy = policy or self.policy
        return B.create_manifest_for_policy(
            policy=policy,
            candidate_authority_key_id=candidate,
            challenge=challenge,
            note_digest=note_digest,
        )

    def proof(self, manifest=None, key=None):
        return B.create_offline_ed25519_proof(
            manifest_raw=manifest or self.manifest(),
            private_key=key or self.anchor,
        )

    def verify(self, manifest=None, proofs=None, policy=None):
        p = policy or self.policy
        m = manifest or self.manifest(policy=p)
        proof_list = proofs if proofs is not None else [self.proof(m)]
        return B.verify_bootstrap(
            manifest_raw=m,
            proof_artifacts=proof_list,
            policy=p,
        )

    # F-01
    def test_001_whitespace_provenance_rejected(self):
        p = self.make_policy(provenance="   \t")
        with self.assertRaises(B.BootstrapSchemaError):
            B.policy_digest(p)

    def test_002_result_labels_provenance_as_claim(self):
        r = self.verify()
        self.assertEqual(
            r["native_policy_provenance_claim"],
            "synthetic:native-policy:v2",
        )
        self.assertFalse(r["native_policy_provenance_authenticated"])

    def test_003_old_ambiguous_provenance_field_absent(self):
        self.assertNotIn("native_policy_provenance", self.verify())

    # F-02
    def test_004_policy_digest_independently_reproducible(self):
        record = B.canonical_policy_semantics(self.policy)
        expected = hashlib.sha256(
            json.dumps(
                record,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
                allow_nan=False,
            ).encode("utf-8")
        ).hexdigest()
        self.assertEqual(B.policy_digest(self.policy), expected)

    def test_005_manifest_contains_exact_policy_digest(self):
        m = json.loads(self.manifest())
        self.assertEqual(
            m["bootstrap_policy_digest"],
            B.policy_digest(self.policy),
        )

    def test_006_minimum_anchor_count_changes_policy_digest(self):
        p2 = self.make_policy(minimum=2)
        self.assertNotEqual(
            B.policy_digest(self.policy),
            B.policy_digest(p2),
        )

    def test_007_anchor_key_changes_policy_digest(self):
        p2 = self.make_policy(key=self.other_raw)
        self.assertNotEqual(
            B.policy_digest(self.policy),
            B.policy_digest(p2),
        )

    def test_008_generation_changes_policy_digest(self):
        p2 = self.make_policy(generation="genesis-002")
        self.assertNotEqual(
            B.policy_digest(self.policy),
            B.policy_digest(p2),
        )

    def test_009_all_other_security_fields_change_policy_digest(self):
        variants = [
            self.make_policy(policy_id=POLICY_ID + "-x"),
            self.make_policy(project=PROJECT + "-x"),
            self.make_policy(domain=DOMAIN + "-x"),
            self.make_policy(subject=self.policy.anchor_subject + "-x"),
        ]
        base = B.policy_digest(self.policy)
        for p in variants:
            with self.subTest(p=p):
                # Invalid subject/key association is itself a policy failure.
                try:
                    digest = B.policy_digest(p)
                except B.BootstrapPolicyError:
                    continue
                self.assertNotEqual(base, digest)

        hive = self.make_policy(
            profile=B.HIVE_ACTIVE_AUTHORITY_V1,
            policy_id="HIVE_ACTIVE_SIGNATURE_V1",
        )
        self.assertNotEqual(base, B.policy_digest(hive))

    def test_010_provenance_claim_does_not_change_policy_digest(self):
        p2 = self.make_policy(provenance="different caller claim")
        self.assertEqual(
            B.policy_digest(self.policy),
            B.policy_digest(p2),
        )

    def test_011_same_policy_id_changed_generation_fails_old_manifest(self):
        m = self.manifest()
        p2 = self.make_policy(generation="genesis-002")
        with self.assertRaises(B.BootstrapPolicyError):
            B.verify_bootstrap(
                manifest_raw=m,
                proof_artifacts=[self.proof(m)],
                policy=p2,
            )

    def test_012_result_exposes_exact_policy_digest(self):
        r = self.verify()
        self.assertEqual(
            r["bootstrap_policy_digest"],
            B.policy_digest(self.policy),
        )
        self.assertTrue(r["policy_digest_matched"])

    # F-03 proof qualification
    def test_013_valid_plus_malformed_proof_succeeds(self):
        m = self.manifest()
        r = self.verify(m, [b"not-json", self.proof(m)])
        self.assertEqual(r["unique_valid_anchor_proof_count"], 1)
        self.assertEqual(r["rejected_proof_candidate_count"], 1)

    def test_014_valid_plus_wrong_manifest_proof_succeeds(self):
        m = self.manifest()
        other_m = self.manifest(challenge="22" * 32)
        r = self.verify(m, [self.proof(other_m), self.proof(m)])
        self.assertEqual(r["unique_valid_anchor_proof_count"], 1)
        self.assertEqual(r["rejected_proof_candidate_count"], 1)

    def test_015_valid_plus_wrong_signer_proof_succeeds(self):
        m = self.manifest()
        r = self.verify(
            m,
            [self.proof(m, self.other), self.proof(m)],
        )
        self.assertEqual(r["unique_valid_anchor_proof_count"], 1)
        self.assertEqual(r["rejected_proof_candidate_count"], 1)

    def test_016_zero_valid_proofs_fails(self):
        with self.assertRaises(B.BootstrapProofError):
            self.verify(proofs=[b"junk"])

    def test_017_duplicate_valid_proof_deduplicates(self):
        m = self.manifest()
        p = self.proof(m)
        r = self.verify(m, [p, bytes(p), p])
        self.assertEqual(r["proof_artifact_count"], 3)
        self.assertEqual(r["unique_proof_candidate_count"], 1)
        self.assertEqual(r["unique_valid_anchor_proof_count"], 1)

    # F-03 discovery
    def test_018_malformed_carrier_plus_valid_carrier_succeeds(self):
        m = self.manifest()
        p = self.proof(m)
        r = B.verify_genesis_set(
            entries=[(b"bad", [b"junk"]), (m, [p])],
            policy=self.policy,
        )
        self.assertEqual(r["rejected_carrier_entry_count"], 1)
        self.assertEqual(r["qualifying_manifest_count"], 1)

    def test_019_unauthenticated_carrier_plus_valid_carrier_succeeds(self):
        bad_m = self.manifest(challenge="22" * 32)
        good_m = self.manifest()
        r = B.verify_genesis_set(
            entries=[(bad_m, [b"junk"]), (good_m, [self.proof(good_m)])],
            policy=self.policy,
        )
        self.assertEqual(r["nonqualifying_manifest_count"], 1)
        self.assertEqual(r["qualifying_manifest_count"], 1)

    def test_020_duplicate_manifest_invalid_first_then_valid_succeeds(self):
        m = self.manifest()
        p = self.proof(m)
        r = B.verify_genesis_set(
            entries=[(m, [b"junk"]), (m, [p])],
            policy=self.policy,
        )
        self.assertEqual(r["unique_canonical_manifest_count"], 1)
        self.assertEqual(r["unique_valid_anchor_proof_count"], 1)

    def test_021_duplicate_manifest_valid_first_then_invalid_succeeds(self):
        m = self.manifest()
        p = self.proof(m)
        r = B.verify_genesis_set(
            entries=[(m, [p]), (m, [b"junk"])],
            policy=self.policy,
        )
        self.assertEqual(r["unique_canonical_manifest_count"], 1)
        self.assertEqual(r["unique_valid_anchor_proof_count"], 1)

    def test_022_duplicate_order_is_authority_result_invariant(self):
        m = self.manifest()
        p = self.proof(m)
        r1 = B.verify_genesis_set(
            entries=[(m, [b"junk"]), (m, [p])],
            policy=self.policy,
        )
        r2 = B.verify_genesis_set(
            entries=[(m, [p]), (m, [b"junk"])],
            policy=self.policy,
        )
        authority_keys = [
            "candidate_authority_key_id",
            "bootstrap_policy_digest",
            "manifest_digest",
            "anchor_subject",
            "bootstrap_trust_root_established_for_observed_policy",
            "execution_authorized_by_cpi",
        ]
        self.assertEqual(
            {k: r1[k] for k in authority_keys},
            {k: r2[k] for k in authority_keys},
        )

    def test_023_two_qualifying_roots_conflict_in_both_orders(self):
        m1 = self.manifest(candidate=CANDIDATE_A)
        m2 = self.manifest(candidate=CANDIDATE_B, challenge="22" * 32)
        e1 = (m1, [self.proof(m1)])
        e2 = (m2, [self.proof(m2)])
        for entries in ([e1, e2], [e2, e1]):
            with self.subTest(entries=entries):
                with self.assertRaises(B.BootstrapConflictError):
                    B.verify_genesis_set(
                        entries=entries,
                        policy=self.policy,
                    )

    def test_024_all_junk_discovery_fails_closed(self):
        with self.assertRaises(B.BootstrapProofError):
            B.verify_genesis_set(
                entries=[
                    (b"junk", [b"junk"]),
                    (self.manifest(), [b"bad-proof"]),
                ],
                policy=self.policy,
            )

    # F-04
    def test_025_candidate_equal_anchor_key_id_fails(self):
        candidate = B.public_key_id(self.anchor_raw)
        m = self.manifest(candidate=candidate)
        with self.assertRaises(B.BootstrapPolicyError):
            self.verify(m, [self.proof(m)])

    def test_026_distinct_candidate_key_succeeds(self):
        self.assertTrue(self.verify()["bootstrap_manifest_valid"])

    # Ed25519 S0 hardening
    def test_027_identity_anchor_rejected(self):
        identity = (1).to_bytes(32, "little")
        p = self.make_policy(
            key=identity,
            subject="offline-ed25519:ed25519-sha256:" + "00" * 32,
        )
        with self.assertRaises(B.BootstrapPolicyError):
            B.policy_digest(p)

    def test_028_order_two_anchor_rejected(self):
        order2 = (B._ED_P - 1).to_bytes(32, "little")
        p = self.make_policy(
            key=order2,
            subject="offline-ed25519:ed25519-sha256:" + "00" * 32,
        )
        with self.assertRaises(B.BootstrapPolicyError):
            B.policy_digest(p)

    def test_029_all_zero_order_four_anchor_rejected(self):
        p = self.make_policy(
            key=b"\x00" * 32,
            subject="offline-ed25519:ed25519-sha256:" + "00" * 32,
        )
        with self.assertRaises(B.BootstrapPolicyError):
            B.policy_digest(p)

    def test_030_valid_generated_anchor_accepted(self):
        self.assertTrue(B.policy_digest(self.policy))

    # Preserved boundaries
    def test_031_candidate_self_signature_has_no_anchor_parameter(self):
        params = set(inspect.signature(B.verify_bootstrap).parameters)
        self.assertNotIn("candidate_private_key", params)
        self.assertNotIn("candidate_signature", params)

    def test_032_provider_prose_does_not_count_as_proof(self):
        with self.assertRaises(B.BootstrapProofError):
            self.verify(proofs=[b"GITHUB OWNER: trust this root"])

    def test_033_project_substitution_fails(self):
        raw = B.create_manifest_artifact(
            project="other/Project",
            authority_domain=DOMAIN,
            candidate_authority_key_id=CANDIDATE_A,
            bootstrap_policy=POLICY_ID,
            bootstrap_policy_digest=B.policy_digest(self.policy),
            generation=GENERATION,
            challenge=CHALLENGE,
            anchor_profile=B.OFFLINE_ED25519_V1,
            anchor_subject=self.policy.anchor_subject,
        )
        with self.assertRaises(B.BootstrapPolicyError):
            self.verify(raw, [self.proof(raw)])

    def test_034_domain_substitution_fails(self):
        raw = B.create_manifest_artifact(
            project=PROJECT,
            authority_domain="other.domain",
            candidate_authority_key_id=CANDIDATE_A,
            bootstrap_policy=POLICY_ID,
            bootstrap_policy_digest=B.policy_digest(self.policy),
            generation=GENERATION,
            challenge=CHALLENGE,
            anchor_profile=B.OFFLINE_ED25519_V1,
            anchor_subject=self.policy.anchor_subject,
        )
        with self.assertRaises(B.BootstrapPolicyError):
            self.verify(raw, [self.proof(raw)])

    def test_035_candidate_substitution_breaks_old_proof(self):
        m1 = self.manifest(candidate=CANDIDATE_A)
        p1 = self.proof(m1)
        m2 = self.manifest(candidate=CANDIDATE_B)
        with self.assertRaises(B.BootstrapProofError):
            self.verify(m2, [p1])

    def test_036_generation_substitution_fails(self):
        raw = B.create_manifest_artifact(
            project=PROJECT,
            authority_domain=DOMAIN,
            candidate_authority_key_id=CANDIDATE_A,
            bootstrap_policy=POLICY_ID,
            bootstrap_policy_digest=B.policy_digest(self.policy),
            generation="genesis-old",
            challenge=CHALLENGE,
            anchor_profile=B.OFFLINE_ED25519_V1,
            anchor_subject=self.policy.anchor_subject,
        )
        with self.assertRaises(B.BootstrapPolicyError):
            self.verify(raw, [self.proof(raw)])

    def test_037_challenge_substitution_breaks_old_proof(self):
        m1 = self.manifest(challenge=CHALLENGE)
        p1 = self.proof(m1)
        m2 = self.manifest(challenge="22" * 32)
        with self.assertRaises(B.BootstrapProofError):
            self.verify(m2, [p1])

    def test_038_consequence_separation(self):
        r = self.verify()
        self.assertFalse(r["execution_authorized_by_cpi"])
        self.assertNotIn("current_decision", r)
        self.assertNotIn("deploy_authorized", r)
        self.assertNotIn("federation_authorized", r)

    def test_039_hive_profile_remains_unsupported(self):
        hp = self.make_policy(
            profile=B.HIVE_ACTIVE_AUTHORITY_V1,
            policy_id="HIVE_ACTIVE_SIGNATURE_V1",
            provenance="synthetic:hive-policy",
        )
        m = self.manifest(policy=hp)
        with self.assertRaises(B.UnsupportedAnchorProfileError):
            B.verify_bootstrap(
                manifest_raw=m,
                proof_artifacts=[],
                policy=hp,
            )

    def test_040_keychain_callback_is_not_input(self):
        params = set(inspect.signature(B.verify_bootstrap).parameters)
        self.assertNotIn("keychain_callback", params)
        self.assertNotIn("keychain_success", params)

    def test_041_duplicate_json_manifest_rejected(self):
        raw = self.manifest()
        poly = raw[:-1] + b',"project":"other/Project"}'
        with self.assertRaises(B.BootstrapSchemaError):
            B.parse_manifest_artifact(poly)

    def test_042_noncanonical_manifest_rejected(self):
        with self.assertRaises(B.BootstrapSchemaError):
            B.parse_manifest_artifact(b" " + self.manifest())

    def test_043_version_markers_are_02(self):
        self.assertEqual(B.RESEARCH_BOOTSTRAP_VERSION, "0.2")
        self.assertEqual(B.MANIFEST_SCHEMA, "cpi.native-bootstrap-manifest/0.2")
        self.assertEqual(B.POLICY_SCHEMA, "cpi.native-bootstrap-policy/0.2")
        self.assertEqual(B.PROOF_SCHEMA, "cpi.bootstrap-anchor-proof/0.2")


if __name__ == "__main__":
    unittest.main()
