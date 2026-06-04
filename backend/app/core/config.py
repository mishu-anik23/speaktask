from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "SpeakTask"
    debug: bool = False
    api_version: str = "v1"

    # Database
    database_url: str = "postgresql://user:password@localhost:5432/speaktask"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # JWT
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    # Encryption
    fernet_secret: str

    # API Keys
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    google_api_key: str = ""
    whisper_api_key: str = ""

    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:8000"]

    # Rate limiting
    rate_limit_commands_per_minute: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
