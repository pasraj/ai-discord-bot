from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    secret_key: str
    open_ai_key: str
    assistant_id: str
    discord_bot_token: str



@lru_cache()
def get_settings():
    return Settings()