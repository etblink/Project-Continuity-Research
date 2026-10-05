from __future__ import annotations

import base64
import binascii
import hashlib
import json
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Iterable, List, Mapping, NoReturn, Sequence, Tuple

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat


SCHEMA = "cpi.authority-capsule/0.1"
SIGNATURE_ALGORITHM = "Ed25519"
DECISIONS = {"PASS", "HOLD", "REJECT", "WITHDRAW"}
MAX_SEQUENCE = 2**63 - 1
RESEARCH_VERIFIER_VERSION = "0.1.2"

__all__ = [
    "CapsuleError",
    "CapsuleSchemaError",
    "CapsuleSignatureError",
    "CapsuleChainError",
    "CapsuleBindingError",
    "CapsuleCompletenessError",
    "PinValidationError",
    "PinnedAuthorityKey",
    "public_key_id",
    "validate_pin",
    "pin_provenance_digest",
    "capsule_artifact_digest",
    "note_digest",
    "parse_capsule_artifact",
    "sign_capsule_artifact",
    "verify_observed_chain",
    "require_current_decision",
]

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


class CapsuleCompletenessError(CapsuleError):
    pass


class PinValidationError(CapsuleError):
    pass


@dataclass(frozen=True)
class PinnedAuthorityKey:
    public_key: bytes
    project: str
    authority_domain: str
    provenance_id: str
    provenance_revision: str


