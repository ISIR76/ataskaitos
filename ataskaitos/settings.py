"""Application settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # API Keys
    openai_api_key: str | None = None
    google_api_key: str | None = None
    anthropic_api_key: str | None = None

    # Default models for agents (format: "provider:model")
    default_article_model: str = "openai:gpt-4o"
    default_report_model: str = "openai:gpt-4o"
    default_mtep_model: str = "openai:gpt-4o"

    # Model settings
    default_temperature: float = 0.0

    # Storage configuration
    data_directory: str = "data"
    uploads_directory: str = "data/uploads"
    database_url: str = "sqlite:///data/database/ataskaitos.db"


settings = Settings()
