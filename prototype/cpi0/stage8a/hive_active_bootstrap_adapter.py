from __future__ import annotations

import base64
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple

_COMMON_DIR = Path(__file__).resolve().parent.parent / "stage7e"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

import native_bootstrap_manifest_v0_2_1 as common  # noqa: E402


PROFILE = "HIVE_ACTIVE_AUTHORITY_V1"
HIVE_NETWORK = "hive-mainnet"
HIVE_CHAIN_ID = "beeab0de00000000000000000000000000000000000000000000000000000000"
HIVE_KEY_PREFIX = "STM"
AUTHORITY_LEVEL = "active"
AUTHORITY_RULESET = "HIVE_HF28_STRICT_ACTIVE_V1"
KEYCHAIN_SIGNING_SEMANTICS = "HIVE_KEYCHAIN_SIGN_BUFFER_HIVEJS_V1"

SNAPSHOT_SCHEMA = "cpi.hive-authority-snapshot/0.1"
POLICY_SCHEMA = "cpi.native-bootstrap-policy/0.3"
PROOF_SCHEMA = "cpi.hive-active-bootstrap-proof/0.1"
ADAPTER_VERSION = "0.1.0"

MAX_SIG_CHECK_DEPTH = 2
MAX_AUTHORITY_MEMBERSHIP = 40
MAX_SIG_CHECK_ACCOUNTS = 125

# secp256k1
_SECP_P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
_SECP_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
_SECP_G = (
    0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
)
_B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
_B58_IDX = {c: i for i, c in enumerate(_B58)}

_ACCOUNT_RE = re.compile(r"^[a-z][a-z0-9.-]{0,15}$")


class HiveAdapterError(ValueError):
    pass


class HiveSchemaError(HiveAdapterError):
    pass


class HivePolicyError(HiveAdapterError):
    pass


class HiveProofError(HiveAdapterError):
    pass


class HiveAuthorityError(HiveAdapterError):
    pass


@dataclass(frozen=True)
class HiveActivePolicy:
    policy_id: str
    project: str
    authority_domain: str
    anchor_subject: str
    expected_generation: str
    minimum_anchor_count: int
    hive_account: str
    hive_authority_snapshot_digest: str
    native_policy_provenance_claim: str


