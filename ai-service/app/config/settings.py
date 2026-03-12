# app/config/settings.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    app_name: str = "Plantive AI Service"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000

    allowed_hosts: List[str] = ["*"]

    disease_model_path: str = "ml_models/disease_model/plant_disease_model.pkl"
    fertilizer_model_path: str = "ml_models/recommendation_model/fertilizer_model.joblib"

    max_upload_size_mb: int = 10

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()