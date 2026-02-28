from __future__ import annotations

from abc import ABC, abstractmethod


class Plugin(ABC):
    """Base contract for all kernel plugins (neural, genesis, web-ui, drivers)."""

    name: str

    @abstractmethod
    async def start(self) -> None:
        ...

    @abstractmethod
    async def stop(self) -> None:
        ...
