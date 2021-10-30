import fastapi

from phex import configuration
from phex.usermanagement import router as router_usermanagement

app = fastapi.FastAPI(debug=configuration.get().debug)

app.include_router(router_usermanagement)
