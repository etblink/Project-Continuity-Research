from __future__ import annotations

import base64
import binascii
import hashlib
import json
import re
from typing import Any, Dict, Iterable, List, Mapping

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat


SCHEMA = "cpi.authority-capsule/0.1"
SIGNATURE_ALGORITHM = "Ed25519"
DECISIONS = {"PASS", "HOLD", "REJECT", "WITHDRAW"}

SIGNED_FIELDS = (
    "schema",
    "project",
    "authority_domain",
    "subject",
    "candidate",
    "candidate_revision",
    "sequence",
    "predecessor",
    "decision",
    "note_digest",
    "signer_key_id",
    "signature_algorithm",
)
ENVELOPE_FIELDS = SIGNED_FIELDS + ("signature",)

HEX64 = re.compile(r"^[0-9a-f]{64}$")
KEY_ID = re.compile(r"^ed25519-sha256:[0-9a-f]{64}$")


class CapsuleError(ValueError):
    pass


class CapsuleSchemaError(CapsuleError):
    pass


class CapsuleSignatureError(CapsuleError):
    pass


class CapsuleChainError(CapsuleError):
    pass


class CapsuleBindingError(CapsuleError):
    pass


def _canonical_json(obj: Mapping[str, Any]) -> bytes:
    return json.dumps(
        dict(obj),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _raw_public_key(public_key: Ed25519PublicKey | bytes) -> bytes:
    if isinstance(public_key, Ed25519PublicKey):
        return public_key.public_bytes(Encoding.Raw, PublicFormat.Raw)
    if type(public_key) is not bytes or len(public_key) != 32:
        raise CapsuleSchemaError("pinned public key must be exactly 32 raw Ed25519 bytes")
    return public_key


def public_key_id(public_key: Ed25519PublicKey | bytes) -> str:
    raw = _raw_public_key(public_key)
    return "ed25519-sha256:" + hashlib.sha256(raw).hexdigest()


def _require_string(value: Any, field: str) -> str:
    if type(value) is not str or not value:
        raise CapsuleSchemaError(f"{field} must be a non-empty string")
    return value


def _validate_capsule_shape(capsule: Mapping[str, Any]) -> Dict[str, Any]:
    if not isinstance(capsule, Mapping):
        raise CapsuleSchemaError("capsule must be a mapping")

    keys = set(capsule)
    expected = set(ENVELOPE_FIELDS)
    missing = expected - keys
    extra = keys - expected
    if missing:
        raise CapsuleSchemaError(f"missing fields: {sorted(missing)}")
    if extra:
        raise CapsuleSchemaError(f"unexpected fields: {sorted(extra)}")

    c = dict(capsule)

    if c["schema"] != SCHEMA:
        raise CapsuleSchemaError("unsupported schema")

    for field in (
        "project",
        "authority_domain",
        "subject",
        "candidate",
        "candidate_revision",
    ):
        _require_string(c[field], field)

    if type(c["sequence"]) is not int or c["sequence"] < 1:
        raise CapsuleSchemaError("sequence must be a positive integer")

    predecessor = c["predecessor"]
    if c["sequence"] == 1:
        if predecessor is not None:
            raise CapsuleSchemaError("sequence 1 predecessor must be null")
    else:
        if type(predecessor) is not str or not HEX64.fullmatch(predecessor):
            raise CapsuleSchemaError(
                "sequence >1 predecessor must be 64 lowercase hex characters"
            )

    if c["decision"] not in DECISIONS:
        raise CapsuleSchemaError("unsupported decision")

    note_digest = c["note_digest"]
    if note_digest is not None and (
        type(note_digest) is not str or not HEX64.fullmatch(note_digest)
    ):
        raise CapsuleSchemaError(
            "note_digest must be null or 64 lowercase hex characters"
        )

    if (
        type(c["signer_key_id"]) is not str
        or not KEY_ID.fullmatch(c["signer_key_id"])
    ):
        raise CapsuleSchemaError("invalid signer_key_id")

    if c["signature_algorithm"] != SIGNATURE_ALGORITHM:
        raise CapsuleSchemaError("unsupported signature_algorithm")

    sig_text = c["signature"]
    if type(sig_text) is not str or not sig_text:
        raise CapsuleSchemaError("signature must be a non-empty Base64 string")
    try:
        sig = base64.b64decode(sig_text, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise CapsuleSchemaError("signature is not canonical Base64") from exc
    if len(sig) != 64 or base64.b64encode(sig).decode("ascii") != sig_text:
        raise CapsuleSchemaError("signature is not canonical Ed25519 Base64")

    return c


def canonical_signed_bytes(capsule: Mapping[str, Any]) -> bytes:
    c = _validate_capsule_shape(capsule)
    return _canonical_json({field: c[field] for field in SIGNED_FIELDS})


def canonical_envelope_bytes(capsule: Mapping[str, Any]) -> bytes:
    c = _validate_capsule_shape(capsule)
    return _canonical_json({field: c[field] for field in ENVELOPE_FIELDS})


def capsule_digest(capsule: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_envelope_bytes(capsule)).hexdigest()


def note_digest(note: str | bytes) -> str:
    if isinstance(note, str):
        data = note.encode("utf-8")
    elif type(note) is bytes:
        data = note
    else:
        raise CapsuleSchemaError("note must be str or bytes")
    return hashlib.sha256(data).hexdigest()


def sign_capsule(
    *,
    private_key: Ed25519PrivateKey,
    project: str,
    authority_domain: str,
    subject: str,
    candidate: str,
    candidate_revision: str,
    sequence: int,
    predecessor: str | None,
    decision: str,
    note_digest_value: str | None = None,
) -> Dict[str, Any]:
    if not isinstance(private_key, Ed25519PrivateKey):
        raise CapsuleSchemaError("private_key must be Ed25519PrivateKey")

    pub = private_key.public_key()
    capsule: Dict[str, Any] = {
        "schema": SCHEMA,
        "project": project,
        "authority_domain": authority_domain,
        "subject": subject,
        "candidate": candidate,
        "candidate_revision": candidate_revision,
        "sequence": sequence,
        "predecessor": predecessor,
        "decision": decision,
        "note_digest": note_digest_value,
        "signer_key_id": public_key_id(pub),
        "signature_algorithm": SIGNATURE_ALGORITHM,
        "signature": base64.b64encode(b"\x00" * 64).decode("ascii"),
    }
    _validate_capsule_shape(capsule)
    signed = _canonical_json({field: capsule[field] for field in SIGNED_FIELDS})
    capsule["signature"] = base64.b64encode(private_key.sign(signed)).decode("ascii")
    _validate_capsule_shape(capsule)
    return capsule


def verify_capsule(
    capsule: Mapping[str, Any],
    pinned_public_key: Ed25519PublicKey | bytes,
) -> Dict[str, Any]:
    c = _validate_capsule_shape(capsule)
    raw = _raw_public_key(pinned_public_key)
    expected_key_id = public_key_id(raw)
    if c["signer_key_id"] != expected_key_id:
        raise CapsuleSignatureError("signer_key_id does not match pinned authority key")

    pub = Ed25519PublicKey.from_public_bytes(raw)
    signature = base64.b64decode(c["signature"], validate=True)
    signed = _canonical_json({field: c[field] for field in SIGNED_FIELDS})
    try:
        pub.verify(signature, signed)
    except InvalidSignature as exc:
        raise CapsuleSignatureError("invalid capsule signature") from exc
    return c


def verify_chain(
    capsules: Iterable[Mapping[str, Any]],
    pinned_public_key: Ed25519PublicKey | bytes,
    *,
    expected_project: str,
    expected_authority_domain: str,
    expected_subject: str,
    expected_candidate: str,
    expected_candidate_revision: str,
) -> Dict[str, Any]:
    raw = _raw_public_key(pinned_public_key)
    verified = [verify_capsule(c, raw) for c in capsules]
    if not verified:
        raise CapsuleChainError("authority chain is empty")

    # Identical artifacts replicated across carriers are one capsule.
    unique_by_digest: Dict[str, Dict[str, Any]] = {}
    for c in verified:
        unique_by_digest[capsule_digest(c)] = c
    verified = list(unique_by_digest.values())

    by_sequence: Dict[int, List[Dict[str, Any]]] = {}
    for c in verified:
        by_sequence.setdefault(c["sequence"], []).append(c)

    for sequence, records in by_sequence.items():
        if len(records) != 1:
            raise CapsuleChainError(f"fork at sequence {sequence}")

    sequences = sorted(by_sequence)
    expected_sequences = list(range(1, sequences[-1] + 1))
    if sequences != expected_sequences:
        raise CapsuleChainError(
            f"non-contiguous authority chain: {sequences}"
        )

    ordered = [by_sequence[n][0] for n in sequences]
    first = ordered[0]
    if first["predecessor"] is not None:
        raise CapsuleChainError("genesis predecessor must be null")

    immutable_binding = (
        expected_project,
        expected_authority_domain,
        expected_subject,
        expected_candidate,
    )

    for index, current in enumerate(ordered):
        actual_binding = (
            current["project"],
            current["authority_domain"],
            current["subject"],
            current["candidate"],
        )
        if actual_binding != immutable_binding:
            raise CapsuleBindingError(
                f"authority binding mismatch at sequence {current['sequence']}"
            )
        if index:
            previous = ordered[index - 1]
            expected_predecessor = capsule_digest(previous)
            if current["predecessor"] != expected_predecessor:
                raise CapsuleChainError(
                    f"predecessor mismatch at sequence {current['sequence']}"
                )

    head = ordered[-1]
    if head["candidate_revision"] != expected_candidate_revision:
        raise CapsuleBindingError(
            "head capsule does not bind the requested candidate revision"
        )

    return {
        "capsule_chain_valid": True,
        "project": head["project"],
        "authority_domain": head["authority_domain"],
        "subject": head["subject"],
        "candidate": head["candidate"],
        "candidate_revision": head["candidate_revision"],
        "head_sequence": head["sequence"],
        "head_capsule_digest": capsule_digest(head),
        "observed_decision": head["decision"],
        "signer_key_id": head["signer_key_id"],
        "execution_authorized_by_cpi": False,
    }
