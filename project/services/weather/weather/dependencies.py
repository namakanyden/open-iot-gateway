from functools import lru_cache

from weather.models import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()
