from phex.oidc import OpenIdConnect, OpenIdConnectConfiguration

config = OpenIdConnectConfiguration(
    issuer="https://identity.phex.local/auth/realms/phex",
    client_id="api",
    secret="3bc158ef-ac3f-458e-97c0-1d7765e91756",
    redirect_uri="https://api.phex.local/oidc/callback",
    response_type="code",
    scope="openid api",
)
authentication: OpenIdConnect = OpenIdConnect(config)
