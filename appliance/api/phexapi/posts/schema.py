import datetime
import typing

import pydantic

from ..users.schema import UserObject


class PostCreate(pydantic.BaseModel):
    title: str
    content: str
    published: typing.Optional[bool] = True


class PostObject(pydantic.BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    owner: typing.Optional[UserObject]

    class Config:
        orm_mode = True
