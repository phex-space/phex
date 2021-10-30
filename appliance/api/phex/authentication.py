from typing import Callable

from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi_oidc import get_auth

from phex import configuration

_authUrlBase = configuration.get().oidc_url

scheme = OAuth2AuthorizationCodeBearer(authorizationUrl="{}/protocol/openid-connect/auth".format(_authUrlBase),
                                       tokenUrl="{}/protocol/openid-connect/token".format(_authUrlBase), )

OIDC_config = {
    "client_id": "api",
    "audience": "account",
    "base_authorization_server_uri": configuration.get().oidc_url,
    "issuer": configuration.get().oidc_url,
    "signature_cache_ttl": 3600,
}

authenticate_user: Callable = get_auth(**OIDC_config)
