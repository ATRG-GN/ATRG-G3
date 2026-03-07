import pytest
import asyncio
from core.aether_conductor import AetherConductor
from core.signature import OriginMetadata, AISource


def pytest_configure(config):
    config.addinivalue_line("markers", "asyncio: mark test as asyncio coroutine")


@pytest.hookimpl(tryfirst=True)
def pytest_pyfunc_call(pyfuncitem):
    """Run async tests without depending on external pytest-asyncio plugin."""
    test_fn = pyfuncitem.obj

    if not asyncio.iscoroutinefunction(test_fn):
        return None

    loop = pyfuncitem.funcargs.get("event_loop")
    if loop is None:
        loop = asyncio.new_event_loop()
        try:
            
            kwargs = {name: pyfuncitem.funcargs[name] for name in pyfuncitem._fixtureinfo.argnames}
            loop.run_until_complete(test_fn(**kwargs))
        finally:
            loop.close()
    else:
        
            kwargs = {name: pyfuncitem.funcargs[name] for name in pyfuncitem._fixtureinfo.argnames}
            loop.run_until_complete(test_fn(**kwargs))

    return True

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def clean_conductor():
    """Returns a clean AetherConductor instance for each test.

    Since AetherConductor is a singleton, we need to reset its state
    between tests to ensure isolation.
    """
    # Reset the singleton instance (if possible, or just clear channels)
    # The current implementation of AetherConductor uses __new__ for singleton.
    # We can clear the state of the existing instance.

    conductor = AetherConductor()
    conductor.channels.clear()
    conductor._background_tasks.clear()
    conductor.trust_scores = {
        AISource.HUMAN_ARCHITECT: 100,
        AISource.GEMINI_CORE: 95,
        AISource.UNKNOWN_ECHO: 10
    }
    return conductor
