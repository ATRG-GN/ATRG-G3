from __future__ import annotations

from abc import ABC, abstractmethod


class AIAdapter(ABC):
    """Domain-level abstraction for Neural Bridge backends."""

    @abstractmethod
    async def infer(self, prompt: str) -> str:
        ...
