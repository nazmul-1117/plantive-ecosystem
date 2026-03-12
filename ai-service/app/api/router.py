from fastapi import APIRouter

from app.api import routes_chat
from app.api import routes_recommendation
from app.api import routes_disease

api_router = APIRouter()

api_router.include_router(routes_chat.router)
api_router.include_router(routes_recommendation.router)
api_router.include_router(routes_disease.router)