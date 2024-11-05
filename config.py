from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str
    search_api_key: str
    search_engine_id: str

    model_config = SettingsConfigDict(env_file=".env")


def get_settings():
    return Settings()
