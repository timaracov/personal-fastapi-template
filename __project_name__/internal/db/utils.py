import logging

from typing import Generator

from sqlalchemy.orm import Session

from settings.db import MONGO_CONFIG

from .base import session


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


def get_db_session() -> Generator[Session, None, None]:
    sess = session()
    try:
        yield sess
    except Exception as e:
        sess.rollback()
        raise e
    finally:
        sess.close()


def init_db():
    from .base import engine
    from .base import BaseModel

    BaseModel.metadata.create_all(bind=engine)
