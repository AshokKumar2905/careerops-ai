from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CareerOps AI"
    app_env: str = "development"
    debug: bool = True

    database_url: str

    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    cors_origins: str = "http://localhost:5173"

    ai_provider: str = "local"

    model_config = SettingsConfigDict(
        env_file="backend/.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()
