from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Dict, Mapping, Sequence

_STAGE8_DIR = Path(__file__).resolve().parent.parent / "stage8a"
if str(_STAGE8_DIR) not in sys.path:
    sys.path.insert(0, str(_STAGE8_DIR))
import hive_active_bootstrap_adapter as H8  # noqa: E402

SCHEMA = "cpi.hive-authority-state-provenance-synthetic/0.1"
ARCHITECTURE = "C_VF__VALIDATED_FULL_HISTORY_REPLAY_PLUS_CONSERVATIVE_FINALITY_CERTIFICATE"
FINALITY_PROFILE = "PRODUCED_BLOCK_CONFIRMATION_75PCT_V1"
VALIDATION_PROFILE = "HIVED_VALIDATE_DURING_REPLAY_V1"
PROVENANCE_SCOPE = "SYNTHETIC_C_VF_REFERENCE_FIXTURE_ONLY"
HIVE_NETWORK = H8.HIVE_NETWORK
HIVE_CHAIN_ID = H8.HIVE_CHAIN_ID
IRREVERSIBLE_THRESHOLD_PERCENT = 75


class ProvenanceError(ValueError):
    pass


class HistoryError(ProvenanceError):
    pass


class FinalityError(ProvenanceError):
    pass


class AuthorityStateError(ProvenanceError):
    pass


def _canonical(obj: Any) -> bytes:
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode("utf-8", "strict")


def _digest(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj)).hexdigest()


def _active(value: Mapping[str, Any]) -> Dict[str, Any]:
    if not isinstance(value, Mapping):
        raise AuthorityStateError("active authority must be an object")
    if set(value) != {"weight_threshold", "key_auths", "account_auths"}:
        raise AuthorityStateError("active authority field mismatch")
    threshold = value["weight_threshold"]
    if type(threshold) is not int or threshold <= 0:
        raise AuthorityStateError("invalid weight_threshold")
    key_auths = value["key_auths"]
    account_auths = value["account_auths"]
    if type(key_auths) is not list or type(account_auths) is not list:
        raise AuthorityStateError("authority members must be arrays")
    return {
        "weight_threshold": threshold,
        "key_auths": [list(x) for x in key_auths],
        "account_auths": [list(x) for x in account_auths],
    }


def synthetic_block_id(
    *,
    block_num: int,
    previous: str,
    witness: str,
    scheduled_witnesses: Sequence[str],
    authority_updates: Mapping[str, Mapping[str, Any]],
    fast_confirms: Mapping[str, int] | None = None,
) -> str:
    body = {
        "schema": "cpi.synthetic-hive-block/0.1",
        "network": HIVE_NETWORK,
        "chain_id": HIVE_CHAIN_ID,
        "block_num": block_num,
        "previous": previous,
        "witness": witness,
        "scheduled_witnesses": list(scheduled_witnesses),
        "authority_updates": {
            name: _active(auth) for name, auth in sorted(authority_updates.items())
        },
        "fast_confirms": dict(sorted((fast_confirms or {}).items())),
    }
    return _digest(body)


def make_block(
    *,
    block_num: int,
    previous: str,
    witness: str,
    scheduled_witnesses: Sequence[str],
    authority_updates: Mapping[str, Mapping[str, Any]] | None = None,
    fast_confirms: Mapping[str, int] | None = None,
) -> Dict[str, Any]:
    updates = dict(authority_updates or {})
    confirms = dict(fast_confirms or {})
    block_id = synthetic_block_id(
        block_num=block_num,
        previous=previous,
        witness=witness,
        scheduled_witnesses=scheduled_witnesses,
        authority_updates=updates,
        fast_confirms=confirms,
    )
    return {
        "block_num": block_num,
        "block_id": block_id,
        "previous": previous,
        "witness": witness,
        "scheduled_witnesses": list(scheduled_witnesses),
        "authority_updates": {
            name: _active(auth) for name, auth in sorted(updates.items())
        },
        "fast_confirms": dict(sorted(confirms.items())),
    }


