import asyncio
import logging
from typing import Optional

import httpx
import jwcrypto.jwk

from .access import Access
from .consent import Consent
from .metadata import Metadata
from .openidconnectconfiguration import OpenIdConnectConfiguration
from .signinrequest import SigninRequest
from .utils import abort, decode_jwt

_logger = logging.getLogger(__name__)


class OpenIdConnectClient(object):
    def __init__(self, configuration: OpenIdConnectConfiguration):
        self.__configuration = configuration
        self.__http: httpx.AsyncClient = httpx.AsyncClient()
        self.__metadata: Optional[Metadata] = None

    async def dispose(self):
        await self.__http.aclose()

    @property
    def configuration(self):
        return self.__configuration

    async def get_metadata(self) -> Metadata:
        if not self.__metadata:
            response: httpx.Response = await self.__http.get(
                "{}/.well-known/openid-configuration".format(self.configuration.issuer)
            )
            self.__metadata = Metadata(response.json())
        return self.__metadata

    async def key_set(self) -> jwcrypto.jwk.JWKSet:
        metadata = await self.get_metadata()
        response: httpx.Response = await self.__http.get(metadata.jwks_uri())
        return jwcrypto.jwk.JWKSet.from_json(response.read())

    async def get_token_by_code(self, code: str):
        metadata = await self.get_metadata()
        payload = {
            "code": code,
            "grant_type": "authorization_code",
            "client_id": self.configuration.client_id,
            "client_secret": self.configuration.secret,
            "redirect_uri": self.configuration.redirect_uri,
        }
        response: httpx.Response = await self.__http.post(
            metadata.token_endpoint(),
            data=payload,
        )
        return response.json()

    async def approve_access(
        self, access_token: str, access: list[Access], audience: str
    ):
        metadata, jwks = await asyncio.gather(self.get_metadata(), self.key_set())
        response: httpx.Response = await self.__http.post(
            url=metadata.token_endpoint(),
            headers={"Authorization": f"Bearer {access_token}"},
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:uma-ticket",
                "audience": audience,
                "permission": [str(a) for a in access],
            },
        )
        response_data = response.json()
        _logger.debug("Status: {}".format(response.status_code))
        if response.status_code != 200:
            _logger.error("Permission response: %s - %s", response.status_code, response_data)
            return abort(response.status_code,
                         response_data.get('error', 'InvalidRequest'), response_data.get('error_description', None))
        grant_result = decode_jwt(response_data['access_token'], jwks)
        return Consent(access, grant_result['authorization']['permissions'])

    async def create_signin_request(self) -> SigninRequest:
        return SigninRequest(await self.get_metadata(), self.__configuration)
