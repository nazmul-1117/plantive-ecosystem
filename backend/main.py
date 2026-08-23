from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.redis import init_redis

from app.routers import auth_router
from app.routers.user_router import router as user_router
from app.routers.admin.user_router import router as admin_user_router

from app.routers.plant_species_router import router as plant_species_router
from app.routers.admin.plant_species_router import admin_plant_species_router
from app.routers.admin.plant_category_router import admin_plant_category_router

from app.exceptions.handlers_exception import register_exception_handler

from app.middleware.register import register_middleware


#context manager
@asynccontextmanager
async def lifespan(app: FastAPI):

    print(">>>Server Started Successfully =====>")
    await init_redis(app)

    yield

    await app.state.redis.aclose()
    print(">>>Server Ended successfully =====>")

#app metadata
API_VERSION = settings.API_VERSION
API_PREFIX = f"/api/{API_VERSION}"

#app creation
app = FastAPI(
    title="Plantive Ecosystem",
    description="A centralized Smart Garden management system with Marketplace and Community Post, Like, Comment",
    version=API_VERSION,
    lifespan=lifespan
)

# register handle an error/exception
register_exception_handler(app)

# middleware add
register_middleware(app)


#routers

## auth router
app.include_router(
    router=auth_router.auth_router,
    prefix=f"{API_PREFIX}/auth",
    tags=['Auth']
)

## User router
app.include_router(
    router = user_router,
    prefix = API_PREFIX,
)

## Admin User router
app.include_router(
    router = admin_user_router,
    prefix = f"{API_PREFIX}/admin",
)

## Plant species router
app.include_router(
    router = plant_species_router,
    prefix = f"{API_PREFIX}",
)

## Admin - Plant Species router
app.include_router(
    router = admin_plant_species_router,
    prefix = f"{API_PREFIX}/admin",
)

## Admin - Plant Species router
app.include_router(
    router = admin_plant_category_router,
    prefix = f"{API_PREFIX}/admin",
)




# Root Endpoint
@app.get('/', status_code = status.HTTP_200_OK)
async def root() -> dict[str, str | int]:
    return {
        "status": status.HTTP_200_OK,
        "application": "Plantive",
        "message": "Welcome to the Plantive Ecosystem",
        "version": settings.API_VERSION,
    }