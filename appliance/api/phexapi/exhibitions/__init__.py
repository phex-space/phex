import logging
import os

import fastapi

from phexcore import services
from phexcore.protocol import Configuration

from .routes import router

_logger = logging.getLogger(__name__)


async def initialize(server: fastapi.FastAPI, configuration: Configuration):
    _logger.debug("Initialize exhibitions")
    server.include_router(router)
    _logger.debug("Exhibitions are initialized.")


async def bootstrap():
    from . import controller
    _logger.debug("Setting up exhibitions")
    services.register("exhibitions", controller.ExhibitionService())
    _logger.debug("Exhibitions are set up.")


async def dispose():
    _logger.debug("Disposing exhibitions")
    _logger.debug("Exhibitions are disposed")
