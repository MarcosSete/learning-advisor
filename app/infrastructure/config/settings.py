from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Learning Advisor"
    environment: str = "development"

    database_url: str = Field(
        default="postgresql://learning_advisor:learning_advisor"
        "@localhost:5432/learning_advisor"
    )

    qdrant_url: str = Field(default="http://localhost:6333")

    deepseek_api_key: str = Field(default="")
    deepseek_model: str = Field(default="deepseek-chat")
    deepseek_base_url: str = Field(default="https://api.deepseek.com")



    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()