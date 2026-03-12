# ai-service/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- import middleware
from app.api import routes_chat, routes_recommendation, routes_disease, router
from app.config.settings import settings  # <-- import instance, not module

app = FastAPI(title=settings.app_name, debug=settings.debug)

# -----------------------------
# CORS configuration
# -----------------------------
origins = [
    "http://localhost:5500",  # your HTML project URL (frontend)
    "http://127.0.0.1:5500",  # another possible localhost port
    "*",  # allow all origins (only for testing)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # which origins can make requests
    allow_credentials=True,
    allow_methods=["*"],         # allow all HTTP methods
    allow_headers=["*"],         # allow all headers
)

# -----------------------------
# Include API routers
# -----------------------------
app.include_router(router.api_router)