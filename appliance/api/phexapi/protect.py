import typing
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from phexcore.protocol import Configuration
from starlette.requests import Request
from starlette.responses import Response

origins = [
    "http://localhost:3000",
    "https://phex.local",
    "https://www.phex.local",
    "https://api.phex.local",
]


class Helmet(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: typing.Callable[[Request], Response]
    ):
        host = request.headers.get("host", "api.phex.space")
        response = await call_next(request)
        response.headers["X-DNS-Prefetch-Control"] = "off"
        response.headers[
            "Expect-CT"
        ] = 'max-age=86400, enforce, report-uri="{}"'.format(
            "https://{}/report-transparency".format(host)
        )
        response.headers["X-Frame-Options"] = "sameorigin"
        response.headers[
            "Strict-Transport-Security"
        ] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        return response


def initialize(server: fastapi.FastAPI, configuration: Configuration):
    server.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    server.add_middleware(Helmet)
