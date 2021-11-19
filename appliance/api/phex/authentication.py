from fastapi import Depends

from phex.oidc import (
    Access,
    AuthenticationResult,
    OpenIdConnect,
    OpenIdConnectConfiguration,
)

config = OpenIdConnectConfiguration(
    issuer="https://identity.phex.local/auth/realms/phex",
    client_id="api",
    secret="3bc158ef-ac3f-458e-97c0-1d7765e91756",
    redirect_uri="https://api.phex.local/oidc/callback",
    response_type="code",
    scope="openid",
)
authentication: OpenIdConnect = OpenIdConnect(config)


def approve(*access: Access):
    async def do_approval(auth: AuthenticationResult = Depends(authentication)):
        return await authentication.approve_access(auth.access_token, "api", access)

    return do_approval