def validate_history(
    history: Sequence[Mapping[str, Any]],
    *,
    validation_profile: str,
    checkpoint_mode: str,
) -> None:
    if validation_profile != VALIDATION_PROFILE:
        raise HistoryError("full validation profile is required")
    if checkpoint_mode != "NONE_FROM_GENESIS":
        raise HistoryError("unauthenticated checkpoints are forbidden in C-VF")
    if not history:
        raise HistoryError("history is empty")
    previous = "0" * 64
    expected_num = 1
    for raw in history:
        if not isinstance(raw, Mapping):
            raise HistoryError("block must be an object")
        required = {
            "block_num", "block_id", "previous", "witness", "scheduled_witnesses",
            "authority_updates", "fast_confirms"
        }
        if set(raw) != required:
            raise HistoryError("block field mismatch")
        if raw["block_num"] != expected_num:
            raise HistoryError("block numbers must be contiguous from genesis")
        if raw["previous"] != previous:
            raise HistoryError("previous-id linkage failure")
        schedule = raw["scheduled_witnesses"]
        if type(schedule) is not list or not schedule or len(set(schedule)) != len(schedule):
            raise HistoryError("invalid scheduled witness set")
        if raw["witness"] not in schedule:
            raise HistoryError("producer is absent from scheduled witness set")
        for witness, target_num in raw["fast_confirms"].items():
            if (
                witness not in schedule
                or type(target_num) is not int
                or target_num < 1
                or target_num > raw["block_num"]
            ):
                raise HistoryError("invalid synthetic fast-confirm")
        expected_id = synthetic_block_id(
            block_num=raw["block_num"],
            previous=raw["previous"],
            witness=raw["witness"],
            scheduled_witnesses=schedule,
            authority_updates=raw["authority_updates"],
            fast_confirms=raw["fast_confirms"],
        )
        if raw["block_id"] != expected_id:
            raise HistoryError("block content/id mismatch")
        previous = raw["block_id"]
        expected_num += 1


def _find_block(
    history: Sequence[Mapping[str, Any]], num: int, block_id: str
) -> Mapping[str, Any]:
    if type(num) is not int or num < 1 or num > len(history):
        raise HistoryError("context block number out of range")
    block = history[num - 1]
    if block["block_id"] != block_id:
        raise HistoryError("context block id mismatch")
    return block


