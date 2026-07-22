from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Interview IQ API"
    app_env: str = "development"
    mysql_user: str = "root"
    mysql_password: str = "password"
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_db: str = "interview_iq"
    allowed_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    database_url: str | None = None
    use_sqlite_fallback: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
