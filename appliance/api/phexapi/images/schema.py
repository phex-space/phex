import datetime
import pydantic
import typing
import uuid

from ..users.schema import UserObject


class ImageCreate(pydantic.BaseModel):
    id: str = pydantic.Field(default_factory=lambda: str(uuid.uuid4()))
    path: str
    name: str
    mimetype: str
    size: int
    modified: datetime.datetime


class ImageUpdate(pydantic.BaseModel):
    title: typing.Optional[str]
    description: typing.Optional[str]


class ImageInfoObject(pydantic.BaseModel):
    id: typing.Optional[str]
    title: typing.Optional[str]
    description: typing.Optional[str]
    updated_at: typing.Optional[datetime.datetime]
    owner: typing.Optional[UserObject]

    class Config:
        orm_mode = True


class ImageObject(ImageCreate):
    title: typing.Optional[str]
    description: typing.Optional[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    owner: UserObject

    class Config:
        orm_mode = True
