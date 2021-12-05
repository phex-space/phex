import pydantic
import datetime


class UserCreate(pydantic.BaseModel):
    id: str
    login: str
    lastname: str
    firstname: str
    email: str

    class Config:
        frozen = True


class UserObject(pydantic.BaseModel):
    id: str
    login: str
    lastname: str
    firstname: str
    email: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
