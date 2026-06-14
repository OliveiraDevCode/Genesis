import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables and .env files.

    Loading priority (highest wins):
      1. Actual environment variables
      2. .env.{environment} file (e.g. .env.development, .env.production)
      3. .env file (shared defaults)
      4. Class-level defaults

    Environment is determined by the GENESIS_ENVIRONMENT env var.
    """

    # --- Core ---
    service_name: str = "genesis"
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # --- OpenTelemetry ---
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
        """Load settings with environment-specific .env file."""
        current_env = os.getenv("GENESIS_ENVIRONMENT", "development")
        env_file = _resolve_env_file(current_env)
        return cls(_env_file=env_file)


def _resolve_env_file(environment: str) -> str:
    """Return the appropriate .env file path for the given environment.

    Priority:
      1. .env.{environment} (e.g. .env.production)
      2. .env (fallback)
    """
    specific = f".env.{environment}"
    if os.path.isfile(specific):
        return specific
    return ".env"
