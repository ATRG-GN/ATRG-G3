import asyncio
import unittest

from aetherium_core.kernel.core_engine import AetheriumCore
from aetherium_core.kernel.events import Event


class TestMicrokernelArchitecture(unittest.IsolatedAsyncioTestCase):
    async def test_dynamic_plugin_loading_and_lifecycle(self):
        core = AetheriumCore()
        plugin = core.load_plugin("aetherium_core.plugins.web_ui_plugin:WebUIPlugin")

        await core.start()
        self.assertTrue(plugin.serving)

        await core.stop()
        self.assertFalse(plugin.serving)

    async def test_event_bus_and_router(self):
        core = AetheriumCore()
        observed = []

        async def on_event(event: Event):
            observed.append(event.name)

        async def on_route(event: Event):
            observed.append(f"route:{event.name}")

        core.event_bus.subscribe("kernel.events", on_event)
        core.router.register("neural.infer", on_route)

        event = Event(name="test")
        await core.event_bus.publish("kernel.events", event)
        await core.router.route("neural.infer", event)

        self.assertEqual(observed, ["test", "route:test"])


if __name__ == "__main__":
    unittest.main()
