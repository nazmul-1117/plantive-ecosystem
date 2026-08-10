from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_VERSION: str
    
    DATABASE_URL: str
    
    REDIS_HOSTNAME: str
    REDIS_USERNAME: str
    REDIS_PASSWORD: str
    REDIS_PORT: int

    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_ISSUER: str
    JWT_AUDIENCE: str
    
    REFRESH_TOKEN_EXPIRE_DAYS: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    ALLOWED_ORIGINS: list[str] = [
            "http://localhost:5500",
            "http://127.0.0.1:5500",
    ]
    
    ALLOWED_METHODS: list[str] = [
        "GET",
        "POST",
        "PATCH",
        "DELETE"
    ]

    ALLOWED_HEADERS: list[str] = [
        "Authorization",
        "Content-Type"
    ]


    # Email Configuration
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str
    SMTP_FROM_NAME: str


    BACKEND_PUBLIC_URL: str


    model_config = SettingsConfigDict(
        title="Settings Config Dict",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()