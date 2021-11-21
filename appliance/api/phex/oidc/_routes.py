import fastapi
from starlette.requests import Request
from starlette.responses import Response

from phex.oidc.openidconnectclient import OpenIdConnectClient
from phex.oidc.utils import decode_jwt, abort


def register_callback(app: fastapi.FastAPI, client: OpenIdConnectClient, store: dict):
    @app.get("/oidc/callback")
    async def oidc_callback(request: Request, response: Response):
        state_id = request.query_params["state"]
        code = request.query_params["code"]
        state = await client.pop_state(state_id)
        sr = state["request"]
        tokens = await client.get_token_by_code(code)
        access_token = tokens.get("access_token")
        expires_in = tokens.get("expires_in")
        decoded_token = decode_jwt(access_token, await client.key_set())
        if "nonce" not in decoded_token or decoded_token["nonce"] != sr.nonce:
            return abort(401, "WrongNonce")
        response.status_code = 307
        if "redirect_url" in state:
            response.headers["Location"] = state["redirect_url"]
            response.set_cookie(
                "phex_auth",
                "Bearer {}".format(access_token),
                httponly=True,
                secure=True,
                expires=expires_in,
            )
            return
        return tokens

    @app.get("/oidc/login")
    async def login(request: Request, response: Response):
        sr = await client.create_signin_request()
        response.status_code = 307
        response.headers["Location"] = await sr.signin_url()
