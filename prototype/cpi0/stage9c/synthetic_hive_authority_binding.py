from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence

_STAGE9A_DIR = Path(__file__).resolve().parent.parent / "stage9a"
if str(_STAGE9A_DIR) not in sys.path:
    sys.path.insert(0, str(_STAGE9A_DIR))

import hive_authority_state_provenance as H9A  # noqa: E402

SCHEMA = "cpi.hive-authority-state-binding-synthetic/0.2"
PROFILE = "SYNTHETIC_AUTHORITY_STATE_BINDING_V2"
THRESHOLD_PROFILE = "SYNTHETIC_PRODUCED_WITNESS_THRESHOLD_75PCT_V2"
PROVENANCE_SCOPE = "SYNTHETIC_FIXTURE_ONLY__NO_NATIVE_FINALITY"
HIVE_NETWORK = H9A.HIVE_NETWORK
HIVE_CHAIN_ID = H9A.HIVE_CHAIN_ID
VALIDATION_PROFILE = H9A.VALIDATION_PROFILE
IRREVERSIBLE_THRESHOLD_PERCENT = H9A.IRREVERSIBLE_THRESHOLD_PERCENT

# Frozen-source correction from Stage-9B F-07.
HIVE_MAINNET_START_MINER_VOTING_BLOCK = 864000
HIVE_TESTNET_START_MINER_VOTING_BLOCK = 30

# Re-export fixture builders/arithmetic only. Stage-9A finality/provenance
# conclusions are intentionally not re-exported.
make_block = H9A.make_block
required_witness_count = H9A.required_witness_count


class Stage9CError(ValueError):
    pass


class SyntheticBindingError(Stage9CError):
    pass


def _canonical(obj: Any) -> bytes:
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8", "strict")


def _digest(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj)).hexdigest()


