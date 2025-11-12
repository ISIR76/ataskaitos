"""Application settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # API Keys
    openai_api_key: str | None = None
    google_api_key: str | None = None

    # Agent models
    literature_model: str = "openai:gpt-4o"
    validity_model: str = "openai:gpt-4o"
    evaluation_model: str = "openai:gpt-4o"


settings = Settings()
