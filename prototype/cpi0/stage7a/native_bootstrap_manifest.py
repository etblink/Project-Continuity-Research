from __future__ import annotations

import base64
import binascii
import hashlib
import json
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat


MANIFEST_SCHEMA = "cpi.native-bootstrap-manifest/0.1"
POLICY_SCHEMA = "cpi.native-bootstrap-policy/0.1"
PROOF_SCHEMA = "cpi.bootstrap-anchor-proof/0.1"
OFFLINE_ED25519_V1 = "OFFLINE_ED25519_V1"
HIVE_ACTIVE_AUTHORITY_V1 = "HIVE_ACTIVE_AUTHORITY_V1"
SIGNATURE_ALGORITHM = "Ed25519"

MANIFEST_FIELDS = (
    "schema",
    "project",
    "authority_domain",
    "candidate_authority_key_id",
    "bootstrap_policy",
    "generation",
    "challenge",
    "anchor_profile",
    "anchor_subject",
    "note_digest",
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
    native_policy_provenance: str


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


def public_key_id(public_key: bytes) -> str:
    if type(public_key) is not bytes or len(public_key) != 32:
        raise BootstrapPolicyError("Ed25519 public key must be exactly 32 raw bytes")
    try:
        Ed25519PublicKey.from_public_bytes(public_key)
    except ValueError as exc:
        raise BootstrapPolicyError("invalid Ed25519 public key") from exc
    return "ed25519-sha256:" + hashlib.sha256(public_key).hexdigest()


def offline_anchor_subject(public_key: bytes) -> str:
    return "offline-ed25519:" + public_key_id(public_key)


def _validate_manifest_mapping(value: Mapping[str, Any]) -> Dict[str, Any]:
    if not isinstance(value, Mapping):
        raise BootstrapSchemaError("manifest must be an object")
    keys = set(value)
    expected = set(MANIFEST_FIELDS)
    if keys != expected:
        missing = sorted(expected - keys)
        extra = sorted(keys - expected)
        raise BootstrapSchemaError(f"manifest field mismatch missing={missing} extra={extra}")
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
    _hex64(m["challenge"], "challenge")
    _note_digest(m["note_digest"])
    return m


def _pairs_no_duplicates(pairs: Sequence[Tuple[str, Any]]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise BootstrapSchemaError(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def _reject_number(_: str) -> Any:
    raise BootstrapSchemaError("numeric JSON values are forbidden in bootstrap artifacts")


def _parse_canonical_object(raw: bytes, kind: str) -> Dict[str, Any]:
    if type(raw) is not bytes:
        raise BootstrapSchemaError(f"{kind} artifact must be raw bytes")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise BootstrapSchemaError("UTF-8 BOM is forbidden")
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise BootstrapSchemaError(f"{kind} artifact is not valid UTF-8") from exc
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
        raise BootstrapSchemaError(f"{kind} artifact is not strict JSON") from exc
    if type(parsed) is not dict:
        raise BootstrapSchemaError(f"{kind} artifact root must be an object")
    return parsed


def create_manifest_artifact(
    *,
    project: str,
    authority_domain: str,
    candidate_authority_key_id: str,
    bootstrap_policy: str,
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
        "generation": generation,
        "challenge": challenge,
        "anchor_profile": anchor_profile,
        "anchor_subject": anchor_subject,
        "note_digest": note_digest,
    }
    checked = _validate_manifest_mapping(manifest)
    return _canonical_json({field: checked[field] for field in MANIFEST_FIELDS})


def parse_manifest_artifact(raw: bytes) -> Dict[str, Any]:
    parsed = _parse_canonical_object(raw, "manifest")
    checked = _validate_manifest_mapping(parsed)
    canonical = _canonical_json({field: checked[field] for field in MANIFEST_FIELDS})
    if raw != canonical:
        raise BootstrapSchemaError("manifest bytes are not canonical")
    return checked


def manifest_digest(raw: bytes) -> str:
    parse_manifest_artifact(raw)
    return hashlib.sha256(raw).hexdigest()


def anchor_statement(manifest_raw: bytes) -> bytes:
    digest = manifest_digest(manifest_raw)
    return (
        "CPI-NATIVE-BOOTSTRAP/0.1\n"
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
        raise BootstrapSchemaError(f"proof field mismatch missing={missing} extra={extra}")
    p = dict(value)
    if p["schema"] != PROOF_SCHEMA:
        raise BootstrapSchemaError("unsupported proof schema")
    _hex64(p["manifest_digest"], "manifest_digest")
    for field in ("anchor_profile", "anchor_subject", "signature_algorithm", "signature"):
        _nonempty_text(p[field], field)
    _key_id(p["signer_key_id"], "signer_key_id")
    if p["signature_algorithm"] != SIGNATURE_ALGORITHM:
        raise BootstrapSchemaError("unsupported signature algorithm")
    try:
        sig = base64.b64decode(p["signature"], validate=True)
    except (binascii.Error, ValueError) as exc:
        raise BootstrapSchemaError("signature is not canonical base64") from exc
    if len(sig) != 64 or base64.b64encode(sig).decode("ascii") != p["signature"]:
        raise BootstrapSchemaError("signature is not canonical Ed25519 base64")
    return p


def create_offline_ed25519_proof(
    *,
    manifest_raw: bytes,
    private_key: Ed25519PrivateKey,
) -> bytes:
    if not isinstance(private_key, Ed25519PrivateKey):
        raise BootstrapProofError("private_key must be Ed25519PrivateKey")
    public_raw = private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    proof = {
        "schema": PROOF_SCHEMA,
        "manifest_digest": manifest_digest(manifest_raw),
        "anchor_profile": OFFLINE_ED25519_V1,
        "anchor_subject": offline_anchor_subject(public_raw),
        "signer_key_id": public_key_id(public_raw),
        "signature_algorithm": SIGNATURE_ALGORITHM,
        "signature": base64.b64encode(private_key.sign(anchor_statement(manifest_raw))).decode("ascii"),
    }
    checked = _validate_proof_mapping(proof)
    return _canonical_json({field: checked[field] for field in PROOF_FIELDS})


def parse_proof_artifact(raw: bytes) -> Dict[str, Any]:
    parsed = _parse_canonical_object(raw, "proof")
    checked = _validate_proof_mapping(parsed)
    canonical = _canonical_json({field: checked[field] for field in PROOF_FIELDS})
    if raw != canonical:
        raise BootstrapSchemaError("proof bytes are not canonical")
    return checked


def validate_policy(policy: NativeBootstrapPolicy) -> NativeBootstrapPolicy:
    if not isinstance(policy, NativeBootstrapPolicy):
        raise BootstrapPolicyError("policy must be NativeBootstrapPolicy")
    for field in (
        "policy_id",
        "project",
        "authority_domain",
        "anchor_profile",
        "anchor_subject",
        "expected_generation",
        "native_policy_provenance",
    ):
        _nonempty_text(getattr(policy, field), f"policy.{field}")
    if type(policy.minimum_anchor_count) is not int or policy.minimum_anchor_count < 1:
        raise BootstrapPolicyError("minimum_anchor_count must be a positive integer")

    if policy.anchor_profile == OFFLINE_ED25519_V1:
        if policy.minimum_anchor_count != 1:
            raise BootstrapPolicyError("OFFLINE_ED25519_V1 prototype supports exactly one anchor")
        if type(policy.pinned_anchor_public_key) is not bytes:
            raise BootstrapPolicyError("OFFLINE_ED25519_V1 requires a pinned raw Ed25519 key")
        expected_subject = offline_anchor_subject(policy.pinned_anchor_public_key)
        if policy.anchor_subject != expected_subject:
            raise BootstrapPolicyError("offline anchor_subject does not match pinned key")
    elif policy.anchor_profile == HIVE_ACTIVE_AUTHORITY_V1:
        if policy.pinned_anchor_public_key is not None:
            raise BootstrapPolicyError("Hive profile does not use Ed25519 pinned_anchor_public_key")
    else:
        raise UnsupportedAnchorProfileError(f"unsupported anchor profile: {policy.anchor_profile}")
    return policy


def _match_manifest_to_policy(
    manifest: Mapping[str, Any],
    policy: NativeBootstrapPolicy,
) -> None:
    pairs = (
        ("project", manifest["project"], policy.project),
        ("authority_domain", manifest["authority_domain"], policy.authority_domain),
        ("bootstrap_policy", manifest["bootstrap_policy"], policy.policy_id),
        ("anchor_profile", manifest["anchor_profile"], policy.anchor_profile),
        ("anchor_subject", manifest["anchor_subject"], policy.anchor_subject),
        ("generation", manifest["generation"], policy.expected_generation),
    )
    mismatches = [name for name, actual, expected in pairs if actual != expected]
    if mismatches:
        raise BootstrapPolicyError(f"manifest does not match native policy: {mismatches}")


def verify_bootstrap(
    *,
    manifest_raw: bytes,
    proof_artifacts: Iterable[bytes],
    policy: NativeBootstrapPolicy,
) -> Dict[str, Any]:
    validate_policy(policy)
    manifest = parse_manifest_artifact(manifest_raw)
    _match_manifest_to_policy(manifest, policy)

    if policy.anchor_profile == HIVE_ACTIVE_AUTHORITY_V1:
        raise UnsupportedAnchorProfileError(
            "HIVE_ACTIVE_AUTHORITY_V1 is specified but not implemented in Stage 7A"
        )
    if policy.anchor_profile != OFFLINE_ED25519_V1:
        raise UnsupportedAnchorProfileError(policy.anchor_profile)

    proof_by_digest: Dict[str, Dict[str, Any]] = {}
    artifact_count = 0
    for raw in proof_artifacts:
        artifact_count += 1
        proof = parse_proof_artifact(raw)
        proof_digest = hashlib.sha256(raw).hexdigest()
        proof_by_digest[proof_digest] = proof

    valid_anchor_proofs = 0
    expected_manifest_digest = manifest_digest(manifest_raw)
    expected_key_id = public_key_id(policy.pinned_anchor_public_key)
    public_key = Ed25519PublicKey.from_public_bytes(policy.pinned_anchor_public_key)

    for proof in proof_by_digest.values():
        if proof["manifest_digest"] != expected_manifest_digest:
            raise BootstrapProofError("proof is bound to a different manifest")
        if proof["anchor_profile"] != policy.anchor_profile:
            raise BootstrapProofError("proof anchor profile mismatch")
        if proof["anchor_subject"] != policy.anchor_subject:
            raise BootstrapProofError("proof anchor subject mismatch")
        if proof["signer_key_id"] != expected_key_id:
            raise BootstrapProofError("proof signer is not the pinned native anchor")
        signature = base64.b64decode(proof["signature"], validate=True)
        try:
            public_key.verify(signature, anchor_statement(manifest_raw))
        except InvalidSignature as exc:
            raise BootstrapProofError("invalid independent anchor signature") from exc
        valid_anchor_proofs += 1

    if valid_anchor_proofs < policy.minimum_anchor_count:
        raise BootstrapProofError(
            f"insufficient independent anchor proofs: {valid_anchor_proofs}"
        )

    return {
        "bootstrap_manifest_valid": True,
        "anchor_policy_matched": True,
        "independent_anchor_proof_valid": True,
        "project": manifest["project"],
        "authority_domain": manifest["authority_domain"],
        "candidate_authority_key_id": manifest["candidate_authority_key_id"],
        "bootstrap_policy": manifest["bootstrap_policy"],
        "bootstrap_generation": manifest["generation"],
        "manifest_digest": expected_manifest_digest,
        "anchor_profile": policy.anchor_profile,
        "anchor_subject": policy.anchor_subject,
        "native_policy_provenance": policy.native_policy_provenance,
        "proof_artifact_count": artifact_count,
        "unique_valid_anchor_proof_count": valid_anchor_proofs,
        "bootstrap_trust_root_established_for_observed_policy": True,
        "execution_authorized_by_cpi": False,
    }


def verify_genesis_set(
    *,
    entries: Iterable[Tuple[bytes, Iterable[bytes]]],
    policy: NativeBootstrapPolicy,
) -> Dict[str, Any]:
    results: Dict[str, Dict[str, Any]] = {}
    for manifest_raw, proofs in entries:
        digest = manifest_digest(manifest_raw)
        if digest in results:
            continue
        results[digest] = verify_bootstrap(
            manifest_raw=manifest_raw,
            proof_artifacts=proofs,
            policy=policy,
        )
    if not results:
        raise BootstrapProofError("no valid bootstrap manifest supplied")
    if len(results) != 1:
        raise BootstrapConflictError(
            "multiple distinct independently valid genesis manifests exist"
        )
    return next(iter(results.values()))
