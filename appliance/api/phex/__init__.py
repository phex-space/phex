import fastapi
from starlette.middleware.gzip import GZipMiddleware

from phex import configuration, logging
from phex.authentication import authentication
from phex.middleware.tracing import TracingMiddleware
from phex.usermanagement import router as router_usermanagement
from phex.pkg import router_pkg


app = fastapi.FastAPI(debug=True)
authentication.engage(app)

app.include_router(router_usermanagement)
app.include_router(router_pkg)
app.add_middleware(GZipMiddleware)
app.add_middleware(TracingMiddleware)
