from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "AI Document Intelligence"
    app_version: str = "1.0.0"

    database_url: str = (
        "postgresql://postgres:postgres@localhost:5432/document_intelligence"
    )

    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.2:3b"

    upload_dir: str = "data/uploads"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()