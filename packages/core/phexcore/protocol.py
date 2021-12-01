import typing

import fastapi
import pydantic


class Configuration(pydantic.BaseSettings):
    debug: bool = False
    database_url: typing.Optional[str]
    database_autocommit: bool = False
    database_autoflush: bool = False


class Initializable(typing.Protocol):
    def initialize(self, app: fastapi.FastAPI, configuration: Configuration) -> None:
        """Initialize the owner."""


class Bootstrappable(typing.Protocol):
    def bootstrap(self) -> None:
        """Bootstrap the owner."""


class Runnable(typing.Protocol):
    def run(self) -> None:
        """Run the owner. Must return immediatly."""


class Disposable(typing.Protocol):
    def dispose(self) -> None:
        """Dispose the owner."""