def _state_after_target(
    history: Sequence[Mapping[str, Any]],
    target_num: int,
    genesis_authorities: Mapping[str, Mapping[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    state = {name: _active(auth) for name, auth in sorted(genesis_authorities.items())}
    for block in history[:target_num]:
        for name, auth in block["authority_updates"].items():
            state[name] = _active(auth)
    if not state:
        raise AuthorityStateError("authority state is empty")
    return state


def _authority_closure(
    state: Mapping[str, Mapping[str, Any]],
    root_account: str,
) -> list[dict[str, Any]]:
    if root_account not in state:
        raise AuthorityStateError("root account missing")
    seen: set[str] = set()
    stack: list[str] = [root_account]
    while stack:
        name = stack.pop()
        if name in seen:
            continue
        if name not in state:
            raise AuthorityStateError(f"delegated account missing: {name}")
        seen.add(name)
        if len(seen) > H8.MAX_SIG_CHECK_ACCOUNTS:
            raise AuthorityStateError("authority closure exceeds Stage-8 account bound")
        auth = _active(state[name])
        for child, _weight in auth["account_auths"]:
            stack.append(child)
    return [
        {"name": name, "active": _active(state[name])}
        for name in sorted(seen)
    ]


def required_witness_count(n: int) -> int:
    if type(n) is not int or n <= 0:
        raise FinalityError("scheduled witness count must be positive")
    offset = (100 - IRREVERSIBLE_THRESHOLD_PERCENT) * n // 100
    return n - offset


def _highest_produced_by_witness(
    history: Sequence[Mapping[str, Any]], confirmation_num: int
) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for block in history[:confirmation_num]:
        out[block["witness"]] = block["block_num"]
    return out


def _highest_native_approval(
    history: Sequence[Mapping[str, Any]], confirmation_num: int
) -> Dict[str, int]:
    out = _highest_produced_by_witness(history, confirmation_num)
    for block in history[:confirmation_num]:
        for witness, approved_num in block["fast_confirms"].items():
            out[witness] = max(out.get(witness, 0), approved_num)
    return out


def build_finality_certificate(
    history: Sequence[Mapping[str, Any]],
    *,
    target_num: int,
    target_id: str,
    confirmation_num: int,
    confirmation_id: str,
) -> Dict[str, Any]:
    _find_block(history, target_num, target_id)
    confirmation = _find_block(history, confirmation_num, confirmation_id)
    if confirmation_num < target_num:
        raise FinalityError("confirmation context precedes target")
    schedule = list(confirmation["scheduled_witnesses"])
    highest = _highest_produced_by_witness(history, confirmation_num)
    approvals = []
    for witness in sorted(schedule):
        produced_num = highest.get(witness, 0)
        approves = produced_num >= target_num
        approvals.append({
            "witness": witness,
            "highest_produced_block_num": produced_num,
            "approves_target": approves,
        })
    required = required_witness_count(len(schedule))
    approving = sum(1 for item in approvals if item["approves_target"])
    body = {
        "schema": "cpi.hive-finality-certificate-synthetic/0.1",
        "profile": FINALITY_PROFILE,
        "target_block_num": target_num,
        "target_block_id": target_id,
        "confirmation_block_num": confirmation_num,
        "confirmation_block_id": confirmation_id,
        "scheduled_witnesses": sorted(schedule),
        "threshold_percent": IRREVERSIBLE_THRESHOLD_PERCENT,
        "required_witness_count": required,
        "approving_witness_count": approving,
        "approvals": approvals,
        "target_irreversibility_established": approving >= required,
    }
    body["certificate_digest"] = _digest(body)
    return body


def produced_only_never_ahead_of_reference(
    history: Sequence[Mapping[str, Any]],
    *,
    target_num: int,
    confirmation_num: int,
) -> bool:
    confirmation = history[confirmation_num - 1]
    schedule = list(confirmation["scheduled_witnesses"])
    produced = _highest_produced_by_witness(history, confirmation_num)
    native = _highest_native_approval(history, confirmation_num)
    produced_count = sum(produced.get(w, 0) >= target_num for w in schedule)
    native_count = sum(native.get(w, 0) >= target_num for w in schedule)
    return produced_count <= native_count


def verify_synthetic_provenance(
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
    validate_history(
        history,
        validation_profile=validation_profile,
        checkpoint_mode=checkpoint_mode,
    )
    _find_block(history, target_block_num, target_block_id)
    _find_block(history, confirmation_block_num, confirmation_block_id)

    state = _state_after_target(history, target_block_num, genesis_authorities)
    accounts = _authority_closure(state, authority_root_account)
    snapshot_raw = H8.create_snapshot_artifact(
        reference_id=f"stage9a-target-{target_block_num}-{target_block_id}",
        accounts=accounts,
    )
    snapshot_digest = H8.snapshot_digest(snapshot_raw)

    certificate = build_finality_certificate(
        history,
        target_num=target_block_num,
        target_id=target_block_id,
        confirmation_num=confirmation_block_num,
        confirmation_id=confirmation_block_id,
    )
    finality_valid = bool(certificate["target_irreversibility_established"])
    monotonic = produced_only_never_ahead_of_reference(
        history,
        target_num=target_block_num,
        confirmation_num=confirmation_block_num,
    )
    if not monotonic:
        raise FinalityError("produced-only finality exceeded reference approvals")

    joint = {
        "schema": SCHEMA,
        "architecture": ARCHITECTURE,
        "network": HIVE_NETWORK,
        "chain_id": HIVE_CHAIN_ID,
        "validation_profile": validation_profile,
        "checkpoint_mode": checkpoint_mode,
        "target_block_num": target_block_num,
        "target_block_id": target_block_id,
        "confirmation_block_num": confirmation_block_num,
        "confirmation_block_id": confirmation_block_id,
        "authority_root_account": authority_root_account,
        "authority_snapshot_digest": snapshot_digest,
        "finality_certificate_digest": certificate["certificate_digest"],
        "provenance_scope": PROVENANCE_SCOPE,
    }
    joint_digest = _digest(joint)

    return {
        "chain_identity_bound": True,
        "history_consensus_validated": True,
        "target_context_bound": True,
        "authority_state_derived": True,
        "authority_closure_complete": True,
        "authority_snapshot_digest": snapshot_digest,
        "authority_snapshot_raw": snapshot_raw,
        "finality_certificate": certificate,
        "finality_certificate_valid": finality_valid,
        "target_irreversibility_established": finality_valid,
        "authority_state_provenance_authenticated": finality_valid,
        "joint_provenance_digest": joint_digest,
        "provenance_scope": PROVENANCE_SCOPE,
        "reindex_reported_lib_observed": reindex_reported_lib,
        "reindex_reported_lib_used_for_finality": False,
        "current_authority_established": False,
        "execution_authorized_by_cpi": False,
    }
