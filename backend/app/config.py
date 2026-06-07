"""Application configuration using Pydantic Settings."""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    All environment variables are prefixed with ``JUMBLE_``.
    For example, ``JUMBLE_HOST=127.0.0.1`` sets the host.
    """

    dictionary_path: str = "data/words.txt"
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"
    default_mode: str = "strict"
    wordfreq_language: str = "en"
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:80",
    ]

    model_config = {
        "env_prefix": "JUMBLE_",
        "case_sensitive": False,
    }


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached application settings instance."""
    return Settings()
