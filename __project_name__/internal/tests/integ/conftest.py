import asyncio

from db.utils import create_collections, drop_collections
from db.base import create_async_mongo_client

from .fixtures import *


def pytest_sessionstart(session):
    test_client = create_async_mongo_client()
    asyncio.run(create_collections(test_client))


def pytest_sessionfinish(session, exitstatus):
    test_client = create_async_mongo_client()
    asyncio.run(drop_collections(test_client))
