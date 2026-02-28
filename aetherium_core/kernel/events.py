from __future__ import annotations

import asyncio
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable, DefaultDict

EventHandler = Callable[["Event"], Awaitable[None]]


@dataclass(slots=True)
class Event:
    """Canonical event envelope used across the microkernel."""

    name: str
    payload: dict[str, Any] = field(default_factory=dict)
    source: str = "unknown"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class EventBus:
    """Async in-process event bus, replaceable by broker adapters."""

    def __init__(self) -> None:
        self._subscribers: DefaultDict[str, list[EventHandler]] = defaultdict(list)

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        self._subscribers[topic].append(handler)

    async def publish(self, topic: str, event: Event) -> None:
        handlers = self._subscribers.get(topic, [])
        if not handlers:
            return
        await asyncio.gather(*(handler(event) for handler in handlers))
