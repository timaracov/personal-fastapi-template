import typing as t

from pathlib import Path
from multiprocessing import cpu_count

from .base import ConfigBase


class ApiConfig(ConfigBase):
    VERSION: str = "0.0.0"

    RELOAD: bool = True

    ENV: str = "dev"
    PROJECT_PATH: str = str(Path(__file__).parents[3])

    HOST: str = "0.0.0.0"
    PORT: int = 8080
    DEBUG: bool = True
    ALLOW_ORIGINS: list[str] = ["*"]

    STATIC_PATH: str = "/api/static"
    STATIC_FOLDER: str = f"{PROJECT_PATH}/static"

    WORKERS: int = cpu_count()*2+1

    SECRET: str = "test"
    ALGORITHM: str = "HS256"


class OpenAPIConfig(ConfigBase):
    NO_DOCS: bool = False

    title: str = "__project_name__ API"
    description: str = "__project_name__ platform backend"
    docs_url: str = "/api/docs"

    if NO_DOCS:
        openapi_url: t.Optional[str] = None
    else:
        openapi_url: t.Optional[str] = "/api/openapi.json"


class CORSConfig(ConfigBase):
    ALLOW_ORIGINS: list[str] = ["*"]
    ALLOW_METHODS: list[str] = ["*"]
    ALLOW_HEADERS: list[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True


API_CONFIG = ApiConfig()
SWAGGER_CONFIG = OpenAPIConfig()
CORS_CONFIG = CORSConfig()
