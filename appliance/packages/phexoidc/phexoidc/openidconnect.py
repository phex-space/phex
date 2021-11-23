from fastapi import HTTPException
from fastapi.security.base import SecurityBase
from starlette.requests import Request
from starlette.responses import Response


class OpenIdConnect(SecurityBase):
    def __init__(self, scheme_name: str = None):
        self.scheme_name = scheme_name or self.__class__.__name__

    def authenticate(self, request: Request, response: Response):
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(
                401,
                {"error": "Unauthorized", "message": "Provide authorization header"},
            )
        return authorization
