import json
from typing import Union

import jwcrypto.jwk
import jwcrypto.jwt


def decode_jwt(
    jwt: str,
    jwks: Union[jwcrypto.jwk.JWK, jwcrypto.jwk.JWKSet],
    check_claims: dict = None,
):
    jw_token = jwcrypto.jwt.JWT(jwt=jwt, key=jwks, check_claims=check_claims)
    if isinstance(jw_token.claims, str):
        return json.loads(jw_token.claims)
    return jw_token.claims
