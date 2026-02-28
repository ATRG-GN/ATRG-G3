from __future__ import annotations

from dataclasses import dataclass, field

from aetherium_core.kernel.core_engine import AetheriumCore
from aetherium_core.kernel.plugins import Plugin


@dataclass
class GenesisNodePlugin(Plugin):
    core: AetheriumCore
    name: str = "genesis_node"
    leader_mode: bool = field(default=False)

    async def start(self) -> None:
        self.leader_mode = True

    async def stop(self) -> None:
        self.leader_mode = False
