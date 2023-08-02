from pathlib import Path
from pydantic import BaseSettings


class ConfigBase(BaseSettings):
    class Config:
        env_file = f"{Path(__file__).parents[3]}/.env"
