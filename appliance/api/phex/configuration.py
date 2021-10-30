import functools

import pydantic


class Configuration(pydantic.BaseSettings):
    debug: bool = False
    oidc_issuer: str = "identity.phex.local"
    oidc_url: str = "https://identity.phex.local/auth/realms/phex"


@functools.lru_cache()
def get() -> Configuration:
    return Configuration()
