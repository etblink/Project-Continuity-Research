from __future__ import annotations

import copy
import hashlib
import json
import unittest

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

import hive_active_bootstrap_adapter as H


CANDIDATE = "ed25519-sha256:" + "aa" * 32
CHALLENGE = "11" * 32


def private_key(d: int):
    return ec.derive_private_key(d, ec.SECP256K1())


def hive_public(priv) -> str:
    raw = priv.public_key().public_bytes(
        Encoding.X962,
        PublicFormat.CompressedPoint,
    )
    return H.hive_public_key_encode(raw)


def compact_sign(priv, message: bytes) -> str:
    der = priv.sign(message, ec.ECDSA(hashes.SHA256()))
    r, s = decode_dss_signature(der)
    expected = hive_public(priv)
    for recid in range(4):
        raw = bytes([31 + recid]) + r.to_bytes(32, "big") + s.to_bytes(32, "big")
        sig = raw.hex()
        try:
            if H.recover_hive_public_key(message, sig) == expected:
                return sig
        except H.HiveAdapterError:
            pass
    raise AssertionError("could not construct compact recoverable signature")


def active(threshold, key_auths=None, account_auths=None):
    return {
        "weight_threshold": threshold,
        "key_auths": sorted(key_auths or [], key=lambda x: x[0]),
        "account_auths": sorted(account_auths or [], key=lambda x: x[0]),
    }


