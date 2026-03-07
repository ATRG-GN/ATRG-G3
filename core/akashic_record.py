from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import json
from typing import Any, Optional


def _normalize_for_signature(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _normalize_for_signature(v) for k, v in sorted(value.items())}
    if isinstance(value, (list, tuple)):
        return [_normalize_for_signature(item) for item in value]
    return value


@dataclass(frozen=True)
class AkashicEnvelope:
    """Immutable event envelope with deterministic signature."""

    id: str
    timestamp: datetime = field(default_factory=datetime.now)
    intent: str = ""
    actor: str = ""
    action_type: str = ""
    payload: Any = None
    previous_hash: Optional[str] = None
    signature: str = ""

    def __post_init__(self):
        if not isinstance(self.timestamp, datetime):
            raise TypeError("timestamp must be datetime")
        for field_name in ("id", "intent", "actor", "action_type"):
            if not getattr(self, field_name):
                raise ValueError(f"{field_name} must not be empty")

        computed_signature = self._compute_signature()
        if self.signature and self.signature != computed_signature:
            raise ValueError("Invalid signature: does not match canonical payload")

        if not self.signature:
            object.__setattr__(self, "signature", computed_signature)

    def _compute_signature(self) -> str:
        signature_payload = {
            "id": self.id,
            "timestamp": _normalize_for_signature(self.timestamp),
            "intent": self.intent,
            "actor": self.actor,
            "action_type": self.action_type,
            "payload": _normalize_for_signature(self.payload),
            "previous_hash": self.previous_hash,
        }
        canonical_json = json.dumps(
            signature_payload,
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()


class AkashicLedger:
    """Simple append-only ledger that validates previous_hash chain integrity."""

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
        print(
            f"📜 [AKASHIC]: Recorded Action '{envelope.action_type}' by {envelope.actor} | "
            f"Hash: {envelope.signature[:8]}..."
        )
