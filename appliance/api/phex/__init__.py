import fastapi

from phex import configuration
from phex.authentication import authentication
from phex.usermanagement import router as router_usermanagement

app = fastapi.FastAPI(debug=configuration.get().debug)
authentication.engage(app)

app.include_router(router_usermanagement)
