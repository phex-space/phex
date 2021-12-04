from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql.functions import func

from phexcore import services
from phexcore.database import DatabaseService

_database: DatabaseService = services.get("database")

_Base = _database.Base


class User(_Base):
    __tablename__ = "users"

    id: str = Column(String(40), nullable=False, primary_key=True)
    login: str = Column(String, nullable=False, unique=True)
    lastname: str = Column(String)
    firstname: str = Column(String)
    email: str = Column(String(255))
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )
