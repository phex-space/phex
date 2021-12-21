import logging
import os

import fastapi

from phexcore import services
from phexcore.protocol import Configuration

from .routes import router

_logger = logging.getLogger(__name__)


async def initialize(server: fastapi.FastAPI, configuration: Configuration):
    _logger.debug("Initialize images")
    server.include_router(router)
    os.makedirs(configuration.images_path, exist_ok=True)
    _logger.debug("Images are initialized.")


async def bootstrap():
    from . import controller
    _logger.debug("Setting up images")
    services.register("images", controller.ImagesService())
    _logger.debug("Images are set up.")


async def dispose():
    _logger.debug("Disposing images")
    _logger.debug("Images are disposed")
