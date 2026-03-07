import asyncio
import inspect

import pytest

from core.aether_conductor import AetherConductor
from core.signature import AISource



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
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def pytest_configure(config):
    config.addinivalue_line("markers", "asyncio: mark test as async and run in local event loop")


def pytest_pyfunc_call(pyfuncitem):
    if "asyncio" not in pyfuncitem.keywords:
        return None

    test_func = pyfuncitem.obj
    if not inspect.iscoroutinefunction(test_func):
        return None

    testargs = {name: pyfuncitem.funcargs[name] for name in pyfuncitem._fixtureinfo.argnames}

    loop = pyfuncitem.funcargs.get("event_loop")
    if loop is None:
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(test_func(**testargs))
        finally:
            loop.close()
        return True

    loop.run_until_complete(test_func(**testargs))
    return True


@pytest.fixture
def clean_conductor():
    conductor = AetherConductor()
    conductor.channels.clear()
    conductor._background_tasks.clear()
    conductor.trust_scores = {
        AISource.HUMAN_ARCHITECT: 100,
        AISource.GEMINI_CORE: 95,
        AISource.UNKNOWN_ECHO: 10,
    }
    return conductor
