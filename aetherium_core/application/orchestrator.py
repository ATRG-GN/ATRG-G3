from __future__ import annotations

from dataclasses import dataclass

from aetherium_core.domain.ai_adapter import AIAdapter
from aetherium_core.kernel.events import Event
from aetherium_core.kernel.core_engine import AetheriumCore


@dataclass
class GenesisOrchestrator:
    """Application layer: coordinates use-cases across plugins/services."""

    core: AetheriumCore
    ai: AIAdapter

    async def handle_prompt(self, prompt: str) -> str:
        answer = await self.ai.infer(prompt)
        await self.core.event_bus.publish(
            "neural.completed",
            Event(name="inference_completed", payload={"prompt": prompt}, source="orchestrator"),
        )
        return answer
