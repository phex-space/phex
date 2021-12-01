import typing
from unittest.mock import AsyncMock
import jwcrypto

import pytest
import httpx
from fastapi import FastAPI, Depends
from jwcrypto import jwt, jwk
from pytest_mock import MockerFixture
from phexsec.access import Access
from pytest_httpx import HTTPXMock
from starlette.testclient import TestClient

from phexsec import (
    OpenIdConnect,
    OpenIdConnectClient,
    OpenIdConnectConfiguration,
    Grant,
)
from phexsec.consent import Consent

_jwks_response = {
    "authorization_endpoint": "",
    "issuer": "",
    "userinfo_endpoint": "",
    "token_endpoint": "https://test.org/token",
    "revocation_endpoint": "",
    "jwks_uri": "https://test.org",
    "end_session_endpoint": "",
}


def _make_jwt_and_key(
    payload: dict, keyset: jwk.JWKSet = None
) -> tuple[jwk.JWKSet, jwt.JWT]:
    if keyset is None:
        key = jwk.JWK(generate="oct", size=256)
        keyset = jwk.JWKSet()
        keyset.add(key)
    token = jwt.JWT(header={"alg": "HS256"}, claims=payload)
    token.make_signed_token(next(keyset.__iter__()))
    return (keyset, token)


@pytest.mark.asyncio
async def test_authenticate(app: FastAPI, client: TestClient, httpx_mock: HTTPXMock):
    test_claims = {"test": "token"}
    expected_grant: typing.Optional[Grant] = None

    keyset, token = _make_jwt_and_key(test_claims)
    httpx_mock.add_response(method="GET", json=_jwks_response)
    httpx_mock.add_response(method="GET", json=keyset.export(as_dict=True))

    oidc_config = OpenIdConnectConfiguration(
        "https://test.org", "test", "secret", None, "code", "openid"
    )
    oidc_client = OpenIdConnectClient(oidc_config)
    oidc = OpenIdConnect(oidc_client)

    @app.get("/test")
    async def test(grant=Depends(oidc)):
        nonlocal expected_grant
        expected_grant = grant

    token_serialized = token.serialize()

    response = client.request(
        "GET", "/test", headers={"Authorization": "Bearer {}".format(token_serialized)}
    )

    assert response.status_code == 200
    assert expected_grant.access_token == token_serialized
    assert expected_grant.user == test_claims

    await oidc_client.dispose()


@pytest.mark.asyncio
async def test_approve(app: FastAPI, client: TestClient, httpx_mock: HTTPXMock):
    test_claims = {"test": "token"}
    test_authorization = {
        "authorization": {"permissions": [{"rsname": "Approve", "scopes": ["test"]}]}
    }
    expected_consent: typing.Optional[Consent] = None

    keyset, token = _make_jwt_and_key(test_claims)
    _, auth_token = _make_jwt_and_key(test_authorization, keyset)

    httpx_mock.add_response(method="GET", json=_jwks_response)
    httpx_mock.add_response(method="GET", json=keyset.export(as_dict=True))
    httpx_mock.add_response(
        method="POST", json={"access_token": auth_token.serialize()}
    )

    oidc_config = OpenIdConnectConfiguration(
        "https://test.org", "test", "secret", None, "code", "openid"
    )
    oidc_client = OpenIdConnectClient(oidc_config)
    oidc = OpenIdConnect(oidc_client)

    @app.get("/test")
    async def test(consent=Depends(oidc.approve(Access("test", "Approve")))):
        nonlocal expected_consent
        expected_consent = consent

    token_serialized = token.serialize()

    response = client.request(
        "GET", "/test", headers={"Authorization": "Bearer {}".format(token_serialized)}
    )

    assert response.status_code == 200
    assert expected_consent.can_test_Approve

    await oidc_client.dispose()