# Ed25519 field / subgroup constants used only to reject invalid or low-order
# public-key pins before delegating signature verification to cryptography.
_ED_P = 2**255 - 19
_ED_D = (-121665 * pow(121666, _ED_P - 2, _ED_P)) % _ED_P
_ED_I = pow(2, (_ED_P - 1) // 4, _ED_P)
_ED_L = 2**252 + 27742317777372353535851937790883648493
_ED_IDENTITY = (0, 1)


def _require_utf8_string(value: Any, field: str) -> str:
    if type(value) is not str or not value:
        raise CapsuleSchemaError(f"{field} must be a non-empty string")
    try:
        value.encode("utf-8", "strict")
    except UnicodeEncodeError as exc:
        raise CapsuleSchemaError(f"{field} is not valid Unicode scalar text") from exc
    return value


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
        raise CapsuleSchemaError("object cannot be canonically serialized") from exc


def _raw_public_key(public_key: bytes) -> bytes:
    if type(public_key) is not bytes or len(public_key) != 32:
        raise PinValidationError(
            "pinned public key must be exactly 32 raw Ed25519 bytes"
        )
    return public_key


def _ed_decode(raw: bytes) -> Tuple[int, int]:
    n = int.from_bytes(raw, "little")
    sign = (n >> 255) & 1
    y = n & ((1 << 255) - 1)
    if y >= _ED_P:
        raise PinValidationError("non-canonical Ed25519 public-key encoding")

    denominator = (_ED_D * y * y + 1) % _ED_P
    if denominator == 0:
        raise PinValidationError("invalid Ed25519 public-key point")

    x2 = ((y * y - 1) * pow(denominator, _ED_P - 2, _ED_P)) % _ED_P
    x = pow(x2, (_ED_P + 3) // 8, _ED_P)
    if (x * x - x2) % _ED_P != 0:
        x = (x * _ED_I) % _ED_P
    if (x * x - x2) % _ED_P != 0:
        raise PinValidationError("invalid Ed25519 public-key point")
    if x == 0 and sign:
        raise PinValidationError("non-canonical Ed25519 x sign")
    if (x & 1) != sign:
        x = _ED_P - x

    if (-x * x + y * y - 1 - _ED_D * x * x * y * y) % _ED_P != 0:
        raise PinValidationError("public key is not on the Ed25519 curve")
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
        raise PinValidationError("invalid Ed25519 subgroup arithmetic")
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


@lru_cache(maxsize=64)
def _validate_public_key_bytes(raw: bytes) -> bytes:
    if type(raw) is not bytes or len(raw) != 32:
        raise PinValidationError(
            "pinned public key must be exactly 32 raw Ed25519 bytes"
        )
    point = _ed_decode(raw)
    if point == _ED_IDENTITY:
        raise PinValidationError("identity Ed25519 public key is forbidden")
    if _ed_mul(_ED_L, point) != _ED_IDENTITY:
        raise PinValidationError(
            "Ed25519 public key is not in the prime-order subgroup"
        )
    # cryptography should also accept the canonical point representation.
    try:
        Ed25519PublicKey.from_public_bytes(raw)
    except ValueError as exc:
        raise PinValidationError("invalid Ed25519 public key") from exc
    return raw


def public_key_id(public_key: bytes) -> str:
    raw = _raw_public_key(public_key)
    _validate_public_key_bytes(raw)
    return "ed25519-sha256:" + hashlib.sha256(raw).hexdigest()


def validate_pin(pin: PinnedAuthorityKey) -> PinnedAuthorityKey:
    if not isinstance(pin, PinnedAuthorityKey):
        raise PinValidationError("pin must be PinnedAuthorityKey")
    _validate_public_key_bytes(_raw_public_key(pin.public_key))
    _require_utf8_string(pin.project, "pin.project")
    _require_utf8_string(pin.authority_domain, "pin.authority_domain")
    _require_utf8_string(pin.provenance_id, "pin.provenance_id")
    _require_utf8_string(pin.provenance_revision, "pin.provenance_revision")
    return pin


def pin_provenance_digest(pin: PinnedAuthorityKey) -> str:
    validate_pin(pin)
    record = {
        "authority_domain": pin.authority_domain,
        "key_id": public_key_id(pin.public_key),
        "project": pin.project,
        "provenance_id": pin.provenance_id,
        "provenance_revision": pin.provenance_revision,
    }
    return hashlib.sha256(_canonical_json(record)).hexdigest()


def _validate_capsule_shape(capsule: Mapping[str, Any]) -> Dict[str, Any]:
    if not isinstance(capsule, Mapping):
        raise CapsuleSchemaError("capsule must be a mapping")

    try:
        keys = set(capsule)
    except (TypeError, ValueError) as exc:
        raise CapsuleSchemaError("capsule keys are malformed") from exc

    expected = set(ENVELOPE_FIELDS)
    missing = expected - keys
    extra = keys - expected
    if missing:
        raise CapsuleSchemaError(f"missing fields: {sorted(missing)}")
    if extra:
        raise CapsuleSchemaError(f"unexpected fields: {sorted(extra)}")

    try:
        c = dict(capsule)
    except (TypeError, ValueError) as exc:
        raise CapsuleSchemaError("capsule mapping cannot be materialized") from exc

    if c["schema"] != SCHEMA:
        raise CapsuleSchemaError("unsupported schema")

    for field in (
        "project",
        "authority_domain",
        "subject",
        "candidate",
        "candidate_revision",
        "signer_key_id",
        "signature_algorithm",
        "signature",
    ):
        _require_utf8_string(c[field], field)

    if type(c["sequence"]) is not int:
        raise CapsuleSchemaError("sequence must be an integer")
    if not (1 <= c["sequence"] <= MAX_SEQUENCE):
        raise CapsuleSchemaError(
            f"sequence must be between 1 and {MAX_SEQUENCE}"
        )

    predecessor = c["predecessor"]
    if c["sequence"] == 1:
        if predecessor is not None:
            raise CapsuleSchemaError("sequence 1 predecessor must be null")
    else:
        if (
            type(predecessor) is not str
            or len(predecessor) != 64
            or any(ch not in "0123456789abcdef" for ch in predecessor)
        ):
            raise CapsuleSchemaError(
                "sequence >1 predecessor must be 64 lowercase hex characters"
            )

    if type(c["decision"]) is not str or c["decision"] not in DECISIONS:
        raise CapsuleSchemaError("unsupported decision")

    note = c["note_digest"]
    if note is not None and (
        type(note) is not str
        or len(note) != 64
        or any(ch not in "0123456789abcdef" for ch in note)
    ):
        raise CapsuleSchemaError(
            "note_digest must be null or 64 lowercase hex characters"
        )

    key_id = c["signer_key_id"]
    prefix = "ed25519-sha256:"
    digest = key_id[len(prefix):] if key_id.startswith(prefix) else ""
    if (
        not key_id.startswith(prefix)
        or len(digest) != 64
        or any(ch not in "0123456789abcdef" for ch in digest)
    ):
        raise CapsuleSchemaError("invalid signer_key_id")

    if c["signature_algorithm"] != SIGNATURE_ALGORITHM:
        raise CapsuleSchemaError("unsupported signature_algorithm")

    sig_text = c["signature"]
    try:
        sig = base64.b64decode(sig_text, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise CapsuleSchemaError("signature is not canonical Base64") from exc
    if len(sig) != 64 or base64.b64encode(sig).decode("ascii") != sig_text:
        raise CapsuleSchemaError("signature is not canonical Ed25519 Base64")

    return c


def _canonical_signed_bytes(capsule: Mapping[str, Any]) -> bytes:
    c = _validate_capsule_shape(capsule)
    return _canonical_json({field: c[field] for field in SIGNED_FIELDS})


def _canonical_envelope_bytes(capsule: Mapping[str, Any]) -> bytes:
    c = _validate_capsule_shape(capsule)
    return _canonical_json({field: c[field] for field in ENVELOPE_FIELDS})


def _capsule_digest_mapping(capsule: Mapping[str, Any]) -> str:
    return hashlib.sha256(__canonical_envelope_bytes(capsule)).hexdigest()


def _serialize_capsule_mapping(capsule: Mapping[str, Any]) -> bytes:
    return _canonical_envelope_bytes(capsule)


def capsule_artifact_digest(raw: bytes) -> str:
    parse_capsule_artifact(raw)
    return hashlib.sha256(raw).hexdigest()


def note_digest(note: str | bytes) -> str:
    if isinstance(note, str):
        try:
            data = note.encode("utf-8", "strict")
        except UnicodeEncodeError as exc:
            raise CapsuleSchemaError("note is not valid Unicode scalar text") from exc
    elif type(note) is bytes:
        data = note
    else:
        raise CapsuleSchemaError("note must be str or bytes")
    return hashlib.sha256(data).hexdigest()


def _reject_json_float(_: str) -> Any:
    raise CapsuleSchemaError("JSON floating-point numbers are forbidden")


def _reject_json_constant(_: str) -> Any:
    raise CapsuleSchemaError("non-standard JSON numeric constants are forbidden")


def _parse_json_int(text: str) -> int:
    try:
        value = int(text)
    except ValueError as exc:
        raise CapsuleSchemaError("invalid JSON integer") from exc
    if not (-MAX_SEQUENCE <= value <= MAX_SEQUENCE):
        raise CapsuleSchemaError("JSON integer exceeds signed 64-bit range")
    return value


def _pairs_without_duplicates(
    pairs: Sequence[Tuple[str, Any]],
) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise CapsuleSchemaError(f"duplicate JSON object key: {key}")
        out[key] = value
    return out


def parse_capsule_artifact(raw: bytes) -> Dict[str, Any]:
    if type(raw) is not bytes:
        raise CapsuleSchemaError("capsule artifact must be raw bytes")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise CapsuleSchemaError("UTF-8 BOM is forbidden")
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise CapsuleSchemaError("capsule artifact is not valid UTF-8") from exc

    try:
        parsed = json.loads(
            text,
            object_pairs_hook=_pairs_without_duplicates,
            parse_float=_reject_json_float,
            parse_int=_parse_json_int,
            parse_constant=_reject_json_constant,
        )
    except CapsuleError:
        raise
    except (json.JSONDecodeError, TypeError, ValueError, RecursionError) as exc:
        raise CapsuleSchemaError("capsule artifact is not strict JSON") from exc

    if type(parsed) is not dict:
        raise CapsuleSchemaError("capsule artifact root must be a JSON object")

    capsule = _validate_capsule_shape(parsed)
    canonical = canonical_envelope_bytes(capsule)
    if raw != canonical:
        raise CapsuleSchemaError(
            "capsule artifact bytes are not the exact canonical envelope"
        )
    return capsule


def _sign_capsule_mapping(
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

    pub_raw = private_key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
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
        "signer_key_id": public_key_id(pub_raw),
        "signature_algorithm": SIGNATURE_ALGORITHM,
        "signature": base64.b64encode(b"\x00" * 64).decode("ascii"),
    }
    _validate_capsule_shape(capsule)
    signed = _canonical_json({field: capsule[field] for field in SIGNED_FIELDS})
    capsule["signature"] = base64.b64encode(private_key.sign(signed)).decode(
        "ascii"
    )
    _validate_capsule_shape(capsule)
    return capsule


def sign_capsule_artifact(**kwargs: Any) -> bytes:
    return _serialize_capsule_mapping(_sign_capsule_mapping(**kwargs))


def _verify_parsed_capsule(
    capsule: Mapping[str, Any],
    pin: PinnedAuthorityKey,
) -> Dict[str, Any]:
    c = _validate_capsule_shape(capsule)
    validate_pin(pin)
    expected_key_id = public_key_id(pin.public_key)
    if c["signer_key_id"] != expected_key_id:
        raise CapsuleSignatureError(
            "signer_key_id does not match pinned authority key"
        )

    signature = base64.b64decode(c["signature"], validate=True)
    signed = _canonical_json({field: c[field] for field in SIGNED_FIELDS})
    pub = Ed25519PublicKey.from_public_bytes(pin.public_key)
    try:
        pub.verify(signature, signed)
    except InvalidSignature as exc:
        raise CapsuleSignatureError("invalid capsule signature") from exc
    return c


def _binding(
    capsule: Mapping[str, Any],
) -> Tuple[str, str, str, str]:
    return (
        capsule["project"],
        capsule["authority_domain"],
        capsule["subject"],
        capsule["candidate"],
    )


def verify_observed_chain(
    artifacts: Iterable[bytes],
    pin: PinnedAuthorityKey,
    *,
    expected_subject: str,
    expected_candidate: str,
    expected_candidate_revision: str,
) -> Dict[str, Any]:
    validate_pin(pin)
    _require_utf8_string(expected_subject, "expected_subject")
    _require_utf8_string(expected_candidate, "expected_candidate")
    _require_utf8_string(
        expected_candidate_revision,
        "expected_candidate_revision",
    )

    expected_binding = (
        pin.project,
        pin.authority_domain,
        expected_subject,
        expected_candidate,
    )

    target_by_digest: Dict[str, Dict[str, Any]] = {}
    foreign_count = 0
    artifact_count = 0

    try:
        iterator = iter(artifacts)
    except TypeError as exc:
        raise CapsuleSchemaError("artifacts must be iterable raw bytes") from exc

    for raw in iterator:
        artifact_count += 1
        capsule = parse_capsule_artifact(raw)
        if _binding(capsule) != expected_binding:
            foreign_count += 1
            continue
        verified = _verify_parsed_capsule(capsule, pin)
        digest = hashlib.sha256(raw).hexdigest()
        target_by_digest[digest] = verified

    if not target_by_digest:
        raise CapsuleChainError("no target-chain capsules were observed")

    by_sequence: Dict[int, List[Tuple[str, Dict[str, Any]]]] = {}
    for digest, capsule in target_by_digest.items():
        by_sequence.setdefault(capsule["sequence"], []).append((digest, capsule))

    for sequence, records in by_sequence.items():
        if len(records) != 1:
            raise CapsuleChainError(f"fork at sequence {sequence}")

    ordered_sequences = sorted(by_sequence)
    expected_sequence = 1
    ordered: List[Tuple[str, Dict[str, Any]]] = []
    for sequence in ordered_sequences:
        if sequence != expected_sequence:
            raise CapsuleChainError(
                f"non-contiguous observed authority chain at sequence {sequence}; "
                f"expected {expected_sequence}"
            )
        ordered.append(by_sequence[sequence][0])
        expected_sequence += 1

    first_digest, first = ordered[0]
    if first["predecessor"] is not None:
        raise CapsuleChainError("genesis predecessor must be null")

    for index in range(1, len(ordered)):
        previous_digest, _ = ordered[index - 1]
        _, current = ordered[index]
        if current["predecessor"] != previous_digest:
            raise CapsuleChainError(
                f"predecessor mismatch at sequence {current['sequence']}"
            )

    head_digest, head = ordered[-1]
    if head["candidate_revision"] != expected_candidate_revision:
        raise CapsuleBindingError(
            "observed head capsule does not bind the requested candidate revision"
        )

    return {
        "observed_chain_valid": True,
        "authority_state": "OBSERVED_CHAIN_ONLY",
        "completeness_status": "NOT_ESTABLISHED",
        "current_decision": None,
        "latest_observed_decision": head["decision"],
        "project": head["project"],
        "authority_domain": head["authority_domain"],
        "subject": head["subject"],
        "candidate": head["candidate"],
        "candidate_revision": head["candidate_revision"],
        "verified_through_sequence": head["sequence"],
        "verified_through_capsule_digest": head_digest,
        "signer_key_id": head["signer_key_id"],
        "pin_provenance_id": pin.provenance_id,
        "pin_provenance_revision": pin.provenance_revision,
        "pin_provenance_digest": pin_provenance_digest(pin),
        "artifact_count": artifact_count,
        "target_unique_capsule_count": len(target_by_digest),
        "foreign_artifact_count": foreign_count,
        "execution_authorized_by_cpi": False,
    }


def require_current_decision(_: Mapping[str, Any]) -> NoReturn:
    raise CapsuleCompletenessError(
        "Authority Capsule v0.1.1 defines no authenticated completeness "
        "mechanism; current authority cannot be derived from an observed chain"
    )
