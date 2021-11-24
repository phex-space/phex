import logging

from fastapi import HTTPException, Depends
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette.responses import Response

from . import Access, Grant
from .openidconnectclient import OpenIdConnectClient
from .utils import decode_jwt

_logger = logging.getLogger(__name__)


class OpenIdConnect(SecurityBase):
    def __init__(self, client: OpenIdConnectClient, scheme_name: str = None):
        self.scheme_name = scheme_name or self.__class__.__name__
        self.__client = client

    @property
    def client(self):
        return self.__client

    async def authenticate(self, request: Request, response: Response):
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(
                401,
                {"error": "Unauthorized", "message": "Provide authorization header"},
            )
        scheme, access_token = get_authorization_scheme_param(authorization)
        return Grant(
            access_token=access_token,
            decoded_token=decode_jwt(access_token, await self.client.keyset()),
        )

    def approve(self, *access: Access):
        async def do_approve(grant: Grant = Depends(self.authenticate)):
            return None

        return do_approve
