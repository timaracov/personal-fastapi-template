from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{Path(__file__).parents[3]}/.env",
        extra="ignore",
    )
