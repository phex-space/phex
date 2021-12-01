import asyncio
from typing import Optional
import fastapi

import httpx
import jwcrypto.jwk


from .access import Access
from .consent import Consent
from .openidconnectconfiguration import OpenIdConnectConfiguration
from .metadata import Metadata
from .utils import decode_jwt


class OpenIdConnectClient:
    def __init__(self, configuration: OpenIdConnectConfiguration):
        self.__configuratoon = configuration
        self.__http = httpx.AsyncClient()
        self.__keyset: Optional[jwcrypto.jwk.JWKSet] = None
        self.__metadata = None

    async def dispose(self):
        await self.__http.aclose()

    @property
    def configuration(self):
        return self.__configuratoon

    async def keyset(self) -> jwcrypto.jwk.JWKSet:
        if self.__keyset is None:
            metadata = await self.get_metadata()
            response: httpx.Response = await self.__http.get(metadata.jwks_uri)
            self.__keyset = jwcrypto.jwk.JWKSet.from_json(response.read())
        return self.__keyset

    async def get_metadata(self) -> Metadata:
        if not self.__metadata:
            response: httpx.Response = await self.__http.get(
                url="{}/.well-known/openid-configuration".format(
                    self.configuration.issuer
                )
            )
            self.__metadata = Metadata(response.json())
        return self.__metadata

    async def get_userinfo(self, access_token: str) -> dict:
        metadata, jwks = await asyncio.gather(self.get_metadata(), self.keyset())
        response: httpx.Response = await self.__http.get(
            url=metadata.userinfo_endpoint,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        return response.json()

    async def approve_access(
        self, access_token: str, access: list[Access], audience: str
    ):
        if not access_token:
            raise ValueError("access_token")
        if not access_token:
            raise ValueError("access")
        metadata, jwks = await asyncio.gather(self.get_metadata(), self.keyset())
        response: httpx.Response = await self.__http.post(
            url=metadata.token_endpoint,
            headers={"Authorization": f"Bearer {access_token}"},
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:uma-ticket",
                "audience": audience,
                "permission": [str(a) for a in access],
            },
        )
        response_data = response.json()
        if response.status_code != 200:
            raise fastapi.HTTPException(response.status_code, "InvalidRequest")
        grant_result = decode_jwt(response_data["access_token"], jwks)
        return Consent(access, grant_result["authorization"]["permissions"])
