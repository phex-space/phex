import logging
import shutil
import tempfile

import fastapi
import pytest
import starlette.testclient

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def app() -> fastapi.FastAPI:
    return fastapi.FastAPI()


@pytest.fixture
def client(app: fastapi.FastAPI) -> starlette.testclient.TestClient:
    return starlette.testclient.TestClient(app)


@pytest.fixture
def db_url():
    tmpdir = tempfile.mkdtemp(prefix="phexcore_")
    try:
        yield "sqlite:///{}/test.db".format(tmpdir)
    finally:
        shutil.rmtree(tmpdir)
        pass
