import pytest
from fastapi import FastAPI, Depends
from jwcrypto import jwt, jwk
from starlette.testclient import TestClient

from phexoidc.openidconnect import OpenIdConnect


@pytest.mark.asyncio
async def test_authenticate(app: FastAPI, client: TestClient):
    expected_token = None
    auth = OpenIdConnect()

    @app.get("/test")
    async def test(grant=Depends(auth.authenticate)):
        nonlocal expected_token
        expected_token = grant

    key = jwk.JWK(generate="oct", size=256)
    token = jwt.JWT(header={"alg": "HS256"}, claims={"test": "token"})
    token.make_signed_token(key)
    token_serialized = token.serialize()
    response = client.request(
        "GET", "/test", headers={"Authorization": token_serialized}
    )

    assert response.status_code == 200
    assert expected_token == token_serialized
