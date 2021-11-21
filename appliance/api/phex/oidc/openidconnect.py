import fastapi
from fastapi import HTTPException

from starlette.requests import Request
from starlette.responses import Response

from ._routes import register_callback
from .access import Access
from .authenticationresult import AuthenticationResult
from .openidconnectconfiguration import OpenIdConnectConfiguration
from .openidconnectclient import OpenIdConnectClient
from .utils import request_url, decode_jwt

store = {}


class OpenIdConnect(object):
    def __init__(self, configuration: OpenIdConnectConfiguration):
        self.__client = OpenIdConnectClient(configuration)

    def engage(self, app: fastapi.FastAPI):
        register_callback(app, self.__client, store)

    async def __call__(self, request: Request, response: Response):
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            authorization = request.cookies.get("phex_auth")

        if not authorization:
            sr = await self.__client.create_signin_request(
                {"redirect_url": request_url(request)}
            )
            raise HTTPException(307, headers={"Location": await sr.signin_url()})

        auth_type, access_token = authorization.split(" ")
        return AuthenticationResult(
            access_token, decode_jwt(access_token, await self.__client.key_set())
        )

    async def approve_access(self, access_token, audience, *access: Access):
        return await self.__client.approve_access(
            access_token,
            *access,
            audience,
        )


"""
curl --location --request POST 'http://localhost:8080/auth/realms/appsdeveloperblog/protocol/openid-connect/token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=authorization_code' \
--data-urlencode 'client_id=photo-app-code-flow-client' \
--data-urlencode 'client_secret=3424193f-4728-4d19-8517-d450d7c6f2f5' \
--data-urlencode 'code=c081f6ca-ae87-40b6-8138-5afd4162d181.f109bb89-cd34-4374-b084-c3c1cf2c8a0b.1dc15d06-d8b9-4f0f-a042-727eaa6b98f7' \
--data-urlencode 'redirect_uri=http://localhost:8081/callback'
"""
