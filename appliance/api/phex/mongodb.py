import motor.motor_asyncio
from pydantic import BaseModel, Field
from pymongo.collection import ObjectId

from phex import configuration

_client = None


def client():
    global _client
    if _client is None:
        config = configuration.get()
        _client = motor.motor_asyncio.AsyncIOMotorClient(
            config.mongodb_url,
            username=config.mongodb_user,
            password=config.mongodb_user_password,
        )
    return _client


def database():
    return client()[configuration.get().mongodb_database]


class PhexObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class PhexBaseModel(BaseModel):
    id: PhexObjectId = Field(default_factory=PhexObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
