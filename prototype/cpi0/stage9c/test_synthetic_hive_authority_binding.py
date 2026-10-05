from __future__ import annotations

import copy
import unittest

import synthetic_hive_authority_binding as P


KEY = "STM8gAFEMLo7L2EoHRizg2AAUiRvTi24UYxQXNbCWjuwAJe8ViDJL"


def active(threshold=1, key_auths=None, account_auths=None):
    return {
        "weight_threshold": threshold,
        "key_auths": sorted(key_auths or [], key=lambda x: x[0]),
        "account_auths": sorted(account_auths or [], key=lambda x: x[0]),
    }


def fixture(
    block_count=30,
    target=6,
    confirmation=None,
    mutate_delegate_at=None,
    witness_count=21,
):
    if confirmation is None:
        confirmation = block_count
    witnesses = [f"wit{i:02d}" for i in range(1, witness_count + 1)]
    genesis = {
        "rootacct": active(1, account_auths=[["delegate", 1]]),
        "delegate": active(1, key_auths=[[KEY, 1]]),
    }
    history = []
    previous = "0" * 64
    for n in range(1, block_count + 1):
        updates = {}
        if mutate_delegate_at == n:
            updates["delegate"] = active(2, key_auths=[[KEY, 1]])
        block = P.make_block(
            block_num=n,
            previous=previous,
            witness=witnesses[(n - 1) % len(witnesses)],
            scheduled_witnesses=witnesses,
            authority_updates=updates,
        )
        history.append(block)
        previous = block["block_id"]
    return witnesses, genesis, history, target, confirmation


def one_block_fixture():
    witnesses = ["wit01"]
    genesis = {"rootacct": active(1, key_auths=[[KEY, 1]])}
    block = P.make_block(
        block_num=1,
        previous="0" * 64,
        witness="wit01",
        scheduled_witnesses=witnesses,
    )
    return witnesses, genesis, [block], 1, 1


def verify(fx, **overrides):
    _w, genesis, history, target, confirmation = fx
    args = dict(
        history=history,
        genesis_authorities=genesis,
        authority_root_account="rootacct",
        target_block_num=target,
        target_block_id=history[target - 1]["block_id"],
        confirmation_block_num=confirmation,
        confirmation_block_id=history[confirmation - 1]["block_id"],
        validation_profile=P.VALIDATION_PROFILE,
        checkpoint_mode="NONE_FROM_GENESIS",
        reindex_reported_lib=confirmation,
    )
    args.update(overrides)
    return P.verify_synthetic_binding(**args)


