from __future__ import annotations

from dataclasses import dataclass, field

from aetherium_core.kernel.core_engine import AetheriumCore
from aetherium_core.kernel.events import Event
from aetherium_core.kernel.plugins import Plugin


@dataclass
class NeuralPlugin(Plugin):
    core: AetheriumCore
    name: str = "neural"
    booted: bool = field(default=False, init=False)

    async def start(self) -> None:
        self.booted = True
        await self.core.event_bus.publish(
            "plugin.lifecycle",
            Event(name="plugin_started", source=self.name),
        )

    async def stop(self) -> None:
        self.booted = False
