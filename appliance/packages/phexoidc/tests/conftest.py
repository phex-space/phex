import logging

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

logging.basicConfig(level=logging.DEBUG, filename="test.log")


@pytest.fixture()
def app():
    test_app = FastAPI()
    yield test_app


@pytest.fixture()
def client(app):
    return TestClient(app)
