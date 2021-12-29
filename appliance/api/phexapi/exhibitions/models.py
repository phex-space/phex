from sqlalchemy import ARRAY, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func

from phexcore import services
from phexcore.database import DatabaseService

_database: DatabaseService = services.get("database")

_Base = _database.Base


class ExhibitionImageAssociation(_Base):
    __tablename__ = "exhibition_image"

    exhibition_id = Column(ForeignKey("exhibitions.id"), primary_key=True)
    image_id = Column(ForeignKey("images.id"), primary_key=True)

    image = relationship("Image", back_populates="exhibitions")
    exhibition = relationship("Exhibition", back_populates="images")


class Exhibition(_Base):
    __tablename__ = "exhibitions"

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String(1024), nullable=False, index=True)
    description = Column(String(8192))
    starts_at = Column(DateTime(timezone=False), index=True)
    ends_at = Column(DateTime(timezone=False))
    tags = Column(ARRAY(String))
    active = Column(Boolean, nullable=False, default=False)
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

    images = relationship("ExhibitionImageAssociation", back_populates="exhibition")
