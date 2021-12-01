import logging

import fastapi
import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy.orm.session import Session

from phexcore import services
from phexcore.protocol import Configuration

_logger = logging.getLogger(__name__)


class DatabaseService(object):
    def __init__(self, configuration: Configuration) -> None:
        super().__init__()
        self.__engine = sqlalchemy.create_engine(configuration.database_url)
        self.__base_class = sqlalchemy.ext.declarative.declarative_base()
        self.__session_creator = sqlalchemy.orm.sessionmaker(
            autocommit=configuration.database_autocommit,
            autoflush=configuration.database_autoflush,
            bind=self.__engine,
        )
        setattr(self.__base_class, "_asdict", _asdict)

    @property
    def engine(self) -> sqlalchemy.engine.Engine:
        return self.__engine

    @property
    def Base(self):
        return self.__base_class

    def new_session(self) -> sqlalchemy.orm.Session:
        return self.__session_creator()


def initialize(app: fastapi.FastAPI, configuration: Configuration):
    services.register("database", DatabaseService(configuration))


def run():
    database: DatabaseService = services.get("database")
    database.Base.metadata.create_all(bind=database.engine)


def dispose():
    services.unregister("database")


def _asdict(self):
    return {
        c.key: getattr(self, c.key)
        for c in sqlalchemy.inspect(self).mapper.column_attrs
    }