def _normalize_genesis(
    genesis_authorities: Mapping[str, Mapping[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    if not isinstance(genesis_authorities, Mapping):
        raise SyntheticBindingError("genesis authorities must be an object")
    return {
        name: H9A._active(authority)
        for name, authority in sorted(genesis_authorities.items())
    }


def _validate_reindex_observation(value: int | None) -> int | None:
    if value is None:
        return None
    if type(value) is not int or value < 0 or value > 2**53 - 1:
        raise SyntheticBindingError(
            "reindex_reported_lib must be null or a bounded non-negative integer"
        )
    return value


def _produced_threshold_observation(
    history: Sequence[Mapping[str, Any]],
    *,
    target_num: int,
    target_id: str,
    confirmation_num: int,
    confirmation_id: str,
) -> Dict[str, Any]:
    H9A._find_block(history, target_num, target_id)
    confirmation = H9A._find_block(history, confirmation_num, confirmation_id)
    if confirmation_num < target_num:
        raise H9A.FinalityError("confirmation context precedes target")

    schedule = list(confirmation["scheduled_witnesses"])
    highest = H9A._highest_produced_by_witness(history, confirmation_num)

    approvals = []
    for witness in sorted(schedule):
        produced_num = highest.get(witness, 0)
        approves = produced_num >= target_num
        approvals.append(
            {
                "witness": witness,
                "highest_produced_block_num_on_supplied_linear_history": produced_num,
                "meets_synthetic_target_threshold_condition": approves,
            }
        )

    required = required_witness_count(len(schedule))
    approving = sum(
        1
        for item in approvals
        if item["meets_synthetic_target_threshold_condition"]
    )

    body: Dict[str, Any] = {
        "schema": "cpi.synthetic-produced-witness-threshold-observation/0.2",
        "profile": THRESHOLD_PROFILE,
        "scope": PROVENANCE_SCOPE,
        "target_block_num": target_num,
        "target_block_id": target_id,
        "confirmation_block_num": confirmation_num,
        "confirmation_block_id": confirmation_id,
        "scheduled_witnesses_from_supplied_confirmation_block": sorted(schedule),
        "threshold_percent": IRREVERSIBLE_THRESHOLD_PERCENT,
        "required_witness_count": required,
        "approving_witness_count_on_supplied_linear_history": approving,
        "synthetic_produced_threshold_met": approving >= required,
        "native_hive_finality_claim": "NOT_ESTABLISHED",
    }
    body["observation_digest"] = _digest(body)
    return body


def verify_synthetic_binding(
    *,
    history: Sequence[Mapping[str, Any]],
    genesis_authorities: Mapping[str, Mapping[str, Any]],
    authority_root_account: str,
    target_block_num: int,
    target_block_id: str,
    confirmation_block_num: int,
    confirmation_block_id: str,
    validation_profile: str,
    checkpoint_mode: str,
    reindex_reported_lib: int | None = None,
) -> Dict[str, Any]:
    """Verify only the narrowed Stage-9C synthetic binding profile.

    This function deliberately does not establish native Hive consensus
    validation, native Hive irreversibility/finality, or authenticated Hive
    authority-state provenance.
    """

    observed_reindex_lib = _validate_reindex_observation(reindex_reported_lib)

    H9A.validate_history(
        history,
        validation_profile=validation_profile,
        checkpoint_mode=checkpoint_mode,
    )

    if confirmation_block_num != len(history):
        raise SyntheticBindingError(
            "confirmation context must be the supplied synthetic history tip"
        )

    H9A._find_block(history, target_block_num, target_block_id)
    H9A._find_block(history, confirmation_block_num, confirmation_block_id)

    if confirmation_block_num < target_block_num:
        raise H9A.FinalityError("confirmation context precedes target")

    normalized_genesis = _normalize_genesis(genesis_authorities)
    genesis_authorities_digest = _digest(
        {
            "schema": "cpi.synthetic-genesis-authorities/0.1",
            "authorities": normalized_genesis,
        }
    )

    state = H9A._state_after_target(
        history,
        target_block_num,
        normalized_genesis,
    )
    accounts = H9A._authority_closure(state, authority_root_account)

    snapshot_raw = H9A.H8.create_snapshot_artifact(
        reference_id=f"stage9c-target-{target_block_num}-{target_block_id}",
        accounts=accounts,
    )
    snapshot_digest = H9A.H8.snapshot_digest(snapshot_raw)

    threshold_observation = _produced_threshold_observation(
        history,
        target_num=target_block_num,
        target_id=target_block_id,
        confirmation_num=confirmation_block_num,
        confirmation_id=confirmation_block_id,
    )

    joint = {
        "schema": SCHEMA,
        "profile": PROFILE,
        "network_label": HIVE_NETWORK,
        "chain_id_profile_value": HIVE_CHAIN_ID,
        "validation_profile_label": validation_profile,
        "checkpoint_mode": checkpoint_mode,
        "target_block_num": target_block_num,
        "target_block_id": target_block_id,
        "confirmation_block_num": confirmation_block_num,
        "confirmation_block_id": confirmation_block_id,
        "authority_root_account": authority_root_account,
        "complete_genesis_authorities_digest": genesis_authorities_digest,
        "authority_snapshot_digest": snapshot_digest,
        "synthetic_threshold_observation_digest": threshold_observation[
            "observation_digest"
        ],
        "provenance_scope": PROVENANCE_SCOPE,
    }

    return {
        "schema": SCHEMA,
        "profile": PROFILE,
        "provenance_scope": PROVENANCE_SCOPE,
        "synthetic_profile_chain_id_pinned": True,
        "synthetic_history_self_consistent": True,
        "synthetic_history_tip_bound": True,
        "synthetic_target_context_bound": True,
        "synthetic_authority_state_derived": True,
        "synthetic_authority_closure_derived": True,
        "synthetic_produced_threshold_met": threshold_observation[
            "synthetic_produced_threshold_met"
        ],
        "complete_genesis_authorities_digest": genesis_authorities_digest,
        "authority_snapshot_digest": snapshot_digest,
        "authority_snapshot_raw": snapshot_raw,
        "synthetic_threshold_observation": threshold_observation,
        "joint_synthetic_binding_digest": _digest(joint),
        "real_hive_chain_identity_authenticated": False,
        "real_hive_history_authenticated": False,
        "native_hive_consensus_validated": False,
        "native_hive_target_irreversibility_established": False,
        "real_hive_authority_snapshot_authenticated": False,
        "authority_state_provenance_authenticated": False,
        "current_authority_established": False,
        "execution_authorized_by_cpi": False,
        "reindex_reported_lib_observed": observed_reindex_lib,
        "reindex_reported_lib_used_for_synthetic_threshold": False,
        "reindex_reported_lib_used_for_native_finality": False,
    }
