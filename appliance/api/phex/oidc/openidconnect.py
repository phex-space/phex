import json
import urllib.parse
import uuid

import fastapi
import httpx
import jwcrypto.jwt
from fastapi import Depends, HTTPException

from starlette.requests import Request
from starlette.responses import Response, RedirectResponse

from .access import Access
from .metadata import Metadata
from .openidconnectconfiguration import OpenIdConnectConfiguration
from .openidconnectclient import OpenIdConnectClient
from .signinrequest import SigninRequest
from .utils import request_url, get_string_value, decode_jwt, abort

store = {}


class OpenIdConnect(object):
    def __init__(self, configuration: OpenIdConnectConfiguration):
        self.__client = OpenIdConnectClient(configuration)

    def engage(self, app: fastapi.FastAPI):
        @app.get("/oidc/callback")
        async def oidc_callback(state: str, code: str, response: Response):
            if state not in store:
                raise HTTPException(401)
            session = store[state]
            sr = session["request"]
            tokens = await self.__client.get_token_by_code(code)
            id_token = tokens.get("id_token")
            access_token = tokens.get("access_token")
            expires_in = tokens.get("expires_in")
            decoded_token = decode_jwt(access_token, await self.__client.key_set())
            print(decoded_token, tokens, flush=True)
            if "nonce" not in decoded_token or decoded_token["nonce"] != sr.nonce:
                return abort(401, "WrongNonce")
            del store[state]
            store[decoded_token.get("session_state")] = tokens
            response.status_code = 307
            response.headers["Location"] = session["redirect_url"]
            response.set_cookie(
                "phex_auth",
                "Bearer {}".format(access_token),
                httponly=True,
                secure=True,
                expires=expires_in,
            )
            print(tokens, flush=True)

    async def __call__(self, request: Request, response: Response):
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            authorization = request.cookies.get("phex_auth")

        if not authorization:
            state = uuid.uuid4().hex
            sr = await self.__client.create_signin_request()
            store[state] = {"request": sr, "redirect_url": request_url(request)}
            raise HTTPException(307, headers={"Location": await sr.signin_url(state)})

        auth_type, access_token = authorization.split(" ")
        return {
            "jwt": decode_jwt(access_token, await self.__client.key_set()),
            "permission": str(await self.__client.approve_access(access_token, [
                Access("read", "license")
            ], "api"))
        }


"""
curl --location --request POST 'http://localhost:8080/auth/realms/appsdeveloperblog/protocol/openid-connect/token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=authorization_code' \
--data-urlencode 'client_id=photo-app-code-flow-client' \
--data-urlencode 'client_secret=3424193f-4728-4d19-8517-d450d7c6f2f5' \
--data-urlencode 'code=c081f6ca-ae87-40b6-8138-5afd4162d181.f109bb89-cd34-4374-b084-c3c1cf2c8a0b.1dc15d06-d8b9-4f0f-a042-727eaa6b98f7' \
--data-urlencode 'redirect_uri=http://localhost:8081/callback'
"""
