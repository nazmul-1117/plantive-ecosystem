from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    API_VERSION : str

    model_config = SettingsConfigDict(
        title="Settings Config Dict",
        env_file=".env",
        extra="ignore"
    )

settings = Settings()