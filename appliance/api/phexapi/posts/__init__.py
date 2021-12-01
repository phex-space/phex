import logging
import typing

import fastapi
from phexcore import services
from sqlalchemy.orm.session import Session

from phexcore.protocol import Configuration
from .routes import router

_logger = logging.getLogger(__name__)

async def initialize(server: fastapi.FastAPI, configuration: Configuration):
    _logger.debug("Initialize posts")
    server.include_router(router)
    _logger.debug("Posts are initialized.")


async def bootstrap():
    _logger.debug("Setting up posts")
    from . import controller
    services.register("posts", controller.PostsService())
    _logger.debug("Posts are set up.")


async def dispose():
    _logger.debug("Disposing posts")
    _logger.debug("Posts are disposed")
