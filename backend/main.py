from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging import logging
from app.core.redis import init_redis

from app.routers import plant_router, auth_router
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
app.include_router(
    router=auth_router.auth_router,
    prefix=f"{API_PREFIX}/auth",
    tags=['Auth']
)

app.include_router(
    router = plant_router.router,
    prefix = f"{API_PREFIX}/plants",
    tags = ["Plants"]
)




@app.get('/', status_code = status.HTTP_200_OK)
def root() -> dict:

    # print()
    
    return {
        "status": 200,
        "extra-data": settings.DATABASE_URL,
        "message": "Welcome to Plative Ecosystem, This is landing page ......",
    }



