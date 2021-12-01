import asyncio
import importlib
import logging
import types
import typing

import fastapi

from phexcore.protocol import Bootstrappable, Configuration, Disposable, Initializable

_logger = logging.getLogger(__name__)


async def load_phexlets(
    type_names: list[str], app: fastapi.FastAPI, configuration: Configuration, suppress_errors: bool = False
) -> typing.Union[Initializable, Bootstrappable, Disposable]:

    services = []
    for type_name in type_names:
        service: typing.Union[
            Initializable, Bootstrappable, Disposable
        ] = _import_module(type_name)
        services.append(service)
    await asyncio.gather(
        *[
            _execute(service, "initialize", suppress_errors, app, configuration)
            for service in services
        ]
    )
    return services


async def bootstrap_phexlets(
    services: list[Disposable], suppress_errors: bool = False
) -> None:
    await asyncio.gather(
        *[_execute(service, "bootstrap", suppress_errors) for service in services]
    )


async def run_phexlets(
    services: list[Disposable], suppress_errors: bool = False
) -> None:
    await asyncio.gather(
        *[_execute(service, "run", suppress_errors) for service in services]
    )


async def dispose_phexlets(
    services: list[Disposable], suppress_errors: bool = False
) -> None:
    await asyncio.gather(
        *[_execute(service, "dispose", suppress_errors) for service in services]
    )


def _import_module(type_name: str):
    return importlib.import_module(type_name)


async def _execute(
    module: types.ModuleType, name: str, suppress_errors: bool, *args, **kwargs
):
    try:
        if hasattr(module, name):
            callable = getattr(module, name)
            if asyncio.iscoroutinefunction(callable):
                return await callable(*args, **kwargs)
            else:
                return callable(*args, **kwargs)
    except Exception:
        if suppress_errors:
            _logger.error("Failed calling '{}' of '{}'".format(name, module.__name__))
            return
        raise
