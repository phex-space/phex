import datetime
import pydantic
import typing
import uuid

from ..users.schema import UserObject
from ..images import schema as images_schema


class ExhibitionCreate(pydantic.BaseModel):
    title: str
    description: typing.Optional[str]
    starts_at: typing.Optional[datetime.datetime]
    ends_at: typing.Optional[datetime.datetime]
    tags: typing.Optional[list[str]]
    active: typing.Optional[bool]


class ExhibitionInfoObject(pydantic.BaseModel):
    id: typing.Optional[str]
    title: str
    description: typing.Optional[str]
    starts_at: typing.Optional[datetime.datetime]
    ends_at: typing.Optional[datetime.datetime]
    tags: typing.Optional[list[str]]
    active: typing.Optional[bool]
    owner: typing.Optional[UserObject]

    class Config:
        orm_mode = True


class ExhibitionObject(ExhibitionCreate):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    owner: UserObject
    images: list[images_schema.ImageInfoObject]

    class Config:
        orm_mode = True
