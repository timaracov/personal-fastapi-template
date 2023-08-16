import uuid

from typing import Type, Optional

from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

from settings.db import MONGO_CONFIG


class DbBaseController:
    """
    Base class for database controllers for mongodb.

    Inherite from this class to  create new controller:

    ```python
    class UserDbController(DbBaseController):
        db_dto_model = UserDbCreate
        db_dto_model_get = UserDbGet
        db_table = "users"
    ```
    * models must be pydantic BaseModel classes

    """

    db_dto_model = None
    db_dto_model_get = None
    db_table: str = "db_table"

    def __init__(self, db: AsyncIOMotorClient):  # type:ignore
        if self.db_dto_model is None:
            raise NotImplementedError("db_dto_model not implemented")
        if self.db_dto_model_get is None:
            raise NotImplementedError("db_dto_model_get not implemented")

        self.db = db[MONGO_CONFIG.MONGO_DB]
        self.db_collection = db[MONGO_CONFIG.MONGO_DB][self.db_table]

    async def get_one(self, **query_param: str):
        from_db = await self.db_collection.find_one(query_param)
        if from_db is None:
            return {}
        from_db["id"] = from_db["_id"]
        return self.db_dto_model_get.model_validate(from_db)  # type:ignore

    async def check_if_exists(self, **query_param: str):
        in_db = await self.get_one(**query_param)
        return in_db is not None and in_db != {}

    async def get_many(self, page: int = 0, num: int = 100, **query: str):
        from_db = await self.db_collection.aggregate(
            [
                {"$match": query},
                {"$skip": page},
                {"$limit": num},
            ]
        ).to_list(num)

        if from_db is None:
            return []

        for item in from_db:
            item["id"] = item["_id"]
            del item["_id"]
        return [
            self.db_dto_model_get.model_validate(obj) for obj in from_db
        ]  # type:ignore

    async def get_all(self, page: int = 0, num: int = 100):
        from_db = await self.db_collection.aggregate(
            [
                {"$skip": page},
                {"$limit": num},
            ]
        ).to_list(num)

        if from_db is None:
            return []

        for item in from_db:
            item["id"] = item["_id"]
            del item["_id"]
        return [
            self.db_dto_model_get.model_validate(obj) for obj in from_db
        ]  # type:ignore

    async def create(self, dto_model_create: BaseModel) -> str:
        dto_as_dict = dto_model_create.model_dump()
        if dto_as_dict.get("id"):
            dto_as_dict["_id"] = dto_as_dict["id"]
            del dto_as_dict["id"]
        else:
            dto_as_dict["_id"] = str(uuid.uuid4())
        await self.db_collection.insert_one(dto_as_dict)
        return dto_as_dict["_id"]

    async def update(self, dto_model_update: BaseModel, **query_param: str) -> None:
        dto_as_dict = dto_model_update.model_dump()
        for k, v in dto_as_dict.copy().items():
            if v is None:
                del dto_as_dict[k]
        await self.db_collection.find_one_and_update(query_param, {"$set": dto_as_dict})

    async def delete(self, **query_param: str) -> None:
        await self.db_collection.delete_one(query_param)

    async def delete_all(self) -> None:
        await self.db_collection.delete_many({})


class DbBaseControllerInjector:
    controller: Optional[Type[DbBaseController]] = None

    def __init__(self, db):
        if self.controller is None:
            raise NotImplementedError("controller is not implemented")

        self.db_controller = self.controller(db)
