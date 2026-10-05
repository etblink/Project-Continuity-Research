from __future__ import annotations

import base64
import binascii
import hashlib
import json
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat


MANIFEST_SCHEMA = "cpi.native-bootstrap-manifest/0.2"
POLICY_SCHEMA = "cpi.native-bootstrap-policy/0.2"
PROOF_SCHEMA = "cpi.bootstrap-anchor-proof/0.2"
OFFLINE_ED25519_V1 = "OFFLINE_ED25519_V1"
HIVE_ACTIVE_AUTHORITY_V1 = "HIVE_ACTIVE_AUTHORITY_V1"
SIGNATURE_ALGORITHM = "Ed25519"
RESEARCH_BOOTSTRAP_VERSION = "0.2.1"

MANIFEST_FIELDS = (
    "schema",
    "project",
    "authority_domain",
    "candidate_authority_key_id",
    "bootstrap_policy",
    "bootstrap_policy_digest",
    "generation",
    "challenge",
    "anchor_profile",
    "anchor_subject",
    "note_digest",
)

POLICY_SEMANTIC_FIELDS = (
    "policy_schema",
    "policy_id",
    "project",
    "authority_domain",
    "anchor_profile",
    "anchor_subject",
    "expected_generation",
    "minimum_anchor_count",
    "anchor_key_id",
)

PROOF_FIELDS = (
    "schema",
    "manifest_digest",
    "anchor_profile",
    "anchor_subject",
    "signer_key_id",
    "signature_algorithm",
    "signature",
)


class BootstrapError(ValueError):
    pass


class BootstrapSchemaError(BootstrapError):
    pass


class BootstrapPolicyError(BootstrapError):
    pass


class BootstrapProofError(BootstrapError):
    pass


class BootstrapConflictError(BootstrapError):
    pass


class UnsupportedAnchorProfileError(BootstrapError):
    pass


@dataclass(frozen=True)
class NativeBootstrapPolicy:
    policy_id: str
    project: str
    authority_domain: str
    anchor_profile: str
    anchor_subject: str
    expected_generation: str
    minimum_anchor_count: int
    pinned_anchor_public_key: bytes | None
    native_policy_provenance_claim: str


# Ed25519 constants and subgroup checks mirror the independently qualified
# Stage-6 pin-validation expectations.
_ED_P = 2**255 - 19
_ED_D = (-121665 * pow(121666, _ED_P - 2, _ED_P)) % _ED_P
_ED_I = pow(2, (_ED_P - 1) // 4, _ED_P)
_ED_L = 2**252 + 27742317777372353535851937790883648493
_ED_IDENTITY = (0, 1)


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
        raise BootstrapSchemaError("object cannot be canonically serialized") from exc


def _nonempty_text(value: Any, field: str) -> str:
    if type(value) is not str or not value:
        raise BootstrapSchemaError(f"{field} must be a non-empty string")
    try:
        value.encode("utf-8", "strict")
    except UnicodeEncodeError as exc:
        raise BootstrapSchemaError(f"{field} is not valid Unicode scalar text") from exc
    return value


def _nonblank_text(value: Any, field: str) -> str:
    value = _nonempty_text(value, field)
    if not value.strip():
        raise BootstrapSchemaError(f"{field} must not be whitespace-only")
    return value


def _provenance_claim(value: Any, field: str) -> str:
    value = _nonblank_text(value, field)
    if len(value) > 512:
        raise BootstrapSchemaError(f"{field} must be at most 512 Unicode scalars")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in value):
        raise BootstrapSchemaError(f"{field} must not contain control characters")
    return value


def _hex64(value: Any, field: str) -> str:
    if type(value) is not str or len(value) != 64:
        raise BootstrapSchemaError(f"{field} must be 64 lowercase hex characters")
    if any(ch not in "0123456789abcdef" for ch in value):
        raise BootstrapSchemaError(f"{field} must be 64 lowercase hex characters")
    return value


def _key_id(value: Any, field: str) -> str:
    value = _nonempty_text(value, field)
    prefix = "ed25519-sha256:"
    if not value.startswith(prefix):
        raise BootstrapSchemaError(f"{field} must use ed25519-sha256")
    _hex64(value[len(prefix):], field)
    return value


