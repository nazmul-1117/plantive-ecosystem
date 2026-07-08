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
    
    REFRESH_TOKEN_EXPIRE_DAYS: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        title="Settings Config Dict",
        env_file=".env",
        extra="ignore"
    )

settings = Settings()