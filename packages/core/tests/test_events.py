import asyncio
import pytest
import time
from pytest_mock import MockFixture
from phexcore import events


def test_event_subscribe_synchronous(mocker: MockFixture):
    first = None
    second = None

    def callback(_first, _second):
        nonlocal first, second
        first = _first
        second = _second

    subscription = events.subscribe("test_event", callback)

    events.emit("test_event", "Some", "args")

    assert first == "Some"
    assert second == "args"

    subscription.unsubscribe()


def test_event_throw_exception_synchronous(mocker: MockFixture):
    first = None
    second = None

    def callback(_first, _second):
        nonlocal first, second
        first = _first
        second = _second

    def callback_with_failure(_first, _second):
        raise ValueError()

    subscription = events.subscribe("test_event", callback)
    subscription_with_failure = events.subscribe("test_event", callback_with_failure)

    try:
        events.emit("test_event", "Some", "args")
    except:
        assert False, "Exception while emitting event throws exception"
    assert first == "Some"
    assert second == "args"

    subscription.unsubscribe()
    subscription_with_failure.unsubscribe()


@pytest.mark.asyncio
async def test_event_subscribe_asynchronous(mocker: MockFixture):
    first = None
    second = None

    async def _first_func():
        return "Some"

    task = asyncio.create_task(_first_func())

    async def callback(_second):
        nonlocal first, second
        first = await task
        second = _second

    subscription = events.subscribe("test_event", callback)

    events.emit("test_event", "args")

    start = time.time()
    while first is None and (time.time() - start) < 1.0:
        await asyncio.sleep(0.01)

    assert first == "Some"
    assert second == "args"

    subscription.unsubscribe()


@pytest.mark.asyncio
async def test_event_throw_exception_asynchronous(mocker: MockFixture):
    first = None
    second = None

    async def _first_func():
        return "Some"

    task = asyncio.create_task(_first_func())

    async def callback(_second):
        nonlocal first, second
        first = await task
        second = _second

    async def callback_with_failure(_second):
        raise ValueError()

    subscription = events.subscribe("test_event", callback)
    subscription_with_failure = events.subscribe("test_event", callback_with_failure)

    events.emit("test_event", "args")

    start = time.time()
    while first is None and (time.time() - start) < 1.0:
        await asyncio.sleep(0.01)

    assert first == "Some"
    assert second == "args"

    subscription.unsubscribe()
    subscription_with_failure.unsubscribe()


def test_event_is_missing(mocker: MockFixture):
    try:
        events.emit("missing_event", "Some", "args")
        assert True
    except:
        assert False, "Exception while emitting missing event"
