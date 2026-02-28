from __future__ import annotations

from dataclasses import dataclass, field

from aetherium_core.kernel.core_engine import AetheriumCore
from aetherium_core.kernel.plugins import Plugin


@dataclass
class WebUIPlugin(Plugin):
    core: AetheriumCore
    name: str = "web_ui"
    serving: bool = field(default=False, init=False)

    async def start(self) -> None:
        self.serving = True

    async def stop(self) -> None:
        self.serving = False
