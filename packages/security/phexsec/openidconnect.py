import contextvars
import logging
from os import path
import typing

from fastapi import HTTPException, Depends
from fastapi.openapi.models import SecurityBase as SecurityBaseModel, SecuritySchemeType
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from jwcrypto.jwt import JWException
from pydantic.fields import Field
from starlette.requests import Request
from starlette.responses import Response

from .access import Access
from .grant import Grant
from .user import User
from .openidconnectclient import OpenIdConnectClient
from .utils import decode_jwt

_logger = logging.getLogger(__name__)


OpenIdConnectListener = typing.Callable[[str, User], None]


class OpenIdConnect(SecurityBase):
    def __init__(self, client: OpenIdConnectClient, scheme_name: str = None):
        self.scheme_name = scheme_name or self.__class__.__name__
        self.model = OpenIdConnectModel(openIdConnectUrl=client.configuration.issuer)
        self.__client = client
        self.__grant = contextvars.ContextVar("grant")
        self.__listeners = set()

    @property
    def client(self):
        return self.__client

    @property
    def grant(self) -> Grant:
        result = self.__grant.get()
        if result is None:
            raise HTTPException(403, "Forbidden")
        return result

    def add_listener(self, handler: OpenIdConnectListener):
        _logger.debug("Add listener '{}'".format(handler.__name__))
        self.__listeners.add(handler)

    def remove_listener(self, handler: OpenIdConnectListener):
        _logger.debug("Remove listener '{}'".format(handler.__name__))
        self.__listeners.remove(handler)

    async def __call__(self, request: Request, response: Response):
        authorization = request.headers.get("Authorization")
        if not authorization:
            authorization: str = request.cookies.get("phex_token", None)
            if not authorization:
                raise HTTPException(
                    401,
                    {
                        "error": "Unauthorized",
                        "message": "Provide authorization header",
                    },
                )
        else:
            _, authorization = get_authorization_scheme_param(authorization)
        if (
            "phex_token" not in request.cookies
            or authorization != request.cookies["phex_token"]
        ):
            response.set_cookie(
                "phex_token",
                authorization,
                path="/",
                domain=request.headers.get("host"),
                secure=True,
                httponly=True,
                samesite="None",
            )
        access_token = authorization
        try:
            grant = Grant(
                access_token=access_token,
                decoded_token=decode_jwt(access_token, await self.client.keyset()),
            )
            self.__grant.set(grant)
            await self._fire_event("user_authorized", grant.user)
            yield grant
        except JWException:
            raise HTTPException(
                403,
                {
                    "error": "JwtInvalid",
                    "message": "The provided JWT is invalid. May be it is expired.",
                },
            )
        finally:
            self.__grant.set(None)

    def approve(self, audience: str, *access: Access):
        async def do_approve(grant: Grant = Depends(self)):
            return await self.client.approve_access(
                grant.access_token, access, audience=audience
            )

        return do_approve

    async def _fire_event(self, event_type: str, user: User):
        _logger.debug("Firing OpenId Connect event '{}': {}".format(event_type, user))
        for listener in self.__listeners:
            try:
                await listener(event_type, user)
            except Exception:
                _logger.error(
                    "Error firing OpenId Connect event {}".format(event_type),
                    exc_info=True,
                )
        _logger.debug("Fired OpenId Connect event '{}'".format(event_type))


class OpenIdConnectModel(SecurityBaseModel):
    type_ = Field(SecuritySchemeType.openIdConnect, alias="type")
    openIdConnectUrl: str
