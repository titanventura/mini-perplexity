from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # class Config:
    #     frozen = True

    gemini_api_key: str
    search_api_key: str
    search_engine_id: str

    model_config = SettingsConfigDict(env_file=".env")


# @lru_cache
def get_settings():
    return Settings()
