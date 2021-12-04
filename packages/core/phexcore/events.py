import asyncio
import dataclasses
import logging
import queue
import threading
import typing

_logger = logging.getLogger(__name__)

_callbacks = dict()
_async_callbacks = dict()
_async_event_queue = queue.Queue()


class Subscription:
    def __init__(
        self, event_type: str, callback: typing.Callable, asynchronous: bool
    ) -> None:
        self.__event_type = event_type
        self.__callback = callback
        self.__asynchronous = asynchronous

    def unsubscribe(self):
        if self.__asynchronous:
            handlers = _async_callbacks.get(self.__event_type, [])
        else:
            handlers = _callbacks.get(self.__event_type, [])
        handlers.remove(self.__callback)


def subscribe(event_type: str, callback: typing.Callable) -> Subscription:
    asynchronous = asyncio.iscoroutinefunction(callback)
    if asynchronous:
        handlers = _async_callbacks
        _logger.debug(
            "Register asynchronous '{}' callback to event type '{}'.".format(
                callback.__name__, event_type
            )
        )
    else:
        handlers = _callbacks
        _logger.debug(
            "Register synchronous '{}' callback to event type '{}'.".format(
                callback.__name__, event_type
            )
        )
    if event_type not in handlers:
        handlers[event_type] = []
    handlers[event_type].append(callback)
    return Subscription(event_type, callback, asynchronous)


def emit(event_type: str, *args, **kwargs):
    _logger.debug(
        "Emitting event '{}'. args: {} - kwargs: {}".format(event_type, args, kwargs)
    )
    _async_event_queue.put({"type": event_type, "args": args, "kwargs": kwargs})
    try:
        _emit(event_type, args, kwargs)
    finally:
        _logger.debug("Emitted event '{}'.".format(event_type))


async def aemit(event_type: str, *args, **kwargs):
    _logger.debug(
        "Asynchronous emitting event '{}'. args: {} - kwargs: {}".format(event_type, args, kwargs)
    )
    try:
        _emit(event_type, args, kwargs)
        await _emit_async(event_type, args, kwargs)
    finally:
        _logger.debug("Asynchronous emitted event '{}'.".format(event_type))


def _emit(event_type: str, args, kwargs):
    if event_type not in _callbacks:
        return
    for callback in _callbacks[event_type]:
        try:
            callback(*args, **kwargs)
        except:
            _logger.error("Error firing event '{}'.".format(callback.__name__))


async def _emit_async(event_type: str, args, kwargs):
    if event_type not in _async_callbacks:
        return
    for callback in _async_callbacks[event_type]:
        try:
            await callback(*args, **kwargs)
        except:
            _logger.error(
                "Error firing asynchronous event '{}'.".format(callback.__name__),
                exc_info=True,
            )


def _async_event_worker():
    loop = asyncio.new_event_loop()
    while True:
        event_data = _async_event_queue.get()
        _logger.debug("Realease asynchronous event: {}".format(_async_callbacks))
        loop.run_until_complete(
            _emit_async(event_data["type"], event_data["args"], event_data["kwargs"])
        )
        _async_event_queue.task_done()


threading.Thread(target=_async_event_worker, daemon=True).start()
