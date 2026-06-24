from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Bebederos API"
    api_v1_prefix: str = "/api/v1"
    environment: str = "development"
    database_url: str = Field(
        default="mysql+pymysql://bebederos:bebederos@localhost:3306/bebederos"
    )
    jwt_secret_key: str = Field(default="change-me-in-env")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
