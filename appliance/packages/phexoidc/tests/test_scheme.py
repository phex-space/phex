from typing import Optional
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI, Depends
from jwcrypto import jwt, jwk
from pytest_mock import MockerFixture
from starlette.testclient import TestClient

from phexoidc import OpenIdConnect, OpenIdConnectClient, Grant


@pytest.mark.asyncio
async def test_authenticate(app: FastAPI, client: TestClient, mocker: MockerFixture):
    keyset = AsyncMock()
    key = jwk.JWK(generate="oct", size=256)
    tmp = jwk.JWKSet()
    tmp.add(key)

    oidc_client = OpenIdConnectClient()
    setattr(oidc_client, "keyset", keyset)
    keyset.return_value = tmp

    oidc = OpenIdConnect(oidc_client)
    expected_token: Optional[Grant] = None

    @app.get("/test")
    async def test(grant=Depends(oidc.authenticate)):
        nonlocal expected_token
        expected_token = grant

    test_claims = {"test": "token"}
    token = jwt.JWT(header={"alg": "HS256"}, claims=test_claims)
    token.make_signed_token(key)
    token_serialized = token.serialize()

    response = client.request(
        "GET", "/test", headers={"Authorization": "Bearer {}".format(token_serialized)}
    )

    assert response.status_code == 200
    assert expected_token.access_token == token_serialized
    assert expected_token.user == test_claims
