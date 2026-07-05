from fastapi import FastAPI, status
from app.routers import plant_router
from app.config.settings import settings
from app.config.database import init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def life_span(app: FastAPI):
    print("Server Started successfully ------------>")
    await init_db()
    yield
    
    print("Server Ended successfully ------------>")

version = "v1"
version_prefix = f"/api/{version}"

app = FastAPI(
    title="Plantive Ecosystem",
    description="A centralized Smart Garden management system with Marketplace and Community Post, Like, Comment",
    version=version,
    lifespan=life_span
    )

app.include_router(router = plant_router.router, prefix = f"{version_prefix}/plants", tags = ["Plants"])

@app.get('/', status_code = status.HTTP_200_OK)
def root() -> dict:

    # print()
    
    return {
        "status": 200,
        "extra-data": settings.DATABASE_URL,
        "message": "Welcome to Plative Ecosystem, This is landing page ......",
    }



