import asyncio
import functools
import logging
import os

import fastapi
import toml
from dotenv import dotenv_values
from fastapi.params import Header

import phexcore
import phexsec
from phexcore import loader, services
from phexcore.protocol import Configuration

_phexlets = []

config = Configuration(
    **{
        **dotenv_values(".env"),
        **dotenv_values(".env.development"),
        **dotenv_values(".env.{}".format(os.environ.get("USERNAME", "ignore"))),
    }
)

if config.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

server = fastapi.FastAPI(debug=config.debug)
services.register("config", config)


async def initialize():
    global _phexlets
    _phexlets = await loader.load_phexlets(
        ["phexcore.database", "phexapi.posts"], server, config, suppress_errors=True
    )


asyncio.run(initialize())

_logger.debug("Register startup event.")


@server.on_event("startup")
async def setup():
    await loader.bootstrap_phexlets(_phexlets)
    await loader.run_phexlets(_phexlets)


@server.on_event("shutdown")
async def setup():
    await loader.dispose_phexlets(_phexlets, suppress_errors=True)


@server.get("/")
def api_info():
    return _get_root_info()


@functools.lru_cache(maxsize=1)
def _get_root_info():
    with open("pyproject.toml", "r") as fp:
        _project = toml.load(fp)
    poetry = _project["tool"]["poetry"]
    return {
        "name": poetry["name"],
        "version": poetry["version"],
        "description": poetry["description"],
        "libs": [{"phexcore": phexcore.__version__},{"phexsec": phexsec.__version__}],
    }
