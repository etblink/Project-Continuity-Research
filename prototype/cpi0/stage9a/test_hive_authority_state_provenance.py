from __future__ import annotations

import copy
import unittest

import hive_authority_state_provenance as P


KEY = "STM8gAFEMLo7L2EoHRizg2AAUiRvTi24UYxQXNbCWjuwAJe8ViDJL"


def active(threshold=1, key_auths=None, account_auths=None):
    return {
        "weight_threshold": threshold,
        "key_auths": sorted(key_auths or [], key=lambda x: x[0]),
        "account_auths": sorted(account_auths or [], key=lambda x: x[0]),
    }


def fixture(block_count=30, target=6, confirmation=30, mutate_delegate_at=None, fast_confirm=False):
    witnesses = [f"wit{i:02d}" for i in range(1, 22)]
    genesis = {
        "rootacct": active(1, account_auths=[["delegate", 1]]),
        "delegate": active(1, key_auths=[[KEY, 1]]),
    }
    history = []
    previous = "0" * 64
    for n in range(1, block_count + 1):
        witness = witnesses[(n - 1) % len(witnesses)]
        updates = {}
        if mutate_delegate_at == n:
            updates["delegate"] = active(2, key_auths=[[KEY, 1]])
        confirms = {}
        if fast_confirm and n == target + 1:
            for w in witnesses[:16]:
                confirms[w] = target
        block = P.make_block(
            block_num=n,
            previous=previous,
            witness=witness,
            scheduled_witnesses=witnesses,
            authority_updates=updates,
            fast_confirms=confirms,
        )
        history.append(block)
        previous = block["block_id"]
    return witnesses, genesis, history, target, confirmation


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
    return P.verify_synthetic_provenance(**args)


