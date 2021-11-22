import logging

import pydantic
from fastapi import HTTPException
from pymongo.collection import Collection, ObjectId
from pymongo.results import InsertOneResult, UpdateResult

from phex import mongodb
from .schema import Package

_logger = logging.getLogger(__name__)


async def list_packages() -> list[Package]:
    _logger.info("List packages")
    database = mongodb.database()
    packages: Collection = database.packages
    result = []
    async for doc in packages.find():
        _logger.info(doc)
        result.append(pydantic.parse_obj_as(Package, doc))
    return result


async def create_package(pkg: Package) -> Package:
    database = mongodb.database()
    packages: Collection = database.packages
    result: InsertOneResult = await packages.insert_one(pkg.dict(exclude_unset=True, exclude_none=True))
    return await read_package(str(result.inserted_id))


async def read_package(id_: str) -> Package:
    _logger.debug("Read package {}".format(id_))
    database = mongodb.database()
    packages: Collection = database.packages
    doc = await packages.find_one({"_id": ObjectId(id_)})
    print(doc, flush=True)
    if not doc:
        raise HTTPException(404, detail={"error": "PackageNotFound"})
    return pydantic.parse_obj_as(Package, doc)


async def update_package(id_: str, pkg: Package) -> Package:
    database = mongodb.database()
    packages: Collection = database.packages
    new_doc = pkg.dict(exclude_unset=True, exclude_none=True)
    new_doc["_id"] = ObjectId(id_)
    result: UpdateResult = await packages.update_one({"_id": ObjectId(id_)}, {"$set": new_doc})
    if result.matched_count == 0:
        raise HTTPException(404, detail={"error": "PackageNotFound"})
    return await read_package(id_)


async def delete_package(id_: str) -> Package:
    database = mongodb.database()
    packages: Collection = database.packages
    doc = read_package(id_)
    await packages.delete_one({"_id": ObjectId(id_)})
    return pydantic.parse_obj_as(Package, doc)
