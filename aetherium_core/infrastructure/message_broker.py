from __future__ import annotations

from abc import ABC, abstractmethod

from aetherium_core.kernel.events import Event


class MessageBroker(ABC):
    """Infrastructure contract (Redis Streams / NATS / Kafka adapters)."""

    @abstractmethod
    async def publish(self, topic: str, event: Event) -> None:
        ...


class InMemoryBroker(MessageBroker):
    def __init__(self) -> None:
        self.history: list[tuple[str, Event]] = []

    async def publish(self, topic: str, event: Event) -> None:
        self.history.append((topic, event))