class ProvenanceTests(unittest.TestCase):
    def test_001_happy_path_joint_provenance_passes(self):
        r = verify(fixture())
        self.assertTrue(r["authority_state_provenance_authenticated"])
        self.assertTrue(r["target_irreversibility_established"])
        self.assertFalse(r["current_authority_established"])
        self.assertFalse(r["execution_authorized_by_cpi"])

    def test_002_stage8_snapshot_is_canonical_and_bound(self):
        r = verify(fixture())
        self.assertEqual(
            P.H8.snapshot_digest(r["authority_snapshot_raw"]),
            r["authority_snapshot_digest"],
        )

    def test_003_default_replay_profile_rejected(self):
        with self.assertRaises(P.HistoryError):
            verify(fixture(), validation_profile="DEFAULT_REPLAY")

    def test_004_checkpoint_mode_rejected(self):
        with self.assertRaises(P.HistoryError):
            verify(fixture(), checkpoint_mode="BLOCK_ID_ONLY")

    def test_005_wrong_target_id_rejected(self):
        with self.assertRaises(P.HistoryError):
            verify(fixture(), target_block_id="0" * 64)

    def test_006_wrong_confirmation_id_rejected(self):
        with self.assertRaises(P.HistoryError):
            verify(fixture(), confirmation_block_id="0" * 64)

    def test_007_broken_previous_link_rejected(self):
        fx = fixture()
        history = copy.deepcopy(fx[2])
        history[10]["previous"] = "f" * 64
        with self.assertRaises(P.HistoryError):
            verify(fx, history=history)

    def test_008_block_content_id_mismatch_rejected(self):
        fx = fixture()
        history = copy.deepcopy(fx[2])
        history[10]["witness"] = "wit02" if history[10]["witness"] != "wit02" else "wit03"
        with self.assertRaises(P.HistoryError):
            verify(fx, history=history)

    def test_009_producer_absent_from_schedule_rejected(self):
        fx = fixture()
        history = copy.deepcopy(fx[2])
        block = history[8]
        block["scheduled_witnesses"] = [
            w for w in block["scheduled_witnesses"] if w != block["witness"]
        ]
        with self.assertRaises(P.HistoryError):
            verify(fx, history=history)

    def test_010_reindex_lib_is_not_used_for_finality(self):
        fx = fixture(block_count=12, target=6, confirmation=12)
        r = verify(fx, reindex_reported_lib=12)
        self.assertFalse(r["target_irreversibility_established"])
        self.assertFalse(r["authority_state_provenance_authenticated"])
        self.assertEqual(r["reindex_reported_lib_observed"], 12)
        self.assertFalse(r["reindex_reported_lib_used_for_finality"])

    def test_011_insufficient_produced_witnesses_fails_finality_only(self):
        fx = fixture(block_count=15, target=6, confirmation=15)
        r = verify(fx)
        self.assertTrue(r["authority_state_derived"])
        self.assertFalse(r["target_irreversibility_established"])
        self.assertFalse(r["authority_state_provenance_authenticated"])

    def test_012_exact_16_of_21_passes_threshold(self):
        fx = fixture(block_count=21, target=6, confirmation=21)
        r = verify(fx)
        cert = r["finality_certificate"]
        self.assertEqual(cert["required_witness_count"], 16)
        self.assertEqual(cert["approving_witness_count"], 16)
        self.assertTrue(cert["target_irreversibility_established"])

    def test_013_15_of_21_fails_threshold(self):
        fx = fixture(block_count=20, target=6, confirmation=20)
        r = verify(fx)
        cert = r["finality_certificate"]
        self.assertEqual(cert["approving_witness_count"], 15)
        self.assertFalse(cert["target_irreversibility_established"])

    def test_014_fast_confirm_can_help_reference_but_not_produced_certificate(self):
        fx = fixture(block_count=7, target=6, confirmation=7, fast_confirm=True)
        r = verify(fx)
        self.assertFalse(r["target_irreversibility_established"])
        self.assertTrue(P.produced_only_never_ahead_of_reference(
            fx[2], target_num=6, confirmation_num=7
        ))

    def test_015_fast_confirm_omission_never_increases_approval_count(self):
        fx = fixture(block_count=30, target=6, confirmation=30, fast_confirm=True)
        self.assertTrue(P.produced_only_never_ahead_of_reference(
            fx[2], target_num=6, confirmation_num=30
        ))

    def test_016_target_snapshot_ignores_later_authority_rotation(self):
        base = fixture(block_count=30, target=6, confirmation=30)
        later = fixture(
            block_count=30, target=6, confirmation=30, mutate_delegate_at=20
        )
        self.assertEqual(
            verify(base)["authority_snapshot_digest"],
            verify(later)["authority_snapshot_digest"],
        )

    def test_017_pre_target_authority_rotation_changes_snapshot(self):
        base = fixture(block_count=30, target=6, confirmation=30)
        before = fixture(
            block_count=30, target=6, confirmation=30, mutate_delegate_at=5
        )
        self.assertNotEqual(
            verify(base)["authority_snapshot_digest"],
            verify(before)["authority_snapshot_digest"],
        )

    def test_018_missing_delegated_account_fails(self):
        fx = fixture()
        bad_genesis = {"rootacct": active(1, account_auths=[["delegate", 1]])}
        with self.assertRaises(P.AuthorityStateError):
            verify(fx, genesis_authorities=bad_genesis)

    def test_019_confirmation_before_target_fails(self):
        fx = fixture()
        history = fx[2]
        with self.assertRaises(P.FinalityError):
            verify(
                fx,
                confirmation_block_num=5,
                confirmation_block_id=history[4]["block_id"],
            )

    def test_020_schedule_substitution_breaks_block_id(self):
        fx = fixture()
        history = copy.deepcopy(fx[2])
        history[-1]["scheduled_witnesses"] = history[-1]["scheduled_witnesses"][:-1]
        with self.assertRaises(P.HistoryError):
            verify(fx, history=history)

    def test_021_finality_certificate_binds_target_and_confirmation(self):
        r = verify(fixture())
        cert = r["finality_certificate"]
        self.assertEqual(cert["target_block_num"], 6)
        self.assertEqual(cert["confirmation_block_num"], 30)
        self.assertEqual(len(cert["certificate_digest"]), 64)

    def test_022_joint_digest_changes_with_confirmation_context(self):
        fx1 = fixture(block_count=31, target=6, confirmation=30)
        fx2 = fixture(block_count=31, target=6, confirmation=31)
        self.assertNotEqual(
            verify(fx1)["joint_provenance_digest"],
            verify(fx2)["joint_provenance_digest"],
        )

    def test_023_current_authority_never_claimed(self):
        r = verify(fixture(mutate_delegate_at=20))
        self.assertFalse(r["current_authority_established"])

    def test_024_execution_authority_never_claimed(self):
        self.assertFalse(verify(fixture())["execution_authorized_by_cpi"])

    def test_025_required_witness_count_matches_hive_integer_formula(self):
        self.assertEqual(P.required_witness_count(21), 16)
        self.assertEqual(P.required_witness_count(4), 3)
        self.assertEqual(P.required_witness_count(3), 3)

    def test_026_fake_provenance_label_has_no_input_surface(self):
        with self.assertRaises(TypeError):
            verify(fixture(), authenticated=True)

    def test_027_noncontiguous_history_rejected(self):
        fx = fixture()
        history = copy.deepcopy(fx[2])
        history[4]["block_num"] = 99
        with self.assertRaises(P.HistoryError):
            verify(fx, history=history)

    def test_028_invalid_fast_confirm_rejected(self):
        fx = fixture()
        history = copy.deepcopy(fx[2])
        history[5]["fast_confirms"] = {"outsider": 5}
        with self.assertRaises(P.HistoryError):
            verify(fx, history=history)


if __name__ == "__main__":
    unittest.main()
