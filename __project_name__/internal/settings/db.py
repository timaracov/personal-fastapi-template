from .base import ConfigBase
from .api import API_CONFIG


class MongoConfig(ConfigBase):
    MONGO_HOST: str = "cluster666.sqva8jf.mongodb.net"
    MONGO_USER: str = "meizu"
    MONGO_PORT: int = 80
    MONGO_PASS: str = "PasFusQwe167"
    MONGO_DB: str = "__project_name___db"

    def build_uri(self):
        if API_CONFIG.ENV == "test":
            return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASS}@{self.MONGO_HOST}:{self.MONGO_PORT}"
        else:
            return (
                f"mongodb+srv://{self.MONGO_USER}:{self.MONGO_PASS}@{self.MONGO_HOST}"
            )


class PostgresConfig(ConfigBase):
    PG_HOST: str = "localhost"
    PG_USER: str = "postgres"
    PG_PORT: int = 5432
    PG_PASS: str = "pass"
    PG_DB: str = "__project_name___db"

    def build_uri(self):
        return f"postgersql://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"


MONGO_CONFIG = MongoConfig()
PG_CONFIG = PostgresConfig()