class Stage9CCorrectiveTests(unittest.TestCase):
    def test_001_happy_path_claims_only_synthetic_binding(self):
        r = verify(fixture())
        self.assertTrue(r["synthetic_history_self_consistent"])
        self.assertTrue(r["synthetic_target_context_bound"])
        self.assertTrue(r["synthetic_authority_state_derived"])
        self.assertTrue(r["synthetic_produced_threshold_met"])
        self.assertEqual(
            r["provenance_scope"],
            "SYNTHETIC_FIXTURE_ONLY__NO_NATIVE_FINALITY",
        )

    def test_002_stage9a_positive_overclaim_keys_are_removed_or_false(self):
        r = verify(fixture())
        self.assertNotIn("history_consensus_validated", r)
        self.assertNotIn("chain_identity_bound", r)
        self.assertNotIn("target_irreversibility_established", r)
        self.assertNotIn("finality_certificate_valid", r)
        self.assertFalse(r["authority_state_provenance_authenticated"])

    def test_003_native_and_real_conclusions_are_explicitly_false(self):
        r = verify(fixture())
        self.assertFalse(r["real_hive_chain_identity_authenticated"])
        self.assertFalse(r["real_hive_history_authenticated"])
        self.assertFalse(r["native_hive_consensus_validated"])
        self.assertFalse(r["native_hive_target_irreversibility_established"])
        self.assertFalse(r["real_hive_authority_snapshot_authenticated"])

    def test_004_one_block_attacker_fixture_can_only_pass_synthetic_threshold(self):
        r = verify(one_block_fixture())
        self.assertTrue(r["synthetic_history_self_consistent"])
        self.assertTrue(r["synthetic_produced_threshold_met"])
        self.assertFalse(r["native_hive_consensus_validated"])
        self.assertFalse(r["native_hive_target_irreversibility_established"])
        self.assertFalse(r["authority_state_provenance_authenticated"])

    def test_005_threshold_observation_is_not_labeled_finality_or_irreversibility(self):
        r = verify(fixture(block_count=21, target=6))
        obs = r["synthetic_threshold_observation"]
        self.assertEqual(obs["required_witness_count"], 16)
        self.assertEqual(obs["approving_witness_count_on_supplied_linear_history"], 16)
        self.assertTrue(obs["synthetic_produced_threshold_met"])
        self.assertNotIn("target_irreversibility_established", obs)
        self.assertNotIn("finality_certificate_valid", obs)

    def test_006_15_of_21_is_only_a_synthetic_threshold_failure(self):
        r = verify(fixture(block_count=20, target=6))
        obs = r["synthetic_threshold_observation"]
        self.assertEqual(obs["approving_witness_count_on_supplied_linear_history"], 15)
        self.assertFalse(obs["synthetic_produced_threshold_met"])
        self.assertFalse(r["native_hive_target_irreversibility_established"])

    def test_007_stage8_snapshot_remains_canonical_and_bound(self):
        r = verify(fixture())
        self.assertEqual(
            P.H9A.H8.snapshot_digest(r["authority_snapshot_raw"]),
            r["authority_snapshot_digest"],
        )

    def test_008_complete_genesis_digest_binds_out_of_closure_accounts(self):
        fx = fixture()
        genesis_a = copy.deepcopy(fx[1])
        genesis_b = copy.deepcopy(fx[1])
        genesis_a["unrelated"] = active(1, key_auths=[[KEY, 1]])
        genesis_b["unrelated"] = active(1, key_auths=[[KEY, 2]])
        ra = verify(fx, genesis_authorities=genesis_a)
        rb = verify(fx, genesis_authorities=genesis_b)
        self.assertNotEqual(
            ra["complete_genesis_authorities_digest"],
            rb["complete_genesis_authorities_digest"],
        )
        self.assertNotEqual(
            ra["joint_synthetic_binding_digest"],
            rb["joint_synthetic_binding_digest"],
        )
        self.assertEqual(ra["authority_snapshot_digest"], rb["authority_snapshot_digest"])

    def test_009_structured_reindex_lib_is_rejected_not_echoed(self):
        with self.assertRaises(P.SyntheticBindingError):
            verify(fixture(), reindex_reported_lib={"authenticated": True})

    def test_010_boolean_reindex_lib_is_rejected(self):
        with self.assertRaises(P.SyntheticBindingError):
            verify(fixture(), reindex_reported_lib=True)

    def test_011_integer_reindex_lib_is_observational_only(self):
        r = verify(fixture(), reindex_reported_lib=999)
        self.assertEqual(r["reindex_reported_lib_observed"], 999)
        self.assertFalse(r["reindex_reported_lib_used_for_synthetic_threshold"])
        self.assertFalse(r["reindex_reported_lib_used_for_native_finality"])

    def test_012_confirmation_must_be_supplied_history_tip(self):
        fx = fixture(block_count=31, target=6, confirmation=30)
        with self.assertRaises(P.SyntheticBindingError):
            verify(fx)

    def test_013_target_snapshot_ignores_later_authority_rotation(self):
        base = fixture(block_count=30, target=6)
        later = fixture(block_count=30, target=6, mutate_delegate_at=20)
        self.assertEqual(
            verify(base)["authority_snapshot_digest"],
            verify(later)["authority_snapshot_digest"],
        )

    def test_014_pre_target_authority_rotation_changes_snapshot(self):
        base = fixture(block_count=30, target=6)
        before = fixture(block_count=30, target=6, mutate_delegate_at=5)
        self.assertNotEqual(
            verify(base)["authority_snapshot_digest"],
            verify(before)["authority_snapshot_digest"],
        )

    def test_015_default_replay_and_checkpoint_shortcuts_still_fail_closed(self):
        with self.assertRaises(P.H9A.HistoryError):
            verify(fixture(), validation_profile="DEFAULT_REPLAY")
        with self.assertRaises(P.H9A.HistoryError):
            verify(fixture(), checkpoint_mode="BLOCK_ID_ONLY")

    def test_016_mainnet_and_testnet_voting_constants_are_distinguished(self):
        self.assertEqual(P.HIVE_MAINNET_START_MINER_VOTING_BLOCK, 864000)
        self.assertEqual(P.HIVE_TESTNET_START_MINER_VOTING_BLOCK, 30)

    def test_017_joint_digest_binds_confirmation_context(self):
        fx30 = fixture(block_count=30, target=6)
        fx31 = fixture(block_count=31, target=6)
        self.assertNotEqual(
            verify(fx30)["joint_synthetic_binding_digest"],
            verify(fx31)["joint_synthetic_binding_digest"],
        )

    def test_018_current_authority_and_cpi_execution_remain_false(self):
        r = verify(fixture(mutate_delegate_at=20))
        self.assertFalse(r["current_authority_established"])
        self.assertFalse(r["execution_authorized_by_cpi"])


if __name__ == "__main__":
    unittest.main()
