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

    # Google Cloud Storage configuration
    use_gcs: bool = False  # Set to True to enable GCS storage
    gcs_bucket_name: str | None = None
    gcs_project_id: str | None = None
    gcs_credentials_path: str | None = None  # Path to service account JSON file
    gcs_base_path: str = "ataskaitos"  # Base path within the bucket

    # Server configuration
    server_host: str = "0.0.0.0"
    server_port: int = 8000

    # CORS configuration
    allowed_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    cors_max_age_seconds: int = 3600

    # JWT configuration
    jwt_secret: str | None = None  # Must be set in production
    jwt_lifetime_seconds: int = 3600

    # API configuration
    api_version: str = "0.2.0"
    service_name: str = "ataskaitos-api"
    environment: str = "development"

    # Evaluation configuration
    batch_evaluation_concurrency: int = 5


settings = Settings()
