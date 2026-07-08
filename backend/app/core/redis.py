from redis.asyncio import Redis
from fastapi import FastAPI

from app.core.config import settings

async def init_redis(app: FastAPI) -> None:

    redis = Redis(
        host=settings.REDIS_HOSTNAME,
        port=settings.REDIS_PORT,
        username=settings.REDIS_USERNAME,
        password=settings.REDIS_PASSWORD,
        db=0,
        decode_responses=True
    )
    
    await redis.ping()
    app.state.redis = redis