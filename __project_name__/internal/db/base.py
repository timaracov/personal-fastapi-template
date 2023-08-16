from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_tornado import MotorClient

from settings.db import MONGO_CONFIG


def create_async_mongo_client():
    return AsyncIOMotorClient(MONGO_CONFIG.build_uri())


def create_mongo_client():
    return MotorClient(MONGO_CONFIG.build_uri())
