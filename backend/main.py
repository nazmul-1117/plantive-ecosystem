from fastapi import FastAPI, status
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.redis import init_redis

from app.routers import plant_router, auth_router
from app.exceptions.handlers_exception import register_exception_handler


#context manager
@asynccontextmanager
async def life_span(app: FastAPI):
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
    lifespan=life_span
    )

# register handle an error/exception
register_exception_handler(app)


#routers
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



