import json

import jwcrypto.jwk
import jwcrypto.jwt
from fastapi import HTTPException
from starlette.requests import Request


def request_url(request: Request):
    url = str(request.url)
    if "x-forwarded-proto" in request.headers:
        scheme = request.headers.get("x-forwarded-proto", request.url.scheme)
        return url.replace(request.url.scheme + ":", scheme + ":")
    return url


def get_string_value(data: dict, name: str, default_value: str = None) -> str:
    if not data:
        return default_value
    value = data.get(name, default_value)
    if not value:
        return default_value
    if isinstance(value, (list, tuple)):
        return str(value[0])
    return str(value)


def abort(status_code: int, error: str, message: str = None):
    detail = {"error": error}
    if message:
        detail["message"] = message
    raise HTTPException(status_code, detail=detail)


def decode_jwt(jwt: str, jwks: jwcrypto.jwk.JWKSet):
    jw_token = jwcrypto.jwt.JWT(jwt=jwt, key=jwks)
    if isinstance(jw_token.claims, str):
        return json.loads(jw_token.claims)
    return jw_token.claims
