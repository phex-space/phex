from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql.functions import func

from phexcore import services
from phexcore.database import DatabaseService

_database: DatabaseService = services.get("database")

_Base = _database.Base


class Post(_Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="true", nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )
