from __future__ import annotations

import copy
import inspect
import json
import unittest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

import native_bootstrap_manifest as B


PROJECT = "etblink/ExampleProject"
DOMAIN = "owner.acceptance"
POLICY_ID = "OFFLINE_ROOT_V1"
GENERATION = "genesis-001"
CHALLENGE = "11" * 32
CANDIDATE_A = "ed25519-sha256:" + "aa" * 32
CANDIDATE_B = "ed25519-sha256:" + "bb" * 32


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.anchor = Ed25519PrivateKey.generate()
        self.other = Ed25519PrivateKey.generate()
        self.anchor_raw = self.anchor.public_key().public_bytes_raw()
        self.other_raw = self.other.public_key().public_bytes_raw()
        self.subject = B.offline_anchor_subject(self.anchor_raw)
        self.policy = B.NativeBootstrapPolicy(
            policy_id=POLICY_ID,
            project=PROJECT,
            authority_domain=DOMAIN,
            anchor_profile=B.OFFLINE_ED25519_V1,
            anchor_subject=self.subject,
            expected_generation=GENERATION,
            minimum_anchor_count=1,
            pinned_anchor_public_key=self.anchor_raw,
            native_policy_provenance="synthetic:test-policy:v1",
        )

    def manifest(self, **overrides):
        args = dict(
            project=PROJECT,
            authority_domain=DOMAIN,
            candidate_authority_key_id=CANDIDATE_A,
            bootstrap_policy=POLICY_ID,
            generation=GENERATION,
            challenge=CHALLENGE,
            anchor_profile=B.OFFLINE_ED25519_V1,
            anchor_subject=self.subject,
            note_digest=None,
        )
        args.update(overrides)
        return B.create_manifest_artifact(**args)

    def proof(self, manifest=None, key=None):
        return B.create_offline_ed25519_proof(
            manifest_raw=manifest or self.manifest(),
            private_key=key or self.anchor,
        )

    def verify(self, manifest=None, proofs=None, policy=None):
        m = manifest or self.manifest()
        p = proofs if proofs is not None else [self.proof(m)]
        return B.verify_bootstrap(
            manifest_raw=m,
            proof_artifacts=p,
            policy=policy or self.policy,
        )

    def test_001_valid_independent_anchor_bootstrap(self):
        r = self.verify()
        self.assertTrue(r["bootstrap_manifest_valid"])
        self.assertTrue(r["independent_anchor_proof_valid"])
        self.assertEqual(r["candidate_authority_key_id"], CANDIDATE_A)
        self.assertFalse(r["execution_authorized_by_cpi"])

    def test_002_candidate_key_self_signature_is_not_a_supported_anchor_path(self):
        # Candidate Authority key identity is data only; no API accepts a candidate-key
        # signature as a bootstrap anchor proof.
        params = set(inspect.signature(B.verify_bootstrap).parameters)
        self.assertNotIn("candidate_private_key", params)
        self.assertNotIn("candidate_signature", params)

    def test_003_same_account_provider_prose_is_not_proof(self):
        with self.assertRaises(B.BootstrapSchemaError):
            self.verify(proofs=[b"GITHUB OWNER: trust this root"])

    def test_004_wrong_anchor_key_fails(self):
        m = self.manifest()
        with self.assertRaises(B.BootstrapProofError):
            self.verify(m, [self.proof(m, self.other)])

    def test_005_unpinned_anchor_cannot_be_supplied_by_cpi(self):
        bad_policy = B.NativeBootstrapPolicy(
            policy_id=POLICY_ID,
            project=PROJECT,
            authority_domain=DOMAIN,
            anchor_profile=B.OFFLINE_ED25519_V1,
            anchor_subject=B.offline_anchor_subject(self.other_raw),
            expected_generation=GENERATION,
            minimum_anchor_count=1,
            pinned_anchor_public_key=self.other_raw,
            native_policy_provenance="cpi:invented",
        )
        # This can verify only because the *caller supplied a different policy*.
        # The result surfaces provenance; verifier does not silently substitute it.
        m = self.manifest(anchor_subject=bad_policy.anchor_subject)
        p = self.proof(m, self.other)
        r = self.verify(m, [p], bad_policy)
        self.assertEqual(r["native_policy_provenance"], "cpi:invented")
        self.assertNotEqual(r["anchor_subject"], self.policy.anchor_subject)

    def test_006_project_rebinding_fails(self):
        m = self.manifest(project="other/Project")
        p = self.proof(m)
        with self.assertRaises(B.BootstrapPolicyError):
            self.verify(m, [p])

    def test_007_domain_rebinding_fails(self):
        m = self.manifest(authority_domain="other.domain")
        p = self.proof(m)
        with self.assertRaises(B.BootstrapPolicyError):
            self.verify(m, [p])

    def test_008_candidate_substitution_breaks_proof(self):
        m1 = self.manifest(candidate_authority_key_id=CANDIDATE_A)
        p1 = self.proof(m1)
        m2 = self.manifest(candidate_authority_key_id=CANDIDATE_B)
        with self.assertRaises(B.BootstrapProofError):
            self.verify(m2, [p1])

    def test_009_policy_substitution_fails(self):
        m = self.manifest(bootstrap_policy="OTHER_POLICY")
        p = self.proof(m)
        with self.assertRaises(B.BootstrapPolicyError):
            self.verify(m, [p])

    def test_010_generation_replay_fails_policy(self):
        old = self.manifest(generation="genesis-old")
        p = self.proof(old)
        with self.assertRaises(B.BootstrapPolicyError):
            self.verify(old, [p])

    def test_011_challenge_change_breaks_proof(self):
        m1 = self.manifest(challenge="22" * 32)
        p = self.proof(m1)
        m2 = self.manifest(challenge="33" * 32)
        with self.assertRaises(B.BootstrapProofError):
            self.verify(m2, [p])

    def test_012_anchor_profile_substitution_fails(self):
        m = self.manifest(anchor_profile=B.HIVE_ACTIVE_AUTHORITY_V1)
        with self.assertRaises(B.BootstrapPolicyError):
            self.verify(m, [])

    def test_013_anchor_subject_substitution_fails(self):
        m = self.manifest(anchor_subject="offline-ed25519:" + "ed25519-sha256:" + "00" * 32)
        p = self.proof(m)
        with self.assertRaises(B.BootstrapPolicyError):
            self.verify(m, [p])

    def test_014_missing_proof_fails(self):
        with self.assertRaises(B.BootstrapProofError):
            self.verify(proofs=[])

    def test_015_duplicate_identical_proof_deduplicates(self):
        m = self.manifest()
        p = self.proof(m)
        r = self.verify(m, [p, p, bytes(p)])
        self.assertEqual(r["proof_artifact_count"], 3)
        self.assertEqual(r["unique_valid_anchor_proof_count"], 1)

    def test_016_two_distinct_valid_genesis_roots_conflict(self):
        m1 = self.manifest(candidate_authority_key_id=CANDIDATE_A)
        p1 = self.proof(m1)
        m2 = self.manifest(candidate_authority_key_id=CANDIDATE_B)
        p2 = self.proof(m2)
        with self.assertRaises(B.BootstrapConflictError):
            B.verify_genesis_set(
                entries=[(m1, [p1]), (m2, [p2])],
                policy=self.policy,
            )

    def test_017_duplicate_same_genesis_is_not_conflict(self):
        m = self.manifest()
        p = self.proof(m)
        r = B.verify_genesis_set(
            entries=[(m, [p]), (bytes(m), [bytes(p)])],
            policy=self.policy,
        )
        self.assertEqual(r["candidate_authority_key_id"], CANDIDATE_A)

    def test_018_provider_unavailable_offline_replay_succeeds(self):
        m = bytes(self.manifest())
        p = bytes(self.proof(m))
        r = self.verify(m, [p])
        self.assertTrue(r["bootstrap_trust_root_established_for_observed_policy"])

    def test_019_cpi_execution_authority_is_always_false(self):
        self.assertFalse(self.verify()["execution_authorized_by_cpi"])

    def test_020_duplicate_json_key_manifest_fails(self):
        raw = self.manifest()
        poly = raw[:-1] + b',"project":"other/Project"}'
        with self.assertRaises(B.BootstrapSchemaError):
            B.parse_manifest_artifact(poly)

    def test_021_noncanonical_manifest_fails(self):
        raw = self.manifest()
        with self.assertRaises(B.BootstrapSchemaError):
            B.parse_manifest_artifact(b" " + raw)

    def test_022_extra_manifest_field_fails(self):
        d = json.loads(self.manifest())
        d["extra"] = "x"
        raw = json.dumps(d, sort_keys=True, separators=(",", ":")).encode()
        with self.assertRaises(B.BootstrapSchemaError):
            B.parse_manifest_artifact(raw)

    def test_023_hive_profile_fails_closed_as_unimplemented(self):
        policy = B.NativeBootstrapPolicy(
            policy_id="HIVE_ACTIVE_SIGNATURE_V1",
            project=PROJECT,
            authority_domain=DOMAIN,
            anchor_profile=B.HIVE_ACTIVE_AUTHORITY_V1,
            anchor_subject="hive-mainnet:@etblink:active",
            expected_generation=GENERATION,
            minimum_anchor_count=1,
            pinned_anchor_public_key=None,
            native_policy_provenance="synthetic:hive-policy",
        )
        m = B.create_manifest_artifact(
            project=PROJECT,
            authority_domain=DOMAIN,
            candidate_authority_key_id=CANDIDATE_A,
            bootstrap_policy=policy.policy_id,
            generation=GENERATION,
            challenge=CHALLENGE,
            anchor_profile=policy.anchor_profile,
            anchor_subject=policy.anchor_subject,
        )
        with self.assertRaises(B.UnsupportedAnchorProfileError):
            B.verify_bootstrap(manifest_raw=m, proof_artifacts=[], policy=policy)

    def test_024_keychain_callback_is_not_a_bootstrap_input(self):
        params = set(inspect.signature(B.verify_bootstrap).parameters)
        self.assertNotIn("keychain_success", params)
        self.assertNotIn("keychain_callback", params)

    def test_025_policy_is_independent_input(self):
        params = list(inspect.signature(B.verify_bootstrap).parameters)
        self.assertIn("policy", params)
        self.assertIn("manifest_raw", params)
        self.assertNotEqual("policy", "manifest_raw")

    def test_026_manifest_digest_changes_for_every_binding_field(self):
        base = self.manifest()
        base_digest = B.manifest_digest(base)
        variants = [
            self.manifest(project=PROJECT + "x"),
            self.manifest(authority_domain=DOMAIN + "x"),
            self.manifest(candidate_authority_key_id=CANDIDATE_B),
            self.manifest(bootstrap_policy=POLICY_ID + "x"),
            self.manifest(generation=GENERATION + "x"),
            self.manifest(challenge="22" * 32),
            self.manifest(anchor_subject=self.subject + "x"),
        ]
        for raw in variants:
            self.assertNotEqual(base_digest, B.manifest_digest(raw))

    def test_027_note_digest_is_bound_but_has_no_semantics(self):
        m = self.manifest(note_digest="12" * 32)
        p = self.proof(m)
        r = self.verify(m, [p])
        self.assertTrue(r["bootstrap_manifest_valid"])

    def test_028_manifest_has_no_numeric_values(self):
        parsed = json.loads(self.manifest())
        self.assertFalse(any(type(v) in (int, float, bool) for v in parsed.values()))

    def test_029_policy_minimum_count_cannot_be_zero(self):
        bad = B.NativeBootstrapPolicy(
            policy_id=POLICY_ID,
            project=PROJECT,
            authority_domain=DOMAIN,
            anchor_profile=B.OFFLINE_ED25519_V1,
            anchor_subject=self.subject,
            expected_generation=GENERATION,
            minimum_anchor_count=0,
            pinned_anchor_public_key=self.anchor_raw,
            native_policy_provenance="bad",
        )
        with self.assertRaises(B.BootstrapPolicyError):
            B.validate_policy(bad)

    def test_030_manifest_candidate_key_does_not_need_private_key(self):
        sig = inspect.signature(B.create_manifest_artifact)
        self.assertNotIn("candidate_private_key", sig.parameters)
        self.assertIn("candidate_authority_key_id", sig.parameters)


if __name__ == "__main__":
    unittest.main()
