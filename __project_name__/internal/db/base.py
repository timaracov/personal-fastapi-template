from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_tornado import MotorClient

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings.db import MONGO_CONFIG, PG_CONFIG


def create_async_mongo_client():
    return AsyncIOMotorClient(MONGO_CONFIG.build_uri())


def create_mongo_client():
    return MotorClient(MONGO_CONFIG.build_uri())


uri = PG_CONFIG.build_uri()
engine = create_engine(uri)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseModel = declarative_base()