class HiveAdapterTests(unittest.TestCase):
    def setUp(self):
        self.k1 = private_key(1)
        self.k2 = private_key(2)
        self.k3 = private_key(3)
        self.k4 = private_key(4)
        self.p1 = hive_public(self.k1)
        self.p2 = hive_public(self.k2)
        self.p3 = hive_public(self.k3)
        self.p4 = hive_public(self.k4)

    def snapshot(self, accounts, ref="synthetic-vector"):
        return H.create_snapshot_artifact(reference_id=ref, accounts=sorted(accounts, key=lambda x: x["name"]))

    def policy(self, snapshot_raw, account="rootacct", provenance="synthetic policy"):
        return H.HiveActivePolicy(
            policy_id="HIVE_ACTIVE_SIGNATURE_V1",
            project="example/project",
            authority_domain="owner.acceptance",
            anchor_subject=f"hive-mainnet:@{account}:active",
            expected_generation="genesis-001",
            minimum_anchor_count=1,
            hive_account=account,
            hive_authority_snapshot_digest=H.snapshot_digest(snapshot_raw),
            native_policy_provenance_claim=provenance,
        )

    def manifest(self, policy):
        return H.create_manifest_for_policy(
            policy=policy,
            candidate_authority_key_id=CANDIDATE,
            challenge=CHALLENGE,
        )

    def proof(self, manifest, policy, priv, claimed=True):
        message = H.common.anchor_statement(manifest)
        sig = compact_sign(priv, message)
        return H.create_hive_proof_artifact(
            manifest_raw=manifest,
            policy=policy,
            signature_hex=sig,
            claimed_public_key=hive_public(priv) if claimed else None,
        )

    def basic_fixture(self):
        snap = self.snapshot([
            {"name": "rootacct", "active": active(1, [[self.p1, 1]])}
        ])
        pol = self.policy(snap)
        man = self.manifest(pol)
        prf = self.proof(man, pol, self.k1)
        return snap, pol, man, prf

    def test_001_valid_1_of_1_hive_active_bootstrap(self):
        snap, pol, man, prf = self.basic_fixture()
        r = H.verify_hive_bootstrap(
            manifest_raw=man,
            proof_artifacts=[prf],
            policy=pol,
            snapshot_raw=snap,
        )
        self.assertTrue(r["hive_active_authority_satisfied"])
        self.assertFalse(r["hive_authority_snapshot_authenticated"])
        self.assertFalse(r["execution_authorized_by_cpi"])
        self.assertEqual(
            r["trust_statement_scope"],
            "RELATIVE_TO_SUPPLIED_POLICY_AND_AUTHORITY_SNAPSHOT",
        )

    def test_002_wrong_active_key_fails(self):
        snap, pol, man, _ = self.basic_fixture()
        wrong = self.proof(man, pol, self.k2)
        with self.assertRaises(H.HiveAuthorityError):
            H.verify_hive_bootstrap(
                manifest_raw=man,
                proof_artifacts=[wrong],
                policy=pol,
                snapshot_raw=snap,
            )

    def test_003_posting_like_key_does_not_substitute_for_active(self):
        # p2 is intentionally absent from the Active graph.
        snap, pol, man, _ = self.basic_fixture()
        with self.assertRaises(H.HiveAuthorityError):
            H.verify_hive_bootstrap(
                manifest_raw=man,
                proof_artifacts=[self.proof(man, pol, self.k2)],
                policy=pol,
                snapshot_raw=snap,
            )

    def test_004_owner_like_key_does_not_substitute_for_active(self):
        snap, pol, man, _ = self.basic_fixture()
        with self.assertRaises(H.HiveAuthorityError):
            H.verify_hive_bootstrap(
                manifest_raw=man,
                proof_artifacts=[self.proof(man, pol, self.k3)],
                policy=pol,
                snapshot_raw=snap,
            )

    def test_005_two_of_three_passes(self):
        snap = self.snapshot([{
            "name": "rootacct",
            "active": active(2, [[self.p1, 1], [self.p2, 1], [self.p3, 1]]),
        }])
        pol = self.policy(snap)
        man = self.manifest(pol)
        r = H.verify_hive_bootstrap(
            manifest_raw=man,
            proof_artifacts=[self.proof(man, pol, self.k1), self.proof(man, pol, self.k2)],
            policy=pol,
            snapshot_raw=snap,
        )
        self.assertEqual(r["unique_recovered_signer_count"], 2)

    def test_006_two_of_three_one_signer_fails(self):
        snap = self.snapshot([{
            "name": "rootacct",
            "active": active(2, [[self.p1, 1], [self.p2, 1], [self.p3, 1]]),
        }])
        pol = self.policy(snap)
        man = self.manifest(pol)
        with self.assertRaises(H.HiveAuthorityError):
            H.verify_hive_bootstrap(
                manifest_raw=man,
                proof_artifacts=[self.proof(man, pol, self.k1)],
                policy=pol,
                snapshot_raw=snap,
            )

    def test_007_duplicate_signer_does_not_double_count(self):
        snap = self.snapshot([{
            "name": "rootacct",
            "active": active(2, [[self.p1, 1], [self.p2, 1]]),
        }])
        pol = self.policy(snap)
        man = self.manifest(pol)
        p = self.proof(man, pol, self.k1)
        with self.assertRaises(H.HiveAuthorityError):
            H.verify_hive_bootstrap(
                manifest_raw=man,
                proof_artifacts=[p, p, bytes(p)],
                policy=pol,
                snapshot_raw=snap,
            )

    def test_008_delegated_active_authority_passes(self):
        snap = self.snapshot([
            {"name": "delegate1", "active": active(1, [[self.p2, 1]])},
            {"name": "rootacct", "active": active(1, account_auths=[["delegate1", 1]])},
        ])
        pol = self.policy(snap)
        man = self.manifest(pol)
        r = H.verify_hive_bootstrap(
            manifest_raw=man,
            proof_artifacts=[self.proof(man, pol, self.k2)],
            policy=pol,
            snapshot_raw=snap,
        )
        self.assertTrue(r["hive_active_authority_satisfied"])

    def test_009_delegated_insufficient_fails(self):
        snap = self.snapshot([
            {"name": "delegate1", "active": active(2, [[self.p2, 1], [self.p3, 1]])},
            {"name": "rootacct", "active": active(1, account_auths=[["delegate1", 1]])},
        ])
        pol = self.policy(snap)
        man = self.manifest(pol)
        with self.assertRaises(H.HiveAuthorityError):
            H.verify_hive_bootstrap(
                manifest_raw=man,
                proof_artifacts=[self.proof(man, pol, self.k2)],
                policy=pol,
                snapshot_raw=snap,
            )

    def test_010_two_level_delegation_within_limit(self):
        snap = self.snapshot([
            {"name": "delegate1", "active": active(1, account_auths=[["delegate2", 1]])},
            {"name": "delegate2", "active": active(1, [[self.p3, 1]])},
            {"name": "rootacct", "active": active(1, account_auths=[["delegate1", 1]])},
        ])
        pol = self.policy(snap)
        man = self.manifest(pol)
        r = H.verify_hive_bootstrap(
            manifest_raw=man,
            proof_artifacts=[self.proof(man, pol, self.k3)],
            policy=pol,
            snapshot_raw=snap,
        )
        self.assertTrue(r["hive_active_authority_satisfied"])

    def test_011_beyond_recursion_limit_fails(self):
        snap = self.snapshot([
            {"name": "delegate1", "active": active(1, account_auths=[["delegate2", 1]])},
            {"name": "delegate2", "active": active(1, account_auths=[["delegate3", 1]])},
            {"name": "delegate3", "active": active(1, [[self.p4, 1]])},
            {"name": "rootacct", "active": active(1, account_auths=[["delegate1", 1]])},
        ])
        pol = self.policy(snap)
        man = self.manifest(pol)
        with self.assertRaises(H.HiveAuthorityError):
            H.verify_hive_bootstrap(
                manifest_raw=man,
                proof_artifacts=[self.proof(man, pol, self.k4)],
                policy=pol,
                snapshot_raw=snap,
            )

    def test_012_cycle_fails_without_loop(self):
        snap = self.snapshot([
            {"name": "delegate1", "active": active(1, account_auths=[["rootacct", 1]])},
            {"name": "rootacct", "active": active(1, account_auths=[["delegate1", 1]])},
        ])
        pol = self.policy(snap)
        man = self.manifest(pol)
        with self.assertRaises(H.HiveProofError):
            H.verify_hive_bootstrap(
                manifest_raw=man,
                proof_artifacts=[],
                policy=pol,
                snapshot_raw=snap,
            )

    def test_013_missing_delegated_account_snapshot_rejected(self):
        with self.assertRaises(H.HiveSchemaError):
            self.snapshot([
                {"name": "rootacct", "active": active(1, account_auths=[["missing", 1]])}
            ])

    def test_014_over_membership_snapshot_rejected(self):
        keys = []
        for d in range(10, 51):
            keys.append([hive_public(private_key(d)), 1])
        keys.sort(key=lambda x: x[0])
        with self.assertRaises(H.HiveSchemaError):
            self.snapshot([{"name": "rootacct", "active": active(100, keys)}])

    def test_015_valid_hive_public_key_roundtrip(self):
        raw = self.k1.public_key().public_bytes(Encoding.X962, PublicFormat.CompressedPoint)
        self.assertEqual(H.hive_public_key_decode(H.hive_public_key_encode(raw)), raw)

    def test_016_wrong_public_key_prefix_rejected(self):
        with self.assertRaises(H.HiveSchemaError):
            H.hive_public_key_decode("TST" + self.p1[3:])

    def test_017_bad_public_key_checksum_rejected(self):
        replacement = "1" if self.p1[-1] != "1" else "2"
        with self.assertRaises(H.HiveSchemaError):
            H.hive_public_key_decode(self.p1[:-1] + replacement)

    def test_018_bad_base58_rejected(self):
        with self.assertRaises(H.HiveSchemaError):
            H.hive_public_key_decode("STM0OIl")

    def test_019_message_mutation_invalidates_signature_identity(self):
        snap, pol, man, prf = self.basic_fixture()
        proof = H.parse_hive_proof_artifact(prf)
        altered = H.common.anchor_statement(man) + b"x"
        recovered = H.recover_hive_public_key(altered, proof["signature_hex"])
        self.assertNotEqual(recovered, self.p1)

    def test_020_truncated_signature_rejected(self):
        snap, pol, man, prf = self.basic_fixture()
        p = H.parse_hive_proof_artifact(prf)
        with self.assertRaises(H.HiveProofError):
            H.recover_hive_public_key(H.common.anchor_statement(man), p["signature_hex"][:-2])

    def test_021_bad_recovery_header_rejected(self):
        snap, pol, man, prf = self.basic_fixture()
        p = H.parse_hive_proof_artifact(prf)
        sig = "1e" + p["signature_hex"][2:]
        with self.assertRaises(H.HiveProofError):
            H.recover_hive_public_key(H.common.anchor_statement(man), sig)

    def test_022_zero_r_rejected(self):
        snap, pol, man, prf = self.basic_fixture()
        p = H.parse_hive_proof_artifact(prf)
        sig = p["signature_hex"][:2] + "00" * 32 + p["signature_hex"][66:]
        with self.assertRaises(H.HiveProofError):
            H.recover_hive_public_key(H.common.anchor_statement(man), sig)

    def test_023_claimed_public_key_mismatch_rejected_as_proof(self):
        snap, pol, man, prf = self.basic_fixture()
        p = H.parse_hive_proof_artifact(prf)
        bad = H.create_hive_proof_artifact(
            manifest_raw=man,
            policy=pol,
            signature_hex=p["signature_hex"],
            claimed_public_key=self.p2,
        )
        with self.assertRaises(H.HiveProofError):
            H.verify_hive_bootstrap(
                manifest_raw=man,
                proof_artifacts=[bad],
                policy=pol,
                snapshot_raw=snap,
            )

    def test_024_null_claimed_public_key_is_allowed(self):
        snap, pol, man, _ = self.basic_fixture()
        prf = self.proof(man, pol, self.k1, claimed=False)
        r = H.verify_hive_bootstrap(
            manifest_raw=man,
            proof_artifacts=[prf],
            policy=pol,
            snapshot_raw=snap,
        )
        self.assertEqual(r["recovered_signer_public_keys"], [self.p1])

    def test_025_uppercase_signature_hex_rejected(self):
        snap, pol, man, prf = self.basic_fixture()
        p = H.parse_hive_proof_artifact(prf)
        with self.assertRaises(H.HiveSchemaError):
            H.create_hive_proof_artifact(
                manifest_raw=man,
                policy=pol,
                signature_hex=p["signature_hex"].upper(),
                claimed_public_key=self.p1,
            )

    def test_026_snapshot_key_substitution_changes_digest(self):
        s1, _, _, _ = self.basic_fixture()
        s2 = self.snapshot([
            {"name": "rootacct", "active": active(1, [[self.p2, 1]])}
        ])
        self.assertNotEqual(H.snapshot_digest(s1), H.snapshot_digest(s2))

    def test_027_snapshot_threshold_substitution_changes_digest(self):
        s1, _, _, _ = self.basic_fixture()
        s2 = self.snapshot([
            {"name": "rootacct", "active": active(2, [[self.p1, 1]])}
        ])
        self.assertNotEqual(H.snapshot_digest(s1), H.snapshot_digest(s2))

    def test_028_snapshot_delegation_substitution_changes_digest(self):
        s1, _, _, _ = self.basic_fixture()
        s2 = self.snapshot([
            {"name": "delegate1", "active": active(1, [[self.p1, 1]])},
            {"name": "rootacct", "active": active(1, account_auths=[["delegate1", 1]])},
        ])
        self.assertNotEqual(H.snapshot_digest(s1), H.snapshot_digest(s2))

    def test_029_snapshot_digest_mismatch_policy_fails(self):
        snap, pol, man, prf = self.basic_fixture()
        other = self.snapshot([
            {"name": "rootacct", "active": active(1, [[self.p2, 1]])}
        ])
        with self.assertRaises(H.HivePolicyError):
            H.verify_hive_bootstrap(
                manifest_raw=man,
                proof_artifacts=[prf],
                policy=pol,
                snapshot_raw=other,
            )

    def test_030_account_change_changes_policy_digest(self):
        snap = self.snapshot([
            {"name": "otheracct", "active": active(1, [[self.p1, 1]])},
            {"name": "rootacct", "active": active(1, [[self.p1, 1]])},
        ])
        p1 = self.policy(snap, account="rootacct")
        p2 = self.policy(snap, account="otheracct")
        self.assertNotEqual(H.policy_digest(p1), H.policy_digest(p2))

    def test_031_provenance_does_not_change_policy_digest(self):
        snap, pol, _, _ = self.basic_fixture()
        p2 = self.policy(snap, provenance="different safe provenance")
        self.assertEqual(H.policy_digest(pol), H.policy_digest(p2))

    def test_032_snapshot_reference_changes_digest(self):
        s1 = self.snapshot([{"name": "rootacct", "active": active(1, [[self.p1, 1]])}], ref="a")
        s2 = self.snapshot([{"name": "rootacct", "active": active(1, [[self.p1, 1]])}], ref="b")
        self.assertNotEqual(H.snapshot_digest(s1), H.snapshot_digest(s2))

    def test_033_policy_digest_is_embedded_in_manifest(self):
        snap, pol, man, _ = self.basic_fixture()
        m = H.common.parse_manifest_artifact(man)
        self.assertEqual(m["bootstrap_policy_digest"], H.policy_digest(pol))

    def test_034_project_substitution_fails(self):
        snap, pol, man, prf = self.basic_fixture()
        p2 = H.HiveActivePolicy(
            policy_id=pol.policy_id,
            project="other/project",
            authority_domain=pol.authority_domain,
            anchor_subject=pol.anchor_subject,
            expected_generation=pol.expected_generation,
            minimum_anchor_count=1,
            hive_account=pol.hive_account,
            hive_authority_snapshot_digest=pol.hive_authority_snapshot_digest,
            native_policy_provenance_claim=pol.native_policy_provenance_claim,
        )
        with self.assertRaises(H.HivePolicyError):
            H.verify_hive_bootstrap(
                manifest_raw=man,
                proof_artifacts=[prf],
                policy=p2,
                snapshot_raw=snap,
            )

    def test_035_candidate_root_substitution_breaks_proof(self):
        snap, pol, man, prf = self.basic_fixture()
        man2 = H.create_manifest_for_policy(
            policy=pol,
            candidate_authority_key_id="ed25519-sha256:" + "bb" * 32,
            challenge=CHALLENGE,
        )
        with self.assertRaises(H.HiveProofError):
            H.verify_hive_bootstrap(
                manifest_raw=man2,
                proof_artifacts=[prf],
                policy=pol,
                snapshot_raw=snap,
            )

    def test_036_proof_snapshot_digest_mismatch_is_nonqualifying(self):
        snap, pol, man, prf = self.basic_fixture()
        p = H.parse_hive_proof_artifact(prf)
        p["authority_snapshot_digest"] = "22" * 32
        bad = H._canonical_json({field: p[field] for field in H.PROOF_FIELDS})
        with self.assertRaises(H.HiveProofError):
            H.verify_hive_bootstrap(
                manifest_raw=man,
                proof_artifacts=[bad],
                policy=pol,
                snapshot_raw=snap,
            )

    def test_037_result_explicit_snapshot_unauthenticated(self):
        snap, pol, man, prf = self.basic_fixture()
        r = H.verify_hive_bootstrap(
            manifest_raw=man,
            proof_artifacts=[prf],
            policy=pol,
            snapshot_raw=snap,
        )
        self.assertFalse(r["hive_authority_snapshot_authenticated"])
        self.assertFalse(r["native_policy_provenance_authenticated"])

    def test_038_execution_authority_always_false(self):
        snap, pol, man, prf = self.basic_fixture()
        r = H.verify_hive_bootstrap(
            manifest_raw=man,
            proof_artifacts=[prf],
            policy=pol,
            snapshot_raw=snap,
        )
        self.assertFalse(r["execution_authorized_by_cpi"])
        self.assertNotIn("current_decision", r)
        self.assertNotIn("deploy_authorized", r)
        self.assertNotIn("federation_authorized", r)

    def test_039_chain_constants_are_frozen(self):
        self.assertEqual(H.HIVE_NETWORK, "hive-mainnet")
        self.assertEqual(
            H.HIVE_CHAIN_ID,
            "beeab0de" + "00" * 28,
        )
        self.assertEqual(H.HIVE_KEY_PREFIX, "STM")
        self.assertEqual(H.MAX_SIG_CHECK_DEPTH, 2)
        self.assertEqual(H.MAX_AUTHORITY_MEMBERSHIP, 40)
        self.assertEqual(H.MAX_SIG_CHECK_ACCOUNTS, 125)

    def test_040_snapshot_noncanonical_order_rejected(self):
        accounts = [
            {"name": "rootacct", "active": active(1, [[self.p1, 1]])},
            {"name": "delegate1", "active": active(1, [[self.p2, 1]])},
        ]
        with self.assertRaises(H.HiveSchemaError):
            H.create_snapshot_artifact(reference_id="x", accounts=accounts)

    def test_041_snapshot_duplicate_key_auth_rejected(self):
        with self.assertRaises(H.HiveSchemaError):
            self.snapshot([{
                "name": "rootacct",
                "active": {
                    "weight_threshold": 1,
                    "key_auths": [[self.p1, 1], [self.p1, 1]],
                    "account_auths": [],
                },
            }])

    def test_042_proof_duplicate_json_rejected(self):
        snap, pol, man, prf = self.basic_fixture()
        poly = prf[:-1] + b',"hive_network":"hive-mainnet"}'
        with self.assertRaises(H.HiveSchemaError):
            H.parse_hive_proof_artifact(poly)

    def test_043_snapshot_duplicate_json_rejected(self):
        snap, _, _, _ = self.basic_fixture()
        poly = snap[:-1] + b',"network":"hive-mainnet"}'
        with self.assertRaises(H.HiveSchemaError):
            H.parse_snapshot_artifact(poly)

    def test_044_no_real_keychain_or_network_surface(self):
        import inspect
        source = inspect.getsource(H)
        self.assertNotIn("window.hive_keychain", source)
        self.assertNotIn("requests.", source)
        self.assertNotIn("api.hive.blog", source)
        self.assertNotIn("broadcast", source.lower())

    def test_045_adapter_version_and_profile(self):
        self.assertEqual(H.ADAPTER_VERSION, "0.1.0")
        self.assertEqual(H.PROFILE, "HIVE_ACTIVE_AUTHORITY_V1")
        self.assertEqual(H.AUTHORITY_LEVEL, "active")


if __name__ == "__main__":
    unittest.main()
