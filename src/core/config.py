import os
from functools import lru_cache
from pathlib import Path

import yaml  # type: ignore
from pydantic import BaseSettings

__all__ = (
    "Settings",
    "yaml_settings",
    "get_settings",
)


class App(BaseSettings):
    project_name: str
    description: str
    version: str
    api_doc_prefix: str
    host: str
    port: int
    debug: bool


class Postgres(BaseSettings):
    host: str
    port: int
    dbname: str
    user: str
    password: str

    @property
    def async_dsn(self) -> str:
        host: str = self.host
        port: int = self.port
        dbname: str = self.dbname
        user: str = self.user
        password: str = self.password
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{dbname}"


class Settings(BaseSettings):
    app: App
    postgres: Postgres


settings_path = Path(__file__).parent / os.getenv("CONFIG_FILE")  # type: ignore
with settings_path.open("r") as f:
    yaml_settings = yaml.load(f, Loader=yaml.Loader)


@lru_cache
async def get_settings() -> Settings:
    return Settings(**yaml_settings)
