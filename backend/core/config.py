from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from functools import lru_cache

BASE_URL = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_URL / ".env"

class PostgresSettings(BaseSettings):
    model_config=SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix="POSTGRES_",
        extra="ignore"
    )


@lru_cache
def get_postgres_settings() -> PostgresSettings:
    return PostgresSettings()
