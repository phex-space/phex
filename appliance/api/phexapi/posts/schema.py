import datetime
import typing

import pydantic


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
