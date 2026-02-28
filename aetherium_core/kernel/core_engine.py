from __future__ import annotations

import importlib
from dataclasses import dataclass, field

from .events import EventBus
from .plugins import Plugin
from .routing import MessageRouter


@dataclass
class AetheriumCore:
    """Microkernel core: lifecycle, event bus, routing, plugin management."""

    event_bus: EventBus = field(default_factory=EventBus)
    router: MessageRouter = field(default_factory=MessageRouter)
    _plugins: dict[str, Plugin] = field(default_factory=dict, init=False)

    def register_plugin(self, plugin: Plugin) -> None:
        self._plugins[plugin.name] = plugin

    def load_plugin(self, dotted_path: str) -> Plugin:
        """Dynamic loading with `module:ClassName` syntax."""
        module_name, class_name = dotted_path.split(":", maxsplit=1)
        module = importlib.import_module(module_name)
        plugin_cls = getattr(module, class_name)
        plugin: Plugin = plugin_cls(core=self)
        self.register_plugin(plugin)
        return plugin

    async def start(self) -> None:
        for plugin in self._plugins.values():
            await plugin.start()

    async def stop(self) -> None:
        for plugin in reversed(list(self._plugins.values())):
            await plugin.stop()
