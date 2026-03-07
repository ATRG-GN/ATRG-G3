from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import json
from typing import Any, Optional


def _normalize_for_signature(value: Any) -> Any:
    """Normalize values into deterministic JSON-safe structures."""
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _normalize_for_signature(v) for k, v in sorted(value.items())}
    if isinstance(value, list):
        return [_normalize_for_signature(item) for item in value]
    return value


def _build_signature_payload(envelope: "AkashicEnvelope") -> dict[str, Any]:
    return {
        "id": envelope.id,
        "timestamp": _normalize_for_signature(envelope.timestamp),
        "intent": envelope.intent,
        "actor": envelope.actor,
        "action_type": envelope.action_type,
        "payload": _normalize_for_signature(envelope.payload),
        "previous_hash": envelope.previous_hash,
    }


@dataclass(frozen=True)
class AkashicEnvelope:
    """Immutable ledger envelope with deterministic signature generation."""

    id: str
    intent: str
    actor: str
    action_type: str
    payload: Any
    previous_hash: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    signature: str = ""

    def __post_init__(self):
        if self.signature:
            return

        canonical_json = json.dumps(
            _build_signature_payload(self),
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        digest = hashlib.sha256(canonical_json.encode()).hexdigest()
        object.__setattr__(self, "signature", digest)


class AkashicLedger:
    """Append-only ledger for Akashic envelopes."""

    def __init__(self):
        self._chain = []

    def record(self, envelope: AkashicEnvelope):
        if len(self._chain) > 0:
            last_record = self._chain[-1]
            expected_previous_hash = last_record.signature

            if envelope.previous_hash != expected_previous_hash:
                raise ValueError("Invalid previous_hash: expected hash of the latest record")

        elif envelope.previous_hash is not None:
            raise ValueError("Invalid previous_hash: genesis record must not reference a previous hash")

        self._chain.append(envelope)
        print(f"📜 [AKASHIC]: Recorded Action '{envelope.action_type}' by {envelope.actor} | Hash: {envelope.signature[:8]}...")
