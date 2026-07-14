from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.api.router import api_router   # 👈 cleaner import

app = FastAPI(title=settings.app_name, debug=settings.debug)

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "https://api.plantive.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)