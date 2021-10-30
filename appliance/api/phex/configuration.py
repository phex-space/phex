import functools

import pydantic


class Configuration(pydantic.BaseSettings):
    debug: bool = False


@functools.lru_cache()
def get() -> Configuration:
    return Configuration()
