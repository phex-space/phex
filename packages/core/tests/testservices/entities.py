from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql.functions import func

from phexcore import services
from phexcore.database import DatabaseService


def bootstrap():
    database: DatabaseService = services.get("database")

    class Post(database.Base):
        __tablename__ = "posts"

        id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
        title = Column(String, nullable=False)
        content = Column(String, nullable=False)
        published = Column(Boolean, server_default="true", nullable=False)
        create_at = Column(DateTime(timezone=False), server_default=func.now())

    services.register("Post", Post)


def dispose():
    services.unregister("Post")
