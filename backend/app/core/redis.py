from redis.asyncio import Redis
from collections.abc import AsyncGenerator

from app.core.config import settings

redis = Redis(
    host=settings.REDIS_HOSTNAME,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)

async def get_redis() -> AsyncGenerator[Redis, None]:
    yield redis