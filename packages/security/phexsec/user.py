import pydantic


class User(pydantic.BaseModel):
    id: str
    login: str
    lastname: str
    firstname: str
    email: str
