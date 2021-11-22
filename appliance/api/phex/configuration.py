import functools

import pydantic


class Configuration(pydantic.BaseSettings):
    debug: bool = False
    oidc_issuer: str = "identity.phex.local"
    oidc_url: str = "https://identity.phex.local/auth/realms/phex"
    mongodb_url: str = "mongodb://mongo:27017"
    mongodb_user: str = "phex"
    mongodb_user_password: str = "242t3m"
    mongodb_database: str = "phex"


@functools.lru_cache()
def get() -> Configuration:
    return Configuration()
