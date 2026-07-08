from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_db

from app.routers import plant_router, auth_router


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server Started successfully ------------>")
    # await init_db()
    yield
    print("Server Ended successfully ------------>")

API_VERSION = settings.API_VERSION
API_PREFIX = f"/api/{API_VERSION}"

app = FastAPI(
    title="Plantive Ecosystem",
    description="A centralized Smart Garden management system with Marketplace and Community Post, Like, Comment",
    version=API_VERSION,
    lifespan=life_span
    )

app.include_router(
    router = plant_router.router,
    prefix = f"{API_PREFIX}/plants",
    tags = ["Plants"]
)

app.include_router(
    router=auth_router.auth_router,
    prefix=f"{API_PREFIX}/auth",
    tags=['Auth']
)




@app.get('/', status_code = status.HTTP_200_OK)
def root() -> dict:

    # print()
    
    return {
        "status": 200,
        "extra-data": settings.DATABASE_URL,
        "message": "Welcome to Plative Ecosystem, This is landing page ......",
    }



