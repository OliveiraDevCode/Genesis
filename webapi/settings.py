import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "genesis"
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"
    otel_exporter: str = "console"
    otel_endpoint: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="GENESIS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @classmethod
    def load(cls) -> "Settings":
        current_env = os.getenv("GENESIS_ENVIRONMENT", "development")
        env_file = _resolve_env_file(current_env)
        return cls(_env_file=env_file)


def _resolve_env_file(environment: str) -> str:
    specific = f".env.{environment}"
    if os.path.isfile(specific):
        return specific
    return ".env"