def _pairs_no_duplicates(pairs: Sequence[Tuple[str, Any]]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise HiveSchemaError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def _reject_float(_: str) -> Any:
    raise HiveSchemaError("floating-point JSON values are forbidden")


def _reject_constant(_: str) -> Any:
    raise HiveSchemaError("non-finite JSON values are forbidden")


def _strict_json_object(raw: bytes, kind: str) -> Dict[str, Any]:
    if type(raw) is not bytes:
        raise HiveSchemaError(f"{kind} must be raw bytes")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise HiveSchemaError("UTF-8 BOM is forbidden")
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise HiveSchemaError(f"{kind} is not valid UTF-8") from exc
    try:
        obj = json.loads(
            text,
            object_pairs_hook=_pairs_no_duplicates,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
    except HiveAdapterError:
        raise
    except (json.JSONDecodeError, TypeError, ValueError, RecursionError) as exc:
        raise HiveSchemaError(f"{kind} is not strict JSON") from exc
    if type(obj) is not dict:
        raise HiveSchemaError(f"{kind} root must be an object")
    return obj


def _canonical_json(obj: Mapping[str, Any]) -> bytes:
    try:
        return json.dumps(
            dict(obj),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8", "strict")
    except (TypeError, ValueError, UnicodeEncodeError) as exc:
        raise HiveSchemaError("object cannot be canonically serialized") from exc


def _text(value: Any, field: str) -> str:
    if type(value) is not str or not value:
        raise HiveSchemaError(f"{field} must be a non-empty string")
    try:
        value.encode("utf-8", "strict")
    except UnicodeEncodeError as exc:
        raise HiveSchemaError(f"{field} contains invalid Unicode") from exc
    return value


def _safe_claim(value: Any, field: str) -> str:
    value = _text(value, field)
    if not value.strip():
        raise HiveSchemaError(f"{field} must not be whitespace-only")
    if len(value) > 512:
        raise HiveSchemaError(f"{field} must be <= 512 Unicode scalars")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in value):
        raise HiveSchemaError(f"{field} contains forbidden controls")
    return value


def _hex64(value: Any, field: str) -> str:
    if type(value) is not str or len(value) != 64:
        raise HiveSchemaError(f"{field} must be 64 lowercase hex characters")
    if any(ch not in "0123456789abcdef" for ch in value):
        raise HiveSchemaError(f"{field} must be 64 lowercase hex characters")
    return value


def _account_name(value: Any, field: str) -> str:
    value = _text(value, field)
    if not _ACCOUNT_RE.fullmatch(value):
        raise HiveSchemaError(f"{field} is not a supported Hive account name")
    return value


def _positive_int(value: Any, field: str, maximum: int = 2**53 - 1) -> int:
    if type(value) is not int or not (1 <= value <= maximum):
        raise HiveSchemaError(f"{field} must be a positive bounded integer")
    return value


def _b58encode(raw: bytes) -> str:
    n = int.from_bytes(raw, "big")
    chars = []
    while n:
        n, rem = divmod(n, 58)
        chars.append(_B58[rem])
    leading = len(raw) - len(raw.lstrip(b"\x00"))
    return "1" * leading + ("".join(reversed(chars)) if chars else "")


def _b58decode(text: str) -> bytes:
    if type(text) is not str or not text:
        raise HiveSchemaError("invalid Base58 text")
    n = 0
    for ch in text:
        if ch not in _B58_IDX:
            raise HiveSchemaError("invalid Base58 character")
        n = n * 58 + _B58_IDX[ch]
    body = b"" if n == 0 else n.to_bytes((n.bit_length() + 7) // 8, "big")
    leading = len(text) - len(text.lstrip("1"))
    return b"\x00" * leading + body


def _ripemd160(raw: bytes) -> bytes:
    try:
        h = hashlib.new("ripemd160")
    except ValueError as exc:
        raise HiveSchemaError("RIPEMD160 unavailable") from exc
    h.update(raw)
    return h.digest()


def _point_add(
    left: Tuple[int, int] | None,
    right: Tuple[int, int] | None,
) -> Tuple[int, int] | None:
    if left is None:
        return right
    if right is None:
        return left
    x1, y1 = left
    x2, y2 = right
    if x1 == x2 and (y1 + y2) % _SECP_P == 0:
        return None
    if left == right:
        if y1 == 0:
            return None
        slope = (3 * x1 * x1) * pow(2 * y1, -1, _SECP_P) % _SECP_P
    else:
        slope = (y2 - y1) * pow((x2 - x1) % _SECP_P, -1, _SECP_P) % _SECP_P
    x3 = (slope * slope - x1 - x2) % _SECP_P
    y3 = (slope * (x1 - x3) - y1) % _SECP_P
    return x3, y3


def _point_mul(k: int, point: Tuple[int, int] | None) -> Tuple[int, int] | None:
    if point is None or k == 0:
        return None
    result = None
    current = point
    while k:
        if k & 1:
            result = _point_add(result, current)
        current = _point_add(current, current)
        k >>= 1
    return result


def _point_from_x(x: int, odd: int) -> Tuple[int, int]:
    if not (0 <= x < _SECP_P):
        raise HiveProofError("recovery x coordinate outside secp256k1 field")
    alpha = (pow(x, 3, _SECP_P) + 7) % _SECP_P
    y = pow(alpha, (_SECP_P + 1) // 4, _SECP_P)
    if (y * y - alpha) % _SECP_P != 0:
        raise HiveProofError("invalid secp256k1 recovery point")
    if (y & 1) != odd:
        y = _SECP_P - y
    return x, y


def _compressed_point(point: Tuple[int, int]) -> bytes:
    x, y = point
    return bytes([2 | (y & 1)]) + x.to_bytes(32, "big")


def _decode_compressed(raw: bytes) -> Tuple[int, int]:
    if type(raw) is not bytes or len(raw) != 33 or raw[0] not in (2, 3):
        raise HiveSchemaError("invalid compressed secp256k1 key")
    point = _point_from_x(int.from_bytes(raw[1:], "big"), raw[0] & 1)
    if _point_mul(_SECP_N, point) is not None:
        raise HiveSchemaError("public key is not in secp256k1 subgroup")
    return point


def hive_public_key_encode(raw_compressed: bytes, prefix: str = HIVE_KEY_PREFIX) -> str:
    _decode_compressed(raw_compressed)
    checksum = _ripemd160(raw_compressed)[:4]
    return prefix + _b58encode(raw_compressed + checksum)


def hive_public_key_decode(text: str, prefix: str = HIVE_KEY_PREFIX) -> bytes:
    if type(text) is not str or not text.startswith(prefix):
        raise HiveSchemaError("Hive public-key prefix mismatch")
    payload = _b58decode(text[len(prefix):])
    if len(payload) != 37:
        raise HiveSchemaError("Hive public-key payload length mismatch")
    raw, checksum = payload[:-4], payload[-4:]
    if _ripemd160(raw)[:4] != checksum:
        raise HiveSchemaError("Hive public-key checksum mismatch")
    _decode_compressed(raw)
    return raw


def recover_hive_public_key(message: bytes, signature_hex: str) -> str:
    if type(message) is not bytes:
        raise HiveProofError("message must be bytes")
    if type(signature_hex) is not str or len(signature_hex) != 130:
        raise HiveProofError("compact signature must be 130 lowercase hex characters")
    if any(ch not in "0123456789abcdef" for ch in signature_hex):
        raise HiveProofError("compact signature must be lowercase hex")
    raw = bytes.fromhex(signature_hex)
    header = raw[0]
    if header not in (31, 32, 33, 34):
        raise HiveProofError("unsupported compact signature recovery header")
    r = int.from_bytes(raw[1:33], "big")
    s = int.from_bytes(raw[33:65], "big")
    if not (1 <= r < _SECP_N and 1 <= s < _SECP_N):
        raise HiveProofError("invalid compact signature r/s")

    recid = header - 31
    x = r + (recid >> 1) * _SECP_N
    if x >= _SECP_P:
        raise HiveProofError("invalid compact signature recovery x")
    R = _point_from_x(x, recid & 1)
    if _point_mul(_SECP_N, R) is not None:
        raise HiveProofError("invalid recovery point order")

    digest = hashlib.sha256(message).digest()
    e = int.from_bytes(digest, "big")
    r_inv = pow(r, -1, _SECP_N)
    sR = _point_mul(s, R)
    eG = _point_mul(e % _SECP_N, _SECP_G)
    neg_eG = None if eG is None else (eG[0], (-eG[1]) % _SECP_P)
    Q = _point_mul(r_inv, _point_add(sR, neg_eG))
    if Q is None:
        raise HiveProofError("recovered public key is infinity")

    # Independent ECDSA verification against recovered Q.
    w = pow(s, -1, _SECP_N)
    u1 = (e * w) % _SECP_N
    u2 = (r * w) % _SECP_N
    X = _point_add(_point_mul(u1, _SECP_G), _point_mul(u2, Q))
    if X is None or X[0] % _SECP_N != r:
        raise HiveProofError("compact signature verification failed")

    return hive_public_key_encode(_compressed_point(Q))


def _snapshot_reference(value: Any) -> Dict[str, str]:
    if type(value) is not dict or set(value) != {"kind", "id"}:
        raise HiveSchemaError("snapshot.reference field mismatch")
    if value["kind"] != "synthetic":
        raise HiveSchemaError("Stage 8A snapshot reference must be synthetic")
    return {"kind": "synthetic", "id": _text(value["id"], "reference.id")}


def _validate_authority(value: Any, field: str) -> Dict[str, Any]:
    if type(value) is not dict or set(value) != {
        "weight_threshold",
        "key_auths",
        "account_auths",
    }:
        raise HiveSchemaError(f"{field} field mismatch")
    threshold = _positive_int(value["weight_threshold"], f"{field}.weight_threshold", 2**32 - 1)
    key_auths = value["key_auths"]
    account_auths = value["account_auths"]
    if type(key_auths) is not list or type(account_auths) is not list:
        raise HiveSchemaError(f"{field} auth lists must be arrays")
    if len(key_auths) + len(account_auths) > MAX_AUTHORITY_MEMBERSHIP:
        raise HiveSchemaError(f"{field} authority membership exceeds Hive limit")

    checked_keys = []
    seen_keys = set()
    for i, pair in enumerate(key_auths):
        if type(pair) is not list or len(pair) != 2:
            raise HiveSchemaError(f"{field}.key_auths[{i}] invalid")
        key = _text(pair[0], f"{field}.key_auths[{i}].key")
        hive_public_key_decode(key)
        weight = _positive_int(pair[1], f"{field}.key_auths[{i}].weight", 65535)
        if key in seen_keys:
            raise HiveSchemaError(f"{field} duplicate key authority")
        seen_keys.add(key)
        checked_keys.append([key, weight])
    if checked_keys != sorted(checked_keys, key=lambda x: x[0]):
        raise HiveSchemaError(f"{field}.key_auths must be sorted")

    checked_accounts = []
    seen_accounts = set()
    for i, pair in enumerate(account_auths):
        if type(pair) is not list or len(pair) != 2:
            raise HiveSchemaError(f"{field}.account_auths[{i}] invalid")
        name = _account_name(pair[0], f"{field}.account_auths[{i}].account")
        weight = _positive_int(pair[1], f"{field}.account_auths[{i}].weight", 65535)
        if name in seen_accounts:
            raise HiveSchemaError(f"{field} duplicate account authority")
        seen_accounts.add(name)
        checked_accounts.append([name, weight])
    if checked_accounts != sorted(checked_accounts, key=lambda x: x[0]):
        raise HiveSchemaError(f"{field}.account_auths must be sorted")

    return {
        "weight_threshold": threshold,
        "key_auths": checked_keys,
        "account_auths": checked_accounts,
    }


def validate_snapshot_mapping(value: Mapping[str, Any]) -> Dict[str, Any]:
    expected = {
        "schema",
        "network",
        "chain_id",
        "authority_ruleset",
        "max_sig_check_depth",
        "max_authority_membership",
        "max_sig_check_accounts",
        "reference",
        "accounts",
    }
    if not isinstance(value, Mapping) or set(value) != expected:
        raise HiveSchemaError("snapshot field mismatch")
    s = dict(value)
    if s["schema"] != SNAPSHOT_SCHEMA:
        raise HiveSchemaError("unsupported snapshot schema")
    if s["network"] != HIVE_NETWORK:
        raise HiveSchemaError("snapshot network mismatch")
    if s["chain_id"] != HIVE_CHAIN_ID:
        raise HiveSchemaError("snapshot chain id mismatch")
    if s["authority_ruleset"] != AUTHORITY_RULESET:
        raise HiveSchemaError("snapshot authority ruleset mismatch")
    if s["max_sig_check_depth"] != MAX_SIG_CHECK_DEPTH:
        raise HiveSchemaError("snapshot recursion limit mismatch")
    if s["max_authority_membership"] != MAX_AUTHORITY_MEMBERSHIP:
        raise HiveSchemaError("snapshot membership limit mismatch")
    if s["max_sig_check_accounts"] != MAX_SIG_CHECK_ACCOUNTS:
        raise HiveSchemaError("snapshot account-check limit mismatch")

    reference = _snapshot_reference(s["reference"])
    if type(s["accounts"]) is not list or not s["accounts"]:
        raise HiveSchemaError("snapshot.accounts must be a non-empty array")
    accounts = []
    names = set()
    for i, item in enumerate(s["accounts"]):
        if type(item) is not dict or set(item) != {"name", "active"}:
            raise HiveSchemaError(f"accounts[{i}] field mismatch")
        name = _account_name(item["name"], f"accounts[{i}].name")
        if name in names:
            raise HiveSchemaError("duplicate snapshot account")
        names.add(name)
        accounts.append({"name": name, "active": _validate_authority(item["active"], f"accounts[{i}].active")})
    if accounts != sorted(accounts, key=lambda x: x["name"]):
        raise HiveSchemaError("snapshot accounts must be sorted")

    # Stage-8A snapshot is required to be closed over its delegated account graph.
    for item in accounts:
        for name, _ in item["active"]["account_auths"]:
            if name not in names:
                raise HiveSchemaError(f"missing delegated account in snapshot: {name}")

    return {
        "schema": SNAPSHOT_SCHEMA,
        "network": HIVE_NETWORK,
        "chain_id": HIVE_CHAIN_ID,
        "authority_ruleset": AUTHORITY_RULESET,
        "max_sig_check_depth": MAX_SIG_CHECK_DEPTH,
        "max_authority_membership": MAX_AUTHORITY_MEMBERSHIP,
        "max_sig_check_accounts": MAX_SIG_CHECK_ACCOUNTS,
        "reference": reference,
        "accounts": accounts,
    }


def create_snapshot_artifact(*, reference_id: str, accounts: list[dict[str, Any]]) -> bytes:
    value = {
        "schema": SNAPSHOT_SCHEMA,
        "network": HIVE_NETWORK,
        "chain_id": HIVE_CHAIN_ID,
        "authority_ruleset": AUTHORITY_RULESET,
        "max_sig_check_depth": MAX_SIG_CHECK_DEPTH,
        "max_authority_membership": MAX_AUTHORITY_MEMBERSHIP,
        "max_sig_check_accounts": MAX_SIG_CHECK_ACCOUNTS,
        "reference": {"kind": "synthetic", "id": reference_id},
        "accounts": accounts,
    }
    checked = validate_snapshot_mapping(value)
    return _canonical_json(checked)


def parse_snapshot_artifact(raw: bytes) -> Dict[str, Any]:
    obj = _strict_json_object(raw, "authority snapshot")
    checked = validate_snapshot_mapping(obj)
    canonical = _canonical_json(checked)
    if raw != canonical:
        raise HiveSchemaError("authority snapshot bytes are not canonical")
    return checked


def snapshot_digest(raw: bytes) -> str:
    parse_snapshot_artifact(raw)
    return hashlib.sha256(raw).hexdigest()


def validate_policy(policy: HiveActivePolicy) -> HiveActivePolicy:
    if not isinstance(policy, HiveActivePolicy):
        raise HivePolicyError("policy must be HiveActivePolicy")
    _text(policy.policy_id, "policy.policy_id")
    _text(policy.project, "policy.project")
    _text(policy.authority_domain, "policy.authority_domain")
    account = _account_name(policy.hive_account, "policy.hive_account")
    expected_subject = f"{HIVE_NETWORK}:@{account}:{AUTHORITY_LEVEL}"
    if policy.anchor_subject != expected_subject:
        raise HivePolicyError("policy anchor_subject mismatch")
    _text(policy.expected_generation, "policy.expected_generation")
    if policy.minimum_anchor_count != 1:
        raise HivePolicyError("Hive profile minimum_anchor_count must be 1")
    _hex64(policy.hive_authority_snapshot_digest, "policy.hive_authority_snapshot_digest")
    _safe_claim(policy.native_policy_provenance_claim, "policy.native_policy_provenance_claim")
    return policy


def canonical_policy_semantics(policy: HiveActivePolicy) -> Dict[str, Any]:
    validate_policy(policy)
    return {
        "policy_schema": POLICY_SCHEMA,
        "policy_id": policy.policy_id,
        "project": policy.project,
        "authority_domain": policy.authority_domain,
        "anchor_profile": PROFILE,
        "anchor_subject": policy.anchor_subject,
        "expected_generation": policy.expected_generation,
        "minimum_anchor_count": 1,
        "hive_network": HIVE_NETWORK,
        "hive_chain_id": HIVE_CHAIN_ID,
        "hive_account": policy.hive_account,
        "hive_authority_level": AUTHORITY_LEVEL,
        "hive_authority_ruleset": AUTHORITY_RULESET,
        "keychain_signing_semantics": KEYCHAIN_SIGNING_SEMANTICS,
        "hive_public_key_prefix": HIVE_KEY_PREFIX,
        "hive_authority_snapshot_digest": policy.hive_authority_snapshot_digest,
        "max_sig_check_depth": MAX_SIG_CHECK_DEPTH,
        "max_authority_membership": MAX_AUTHORITY_MEMBERSHIP,
        "max_sig_check_accounts": MAX_SIG_CHECK_ACCOUNTS,
    }


def canonical_policy_bytes(policy: HiveActivePolicy) -> bytes:
    return _canonical_json(canonical_policy_semantics(policy))


def policy_digest(policy: HiveActivePolicy) -> str:
    return hashlib.sha256(canonical_policy_bytes(policy)).hexdigest()


def create_manifest_for_policy(
    *,
    policy: HiveActivePolicy,
    candidate_authority_key_id: str,
    challenge: str,
    note_digest: str | None = None,
) -> bytes:
    validate_policy(policy)
    return common.create_manifest_artifact(
        project=policy.project,
        authority_domain=policy.authority_domain,
        candidate_authority_key_id=candidate_authority_key_id,
        bootstrap_policy=policy.policy_id,
        bootstrap_policy_digest=policy_digest(policy),
        generation=policy.expected_generation,
        challenge=challenge,
        anchor_profile=PROFILE,
        anchor_subject=policy.anchor_subject,
        note_digest=note_digest,
    )


PROOF_FIELDS = (
    "schema",
    "manifest_digest",
    "anchor_profile",
    "anchor_subject",
    "hive_network",
    "hive_account",
    "authority_level",
    "authority_snapshot_digest",
    "signature_hex",
    "claimed_public_key",
)


def _validate_proof_mapping(value: Mapping[str, Any]) -> Dict[str, Any]:
    if not isinstance(value, Mapping) or set(value) != set(PROOF_FIELDS):
        raise HiveSchemaError("Hive proof field mismatch")
    p = dict(value)
    if p["schema"] != PROOF_SCHEMA:
        raise HiveSchemaError("unsupported Hive proof schema")
    _hex64(p["manifest_digest"], "proof.manifest_digest")
    if p["anchor_profile"] != PROFILE:
        raise HiveSchemaError("proof anchor profile mismatch")
    _text(p["anchor_subject"], "proof.anchor_subject")
    if p["hive_network"] != HIVE_NETWORK:
        raise HiveSchemaError("proof network mismatch")
    _account_name(p["hive_account"], "proof.hive_account")
    if p["authority_level"] != AUTHORITY_LEVEL:
        raise HiveSchemaError("proof authority level mismatch")
    _hex64(p["authority_snapshot_digest"], "proof.authority_snapshot_digest")
    sig = p["signature_hex"]
    if type(sig) is not str or len(sig) != 130 or any(ch not in "0123456789abcdef" for ch in sig):
        raise HiveSchemaError("proof signature_hex must be 130 lowercase hex characters")
    if p["claimed_public_key"] is not None:
        hive_public_key_decode(p["claimed_public_key"])
    return p


def create_hive_proof_artifact(
    *,
    manifest_raw: bytes,
    policy: HiveActivePolicy,
    signature_hex: str,
    claimed_public_key: str | None,
) -> bytes:
    manifest_dig = common.manifest_digest(manifest_raw)
    p = {
        "schema": PROOF_SCHEMA,
        "manifest_digest": manifest_dig,
        "anchor_profile": PROFILE,
        "anchor_subject": policy.anchor_subject,
        "hive_network": HIVE_NETWORK,
        "hive_account": policy.hive_account,
        "authority_level": AUTHORITY_LEVEL,
        "authority_snapshot_digest": policy.hive_authority_snapshot_digest,
        "signature_hex": signature_hex,
        "claimed_public_key": claimed_public_key,
    }
    checked = _validate_proof_mapping(p)
    return _canonical_json({field: checked[field] for field in PROOF_FIELDS})


def parse_hive_proof_artifact(raw: bytes) -> Dict[str, Any]:
    obj = _strict_json_object(raw, "Hive proof")
    checked = _validate_proof_mapping(obj)
    canonical = _canonical_json({field: checked[field] for field in PROOF_FIELDS})
    if raw != canonical:
        raise HiveSchemaError("Hive proof bytes are not canonical")
    return checked


def _snapshot_accounts(snapshot: Mapping[str, Any]) -> Dict[str, Dict[str, Any]]:
    return {item["name"]: item["active"] for item in snapshot["accounts"]}


def active_authority_satisfied(
    *,
    snapshot: Mapping[str, Any],
    account: str,
    signer_keys: set[str],
) -> bool:
    checked = validate_snapshot_mapping(snapshot)
    account = _account_name(account, "account")
    accounts = _snapshot_accounts(checked)
    if account not in accounts:
        return False

    approved_by: set[str] = set()
    account_auth_count = 1  # strict-current Hive sign_state root check

    def check_auth(auth: Mapping[str, Any], depth: int) -> bool:
        nonlocal account_auth_count
        total_weight = 0
        membership = 0

        for key, weight in auth["key_auths"]:
            if key in signer_keys:
                total_weight += weight
                if total_weight >= auth["weight_threshold"]:
                    return True
            membership += 1
            if MAX_AUTHORITY_MEMBERSHIP > 0 and membership >= MAX_AUTHORITY_MEMBERSHIP:
                return False

        for delegated, parent_weight in auth["account_auths"]:
            if delegated in approved_by:
                total_weight += parent_weight
                if total_weight >= auth["weight_threshold"]:
                    return True
            else:
                if depth != MAX_SIG_CHECK_DEPTH:
                    if account_auth_count >= MAX_SIG_CHECK_ACCOUNTS:
                        return False
                    account_auth_count += 1
                    delegated_auth = accounts.get(delegated)
                    if delegated_auth is not None and check_auth(delegated_auth, depth + 1):
                        approved_by.add(delegated)
                        total_weight += parent_weight
                        if total_weight >= auth["weight_threshold"]:
                            return True
            membership += 1
            if MAX_AUTHORITY_MEMBERSHIP > 0 and membership >= MAX_AUTHORITY_MEMBERSHIP:
                return False

        return total_weight >= auth["weight_threshold"]

    return check_auth(accounts[account], 0)


def _match_manifest_policy(
    manifest: Mapping[str, Any],
    policy: HiveActivePolicy,
) -> str:
    digest = policy_digest(policy)
    pairs = (
        ("project", manifest["project"], policy.project),
        ("authority_domain", manifest["authority_domain"], policy.authority_domain),
        ("bootstrap_policy", manifest["bootstrap_policy"], policy.policy_id),
        ("bootstrap_policy_digest", manifest["bootstrap_policy_digest"], digest),
        ("generation", manifest["generation"], policy.expected_generation),
        ("anchor_profile", manifest["anchor_profile"], PROFILE),
        ("anchor_subject", manifest["anchor_subject"], policy.anchor_subject),
    )
    mismatches = [name for name, actual, expected in pairs if actual != expected]
    if mismatches:
        raise HivePolicyError(f"manifest does not match Hive policy: {mismatches}")
    return digest


def verify_hive_bootstrap(
    *,
    manifest_raw: bytes,
    proof_artifacts: Iterable[bytes],
    policy: HiveActivePolicy,
    snapshot_raw: bytes,
) -> Dict[str, Any]:
    validate_policy(policy)
    snapshot = parse_snapshot_artifact(snapshot_raw)
    snapshot_dig = hashlib.sha256(snapshot_raw).hexdigest()
    if snapshot_dig != policy.hive_authority_snapshot_digest:
        raise HivePolicyError("supplied authority snapshot digest does not match policy")

    manifest = common.parse_manifest_artifact(manifest_raw)
    exact_policy_digest = _match_manifest_policy(manifest, policy)
    expected_manifest_digest = common.manifest_digest(manifest_raw)
    message = common.anchor_statement(manifest_raw)

    observed = 0
    rejected = 0
    valid_signers: set[str] = set()

    for raw in proof_artifacts:
        observed += 1
        if type(raw) is not bytes:
            rejected += 1
            continue
        try:
            proof = parse_hive_proof_artifact(raw)
        except HiveAdapterError:
            rejected += 1
            continue

        expected = (
            proof["manifest_digest"] == expected_manifest_digest
            and proof["anchor_subject"] == policy.anchor_subject
            and proof["hive_account"] == policy.hive_account
            and proof["authority_snapshot_digest"] == snapshot_dig
        )
        if not expected:
            rejected += 1
            continue

        try:
            recovered = recover_hive_public_key(message, proof["signature_hex"])
        except HiveAdapterError:
            rejected += 1
            continue

        if proof["claimed_public_key"] is not None and proof["claimed_public_key"] != recovered:
            rejected += 1
            continue

        valid_signers.add(recovered)

    if not valid_signers:
        raise HiveProofError("no qualifying Hive compact signatures")

    if not active_authority_satisfied(
        snapshot=snapshot,
        account=policy.hive_account,
        signer_keys=valid_signers,
    ):
        raise HiveAuthorityError("recovered signer set does not satisfy Hive Active authority")

    return {
        "bootstrap_manifest_valid": True,
        "manifest_policy_binding_valid": True,
        "policy_digest_matched": True,
        "hive_compact_signatures_valid": True,
        "hive_active_authority_satisfied": True,
        "project": manifest["project"],
        "authority_domain": manifest["authority_domain"],
        "candidate_authority_key_id": manifest["candidate_authority_key_id"],
        "bootstrap_policy_id": policy.policy_id,
        "bootstrap_policy_digest": exact_policy_digest,
        "manifest_digest": expected_manifest_digest,
        "anchor_profile": PROFILE,
        "anchor_subject": policy.anchor_subject,
        "hive_network": HIVE_NETWORK,
        "hive_chain_id": HIVE_CHAIN_ID,
        "hive_account": policy.hive_account,
        "hive_authority_level": AUTHORITY_LEVEL,
        "hive_authority_ruleset": AUTHORITY_RULESET,
        "hive_authority_snapshot_digest": snapshot_dig,
        "hive_authority_snapshot_authenticated": False,
        "native_policy_provenance_claim": policy.native_policy_provenance_claim,
        "native_policy_provenance_authenticated": False,
        "trust_statement_scope": "RELATIVE_TO_SUPPLIED_POLICY_AND_AUTHORITY_SNAPSHOT",
        "observed_hive_proof_count": observed,
        "rejected_hive_proof_count": rejected,
        "unique_recovered_signer_count": len(valid_signers),
        "recovered_signer_public_keys": sorted(valid_signers),
        "bootstrap_trust_root_established_for_observed_policy": True,
        "execution_authorized_by_cpi": False,
    }
