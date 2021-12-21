from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func

from phexcore import services
from phexcore.database import DatabaseService

_database: DatabaseService = services.get("database")

_Base = _database.Base

class Image(_Base):
    __tablename__ = "images"

    id = Column(String(40), primary_key=True, nullable=True)
    path = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    mimetype = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    modified = Column(DateTime, nullable=False)
    title = Column(String, index=True)
    description = Column(String(65536))
    created_at = Column(
        DateTime(timezone=False), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )
    owner_id = Column(String, ForeignKey("users.id"), nullable=False)
    owner = relationship("User")
