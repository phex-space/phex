import fastapi
import logging
import os

import phexsec
from phexcore import events, services
from phexcore.protocol import Configuration

from phexapi.auth import oidc_scheme

from . import schema
from .routes import router

_logger = logging.getLogger(__name__)


async def initialize(server: fastapi.FastAPI, configuration: Configuration):
    _logger.debug("Initialize users")
    server.include_router(router)
    _logger.debug("Users are initialized.")


def bootstrap():
    from .controller import UserService

    users: UserService = controller.UserService()
    services.register("users", users)
    oidc_scheme.add_listener(_oidc_listener)


def dispose():
    oidc_scheme.remove_listener(_oidc_listener)


async def _oidc_listener(event_type: str, user: phexsec.User):
    from .controller import UserService

    _logger.debug("Handle event '{}': {}".format(event_type, user))
    users: UserService = services.get("users")
    if event_type == "user_authorized":
        await users.handle_authorized_user(schema.UserCreate(**user.dict()))
