from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings."""
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    external_api_timeout: int = 30
    max_upload_size: int = 10485760

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()