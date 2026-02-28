from datetime import datetime

from core.akashic_record import AkashicEnvelope, AkashicLedger


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

def test_ledger_rejects_invalid_previous_hash_chain_link():
    ledger = AkashicLedger()

    genesis = AkashicEnvelope(
        id="g-1",
        timestamp=datetime(2026, 1, 1, 12, 0, 0),
        intent="test",
        actor="agent-a",
        action_type="code_generation",
        payload={"step": 1},
        previous_hash=None,
    )
    ledger.record(genesis)

    invalid_link = AkashicEnvelope(
        id="g-2",
        timestamp=datetime(2026, 1, 1, 12, 0, 1),
        intent="test",
        actor="agent-a",
        action_type="code_generation",
        payload={"step": 2},
        previous_hash="wrong-hash",
    )

    try:
        ledger.record(invalid_link)
        assert False, "Expected ValueError for invalid previous_hash"
    except ValueError as exc:
        assert "Invalid previous_hash" in str(exc)


def test_ledger_rejects_genesis_with_previous_hash():
    ledger = AkashicLedger()

    invalid_genesis = AkashicEnvelope(
        id="g-0",
        timestamp=datetime(2026, 1, 1, 12, 0, 0),
        intent="test",
        actor="agent-a",
        action_type="code_generation",
        payload={"step": 0},
        previous_hash="should-not-exist",
    )

    try:
        ledger.record(invalid_genesis)
        assert False, "Expected ValueError for genesis previous_hash"
    except ValueError as exc:
        assert "Invalid previous_hash" in str(exc)
