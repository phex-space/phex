from typing import Optional

from jwcrypto import jwk


class OpenIdConnectClient:
    def __init__(self):
        self.__keyset: Optional[jwk.JWKSet] = None

    async def keyset(self) -> jwk.JWKSet:
        return self.__keyset
