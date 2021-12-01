# from fastapi.security import OpenIdConnect
import phexsec
from phexsec.openidconnect import OpenIdConnect
from phexsec.openidconnectclient import OpenIdConnectClient

_oidc_config = phexsec.OpenIdConnectConfiguration(
    issuer="https://identity.phex.local/auth/realms/phex",
    client_id="api",
    secret="f688d7bd-c364-443f-85ba-fcad226121cc",
    response_type="code",
    scope="openid",
    redirect_uri=""
)
oidc_client = OpenIdConnectClient(_oidc_config)
oidc_scheme = OpenIdConnect(oidc_client)
