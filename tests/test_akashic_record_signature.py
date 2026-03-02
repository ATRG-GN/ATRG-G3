from datetime import datetime

from core.akashic_record import AkashicEnvelope


def test_signature_is_stable_for_equivalent_dict_payload_order():
    ts = datetime(2026, 1, 1, 12, 0, 0)

    envelope_a = AkashicEnvelope(
        id="e-1",
        timestamp=ts,
        intent="test",
        actor="agent-a",
        action_type="code_generation",
        payload={"b": 2, "a": 1},
        previous_hash="prev",
    )

    envelope_b = AkashicEnvelope(
        id="e-1",
        timestamp=ts,
        intent="test",
        actor="agent-a",
        action_type="code_generation",
        payload={"a": 1, "b": 2},
        previous_hash="prev",
    )

    assert envelope_a.signature == envelope_b.signature


def test_signature_changes_when_action_context_changes():
    ts = datetime(2026, 1, 1, 12, 0, 0)

    envelope_a = AkashicEnvelope(
        id="e-2",
        timestamp=ts,
        intent="test",
        actor="agent-a",
        action_type="economic_transaction",
        payload={"amount": 10},
        previous_hash="prev",
    )

    envelope_b = AkashicEnvelope(
        id="e-2",
        timestamp=ts,
        intent="test",
        actor="agent-a",
        action_type="code_generation",
        payload={"amount": 10},
        previous_hash="prev",
    )

    assert envelope_a.signature != envelope_b.signature
