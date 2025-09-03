from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TASKS_", env_file=".env", extra="allow")

    environment: str = "local"
    enable_docs: bool = True
    enable_openapi: bool = True
    enable_tasks_feature: bool = True

    cors_allow_origins: List[str] = ["*"]


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return AppSettings()


def reset_settings_cache() -> None:
    # cache_clear may not exist if the decorator changes; be tolerant without hiding other errors
    cache_clear = getattr(get_settings, "cache_clear", None)
    if callable(cache_clear):
        cache_clear()

