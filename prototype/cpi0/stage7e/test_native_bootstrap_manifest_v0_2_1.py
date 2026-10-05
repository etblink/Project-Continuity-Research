from __future__ import annotations

import itertools
import json
import unittest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

import native_bootstrap_manifest_v0_2_1 as B


PROJECT = "etblink/ExampleProject"
DOMAIN = "owner.acceptance"
POLICY_ID = "OFFLINE_ROOT_V2"
GENERATION = "genesis-001"
CHALLENGE_A = "11" * 32
CHALLENGE_B = "22" * 32
CANDIDATE_A = "ed25519-sha256:" + "aa" * 32
CANDIDATE_B = "ed25519-sha256:" + "bb" * 32
CANDIDATE_C = "ed25519-sha256:" + "cc" * 32


class Stage7EContentAddressedDiscoveryTests(unittest.TestCase):
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
        generation=GENERATION,
        provenance="synthetic:native-policy:v2",
    ):
        raw = key if key is not None else self.anchor_raw
        return B.NativeBootstrapPolicy(
            policy_id=policy_id,
            project=project,
            authority_domain=domain,
            anchor_profile=B.OFFLINE_ED25519_V1,
            anchor_subject=B.offline_anchor_subject(raw),
            expected_generation=generation,
            minimum_anchor_count=1,
            pinned_anchor_public_key=raw,
            native_policy_provenance_claim=provenance,
        )

    def manifest(
        self,
        *,
        candidate=CANDIDATE_A,
        challenge=CHALLENGE_A,
        policy=None,
    ):
        p = policy or self.policy
        return B.create_manifest_for_policy(
            policy=p,
            candidate_authority_key_id=candidate,
            challenge=challenge,
        )

    def proof(self, manifest, *, key=None):
        return B.create_offline_ed25519_proof(
            manifest_raw=manifest,
            private_key=key or self.anchor,
        )

    def verify(self, manifest, proofs, *, policy=None):
        return B.verify_bootstrap(
            manifest_raw=manifest,
            proof_artifacts=proofs,
            policy=policy or self.policy,
        )

    def discover(self, entries, *, policy=None):
        return B.verify_genesis_set(
            entries=entries,
            policy=policy or self.policy,
        )

    # N-01: content-addressed routing.
    def test_001_proof_beside_unrelated_manifest_routes_by_digest(self):
        m1 = self.manifest(candidate=CANDIDATE_A, challenge=CHALLENGE_A)
        m2 = self.manifest(candidate=CANDIDATE_B, challenge=CHALLENGE_B)
        p2 = self.proof(m2)
        r = self.discover([(m1, [p2]), (m2, [])])
        self.assertEqual(r["candidate_authority_key_id"], CANDIDATE_B)
        self.assertEqual(r["underproven_manifest_count"], 1)

    def test_002_proof_beside_noncanonical_copy_routes_to_canonical_manifest(self):
        m2 = self.manifest(candidate=CANDIDATE_B, challenge=CHALLENGE_B)
        p2 = self.proof(m2)
        r = self.discover([(m2 + b" ", [p2]), (m2, [])])
        self.assertEqual(r["candidate_authority_key_id"], CANDIDATE_B)
        self.assertGreaterEqual(r["rejected_carrier_entry_count"], 1)

    def test_003_proof_beside_malformed_manifest_routes_to_target(self):
        m2 = self.manifest(candidate=CANDIDATE_B, challenge=CHALLENGE_B)
        p2 = self.proof(m2)
        r = self.discover([(b"not-json", [p2]), (m2, [])])
        self.assertEqual(r["candidate_authority_key_id"], CANDIDATE_B)

    def test_004_proof_before_or_after_manifest_same_authority_result(self):
        m2 = self.manifest(candidate=CANDIDATE_B, challenge=CHALLENGE_B)
        p2 = self.proof(m2)
        a = self.discover([(b"junk", [p2]), (m2, [])])
        b = self.discover([(m2, []), (b"junk", [p2])])
        keys = (
            "candidate_authority_key_id",
            "manifest_digest",
            "bootstrap_policy_digest",
            "execution_authorized_by_cpi",
        )
        self.assertEqual({k: a[k] for k in keys}, {k: b[k] for k in keys})

    def test_005_duplicate_manifest_entries_pool_global_proofs(self):
        m = self.manifest()
        p = self.proof(m)
        r = self.discover([(m, []), (m, [b"junk"]), (m, [p])])
        self.assertEqual(r["unique_canonical_manifest_count"], 1)
        self.assertEqual(r["unique_valid_anchor_signer_count"], 1)

    def test_006_mispaired_second_root_still_creates_conflict(self):
        m1 = self.manifest(candidate=CANDIDATE_A, challenge=CHALLENGE_A)
        m2 = self.manifest(candidate=CANDIDATE_B, challenge=CHALLENGE_B)
        p1 = self.proof(m1)
        p2 = self.proof(m2)
        with self.assertRaises(B.BootstrapConflictError):
            self.discover([(m1, [p1, p2]), (m2, [])])

    def test_007_mixed_carrier_permutations_are_authority_invariant(self):
        m = self.manifest()
        p = self.proof(m)
        orphan_m = self.manifest(candidate=CANDIDATE_B, challenge=CHALLENGE_B)
        orphan_p = self.proof(orphan_m)
        entries = [
            (m, []),
            (b"bad", [p]),
            (b"bad2", [orphan_p]),
            (self.manifest(candidate=CANDIDATE_C, challenge="33" * 32), [b"junk"]),
        ]
        outcomes = set()
        for perm in itertools.permutations(entries):
            r = self.discover(list(perm))
            outcomes.add(
                (
                    r["candidate_authority_key_id"],
                    r["manifest_digest"],
                    r["bootstrap_policy_digest"],
                    r["execution_authorized_by_cpi"],
                )
            )
        self.assertEqual(len(outcomes), 1)

    def test_008_orphan_proof_without_manifest_is_nonqualifying(self):
        m = self.manifest()
        p = self.proof(m)
        with self.assertRaises(B.BootstrapProofError):
            self.discover([(b"bad", [p])])

    def test_009_orphan_proof_plus_valid_root_succeeds_and_is_counted(self):
        m1 = self.manifest()
        p1 = self.proof(m1)
        m2 = self.manifest(candidate=CANDIDATE_B, challenge=CHALLENGE_B)
        p2 = self.proof(m2)
        r = self.discover([(m1, [p1]), (b"bad", [p2])])
        self.assertEqual(r["candidate_authority_key_id"], CANDIDATE_A)
        self.assertEqual(r["orphan_proof_candidate_count"], 1)

    def test_010_forged_proof_routed_to_target_digest_does_not_qualify(self):
        m1 = self.manifest(candidate=CANDIDATE_A, challenge=CHALLENGE_A)
        m2 = self.manifest(candidate=CANDIDATE_B, challenge=CHALLENGE_B)
        p1 = json.loads(self.proof(m1))
        p1["manifest_digest"] = B.manifest_digest(m2)
        forged = json.dumps(
            p1, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()
        with self.assertRaises(B.BootstrapProofError):
            self.discover([(m2, []), (b"bad", [forged])])

    def test_011_one_root_plus_junk_and_orphan_succeeds(self):
        m = self.manifest()
        p = self.proof(m)
        orphan_m = self.manifest(candidate=CANDIDATE_B, challenge=CHALLENGE_B)
        orphan_p = self.proof(orphan_m)
        r = self.discover([
            (b"bad", [b"bad-proof"]),
            (m, [p]),
            (b"bad2", [orphan_p]),
        ])
        self.assertEqual(r["candidate_authority_key_id"], CANDIDATE_A)

    def test_012_two_genuinely_qualifying_roots_always_conflict(self):
        m1 = self.manifest(candidate=CANDIDATE_A, challenge=CHALLENGE_A)
        m2 = self.manifest(candidate=CANDIDATE_B, challenge=CHALLENGE_B)
        p1 = self.proof(m1)
        p2 = self.proof(m2)
        base = [(m1, []), (m2, []), (b"x", [p1]), (b"y", [p2])]
        for perm in itertools.permutations(base):
            with self.subTest(order=perm):
                with self.assertRaises(B.BootstrapConflictError):
                    self.discover(list(perm))

    def test_013_iterator_failure_after_valid_proof_preserves_yielded_proof(self):
        m = self.manifest()
        p = self.proof(m)

        def proofs():
            yield p
            raise RuntimeError("transport broke")

        r = self.discover([(m, proofs())])
        self.assertEqual(r["candidate_authority_key_id"], CANDIDATE_A)
        self.assertGreaterEqual(r["rejected_carrier_entry_count"], 1)

    # N-02: public key type contract.
    def test_014_public_key_id_bytearray_is_policy_error(self):
        with self.assertRaises(B.BootstrapPolicyError):
            B.public_key_id(bytearray(self.anchor_raw))

    def test_015_public_key_id_memoryview_is_policy_error(self):
        with self.assertRaises(B.BootstrapPolicyError):
            B.public_key_id(memoryview(self.anchor_raw))

    def test_016_public_key_id_string_is_policy_error(self):
        with self.assertRaises(B.BootstrapPolicyError):
            B.public_key_id(self.anchor_raw.hex())

    def test_017_public_key_id_none_is_policy_error(self):
        with self.assertRaises(B.BootstrapPolicyError):
            B.public_key_id(None)

    def test_018_public_key_id_valid_bytes_succeeds(self):
        self.assertTrue(B.public_key_id(self.anchor_raw).startswith("ed25519-sha256:"))

    # N-03: provenance safety and explicit scope.
    def test_019_provenance_newline_rejected(self):
        p = self.make_policy(provenance="owner\nverified")
        with self.assertRaises(B.BootstrapSchemaError):
            B.policy_digest(p)

    def test_020_provenance_nul_rejected(self):
        p = self.make_policy(provenance="owner\x00verified")
        with self.assertRaises(B.BootstrapSchemaError):
            B.policy_digest(p)

    def test_021_provenance_escape_rejected(self):
        p = self.make_policy(provenance="owner\x1bverified")
        with self.assertRaises(B.BootstrapSchemaError):
            B.policy_digest(p)

    def test_022_provenance_del_rejected(self):
        p = self.make_policy(provenance="owner\x7fverified")
        with self.assertRaises(B.BootstrapSchemaError):
            B.policy_digest(p)

    def test_023_provenance_over_512_scalars_rejected(self):
        p = self.make_policy(provenance="x" * 513)
        with self.assertRaises(B.BootstrapSchemaError):
            B.policy_digest(p)

    def test_024_safe_provenance_accepted_and_scope_explicit(self):
        m = self.manifest()
        r = self.verify(m, [self.proof(m)])
        self.assertEqual(r["trust_statement_scope"], "RELATIVE_TO_SUPPLIED_POLICY")
        self.assertFalse(r["native_policy_provenance_authenticated"])

    # N-04: signer dedup and diagnostics.
    def test_025_duplicate_valid_signer_counts_once(self):
        m = self.manifest()
        p = self.proof(m)
        r = self.verify(m, [p, p, bytes(p)])
        self.assertEqual(r["unique_valid_anchor_signer_count"], 1)
        self.assertEqual(r["unique_valid_anchor_proof_count"], 1)

    def test_026_invalid_proofs_do_not_add_signer_count(self):
        m = self.manifest()
        p = self.proof(m)
        wrong = self.proof(m, key=self.other)
        r = self.verify(m, [p, wrong, b"junk"])
        self.assertEqual(r["unique_valid_anchor_signer_count"], 1)

    def test_027_discovery_orphan_diagnostic(self):
        m = self.manifest()
        p = self.proof(m)
        om = self.manifest(candidate=CANDIDATE_B, challenge=CHALLENGE_B)
        op = self.proof(om)
        r = self.discover([(m, [p]), (b"junk", [op])])
        self.assertEqual(r["orphan_proof_candidate_count"], 1)

    def test_028_discovery_policy_mismatch_diagnostic(self):
        m = self.manifest()
        p = self.proof(m)
        other_policy = self.make_policy(project="other/Project")
        other_m = self.manifest(policy=other_policy, candidate=CANDIDATE_B)
        other_p = self.proof(other_m)
        r = self.discover([(m, [p]), (other_m, [other_p])])
        self.assertEqual(r["policy_mismatch_manifest_count"], 1)

    def test_029_discovery_underproven_diagnostic(self):
        m = self.manifest()
        p = self.proof(m)
        under = self.manifest(candidate=CANDIDATE_B, challenge=CHALLENGE_B)
        r = self.discover([(m, [p]), (under, [])])
        self.assertEqual(r["underproven_manifest_count"], 1)

    # Preserved F-01/F-02/F-04 and architecture boundaries.
    def test_030_policy_digest_binding_preserved(self):
        m = self.manifest()
        r = self.verify(m, [self.proof(m)])
        self.assertTrue(r["policy_digest_matched"])
        self.assertEqual(r["bootstrap_policy_digest"], B.policy_digest(self.policy))

    def test_031_provenance_remains_outside_policy_digest(self):
        p2 = self.make_policy(provenance="different safe claim")
        self.assertEqual(B.policy_digest(self.policy), B.policy_digest(p2))

    def test_032_candidate_equal_anchor_rejected(self):
        candidate = B.public_key_id(self.anchor_raw)
        m = self.manifest(candidate=candidate)
        with self.assertRaises(B.BootstrapPolicyError):
            self.verify(m, [self.proof(m)])

    def test_033_candidate_self_signature_is_not_anchor_input(self):
        import inspect
        params = set(inspect.signature(B.verify_bootstrap).parameters)
        self.assertNotIn("candidate_signature", params)
        self.assertNotIn("candidate_private_key", params)

    def test_034_provider_prose_not_proof(self):
        m = self.manifest()
        with self.assertRaises(B.BootstrapProofError):
            self.verify(m, [b"GITHUB OWNER: PASS"])

    def test_035_execution_authority_remains_false(self):
        m = self.manifest()
        r = self.verify(m, [self.proof(m)])
        self.assertFalse(r["execution_authorized_by_cpi"])
        self.assertNotIn("current_decision", r)
        self.assertNotIn("deploy_authorized", r)
        self.assertNotIn("federation_authorized", r)

    def test_036_hive_profile_remains_unsupported(self):
        hp = B.NativeBootstrapPolicy(
            policy_id="HIVE_ACTIVE_SIGNATURE_V1",
            project=PROJECT,
            authority_domain=DOMAIN,
            anchor_profile=B.HIVE_ACTIVE_AUTHORITY_V1,
            anchor_subject="hive-mainnet:@etblink:active",
            expected_generation=GENERATION,
            minimum_anchor_count=1,
            pinned_anchor_public_key=None,
            native_policy_provenance_claim="synthetic:hive-profile",
        )
        m = B.create_manifest_for_policy(
            policy=hp,
            candidate_authority_key_id=CANDIDATE_A,
            challenge=CHALLENGE_A,
        )
        with self.assertRaises(B.UnsupportedAnchorProfileError):
            B.verify_bootstrap(manifest_raw=m, proof_artifacts=[], policy=hp)

    def test_037_duplicate_json_manifest_rejected(self):
        raw = self.manifest()
        poly = raw[:-1] + b',"project":"other/Project"}'
        with self.assertRaises(B.BootstrapSchemaError):
            B.parse_manifest_artifact(poly)

    def test_038_noncanonical_manifest_rejected(self):
        with self.assertRaises(B.BootstrapSchemaError):
            B.parse_manifest_artifact(b" " + self.manifest())

    def test_039_version_marker_is_021_and_wire_schema_remains_02(self):
        self.assertEqual(B.RESEARCH_BOOTSTRAP_VERSION, "0.2.1")
        self.assertEqual(B.MANIFEST_SCHEMA, "cpi.native-bootstrap-manifest/0.2")
        self.assertEqual(B.POLICY_SCHEMA, "cpi.native-bootstrap-policy/0.2")
        self.assertEqual(B.PROOF_SCHEMA, "cpi.bootstrap-anchor-proof/0.2")


if __name__ == "__main__":
    unittest.main()
