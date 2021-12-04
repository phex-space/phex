import logging
import fastapi

import phexsec
from phexcore import events, services
from phexcore.protocol import Configuration

from phexapi.auth import oidc_scheme

from . import schema

_logger = logging.getLogger(__name__)


def bootstrap():
    from .controller import UserService

    users: UserService = controller.UserService()
    services.register("users", users)
    oidc_scheme.add_listener(_oidc_listener)


def dispose():
    oidc_scheme.remove_listener(_oidc_listener)


async def _oidc_listener(event_type: str, user: phexsec.User):
    _logger.debug("Handle event '{}': {}".format(event_type, user))
    from .controller import UserService
    users: UserService = services.get("users")
    if event_type == "user_authorized":
        await users.handle_authorized_user(schema.UserCreate(**user.dict()))