def _note_digest(value: Any) -> str | None:
    if value is None:
        return None
    return _hex64(value, "note_digest")


def _ed_decode(raw: bytes) -> Tuple[int, int]:
    n = int.from_bytes(raw, "little")
    sign = (n >> 255) & 1
    y = n & ((1 << 255) - 1)
    if y >= _ED_P:
        raise BootstrapPolicyError("non-canonical Ed25519 public-key encoding")

    denominator = (_ED_D * y * y + 1) % _ED_P
    if denominator == 0:
        raise BootstrapPolicyError("invalid Ed25519 public-key point")

    x2 = ((y * y - 1) * pow(denominator, _ED_P - 2, _ED_P)) % _ED_P
    x = pow(x2, (_ED_P + 3) // 8, _ED_P)
    if (x * x - x2) % _ED_P != 0:
        x = (x * _ED_I) % _ED_P
    if (x * x - x2) % _ED_P != 0:
        raise BootstrapPolicyError("invalid Ed25519 public-key point")
    if x == 0 and sign:
        raise BootstrapPolicyError("non-canonical Ed25519 x sign")
    if (x & 1) != sign:
        x = _ED_P - x

    if (-x * x + y * y - 1 - _ED_D * x * x * y * y) % _ED_P != 0:
        raise BootstrapPolicyError("public key is not on the Ed25519 curve")
    return x, y


def _ed_add(
    left: Tuple[int, int],
    right: Tuple[int, int],
) -> Tuple[int, int]:
    x1, y1 = left
    x2, y2 = right
    product = (_ED_D * x1 * x2 * y1 * y2) % _ED_P
    dx = (1 + product) % _ED_P
    dy = (1 - product) % _ED_P
    if dx == 0 or dy == 0:
        raise BootstrapPolicyError("invalid Ed25519 subgroup arithmetic")
    x3 = ((x1 * y2 + y1 * x2) * pow(dx, _ED_P - 2, _ED_P)) % _ED_P
    y3 = ((y1 * y2 + x1 * x2) * pow(dy, _ED_P - 2, _ED_P)) % _ED_P
    return x3, y3


def _ed_mul(k: int, point: Tuple[int, int]) -> Tuple[int, int]:
    result = _ED_IDENTITY
    current = point
    while k:
        if k & 1:
            result = _ed_add(result, current)
        current = _ed_add(current, current)
        k >>= 1
    return result


@lru_cache(maxsize=128)
def _validate_ed25519_public_key_cached(raw: bytes) -> bytes:
    point = _ed_decode(raw)
    if point == _ED_IDENTITY:
        raise BootstrapPolicyError("identity Ed25519 public key is forbidden")
    if _ed_mul(_ED_L, point) != _ED_IDENTITY:
        raise BootstrapPolicyError(
            "Ed25519 public key is not in the prime-order subgroup"
        )
    try:
        Ed25519PublicKey.from_public_bytes(raw)
    except ValueError as exc:
        raise BootstrapPolicyError("invalid Ed25519 public key") from exc
    return raw


def _validate_ed25519_public_key(raw: bytes) -> bytes:
    if type(raw) is not bytes or len(raw) != 32:
        raise BootstrapPolicyError("Ed25519 public key must be exactly 32 raw bytes")
    return _validate_ed25519_public_key_cached(raw)


def public_key_id(public_key: bytes) -> str:
    raw = _validate_ed25519_public_key(public_key)
    return "ed25519-sha256:" + hashlib.sha256(raw).hexdigest()


def offline_anchor_subject(public_key: bytes) -> str:
    return "offline-ed25519:" + public_key_id(public_key)


def _validate_policy_structure(policy: NativeBootstrapPolicy) -> NativeBootstrapPolicy:
    if not isinstance(policy, NativeBootstrapPolicy):
        raise BootstrapPolicyError("policy must be NativeBootstrapPolicy")

    for field in (
        "policy_id",
        "project",
        "authority_domain",
        "anchor_profile",
        "anchor_subject",
        "expected_generation",
    ):
        _nonempty_text(getattr(policy, field), f"policy.{field}")

    _provenance_claim(
        policy.native_policy_provenance_claim,
        "policy.native_policy_provenance_claim",
    )

    if (
        type(policy.minimum_anchor_count) is not int
        or policy.minimum_anchor_count < 1
        or policy.minimum_anchor_count > 2**53 - 1
    ):
        raise BootstrapPolicyError(
            "minimum_anchor_count must be a positive JCS-safe integer"
        )

    if policy.anchor_profile == OFFLINE_ED25519_V1:
        if type(policy.pinned_anchor_public_key) is not bytes:
            raise BootstrapPolicyError(
                "OFFLINE_ED25519_V1 requires a pinned raw Ed25519 key"
            )
        anchor_key_id = public_key_id(policy.pinned_anchor_public_key)
        expected_subject = "offline-ed25519:" + anchor_key_id
        if policy.anchor_subject != expected_subject:
            raise BootstrapPolicyError(
                "offline anchor_subject does not match pinned key"
            )
    elif policy.anchor_profile == HIVE_ACTIVE_AUTHORITY_V1:
        if policy.pinned_anchor_public_key is not None:
            raise BootstrapPolicyError(
                "Hive profile does not use Ed25519 pinned_anchor_public_key"
            )
    else:
        raise UnsupportedAnchorProfileError(
            f"unsupported anchor profile: {policy.anchor_profile}"
        )

    return policy


def validate_policy(policy: NativeBootstrapPolicy) -> NativeBootstrapPolicy:
    _validate_policy_structure(policy)
    if policy.anchor_profile == OFFLINE_ED25519_V1:
        if policy.minimum_anchor_count != 1:
            raise UnsupportedAnchorProfileError(
                "OFFLINE_ED25519_V1 verifier currently supports exactly one anchor"
            )
    elif policy.anchor_profile == HIVE_ACTIVE_AUTHORITY_V1:
        if policy.minimum_anchor_count != 1:
            raise UnsupportedAnchorProfileError(
                "HIVE_ACTIVE_AUTHORITY_V1 common placeholder expects one profile proof"
            )
    return policy


def canonical_policy_semantics(policy: NativeBootstrapPolicy) -> Dict[str, Any]:
    _validate_policy_structure(policy)
    anchor_key_id: str | None
    if policy.anchor_profile == OFFLINE_ED25519_V1:
        anchor_key_id = public_key_id(policy.pinned_anchor_public_key)
    else:
        anchor_key_id = None

    record: Dict[str, Any] = {
        "policy_schema": POLICY_SCHEMA,
        "policy_id": policy.policy_id,
        "project": policy.project,
        "authority_domain": policy.authority_domain,
        "anchor_profile": policy.anchor_profile,
        "anchor_subject": policy.anchor_subject,
        "expected_generation": policy.expected_generation,
        "minimum_anchor_count": policy.minimum_anchor_count,
        "anchor_key_id": anchor_key_id,
    }
    return record


def canonical_policy_bytes(policy: NativeBootstrapPolicy) -> bytes:
    record = canonical_policy_semantics(policy)
    return _canonical_json(
        {field: record[field] for field in POLICY_SEMANTIC_FIELDS}
    )


def policy_digest(policy: NativeBootstrapPolicy) -> str:
    return hashlib.sha256(canonical_policy_bytes(policy)).hexdigest()


def _validate_manifest_mapping(value: Mapping[str, Any]) -> Dict[str, Any]:
    if not isinstance(value, Mapping):
        raise BootstrapSchemaError("manifest must be an object")
    keys = set(value)
    expected = set(MANIFEST_FIELDS)
    if keys != expected:
        missing = sorted(expected - keys)
        extra = sorted(keys - expected)
        raise BootstrapSchemaError(
            f"manifest field mismatch missing={missing} extra={extra}"
        )

    m = dict(value)
    if m["schema"] != MANIFEST_SCHEMA:
        raise BootstrapSchemaError("unsupported manifest schema")

    for field in (
        "project",
        "authority_domain",
        "bootstrap_policy",
        "generation",
        "anchor_profile",
        "anchor_subject",
    ):
        _nonempty_text(m[field], field)

    _key_id(m["candidate_authority_key_id"], "candidate_authority_key_id")
    _hex64(m["bootstrap_policy_digest"], "bootstrap_policy_digest")
    _hex64(m["challenge"], "challenge")
    _note_digest(m["note_digest"])
    return m


def _pairs_no_duplicates(
    pairs: Sequence[Tuple[str, Any]],
) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise BootstrapSchemaError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def _reject_number(_: str) -> Any:
    raise BootstrapSchemaError(
        "numeric JSON values are forbidden in manifest/proof artifacts"
    )


def _parse_canonical_object(raw: bytes, kind: str) -> Dict[str, Any]:
    if type(raw) is not bytes:
        raise BootstrapSchemaError(f"{kind} artifact must be raw bytes")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise BootstrapSchemaError("UTF-8 BOM is forbidden")

    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise BootstrapSchemaError(
            f"{kind} artifact is not valid UTF-8"
        ) from exc

    try:
        parsed = json.loads(
            text,
            object_pairs_hook=_pairs_no_duplicates,
            parse_int=_reject_number,
            parse_float=_reject_number,
            parse_constant=_reject_number,
        )
    except BootstrapError:
        raise
    except (json.JSONDecodeError, TypeError, ValueError, RecursionError) as exc:
        raise BootstrapSchemaError(
            f"{kind} artifact is not strict JSON"
        ) from exc

    if type(parsed) is not dict:
        raise BootstrapSchemaError(f"{kind} artifact root must be an object")
    return parsed


def create_manifest_artifact(
    *,
    project: str,
    authority_domain: str,
    candidate_authority_key_id: str,
    bootstrap_policy: str,
    bootstrap_policy_digest: str,
    generation: str,
    challenge: str,
    anchor_profile: str,
    anchor_subject: str,
    note_digest: str | None = None,
) -> bytes:
    manifest = {
        "schema": MANIFEST_SCHEMA,
        "project": project,
        "authority_domain": authority_domain,
        "candidate_authority_key_id": candidate_authority_key_id,
        "bootstrap_policy": bootstrap_policy,
        "bootstrap_policy_digest": bootstrap_policy_digest,
        "generation": generation,
        "challenge": challenge,
        "anchor_profile": anchor_profile,
        "anchor_subject": anchor_subject,
        "note_digest": note_digest,
    }
    checked = _validate_manifest_mapping(manifest)
    return _canonical_json({field: checked[field] for field in MANIFEST_FIELDS})


def create_manifest_for_policy(
    *,
    policy: NativeBootstrapPolicy,
    candidate_authority_key_id: str,
    challenge: str,
    note_digest: str | None = None,
) -> bytes:
    _validate_policy_structure(policy)
    return create_manifest_artifact(
        project=policy.project,
        authority_domain=policy.authority_domain,
        candidate_authority_key_id=candidate_authority_key_id,
        bootstrap_policy=policy.policy_id,
        bootstrap_policy_digest=policy_digest(policy),
        generation=policy.expected_generation,
        challenge=challenge,
        anchor_profile=policy.anchor_profile,
        anchor_subject=policy.anchor_subject,
        note_digest=note_digest,
    )


def parse_manifest_artifact(raw: bytes) -> Dict[str, Any]:
    parsed = _parse_canonical_object(raw, "manifest")
    checked = _validate_manifest_mapping(parsed)
    canonical = _canonical_json(
        {field: checked[field] for field in MANIFEST_FIELDS}
    )
    if raw != canonical:
        raise BootstrapSchemaError("manifest bytes are not canonical")
    return checked


def manifest_digest(raw: bytes) -> str:
    parse_manifest_artifact(raw)
    return hashlib.sha256(raw).hexdigest()


def anchor_statement(manifest_raw: bytes) -> bytes:
    digest = manifest_digest(manifest_raw)
    return (
        "CPI-NATIVE-BOOTSTRAP/0.2\n"
        f"manifest-sha256={digest}"
    ).encode("utf-8")


def _validate_proof_mapping(value: Mapping[str, Any]) -> Dict[str, Any]:
    if not isinstance(value, Mapping):
        raise BootstrapSchemaError("proof must be an object")
    keys = set(value)
    expected = set(PROOF_FIELDS)
    if keys != expected:
        missing = sorted(expected - keys)
        extra = sorted(keys - expected)
        raise BootstrapSchemaError(
            f"proof field mismatch missing={missing} extra={extra}"
        )

    p = dict(value)
    if p["schema"] != PROOF_SCHEMA:
        raise BootstrapSchemaError("unsupported proof schema")
    _hex64(p["manifest_digest"], "manifest_digest")

    for field in (
        "anchor_profile",
        "anchor_subject",
        "signature_algorithm",
        "signature",
    ):
        _nonempty_text(p[field], field)

    _key_id(p["signer_key_id"], "signer_key_id")
    if p["signature_algorithm"] != SIGNATURE_ALGORITHM:
        raise BootstrapSchemaError("unsupported signature algorithm")

    try:
        sig = base64.b64decode(p["signature"], validate=True)
    except (binascii.Error, ValueError) as exc:
        raise BootstrapSchemaError(
            "signature is not canonical base64"
        ) from exc

    if (
        len(sig) != 64
        or base64.b64encode(sig).decode("ascii") != p["signature"]
    ):
        raise BootstrapSchemaError(
            "signature is not canonical Ed25519 base64"
        )
    return p


def create_offline_ed25519_proof(
    *,
    manifest_raw: bytes,
    private_key: Ed25519PrivateKey,
) -> bytes:
    if not isinstance(private_key, Ed25519PrivateKey):
        raise BootstrapProofError(
            "private_key must be Ed25519PrivateKey"
        )

    public_raw = private_key.public_key().public_bytes(
        Encoding.Raw,
        PublicFormat.Raw,
    )
    signer_key_id = public_key_id(public_raw)

    proof = {
        "schema": PROOF_SCHEMA,
        "manifest_digest": manifest_digest(manifest_raw),
        "anchor_profile": OFFLINE_ED25519_V1,
        "anchor_subject": "offline-ed25519:" + signer_key_id,
        "signer_key_id": signer_key_id,
        "signature_algorithm": SIGNATURE_ALGORITHM,
        "signature": base64.b64encode(
            private_key.sign(anchor_statement(manifest_raw))
        ).decode("ascii"),
    }

    checked = _validate_proof_mapping(proof)
    return _canonical_json({field: checked[field] for field in PROOF_FIELDS})


def parse_proof_artifact(raw: bytes) -> Dict[str, Any]:
    parsed = _parse_canonical_object(raw, "proof")
    checked = _validate_proof_mapping(parsed)
    canonical = _canonical_json(
        {field: checked[field] for field in PROOF_FIELDS}
    )
    if raw != canonical:
        raise BootstrapSchemaError("proof bytes are not canonical")
    return checked


def _match_manifest_to_policy(
    manifest: Mapping[str, Any],
    policy: NativeBootstrapPolicy,
) -> str:
    digest = policy_digest(policy)
    pairs = (
        ("project", manifest["project"], policy.project),
        (
            "authority_domain",
            manifest["authority_domain"],
            policy.authority_domain,
        ),
        ("bootstrap_policy", manifest["bootstrap_policy"], policy.policy_id),
        (
            "bootstrap_policy_digest",
            manifest["bootstrap_policy_digest"],
            digest,
        ),
        (
            "anchor_profile",
            manifest["anchor_profile"],
            policy.anchor_profile,
        ),
        (
            "anchor_subject",
            manifest["anchor_subject"],
            policy.anchor_subject,
        ),
        (
            "generation",
            manifest["generation"],
            policy.expected_generation,
        ),
    )
    mismatches = [
        name for name, actual, expected in pairs if actual != expected
    ]
    if mismatches:
        raise BootstrapPolicyError(
            f"manifest does not match native policy: {mismatches}"
        )

    if policy.anchor_profile == OFFLINE_ED25519_V1:
        anchor_key_id = public_key_id(policy.pinned_anchor_public_key)
        if manifest["candidate_authority_key_id"] == anchor_key_id:
            raise BootstrapPolicyError(
                "candidate Authority Capsule key must be independent "
                "from the bootstrap anchor key"
            )
    return digest


def _qualify_offline_proofs(
    *,
    manifest_raw: bytes,
    proof_artifacts: Iterable[bytes],
    policy: NativeBootstrapPolicy,
) -> Dict[str, int]:
    expected_manifest_digest = manifest_digest(manifest_raw)
    expected_key_id = public_key_id(policy.pinned_anchor_public_key)
    public_key = Ed25519PublicKey.from_public_bytes(
        policy.pinned_anchor_public_key
    )

    artifact_count = 0
    unique_candidate_count = 0
    rejected_count = 0
    valid_signer_ids: set[str] = set()
    seen_raw_digests: set[str] = set()

    for raw in proof_artifacts:
        artifact_count += 1
        if type(raw) is not bytes:
            rejected_count += 1
            continue

        raw_digest = hashlib.sha256(raw).hexdigest()
        if raw_digest in seen_raw_digests:
            continue
        seen_raw_digests.add(raw_digest)
        unique_candidate_count += 1

        try:
            proof = parse_proof_artifact(raw)
        except BootstrapError:
            rejected_count += 1
            continue

        if proof["manifest_digest"] != expected_manifest_digest:
            rejected_count += 1
            continue
        if proof["anchor_profile"] != policy.anchor_profile:
            rejected_count += 1
            continue
        if proof["anchor_subject"] != policy.anchor_subject:
            rejected_count += 1
            continue
        if proof["signer_key_id"] != expected_key_id:
            rejected_count += 1
            continue

        signature = base64.b64decode(proof["signature"], validate=True)
        try:
            public_key.verify(signature, anchor_statement(manifest_raw))
        except InvalidSignature:
            rejected_count += 1
            continue

        valid_signer_ids.add(proof["signer_key_id"])

    if len(valid_signer_ids) < policy.minimum_anchor_count:
        raise BootstrapProofError(
            "insufficient qualifying independent anchor proofs"
        )

    return {
        "proof_artifact_count": artifact_count,
        "unique_proof_candidate_count": unique_candidate_count,
        "rejected_proof_candidate_count": rejected_count,
        "unique_valid_anchor_proof_count": len(valid_signer_ids),
        "unique_valid_anchor_signer_count": len(valid_signer_ids),
    }


def verify_bootstrap(
    *,
    manifest_raw: bytes,
    proof_artifacts: Iterable[bytes],
    policy: NativeBootstrapPolicy,
) -> Dict[str, Any]:
    validate_policy(policy)
    manifest = parse_manifest_artifact(manifest_raw)
    exact_policy_digest = _match_manifest_to_policy(manifest, policy)

    if policy.anchor_profile == HIVE_ACTIVE_AUTHORITY_V1:
        raise UnsupportedAnchorProfileError(
            "HIVE_ACTIVE_AUTHORITY_V1 is specified but not implemented"
        )
    if policy.anchor_profile != OFFLINE_ED25519_V1:
        raise UnsupportedAnchorProfileError(policy.anchor_profile)

    proof_stats = _qualify_offline_proofs(
        manifest_raw=manifest_raw,
        proof_artifacts=proof_artifacts,
        policy=policy,
    )

    result: Dict[str, Any] = {
        "bootstrap_manifest_valid": True,
        "manifest_policy_binding_valid": True,
        "policy_digest_matched": True,
        "independent_anchor_proof_valid": True,
        "project": manifest["project"],
        "authority_domain": manifest["authority_domain"],
        "candidate_authority_key_id": manifest[
            "candidate_authority_key_id"
        ],
        "bootstrap_policy_id": policy.policy_id,
        "bootstrap_policy_digest": exact_policy_digest,
        "bootstrap_generation": manifest["generation"],
        "manifest_digest": manifest_digest(manifest_raw),
        "anchor_profile": policy.anchor_profile,
        "anchor_subject": policy.anchor_subject,
        "native_policy_provenance_claim":
            policy.native_policy_provenance_claim,
        "native_policy_provenance_authenticated": False,
        "trust_statement_scope": "RELATIVE_TO_SUPPLIED_POLICY",
        "bootstrap_trust_root_established_for_observed_policy": True,
        "execution_authorized_by_cpi": False,
    }
    result.update(proof_stats)
    return result


def verify_genesis_set(
    *,
    entries: Iterable[Tuple[bytes, Iterable[bytes]]],
    policy: NativeBootstrapPolicy,
) -> Dict[str, Any]:
    validate_policy(policy)

    manifests: Dict[str, bytes] = {}
    proof_pool: Dict[str, Dict[str, bytes]] = {}

    observed_carrier_entry_count = 0
    rejected_carrier_entry_count = 0
    observed_proof_candidate_count = 0
    rejected_proof_candidate_count = 0

    for entry in entries:
        observed_carrier_entry_count += 1

        try:
            manifest_raw, proofs = entry
        except Exception:
            rejected_carrier_entry_count += 1
            continue

        # Proof collection is intentionally independent of manifest validity.
        try:
            for proof_raw in proofs:
                observed_proof_candidate_count += 1

                if type(proof_raw) is not bytes:
                    rejected_proof_candidate_count += 1
                    continue

                try:
                    proof = parse_proof_artifact(proof_raw)
                except BootstrapError:
                    rejected_proof_candidate_count += 1
                    continue

                raw_digest = hashlib.sha256(proof_raw).hexdigest()
                by_digest = proof_pool.setdefault(
                    proof["manifest_digest"],
                    {},
                )
                by_digest.setdefault(raw_digest, proof_raw)
        except Exception:
            # Preserve proof candidates already yielded before iterator failure.
            rejected_carrier_entry_count += 1

        try:
            parse_manifest_artifact(manifest_raw)
            digest = hashlib.sha256(manifest_raw).hexdigest()
        except BootstrapError:
            rejected_carrier_entry_count += 1
            continue

        manifests.setdefault(digest, manifest_raw)

    canonical_proof_candidate_count = sum(
        len(items) for items in proof_pool.values()
    )
    orphan_proof_candidate_count = sum(
        len(items)
        for digest, items in proof_pool.items()
        if digest not in manifests
    )

    qualifying: list[Dict[str, Any]] = []
    policy_mismatch_manifest_count = 0
    underproven_manifest_count = 0

    for digest in sorted(manifests):
        manifest_raw = manifests[digest]

        try:
            manifest = parse_manifest_artifact(manifest_raw)
            _match_manifest_to_policy(manifest, policy)
        except BootstrapPolicyError:
            policy_mismatch_manifest_count += 1
            continue
        except BootstrapError:
            underproven_manifest_count += 1
            continue

        routed_proofs = list(proof_pool.get(digest, {}).values())

        try:
            result = verify_bootstrap(
                manifest_raw=manifest_raw,
                proof_artifacts=routed_proofs,
                policy=policy,
            )
        except BootstrapProofError:
            underproven_manifest_count += 1
            continue
        except BootstrapPolicyError:
            policy_mismatch_manifest_count += 1
            continue
        except BootstrapError:
            underproven_manifest_count += 1
            continue

        qualifying.append(result)

    if not qualifying:
        raise BootstrapProofError(
            "no qualifying bootstrap manifest was discovered"
        )
    if len(qualifying) != 1:
        raise BootstrapConflictError(
            "multiple distinct independently valid genesis manifests exist"
        )

    result = dict(qualifying[0])
    result.update(
        {
            "observed_carrier_entry_count":
                observed_carrier_entry_count,
            "rejected_carrier_entry_count":
                rejected_carrier_entry_count,
            "observed_proof_candidate_count":
                observed_proof_candidate_count,
            "canonical_proof_candidate_count":
                canonical_proof_candidate_count,
            "rejected_proof_candidate_count":
                rejected_proof_candidate_count,
            "orphan_proof_candidate_count":
                orphan_proof_candidate_count,
            "unique_canonical_manifest_count": len(manifests),
            "policy_mismatch_manifest_count":
                policy_mismatch_manifest_count,
            "underproven_manifest_count":
                underproven_manifest_count,
            "nonqualifying_manifest_count":
                policy_mismatch_manifest_count + underproven_manifest_count,
            "qualifying_manifest_count": 1,
        }
    )
    return result
