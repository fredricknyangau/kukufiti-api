# pydantic-settings, env vars, never hardcoded values
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    database_url: str
    batches_db_url: str
    finance_db_url: str
    health_db_url: str
    auth_db_url: str

    # Application
    app_name: str = "kukufiti-api"
    app_version: str = "0.1.0"
    debug: bool = False
    log_level: str = "info"

    # Security
    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()  # type: ignore[call-arg]
