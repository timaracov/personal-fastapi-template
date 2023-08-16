import logging

from settings.db import MONGO_CONFIG


MODELS = [
]


async def create_collections(client):
    for model in MODELS:
        try:
            logging.info(
                f"creating collection '{model.db_table}' for model: {model.__name__}..."
            )
            await client[MONGO_CONFIG.MONGO_DB].create_collection(model.db_table)
            logging.info(f"done creating collection for model: {model}")
        except Exception as err:
            logging.info(f"collection already exist: {err}")


async def drop_collections(client):
    collections = await client[MONGO_CONFIG.MONGO_DB].list_collections()
    for coll in collections:
        await client[MONGO_CONFIG.MONGO_DB].drop_collection(coll["name"])
